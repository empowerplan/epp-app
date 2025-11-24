"""Module to implement hooks for django-oemof."""

import logging
import math
from collections import defaultdict

import pandas as pd
from django.http import HttpRequest
from oemof.solph import EnergySystem

from config.settings.base import OEMOF_TSAM
from digiplan.map import config, datapackage, forms


def _map_heat_shares_to_components(distribution: str, heat_shares: dict) -> dict:
    """Map raw heat shares keys to component identifiers for a distribution."""
    mapping = {
        "wood_extchp": f"ABW-wood-extchp_{distribution}",
        "biogas_bpchp": f"ABW-biogas-bpchp_{distribution}",
        "ch4_bpchp": f"ABW-ch4-bpchp_{distribution}",
        "ch4_extchp": f"ABW-ch4-extchp_{distribution}",
        "solar_thermal": f"ABW-solar-thermalcollector_{distribution}",
        "methane": f"ABW-ch4-boiler_{distribution}",
        "hydrogen": f"ABW-ch4-boiler_{distribution}",  # hydrogen is added to methane bus
        "electricity_direct_heating": f"ABW-electricity-pth_{distribution}",
    }
    if distribution == "decentral":
        mapping["wood_oven"] = "ABW-wood-oven"

    heat_share_mapped: dict[str, float] = defaultdict(float)
    for com, share in heat_shares.items():
        if com not in mapping:
            continue
        heat_share_mapped[mapping[com]] += share
    return heat_share_mapped


def read_parameters(scenario: str, data: dict, request: HttpRequest) -> dict:  # noqa: ARG001
    """
    Read parameters from settings panel.

    Parameters
    ----------
    scenario: str
        Used oemof scenario
    data: dict
        Empty dict as parameters are initialized here.
    request: HttpRequest
        Original request from settings panel submit

    Returns
    -------
    dict
        Initial parameters read from settings panel

    Raises
    ------
    ValueError
        if one of the panel forms is invalid

    """
    panel_forms = [
        forms.EnergyPanelForm(config.ENERGY_SETTINGS_PANEL, data=request.POST),
        forms.HeatPanelForm(config.HEAT_SETTINGS_PANEL, data=request.POST),
        forms.TrafficPanelForm(config.TRAFFIC_SETTINGS_PANEL, data=request.POST),
    ]
    for form in panel_forms:
        if not form.is_valid():
            raise ValueError(f"Invalid settings form.\nErrors: {form.errors}")
        data.update(**form.cleaned_data)
    return data


def adapt_electricity_demand(scenario: str, data: dict) -> dict:  # noqa: ARG001
    """
    Read demand settings and scales and aggregates related demands.

    Parameters
    ----------
    scenario: str
        Used oemof scenario
    data : dict
        Raw parameters from user settings

    Returns
    -------
    dict
        Parameters for oemof with adapted demands

    """
    del data["s_v_1"]
    for sector, slider in (("hh", "s_v_3"), ("cts", "s_v_4"), ("ind", "s_v_5")):
        demand = datapackage.get_power_demand(sector)[sector]
        logging.info(f"Adapting electricity demand at {sector=}.")
        data[f"ABW-electricity-demand_{sector}"] = {"amount": float(demand["2022"].sum()) * data.pop(slider) / 100}
    return data


def adapt_heat_demand(scenario: str, data: dict) -> dict:  # noqa: ARG001
    """Set head demands per sector for central/decentral depending on slider values."""
    demand_sliders = {"hh": "w_v_3", "cts": "w_v_4", "ind": "w_v_5"}

    # Get historic heat demands per municipality
    heat_demand_per_municipality = datapackage.get_summed_heat_demand_per_municipality()

    data["demand"] = {"central": 0, "decentral": 0}
    for distribution in ("central", "decentral"):
        # Calculate demands per sector
        for sector in ("hh", "cts", "ind"):
            # Sum up demands of municipalities in year 2022
            summed_demand = int(  # Convert to int, otherwise int64 is used
                heat_demand_per_municipality[sector][distribution[:3]]["2022"].sum(),
            )
            # Get heat demand usage per sector
            percentage = (
                data.pop(demand_sliders[sector]) if distribution == "decentral" else data.get(demand_sliders[sector])
            )
            demand = summed_demand * percentage / 100
            data[f"ABW-heat_{distribution}-demand_{sector}"] = {
                "amount": demand,
            }
            data["demand"][distribution] += demand
    return data


def adapt_heatpumps(scenario: str, data: dict) -> dict:
    """
    Adapt heatpump settings depending on user settings.

    Heatpumps are the only technology which users can set.
    All other heat components settings are derived from heat share.
    """
    hp_sliders = {"hh": "w_d_wp_3", "cts": "w_d_wp_4", "ind": "w_d_wp_5"}
    # Use "central" hardcoded as efficiency does not differ in central/decentral
    hp_efficiency = datapackage.get_thermal_efficiency(
        "electricity-heatpump_central",
        scenario=scenario,
        disaggregate_tsam=OEMOF_TSAM,
    )
    hp_efficiency.sum()

    heat_demand_profile = datapackage.get_heat_demand_profile()

    # Store HP energies for use in upcoming hooks
    data["hp_energy"] = {"central": 0, "decentral": 0}

    for distribution in ("central", "decentral"):
        hp_energy = 0
        hp_capacity = 0
        # Calculate demands per sector
        for sector in ("hh", "cts", "ind"):
            demand = data[f"ABW-heat_{distribution}-demand_{sector}"]["amount"]
            # HP contribution per sector:
            hp_share = data.pop(hp_sliders[sector]) / 100 if distribution == "decentral" else data["w_z_wp_1"] / 100

            # Calculate summed energy from HP
            hp_energy += demand * hp_share
            # Set capacity of HP that it can provide its share at maximum peak demand
            hp_capacity += heat_demand_profile[sector][distribution].max() * demand * hp_share

        # Calculate capacity from HP Jahreszahl and energy
        data[f"ABW-electricity-heatpump_{distribution}"] = {
            "capacity": hp_capacity,
        }
        if hp_capacity > 0:
            data[f"ABW-electricity-heatpump_{distribution}"]["output_parameters"] = {
                "full_load_time_min": hp_energy / hp_capacity,
                "full_load_time_max": hp_energy / hp_capacity,
            }
        data["hp_energy"][distribution] += hp_energy

    return data


def adapt_heat_components(scenario: str, data: dict) -> dict:
    """Share remaining energies across heat components with fixed shares."""
    data["turbines"] = {}
    for distribution in ("central", "decentral"):
        heat_demand = sum(data[f"ABW-heat_{distribution}-demand_{sector}"]["amount"] for sector in ("hh", "cts", "ind"))
        # Reduce heat demand by heatpump supply
        remaining_energy = heat_demand - data["hp_energy"][distribution]

        # Get heat shares for each component in distribution
        heat_shares = datapackage.get_heat_capacity_shares(distribution[:3])
        heat_share_mapped = _map_heat_shares_to_components(distribution, heat_shares)

        for component, share in heat_share_mapped.items():
            energy_share = remaining_energy * share
            efficiency = datapackage.get_thermal_efficiency(
                component[4:],
                scenario=scenario,
                disaggregate_tsam=OEMOF_TSAM,
            )
            if isinstance(efficiency, pd.Series):
                efficiency = efficiency.sum()
            capacity = math.ceil(energy_share / efficiency)

            if "extchp" in component or "bpchp" in component:
                # Store energy share for turbines, as this has to be set in ENERGYSYSTEM hook
                data[component] = {"capacity": capacity}
                data["turbines"][component] = energy_share
                continue

            if capacity == 0:
                continue

            if "boiler" in component:
                # Make boiler nearly inf
                data[component] = {"capacity": 99999999999}
                continue

            if "solar" in component:
                # Solarthermal collectors do not get full_load_times
                data[component] = {"capacity": capacity}
                continue

            data[component] = {
                # Capacity has to be increased, so that times without energy from solar thermal can be covered by other
                # components
                "capacity": capacity,
                "output_parameters": {
                    "full_load_time_min": energy_share / capacity,
                    "full_load_time_max": energy_share / capacity,
                },
            }

    return data


def adapt_storages(scenario: str, data: dict) -> dict:
    """Set up heat storages depending on user settings."""
    storage_sliders = {"decentral": "w_d_s_1", "central": "w_z_s_1"}

    for distribution in ("central", "decentral"):
        heat_demand = sum(data[f"ABW-heat_{distribution}-demand_{sector}"]["amount"] for sector in ("hh", "cts", "ind"))
        avg_demand_per_day = heat_demand / 365
        capacity = float(avg_demand_per_day * data.pop(storage_sliders[distribution]) / 100)
        # Adapt storage capacity to solarthermal collector overpowering (make sure the maximum feedin power of ST can
        # be absorbed by the storage):
        solar_capacity = data[f"ABW-solar-thermalcollector_{distribution}"]["capacity"]
        solar_thermal_energy = (
            datapackage.get_thermal_efficiency(
                f"solar-thermalcollector_{distribution}",
                scenario=scenario,
                disaggregate_tsam=OEMOF_TSAM,
            )
            * solar_capacity
        )
        solar_peak = solar_thermal_energy.max()

        tech_mapping = {"central": "large", "decentral": "small"}
        power = (
            capacity
            * config.TECHNOLOGY_DATA["hot_water_storages"][tech_mapping[distribution]][
                "nominal_power_per_storage_capacity"
            ]
        )
        power = max(power, solar_peak)

        data[f"ABW-heat_{distribution}-storage"] = {
            "storage_capacity": capacity,
            "capacity": power,
        }

    # Adapt biomass to biogas plant size
    biogas_capacity = data["ABW-biogas-bpchp_decentral"]["capacity"] + data["ABW-biogas-bpchp_central"]["capacity"]
    data["ABW-biomass-biogas_plant"] = {"capacity": biogas_capacity}
    data["ABW-biogas-biogas_upgrading_plant"] = {"capacity": biogas_capacity}

    # Remove unnecessary heat settings
    del data["w_v_1"]
    del data["w_d_wp_1"]
    del data["w_z_wp_1"]

    return data


def adapt_renewable_capacities(scenario: str, data: dict) -> dict:
    """
    Read renewable capacities from user input and adapt ES parameters accordingly.

    Parameters
    ----------
    scenario: str
        Name of oemof datapackage
    data: dict
        User-given input parameters

    Returns
    -------
    dict
        Adapted parameters dict with set up capacities

    """
    # 1) Capacities: renewables
    logging.info("Adapting capacities: renewables")
    data["ABW-wind-onshore"] = {"capacity": data.pop("s_w_1")}
    data["ABW-solar-pv_ground"] = {"capacity": data.pop("s_pv_ff_1")}
    data["ABW-solar-pv_rooftop"] = {"capacity": data.pop("s_pv_d_1")}
    data["ABW-hydro-ror"] = {"capacity": data.pop("s_h_1")}

    # Full load hours
    technology_mapping = {
        "ABW-wind-onshore": "wind",
        "ABW-solar-pv_ground": "pv_ground",
        "ABW-solar-pv_rooftop": "pv_roof",
        "ABW-hydro-ror": "ror",
    }
    full_load_hours = datapackage.get_full_load_hours(2045)
    for technology, mapped_key in technology_mapping.items():
        data[technology]["profile"] = datapackage.get_profile(technology[4:], scenario) * full_load_hours[mapped_key]

    # 2) Capacities: batteries
    logging.info("Adapting capacities: batteries")

    # Large scale
    wind_pv_ground_energy_daily = (
        float(
            data["ABW-wind-onshore"]["capacity"] * data["ABW-wind-onshore"]["profile"].sum()
            + data["ABW-solar-pv_ground"]["capacity"] * data["ABW-solar-pv_ground"]["profile"].sum(),
        )
        / 365
    )
    storage_capacity = data.pop("s_s_g_1") / 100 * wind_pv_ground_energy_daily
    data["ABW-electricity-large_scale_battery"] = {
        "storage_capacity": storage_capacity,
        "capacity": (
            storage_capacity * config.TECHNOLOGY_DATA["batteries"]["large"]["nominal_power_per_storage_capacity"]
        ),
    }

    # Home storages
    storage_capacity = (
        data.pop("s_pv_d_4")
        / 100
        * data["ABW-solar-pv_rooftop"]["capacity"]
        * config.TECHNOLOGY_DATA["batteries"]["small"]["storage_capacity_per_pv_power"]
    )
    data["ABW-electricity-small_scale_battery"] = {
        "storage_capacity": storage_capacity,
        "capacity": (
            storage_capacity * config.TECHNOLOGY_DATA["batteries"]["small"]["nominal_power_per_storage_capacity"]
        ),
    }

    # Remove unnecessary renewable sliders:
    for key in ("s_pv_ff_3", "s_pv_ff_4", "s_pv_ff_5", "s_pv_d_3"):
        data.pop(key, None)

    return data


def adapt_extraction_turbines(scenario: str, data: dict, energysystem: EnergySystem) -> EnergySystem:  # noqa: ARG001
    """Set full load times for extraction turbines based on energy share."""
    for component, energy_share in data["turbines"].items():
        distribution = component.split("_")[1]
        flow = next(
            v for k, v in energysystem.groups[component].outputs.data.items() if k.label == f"ABW-heat_{distribution}"
        )
        flow.nominal_value = energy_share
        flow.full_load_time_min = 1
        flow.full_load_time_max = 1
    return energysystem

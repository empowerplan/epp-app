"""Module for calculations used for choropleths or charts."""

from typing import Optional

import pandas as pd
from django.utils.translation import gettext_lazy as _
from django_oemof.results import get_results
from oemof.tabular.postprocessing import calculations, core, helper

from digiplan.map import config, datapackage, models

PV_GROUND_COLUMNS = ["pv_soil_quality_low", "pv_soil_quality_medium", "pv_permanent_crops"]


def select_wind_year(technology_df: pd.DataFrame, wind_year: str) -> pd.DataFrame:
    """Select corresponding wind year based on wind year. Drop non-corresponding wind years."""
    technology_df = technology_df.drop(
        columns=[column for column in technology_df if column.startswith("wind") and column != wind_year],
    )
    return technology_df.rename(columns={wind_year: "wind"})


def calculate_wind_and_pv_distribution(df: pd.DataFrame, parameters: dict) -> pd.DataFrame:
    """Calculate wind and pv distribution based on parameters."""
    # Apply wind capacity from user selection
    df["wind"] = df["wind"] / df["wind"].sum() * parameters["wind"]

    # Apply pv_ground capacity
    pv_ground_sums = df[PV_GROUND_COLUMNS].sum()
    pv_ground_shares = pv_ground_sums / pv_ground_sums.sum()
    df[PV_GROUND_COLUMNS] = df[PV_GROUND_COLUMNS] / pv_ground_sums * pv_ground_shares * parameters["pv_ground"]

    # Apply pv_roof capacity
    df["pv_roof"] = df["pv_roof"] / df["pv_roof"].sum() * parameters["pv_roof"]

    return df


def calculate_square_for_value(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate values related to municipality areas.

    Parameters
    ----------
    df: pd.DataFrame
        Index holds municipality IDs, columns hold random entries

    Returns
    -------
    pd.DataFrame
        Each value is multiplied by related municipality share
    """
    is_series = False
    if isinstance(df, pd.Series):
        is_series = True
        df = pd.DataFrame(df)  # noqa: PD901
    areas = (
        pd.DataFrame.from_records(models.Municipality.objects.all().values("id", "area")).set_index("id").sort_index()
    )
    result = df / areas.sum().sum() if len(df) == 1 else df.sort_index() / areas.to_numpy()
    if is_series:
        return result.iloc[:, 0]
    return result


def value_per_municipality(series: pd.Series) -> pd.DataFrame:
    """Shares values across areas (dummy function)."""
    data = pd.concat([series] * 20, axis=1).transpose()
    data.index = range(20)
    areas = (
        pd.DataFrame.from_records(models.Municipality.objects.all().values("id", "area")).set_index("id").sort_index()
    )
    result = data.sort_index() / areas.to_numpy()
    return result / areas.sum().sum()


def calculate_capita_for_value(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate values related to population. If only one region is given, whole region is assumed.

    Parameters
    ----------
    df: pd.DataFrame
        Index holds municipality IDs, columns hold random entries

    Returns
    -------
    pd.DataFrame
        Each value is multiplied by related municipality population share
    """
    is_series = False
    if isinstance(df, pd.Series):
        is_series = True
        df = pd.DataFrame(df)  # noqa: PD901

    population = (
        pd.DataFrame.from_records(models.Population.objects.filter(year=2022).values("municipality__id", "value"))
        .set_index("municipality__id")
        .sort_index()
    )
    result = df / population.sum().sum() if len(df) == 1 else df.sort_index() / population.to_numpy()
    if is_series:
        return result.iloc[:, 0]
    return result


def employment_per_municipality() -> pd.DataFrame:
    """Return employees per municipality."""
    return datapackage.get_employment()["employees_total"]


def companies_per_municipality() -> pd.DataFrame:
    """Return companies per municipality."""
    return datapackage.get_employment()["companies_total"]


def batteries_per_municipality() -> pd.DataFrame:
    """Return battery count per municipality."""
    return datapackage.get_batteries()["count"]


def battery_capacities_per_municipality() -> pd.DataFrame:
    """Return battery capacity per municipality."""
    return datapackage.get_batteries()["storage_capacity"]


def capacities_per_municipality() -> pd.DataFrame:
    """
    Calculate capacity of renewables per municipality in MW.

    Returns
    -------
    pd.DataFrame
        Capacity per municipality (index) and technology (column)
    """
    return datapackage.get_capacities_from_datapackage()


def capacities_per_municipality_2045(parameters: dict, *, aggregate_pv_ground: bool = True) -> pd.DataFrame:
    """Calculate capacities from 2045 scenario per municipality in MW."""
    potential_capacities = datapackage.get_potential_values()  # in MW
    potential_capacities = select_wind_year(potential_capacities, parameters["wind_year"])
    capacities = {
        "wind": int(parameters["s_w_1"]),
        "pv_ground": int(parameters["s_pv_ff_1"]),
        "pv_roof": int(parameters["s_pv_d_1"]),
    }
    potential_capacities = calculate_wind_and_pv_distribution(potential_capacities, capacities)

    # Set biomass potential to zero
    potential_capacities["bioenergy"] = 0

    if aggregate_pv_ground:
        potential_capacities["pv_ground"] = potential_capacities[PV_GROUND_COLUMNS].sum(axis=1)
        potential_capacities = potential_capacities.drop(PV_GROUND_COLUMNS, axis=1)

        # Correct order (for charts)
        potential_capacities = potential_capacities[["wind", "pv_roof", "pv_ground", "hydro", "bioenergy"]]

    return potential_capacities


def areas_per_municipality_2045(parameters: dict) -> pd.DataFrame:
    """Calculate areas for each municipality depending on capacities in user settings."""
    capacities = capacities_per_municipality_2045(parameters, aggregate_pv_ground=False)
    densities = datapackage.get_power_density()
    densities["bioenergy"] = 1
    areas = capacities * densities
    return areas


def energies_per_municipality() -> pd.DataFrame:
    """
    Calculate energy of renewables per municipality in GWh.

    Returns
    -------
    pd.DataFrame
        Energy per municipality (index) and technology (column)
    """
    capacities = capacities_per_municipality()
    full_load_hours = datapackage.get_full_load_hours(year=2022).drop("st").rename({"ror": "hydro"})
    full_load_hours = full_load_hours.reindex(index=["wind", "pv_roof", "pv_ground", "hydro", "bioenergy"])
    return capacities * full_load_hours.values / 1e3


def energies_per_municipality_2045(parameters: dict) -> pd.DataFrame:
    """Calculate energies from 2045 scenario per municipality in MWh."""
    capacities = capacities_per_municipality_2045(parameters)  # in MW
    full_load_hours = datapackage.get_full_load_hours(year=2045).drop("st").rename({"ror": "hydro"})
    full_load_hours = full_load_hours.reindex(index=["wind", "pv_roof", "pv_ground", "hydro", "bioenergy"])
    energies = capacities * full_load_hours.values
    return energies.fillna(0.0)


def energy_shares_per_municipality() -> pd.DataFrame:
    """
    Calculate energy shares of renewables from electric demand per municipality.

    Returns
    -------
    pd.DataFrame
        Energy share per municipality (index) and technology (column)
    """
    energies = energies_per_municipality()
    demands = datapackage.get_power_demand()
    total_demand = pd.concat([d["2022"] for d in demands.values()], axis=1).sum(axis=1)
    energy_shares = energies.mul(1e3).div(total_demand, axis=0)
    return energy_shares.mul(1e2)


def energy_shares_region() -> pd.DataFrame:
    """
    Calculate energy shares of renewables from electric demand for region.

    Like energy_shares_per_municipality() but with weighted demand for correct
    totals.

    Returns
    -------
    pd.DataFrame
        Energy share per municipality (index) and technology (column)
    """
    energies = energies_per_municipality()
    demands = datapackage.get_power_demand()
    total_demand = pd.concat([d["2022"] for d in demands.values()], axis=1).sum(axis=1)
    total_demand_share = total_demand / total_demand.sum()
    energy_shares = energies.mul(1e3).div(total_demand, axis=0).mul(total_demand_share, axis=0).sum(axis=0)
    return energy_shares.mul(1e2)


def electricity_demand_per_municipality(year: int = 2022) -> pd.DataFrame:
    """
    Calculate electricity demand per sector per municipality in GWh.

    Returns
    -------
    pd.DataFrame
        Electricity demand per municipality (index) and sector (column)
    """
    demands_raw = datapackage.get_power_demand()
    demands_per_sector = pd.concat([demand[str(year)] for demand in demands_raw.values()], axis=1)
    demands_per_sector.columns = [
        _("Electricity Household Demand"),
        _("Electricity CTS Demand"),
        _("Electricity Industry Demand"),
    ]
    return demands_per_sector.astype(float) * 1e-3


def energy_shares_2045_per_municipality(parameters: dict) -> pd.DataFrame:
    """
    Calculate energy shares of renewables from electric demand per municipality in 2045.

    Returns
    -------
    pd.DataFrame
        Energy share per municipality (index) and technology (column)
    """
    energies = energies_per_municipality_2045(parameters).mul(1e-3)
    demands = electricity_demand_per_municipality_2045(parameters).sum(axis=1)
    energy_shares = energies.div(demands, axis=0)
    return energy_shares.astype(float).mul(1e2)


def energy_shares_2045_region(parameters: dict) -> pd.DataFrame:
    """
    Calculate energy shares of renewables from electric demand for region in 2045.

    Like energy_shares_2045_per_municipality() but with weighted demand for
    correct totals.

    Returns
    -------
    pd.DataFrame
        Energy share per municipality (index) and technology (column)
    """
    energies = energies_per_municipality_2045(parameters)
    demands = electricity_demand_per_municipality_2045(parameters).sum(axis=1).mul(1e3)

    demand_share = demands / demands.sum()
    energy_shares = energies.div(demands, axis=0).mul(demand_share, axis=0).sum(axis=0)
    return energy_shares.astype(float).mul(1e2)


def electricity_demand_per_municipality_2045(user_settings: dict) -> pd.DataFrame:
    """
    Calculate electricity demand per sector per municipality in GWh in 2045.

    Returns
    -------
    pd.DataFrame
        Electricity demand per municipality (index) and sector (column)
    """
    demand = electricity_demand_per_municipality(year=2022)
    shares = [int(user_settings[key]) / 100 for key in ("s_v_3", "s_v_4", "s_v_5")]
    return demand.iloc[:] * shares


def heat_demand_per_municipality(year: int) -> pd.DataFrame:
    """
    Calculate heat demand per sector per municipality in GWh.

    Returns
    -------
    pd.DataFrame
        Heat demand per municipality (index) and sector (column)
    """
    demands_raw = datapackage.get_summed_heat_demand_per_municipality()
    demands_per_sector = pd.concat(
        [distributions["cen"][str(year)] + distributions["dec"][str(year)] for distributions in demands_raw.values()],
        axis=1,
    )
    demands_per_sector.columns = [
        _("Electricity Household Demand"),
        _("Electricity CTS Demand"),
        _("Electricity Industry Demand"),
    ]
    return demands_per_sector.astype(float) * 1e-3


def heat_demand_per_municipality_2045(user_settings: dict) -> pd.DataFrame:
    """
    Calculate heat demand per sector per municipality in GWh in 2045.

    Returns
    -------
    pd.DataFrame
        Heat demand per municipality (index) and sector (column)
    """
    demand = heat_demand_per_municipality(year=2022)
    shares = [int(user_settings[key]) / 100 for key in ("w_v_3", "w_v_4", "w_v_5")]
    return demand.iloc[:] * shares


def electricity_from_from_biomass(simulation_id: int) -> pd.Series:
    """
    Calculate electricity from biomass.

    Biomass share to electricity comes from following parts:
    - biomass is turned into biogas
    - biogas powers central and decentral BPCHP which outputs to electricity bus
    - wood powers central and decentral EXTCHP which outputs to electricity bus

    - biogas is further upgraded into methane
    - methane powers following components which all output to electricity bus:
      - BPCHP (central/decentral)
      - EXTCHP (central/decentral)
      - gas turbine

    Regarding the power delivered by methane, we have to distinguish between methane from import and methane from
    upgraded biomass. This is done, by calculating the share of both and multiplying output respectively.

    Returns
    -------
    pd.Series
        containing one entry for electric energy powered by biomass
    """
    results = get_results(
        simulation_id,
        {
            "electricity_production": electricity_production,
            "methane_production": methane_production,
        },
    )
    biomass = results["electricity_production"][
        results["electricity_production"]
        .index.get_level_values(0)
        .isin(
            [
                "ABW-wood-extchp_central",
                "ABW-wood-extchp_decentral",
                "ABW-biogas-bpchp_central",
                "ABW-biogas-bpchp_decentral",
            ],
        )
    ]
    methane_total = results["methane_production"].sum()
    methane_biomass_share = results["methane_production"].loc[["ABW-biogas-biogas_upgrading_plant"]] / methane_total
    electricity_from_methane = (
        results["electricity_production"][
            results["electricity_production"]
            .index.get_level_values(0)
            .isin(
                [
                    "ABW-ch4-gt",
                    "ABW-ch4-extchp_central",
                    "ABW-ch4-extchp_decentral",
                    "ABW-ch4-bpchp_central",
                    "ABW-ch4-bpchp_decentral",
                ],
            )
        ]
        * methane_biomass_share.sum()
    )
    biomass = pd.concat([biomass, electricity_from_methane])
    return biomass.sum()


def wind_turbines_per_municipality_2045(parameters: dict) -> pd.DataFrame:
    """Calculate number of wind turbines from 2045 scenario per municipality."""
    capacities = capacities_per_municipality_2045(parameters)
    return capacities["wind"] / config.TECHNOLOGY_DATA["nominal_power_per_unit"]["wind"]


def electricity_heat_demand(simulation_id: int) -> pd.Series:
    """
    Return electricity demand for heat demand supply.

    Parameters
    ----------
    simulation_id: int
        Simulation ID to get results from

    Returns
    -------
    pd.Series
        containing electricity demand of heating sector
    """
    results = get_results(
        simulation_id,
        {
            "electricity_demand": electricity_demand,
            "heat_demand": heat_demand,
        },
    )

    heat_central_electricity_production = (
        results["electricity_demand"].loc[:, ["ABW-electricity-heatpump_central"]].iloc[0]
    )
    heat_demand_central = results["heat_demand"][results["heat_demand"].index.get_level_values(0) == "ABW-heat_central"]
    heat_demand_central.index = heat_demand_central.index.get_level_values(1)
    electricity_for_heat_central = heat_demand_central / heat_demand_central.sum() * heat_central_electricity_production
    electricity_for_heat_central.index = electricity_for_heat_central.index.map(
        lambda x: f"electricity_heat_demand_{x.split('_')[2]}",
    )

    heat_decentral_electricity_production = (
        results["electricity_demand"].loc[:, ["ABW-electricity-heatpump_decentral"]].iloc[0]
    )
    heat_demand_decentral = results["heat_demand"][
        results["heat_demand"].index.get_level_values(0) == "ABW-heat_decentral"
    ]
    heat_demand_decentral.index = heat_demand_decentral.index.get_level_values(1)
    electricity_for_heat_decentral = (
        heat_demand_decentral / heat_demand_decentral.sum() * heat_decentral_electricity_production
    )
    electricity_for_heat_decentral.index = electricity_for_heat_decentral.index.map(
        lambda x: f"electricity_heat_demand_{x.split('_')[2]}",
    )

    electricity_for_heat_sum = electricity_for_heat_central + electricity_for_heat_decentral
    return electricity_for_heat_sum


def calculate_potential_shares(parameters: dict) -> dict[str, float]:
    """Calculate potential shares depending on user settings."""
    shares = {}
    if "wind_year" in parameters:
        wind_year = parameters["wind_year"]
        share = 1
        if wind_year == "wind_2024":
            share = float(parameters["s_w_6"]) / float(config.ENERGY_SETTINGS_PANEL["s_w_6"]["max"])
        if wind_year == "wind_2027":
            share = float(parameters["s_w_7"]) / 100
        shares["wind"] = share
    if "s_pv_ff_3" in parameters:
        shares.update(
            {
                "pv_soil_quality_low": int(parameters["s_pv_ff_3"]) / 100,
                "pv_soil_quality_medium": int(parameters["s_pv_ff_4"]) / 100,
                "pv_permanent_crops": int(parameters["s_pv_ff_5"]) / 100,
            },
        )
    if "s_pv_d_3" in parameters:
        shares["pv_roof"] = int(parameters["s_pv_d_3"]) / 100
    if "s_h_1" in parameters:
        shares["hydro"] = int(parameters["s_h_1"]) / 100
    return shares


def electricity_overview(year: int) -> pd.Series:
    """
    Return static data for electricity overview chart for given year.

    Parameters
    ----------
    year: int
        Year, either 2022 or 2045

    Returns
    -------
    pd.Series
        containing electricity productions and demands (including heat sector demand for electricity)
    """
    demand = electricity_demand_per_municipality(year).sum()
    production = datapackage.get_full_load_hours(year) * datapackage.get_capacities_from_sliders(year)
    production = production[production.notna()] * 1e-3
    return pd.concat([demand, production])


def electricity_overview_from_user(simulation_id: int) -> pd.Series:
    """
    Return user specific data for electricity overview chart.

    Parameters
    ----------
    simulation_id: int
        Simulation ID to get results from

    Returns
    -------
    pd.Series
        containing electricity productions and demands (including heat sector demand for electricity)
    """
    results = get_results(
        simulation_id,
        {
            "electricity_demand": electricity_demand,
            "electricity_production": electricity_production,
        },
    )
    demand = results["electricity_demand"][
        results["electricity_demand"]
        .index.get_level_values(1)
        .isin([*list(config.SIMULATION_DEMANDS), "ABW-electricity-export"])
    ]
    demand.index = demand.index.get_level_values(1)

    # Electric share of heat production
    # electricity_heat_production_result = electricity_heat_demand(simulation_id)  # noqa: ERA001
    # demand["ABW-electricity-demand_hh"] += electricity_heat_production_result[
    #     "electricity_heat_demand_hh"]
    # demand["ABW-electricity-demand_cts"] += electricity_heat_production_result[
    #     "electricity_heat_demand_cts"]
    # demand["ABW-electricity-demand_ind"] += electricity_heat_production_result[
    #     "electricity_heat_demand_ind"]

    renewables = renewable_electricity_production(simulation_id)

    production_import = results["electricity_production"][
        results["electricity_production"].index.get_level_values(0).isin(["ABW-electricity-import"])
    ]
    production_import.index = ["ABW-electricity-import"]

    overview_data = pd.concat([renewables, demand, production_import])
    overview_data = overview_data.reindex(
        (
            "ABW-wind-onshore",
            "ABW-solar-pv_ground",
            "ABW-solar-pv_rooftop",
            # Bioenergy: Had to be calculated from power output side of BHPs, use decentral as placeholder
            "ABW-biogas-bpchp_decentral",
            "ABW-hydro-ror",
            "ABW-electricity-demand_cts",
            "ABW-electricity-demand_hh",
            "ABW-electricity-demand_ind",
            "ABW-electricity-import",
            "ABW-electricity-export",
        ),
    )
    overview_data = overview_data * 1e-3
    return overview_data


def renewable_electricity_production(simulation_id: int) -> pd.Series:
    """Return electricity production from renewables including biomass."""
    results = get_results(
        simulation_id,
        {
            "electricity_production": electricity_production,
        },
    )
    renewables = results["electricity_production"][
        results["electricity_production"].index.get_level_values(0).isin(config.SIMULATION_RENEWABLES)
    ]
    renewables.index = renewables.index.get_level_values(0)
    renewables = pd.concat([renewables, pd.Series(electricity_from_from_biomass(simulation_id), index=["ABW-biomass"])])
    return renewables


def get_regional_independency(simulation_id: int) -> tuple[int, int, int, int]:
    """Return electricity autarky for 2022 and user scenario."""
    # 2022
    demand = datapackage.get_hourly_electricity_demand(2022)
    full_load_hours = datapackage.get_full_load_hours(2022)
    capacities = datapackage.get_capacities_from_sliders(2022)
    technology_mapping = {
        "ABW-wind-onshore": "wind",
        "ABW-solar-pv_ground": "pv_ground",
        "ABW-solar-pv_rooftop": "pv_roof",
        "ABW-hydro-ror": "ror",
    }
    renewables = []
    for technology, mapped_key in technology_mapping.items():
        renewables.append(
            datapackage.get_profile(technology[4:]) * full_load_hours[mapped_key] * capacities[mapped_key],
        )
    renewables_summed_flow = pd.concat(renewables, axis=1).sum(axis=1)
    # summary
    independency_summary_2022 = round(renewables_summed_flow.sum() / demand.sum() * 100, 1)
    # temporal
    independency_temporal_2022 = renewables_summed_flow - demand
    independency_temporal_2022 = round(sum(independency_temporal_2022 > 0) / 8760 * 100, 1)

    # USER
    results = get_results(
        simulation_id,
        {"renewable_flows": renewable_flows, "demand_flows": demand_flows},
    )
    # summary
    independency_summary = round(results["renewable_flows"].sum().sum() / results["demand_flows"].sum().sum() * 100, 1)
    # temporal
    independency_temporal = results["renewable_flows"].sum(axis=1) - results["demand_flows"].sum(axis=1)
    independency_temporal = round(sum(independency_temporal > 0) / 8760 * 100, 1)
    return independency_summary_2022, independency_temporal_2022, independency_summary, independency_temporal


def get_heat_production(distribution: str, year: int) -> dict:
    """Calculate hea production per technology for given distribution and year."""
    heat_demand_per_sector = datapackage.get_heat_demand(distribution=distribution)
    demand = sum(d[str(year)].sum() for d in heat_demand_per_sector.values())
    heat_shares = datapackage.get_heat_capacity_shares(distribution[:3], year=year, include_heatpumps=True)
    return {tech: demand * share for tech, share in heat_shares.items()}


def get_reduction(simulation_id: int) -> tuple[int, int]:
    """Return electricity reduction from renewables and imports."""
    results = get_results(
        simulation_id,
        {"renewables": reduction_from_renewables, "imports": reduction_from_imports},
    )
    reduction = 2425.9
    res_reduction = results["renewables"].sum()
    import_reduction = results["imports"].sum()
    summed_reduction = res_reduction + import_reduction
    return round(import_reduction / summed_reduction * reduction), round(res_reduction / summed_reduction * reduction)


def heat_overview(simulation_id: int, distribution: str) -> dict:
    """
    Return data for heat overview chart.

    Parameters
    ----------
    simulation_id: int
        Simulation ID to get results from
    distribution: str
        central/decentral

    Returns
    -------
    dict
        containing heat demand and production for all sectors (hh, cts, ind) and technologies
    """
    data = {}
    for year in (2022, 2045):
        demand = datapackage.get_heat_demand(distribution=distribution)
        demand = {f"heat-demand-{sector}": demand[str(year)].sum() for sector, demand in demand.items()}
        data[str(year)] = demand
        data[str(year)].update(get_heat_production(distribution, year))

    results = get_results(
        simulation_id,
        {"heat_demand": heat_demand, "heat_production": heat_production},
    )
    # Filter distribution:
    if distribution == "central":
        demand = results["heat_demand"][
            results["heat_demand"].index.get_level_values(0).map(lambda idx: "decentral" not in idx)
        ]
        production = results["heat_production"][
            results["heat_production"]
            .index.get_level_values(0)
            .map(lambda idx: "decentral" not in idx and idx not in ("ABW-wood-oven", "ABW-heat-import"))
        ]
    else:
        demand = results["heat_demand"][
            results["heat_demand"].index.get_level_values(0).map(lambda idx: "decentral" in idx)
        ]
        production = results["heat_production"][
            results["heat_production"]
            .index.get_level_values(0)
            .map(lambda idx: "decentral" in idx or idx in ("ABW-wood-oven", "ABW-heat-import"))
        ]

    # Demand from user scenario:
    demand.index = demand.index.map(lambda ind: f"heat-demand-{ind[1].split('_')[2]}")
    data["user"] = demand.to_dict()
    # Production from user scenario:
    production.index = production.index.map(lambda ind: ind[0][4:].split("_")[0])
    mapping = {
        "biogas-bpchp": "biogas_bpchp",
        "ch4-boiler": "biogas_bpchp",  # As in future all methane comes from biogas
        "ch4-bpchp": "biogas_bpchp",
        "ch4-extchp": "biogas_bpchp",
        "electricity-heatpump": "heat_pump",
        "electricity-pth": "electricity_direct_heating",
        "solar-thermalcollector": "solar_thermal",
        "wood-extchp": "wood_extchp",
        "wood-bpchp": "wood_bpchp",
        "wood-oven": "wood_oven",
    }
    production = production[production.index.map(lambda idx: idx in mapping)]
    production.index = production.index.map(mapping)
    production = production.reset_index().groupby("index").sum().iloc[:, 0]
    data["user"].update(production.to_dict())
    return data


electricity_demand = core.ParametrizedCalculation(
    calculations.AggregatedFlows,
    {
        "from_nodes": ["ABW-electricity"],
    },
)

heat_demand = core.ParametrizedCalculation(
    calculations.AggregatedFlows,
    {
        "to_nodes": [
            "ABW-heat_decentral-demand_hh",
            "ABW-heat_decentral-demand_cts",
            "ABW-heat_decentral-demand_ind",
            "ABW-heat_central-demand_hh",
            "ABW-heat_central-demand_cts",
            "ABW-heat_central-demand_ind",
        ],
    },
)

electricity_production = core.ParametrizedCalculation(
    calculations.AggregatedFlows,
    {
        "to_nodes": [
            "ABW-electricity",
        ],
    },
)

heat_production = core.ParametrizedCalculation(
    calculations.AggregatedFlows,
    {
        "to_nodes": [
            "ABW-heat_decentral",
            "ABW-heat_central",
        ],
    },
)

methane_production = core.ParametrizedCalculation(
    calculations.AggregatedFlows,
    {
        "to_nodes": [
            "ABW-ch4",
        ],
    },
)

reduction_from_renewables = core.ParametrizedCalculation(
    calculations.AggregatedFlows,
    {
        "from_nodes": [
            "ABW-wind-onshore",
            "ABW-pv_rooftop",
            "ABW-pv_ground",
            "ABW-hydro-ror",
            "ABW-solar-thermalcollector_central",
            "ABW-solar-thermalcollector_decentral",
        ],
    },
)

reduction_from_imports = core.ParametrizedCalculation(
    calculations.AggregatedFlows,
    {
        "from_nodes": [
            "ABW-electricity-import",
            "ABW-ch4-import",
            "ABW-wood-shortage",
            "ABW-lignite-shortage",
            "ABW-biomass-shortage",
        ],
    },
)


class Capacities(core.Calculation):
    """Oemof postprocessing calculation to read capacities."""

    name = "capacities"

    def calculate_result(self) -> pd.Series:
        """Read attribute "capacity" from parameters."""
        capacities = helper.filter_by_var_name(self.scalar_params, "capacity")
        try:
            return capacities.unstack(2)["capacity"]  # noqa: PD010
        except KeyError:
            return pd.Series(dtype="object")


class Flows(core.Calculation):
    """Oemof postprocessing calculation to read flows."""

    name = "flows"

    def __init__(
        self,
        calculator: core.Calculator,
        from_nodes: Optional[list[str]] = None,
        to_nodes: Optional[list[str]] = None,
    ) -> None:
        """Init flows."""
        if not from_nodes and not to_nodes:
            msg = "Either from or to nodes must be set"
            raise ValueError(msg)
        self.from_nodes = from_nodes
        self.to_nodes = to_nodes

        super().__init__(calculator)

    def calculate_result(self) -> pd.DataFrame:
        """Read attribute "capacity" from parameters."""
        from_node_flows = pd.DataFrame()
        to_node_flows = pd.DataFrame()
        if self.from_nodes:
            from_node_flows = self.sequences.iloc[:, self.sequences.columns.get_level_values(0).isin(self.from_nodes)]
            from_node_flows.columns = from_node_flows.columns.droplevel([1, 2])
        if self.to_nodes:
            to_node_flows = self.sequences.iloc[:, self.sequences.columns.get_level_values(1).isin(self.to_nodes)]
            to_node_flows.columns = to_node_flows.columns.droplevel([0, 2])
        return pd.concat([from_node_flows, to_node_flows], axis=1)


renewable_flows = core.ParametrizedCalculation(
    Flows,
    {
        "from_nodes": ["ABW-wind-onshore", "ABW-solar-pv_rooftop", "ABW-solar-pv_ground", "ABW-hydro-ror"],
    },
)

demand_flows = core.ParametrizedCalculation(
    Flows,
    {
        "to_nodes": [
            "ABW-electricity-demand_hh",
            "ABW-electricity-demand_cts",
            "ABW-electricity-demand_ind",
        ],
    },
)

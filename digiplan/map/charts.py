"""Module for extracting structure and data for charts."""

import json
import pathlib
from typing import Any, Optional, Union

import pandas as pd
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from digiplan.map import calculations, config, datapackage, models
from digiplan.map.utils import merge_dicts


class Chart:
    """Base class for charts."""

    lookup: str = None

    def __init__(
        self,
        lookup: Optional[str] = None,
        chart_data: Optional[Any] = None,
        **kwargs,  # noqa: ARG002
    ) -> None:
        """Initialize chart data and chart options."""
        if lookup:
            self.lookup = lookup
        self.chart_data = chart_data if chart_data is not None else self.get_chart_data()
        self.chart_options = self.get_chart_options()

    def render(self) -> dict:
        """
        Create chart based on given lookup and municipality ID or result option.

        Returns
        -------
        dict
            Containing chart filled with data

        """
        if self.chart_data is not None:
            series_type = self.chart_options["series"][0]["type"]
            series_length = len(self.chart_options["series"])
            if series_type == "line":
                data = []
                for key, value in self.chart_data.items():
                    year_as_string = f"{key}"
                    data.append([year_as_string, value])
                self.chart_options["series"][0]["data"] = data
            elif series_length > 1:
                for i in range(0, series_length):
                    values = self.chart_data.iloc[i]
                    if not isinstance(values, (list, tuple)):
                        values = [values]
                    self.chart_options["series"][i]["data"] = values
            else:
                self.chart_options["series"][0]["data"] = self.chart_data

        return self.chart_options

    def get_chart_options(self) -> dict:
        """
        Get the options for a chart from the corresponding json file.

        Returns
        -------
        dict
            Containing the json that can be filled with data

        Raises
        ------
        LookupError
            if lookup can't be found in LOOKUPS
        """
        lookup_path = pathlib.Path(config.CHARTS_DIR.path(f"{self.lookup}.json"))
        if not lookup_path.exists():
            error_msg = f"Could not find lookup '{self.lookup}' in charts folder."
            raise LookupError(error_msg)

        with lookup_path.open("r", encoding="utf-8") as lookup_json:
            lookup_options = json.load(lookup_json)

        with pathlib.Path(config.CHARTS_DIR.path("general_options.json")).open(
            "r",
            encoding="utf-8",
        ) as general_chart_json:
            general_chart_options = json.load(general_chart_json)

        options = merge_dicts(general_chart_options, lookup_options)
        return options

    def get_chart_data(self) -> None:
        """
        Check if chart_data_function is valid.

        Returns
        -------
        None

        """
        return


class PreResultsChart(Chart):
    """For charts based on user settings."""

    def __init__(self, user_settings: dict) -> None:
        """
        Init Chart.

        Parameters
        ----------
        user_settings: dict
            User settings coming from map
        """
        self.user_settings = user_settings
        super().__init__()


class SimulationChart(Chart):
    """For charts based on simulations."""

    def __init__(self, user_settings: dict) -> None:
        """
        Init Chart.

        Parameters
        ----------
        user_settings: dict
            User settings coming from map
        """
        self.simulation_id = user_settings["simulation_id"]
        super().__init__()


class DetailedOverviewChart(SimulationChart):
    """Detailed Overview Chart."""

    lookup = "detailed_overview"

    def get_chart_data(self):  # noqa: D102, ANN201
        return calculations.electricity_overview(simulation_id=self.simulation_id)

    def render(self) -> dict:  # noqa: D102
        for i, item in enumerate(self.chart_options["series"]):
            item["data"][1] = self.chart_data.iloc[i]
        return self.chart_options


class ElectricityOverviewChart(SimulationChart):
    """Chart for electricity overview."""

    lookup = "electricity_overview"

    def get_chart_data(self):  # noqa: ANN201
        """Get chart data from electricity overview calculation."""
        return {
            "2022": calculations.electricity_overview(2022),
            "2045": calculations.electricity_overview(2045),
            "user": calculations.electricity_overview_from_user(simulation_id=self.simulation_id),
        }

    def render(self) -> dict:  # noqa: D102
        mapping = {
            "Aufdach-PV": ("ABW-solar-pv_rooftop", "pv_roof"),
            "Bioenergie": ("ABW-biomass", "bioenergy"),
            "Export*": ("ABW-electricity-export", ""),
            "Freiflächen-PV": ("ABW-solar-pv_ground", "pv_ground"),
            "Import*": ("ABW-electricity-import", ""),
            "Verbrauch GHD": ("ABW-electricity-demand_cts", "Strombedarf GDP"),
            "Verbrauch Haushalte": ("ABW-electricity-demand_hh", "Strombedarf Haushalte"),
            "Verbrauch Industrie": ("ABW-electricity-demand_ind", "Strombedarf Industrie"),
            "Wasserkraft": ("ABW-hydro-ror", "ror"),
            "Windenergie": ("ABW-wind-onshore", "wind"),
        }
        for _i, item in enumerate(self.chart_options["series"]):
            mapped_keys = mapping[item["name"]]
            item["data"][0] = round(
                self.chart_data["2045"].get(mapped_keys[0], self.chart_data["2045"].get(mapped_keys[1], 0.0)),
            )
            item["data"][1] = round(
                self.chart_data["user"].get(mapped_keys[0], self.chart_data["user"].get(mapped_keys[1], 0.0)),
            )
            item["data"][2] = round(
                self.chart_data["2022"].get(mapped_keys[0], self.chart_data["2022"].get(mapped_keys[1], 0.0)),
            )
        return self.chart_options


class ElectricityAutarkyChart(SimulationChart):
    """Chart for electricity autarky."""

    lookup = "electricity_autarky"

    def get_chart_data(self):  # noqa: ANN201
        """Get chart data from electricity overview calculation."""
        return calculations.get_regional_independency(self.simulation_id)

    def render(self) -> dict:  # noqa: D102
        for i, item in enumerate(self.chart_options["series"]):
            item["data"][0] = self.chart_data[i + 2]
            item["data"][1] = self.chart_data[i]
        return self.chart_options


class ElectricityCTSChart(SimulationChart):
    """Electricity CTS Chart. Shows greenhouse gas emissions."""

    lookup = "electricity_autarky"

    def get_chart_data(self):  # noqa: D102, ANN201
        return calculations.detailed_overview(simulation_id=self.simulation_id)

    def render(self) -> dict:  # noqa: D102
        for item in self.chart_options["series"]:
            profile = config.SIMULATION_NAME_MAPPING[item["name"]]
            item["data"][2] = self.chart_data[profile]

        return self.chart_options


class HeatStructureChart(SimulationChart):
    """Heat Structure Chart."""

    def render(self) -> dict:  # noqa: D102
        mapping = {
            "Erdgas": ("methane", "ch4_bpchp", "ch4_extchp"),
            "Heizöl": ("fuel_oil",),
            "Holz": ("wood_oven", "wood_bpchp", "wood_extchp"),
            "Wärmepumpe": ("heat_pump",),
            "El. Direktheizung": ("electricity_direct_heating",),
            "Biogas": ("biogas_bpchp",),
            "Solarthermie": ("solar_thermal",),
            "Sonstige": ("other",),
            "Verbrauch Haushalte": ("heat-demand-hh",),
            "Verbrauch GHD": ("heat-demand-cts",),
            "Verbrauch Industrie": ("heat-demand-ind",),
        }
        for _i, item in enumerate(self.chart_options["series"]):
            item["data"][0] = round(
                sum(self.chart_data["2045"].get(entry, 0.0) for entry in mapping[item["name"]]) * 1e-3,
            )
            item["data"][1] = round(
                sum(self.chart_data["user"].get(entry, 0.0) for entry in mapping[item["name"]]) * 1e-3,
            )
            item["data"][2] = round(
                sum(self.chart_data["2022"].get(entry, 0.0) for entry in mapping[item["name"]]) * 1e-3,
            )
        return self.chart_options


class HeatStructureCentralChart(HeatStructureChart):
    """Heat structure for centralized heat."""

    lookup = "heat_centralized"

    def get_chart_data(self):  # noqa: D102, ANN201
        return calculations.heat_overview(simulation_id=self.simulation_id, distribution="central")


class HeatStructureDecentralChart(HeatStructureChart):
    """Heat structure for decentralized heat."""

    lookup = "heat_decentralized"

    def get_chart_data(self):  # noqa: D102, ANN201
        return calculations.heat_overview(simulation_id=self.simulation_id, distribution="decentral")


class PopulationRegionChart(Chart):
    """Chart for regional population."""

    lookup = "population"

    def get_chart_data(self) -> None:
        """Calculate population for whole region."""
        return models.Population.quantity_per_municipality_per_year().sum()

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        return chart_options


class PopulationDensityRegionChart(Chart):
    """Chart for regional population density."""

    lookup = "population"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return calculations.calculate_square_for_value(
            pd.DataFrame(models.Population.quantity_per_municipality_per_year().sum()).transpose(),
        ).sum()

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("EW/km²")
        return chart_options


class EmployeesRegionChart(Chart):
    """Chart for regional employees."""

    lookup = "wind_turbines"

    def get_chart_data(self) -> list:
        """Calculate population for whole region."""
        return [int(calculations.employment_per_municipality().sum())]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = "Beschäftigte"
        del chart_options["series"][0]["name"]
        return chart_options


class CompaniesRegionChart(Chart):
    """Chart for regional companies."""

    lookup = "wind_turbines"

    def get_chart_data(self) -> list:
        """Calculate population for whole region."""
        return [int(calculations.companies_per_municipality().sum())]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = "Betriebe"
        del chart_options["series"][0]["name"]
        return chart_options


class CapacityRegionChart(Chart):
    """Chart for regional capacities."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return calculations.capacities_per_municipality().sum().round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        return chart_options


class Capacity2045RegionChart(PreResultsChart):
    """Chart for regional capacities in 2045."""

    lookup = "capacity"

    def get_chart_data(self) -> list:
        """Calculate capacities for whole region."""
        status_quo_data = calculations.capacities_per_municipality().sum().round(1)
        future_data = calculations.capacities_per_municipality_2045(self.user_settings).sum().astype(float).round(1)
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        chart_options["title"]["text"] = "Region OLS"
        return chart_options


class CapacitySquareRegionChart(Chart):
    """Chart for regional capacities per square meter."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return (
            calculations.calculate_square_for_value(
                pd.DataFrame(calculations.capacities_per_municipality().sum()).transpose(),
            )
            .round(2)
            .sum()
        )

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("MW")
        return chart_options


class CapacitySquare2045RegionChart(PreResultsChart):
    """Chart for regional capacities in 2045."""

    lookup = "capacity"

    def get_chart_data(self) -> list:
        """Calculate capacities for whole region."""
        status_quo_data = (
            calculations.calculate_square_for_value(
                pd.DataFrame(calculations.capacities_per_municipality().sum()).transpose(),
            )
            .sum()
            .round(2)
        )
        future_data = (
            calculations.calculate_square_for_value(
                pd.DataFrame(calculations.capacities_per_municipality_2045(self.user_settings).sum()).transpose(),
            )
            .sum()
            .astype(float)
            .round(2)
        )
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        chart_options["yAxis"]["name"] = _("MW")
        chart_options["title"]["text"] = "Region OLS"
        return chart_options


class EnergyRegionChart(Chart):
    """Chart for regional energy."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return calculations.energies_per_municipality().sum().round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("GWh")
        return chart_options


class Energy2045RegionChart(PreResultsChart):
    """Chart for regional energy."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        status_quo_data = calculations.energies_per_municipality().sum().round(1)
        future_data = calculations.energies_per_municipality_2045(self.user_settings).sum().astype(float) * 1e-3
        future_data = future_data.round(1)
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("GWh")
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        return chart_options


class EnergyShareRegionChart(Chart):
    """Calculate RES energy shares for whole region."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return calculations.energy_shares_region().round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("%")
        return chart_options


class EnergyShare2045RegionChart(PreResultsChart):
    """Chart for regional energy shares."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate RES energy shares for whole region."""
        status_quo_data = calculations.energy_shares_region().round(1)
        future_data = calculations.energy_shares_2045_region(self.user_settings).round(1)
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("%")
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        return chart_options


class EnergyCapitaRegionChart(Chart):
    """Chart for regional energy shares per capita."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return (
            calculations.calculate_capita_for_value(
                pd.DataFrame(calculations.energies_per_municipality().sum()).transpose(),
            ).sum()
            * 1e3
        ).round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("MWh")
        return chart_options


class EnergyCapita2045RegionChart(PreResultsChart):
    """Chart for regional energy."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        status_quo_data = (
            calculations.calculate_capita_for_value(
                pd.DataFrame(calculations.energies_per_municipality().sum()).transpose(),
            ).sum()
            * 1e3
        ).round(1)
        future_data = (
            (
                calculations.calculate_capita_for_value(
                    pd.DataFrame(calculations.energies_per_municipality_2045(self.user_settings).sum()).transpose(),
                ).sum()
            )
            .astype(float)
            .round(1)
        )
        future_data = future_data.round(1)
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("MWh")
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        return chart_options


class EnergySquareRegionChart(Chart):
    """Chart for regional energy shares per square meter."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return (
            calculations.calculate_square_for_value(
                pd.DataFrame(calculations.energies_per_municipality().sum()).transpose(),
            ).sum()
            * 1e3
        ).round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("MWh")
        return chart_options


class EnergySquare2045RegionChart(PreResultsChart):
    """Chart for regional energy shares per square meter."""

    lookup = "capacity"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        status_quo_data = (
            calculations.calculate_square_for_value(
                pd.DataFrame(calculations.energies_per_municipality().sum()).transpose(),
            ).sum()
            * 1e3
        ).round(1)
        future_data = (
            (
                calculations.calculate_square_for_value(
                    pd.DataFrame(calculations.energies_per_municipality_2045(self.user_settings).sum()).transpose(),
                ).sum()
            )
            .astype(float)
            .round(1)
        )
        future_data = future_data.round(1)
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("MWh")
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        return chart_options


class WindTurbinesRegionChart(Chart):
    """Chart for regional wind turbines."""

    lookup = "wind_turbines"

    def get_chart_data(self) -> list[int]:
        """Calculate population for whole region."""
        return [int(models.WindTurbine2Operating.quantity_per_municipality().sum())]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        return chart_options


class WindTurbines2045RegionChart(PreResultsChart):
    """Chart for regional wind turbines in 2045."""

    lookup = "wind_turbines"

    def get_chart_data(self) -> list[int]:
        """Calculate population for whole region."""
        status_quo_data = models.WindTurbine2Operating.quantity_per_municipality().sum()
        future_data = calculations.wind_turbines_per_municipality_2045(self.user_settings).sum()
        return [int(status_quo_data), int(future_data)]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["xAxis"]["data"] = ["2022", "Dein Szenario"]
        chart_options["title"]["text"] = "Region OLS"
        return chart_options


class WindTurbinesSquareRegionChart(Chart):
    """Chart for regional wind turbines per square meter."""

    lookup = "wind_turbines"

    def get_chart_data(self) -> list[float]:
        """Calculate population for whole region."""
        return [
            float(
                calculations.calculate_square_for_value(
                    pd.DataFrame(
                        {"turbines": models.WindTurbine2Operating.quantity_per_municipality().sum()},
                        index=[1],
                    ),
                )
                .sum()
                .round(2),
            ),
        ]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = "WEA/km²"
        return chart_options


class WindTurbinesSquare2045RegionChart(PreResultsChart):
    """Chart for regional wind turbines per square meter in 2045."""

    lookup = "wind_turbines"

    def get_chart_data(self) -> list[float]:
        """Calculate population for whole region."""
        status_quo_data = (
            calculations.calculate_square_for_value(
                pd.DataFrame({"turbines": models.WindTurbine2Operating.quantity_per_municipality().sum()}, index=[1]),
            )
            .sum()
            .round(2)
        )
        future_data = (
            calculations.calculate_square_for_value(
                pd.DataFrame(
                    {"turbines": calculations.wind_turbines_per_municipality_2045(self.user_settings).sum()},
                    index=[1],
                ),
            )
            .sum()
            .round(2)
        )
        return [float(status_quo_data), float(future_data)]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = ""
        chart_options["xAxis"]["data"] = ["2022", "Dein Szenario"]
        return chart_options


class ElectricityDemandRegionChart(Chart):
    """Chart for regional electricity demand."""

    lookup = "electricity_demand"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return calculations.electricity_demand_per_municipality().sum().round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("GWh")
        return chart_options


class ElectricityDemand2045RegionChart(PreResultsChart):
    """Chart for regional electricity demand."""

    lookup = "electricity_demand"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        status_quo_data = calculations.electricity_demand_per_municipality().sum().round(1)
        future_data = (
            calculations.electricity_demand_per_municipality_2045(self.user_settings).sum().astype(float).round(1)
        )
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("GWh")
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        return chart_options


class ElectricityDemandCapitaRegionChart(Chart):
    """Chart for regional electricity demand per population."""

    lookup = "electricity_demand"

    def get_chart_data(self) -> pd.DataFrame:
        """Calculate capacities for whole region."""
        return (
            calculations.calculate_capita_for_value(
                pd.DataFrame(calculations.electricity_demand_per_municipality().sum()).transpose(),
            ).sum()
            * 1e6
        ).round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("kWh")
        return chart_options


class ElectricityDemandCapita2045RegionChart(PreResultsChart):
    """Chart for regional electricity demand per population in 2045."""

    lookup = "electricity_demand"

    def get_chart_data(self) -> pd.DataFrame:
        """Calculate capacities for whole region."""
        status_quo_data = (
            calculations.calculate_capita_for_value(
                pd.DataFrame(calculations.electricity_demand_per_municipality().sum()).transpose(),
            ).sum()
            * 1e6
        ).round(1)
        future_data = (
            (
                calculations.calculate_capita_for_value(
                    pd.DataFrame(
                        calculations.electricity_demand_per_municipality_2045(self.user_settings).sum(),
                    ).transpose(),
                ).sum()
                * 1e6
            )
            .astype(float)
            .round(1)
        )
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("kWh")
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        return chart_options


class HeatDemandRegionChart(Chart):
    """Chart for regional heat demand."""

    lookup = "heat_demand"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return calculations.heat_demand_per_municipality(year=2022).sum().round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("GWh")
        return chart_options


class HeatDemand2045RegionChart(PreResultsChart):
    """Chart for regional heat demand in 2045."""

    lookup = "heat_demand"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        status_quo_data = calculations.heat_demand_per_municipality(year=2022).sum().round(1)
        future_data = calculations.heat_demand_per_municipality_2045(self.user_settings).sum().astype(float).round(1)
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("GWh")
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        return chart_options


class HeatDemandCapitaRegionChart(Chart):
    """Chart for regional heat demand per population."""

    lookup = "heat_demand"

    def get_chart_data(self) -> None:
        """Calculate capacities for whole region."""
        return (
            calculations.calculate_capita_for_value(
                pd.DataFrame(calculations.heat_demand_per_municipality(year=2022).sum()).transpose(),
            ).sum()
            * 1e6
        ).round(1)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("kWh")
        return chart_options


class HeatDemandCapita2045RegionChart(PreResultsChart):
    """Chart for regional heat demand per population in 2045."""

    lookup = "heat_demand"

    def get_chart_data(self) -> pd.DataFrame:
        """Calculate capacities for whole region."""
        status_quo_data = (
            calculations.calculate_capita_for_value(
                pd.DataFrame(calculations.heat_demand_per_municipality(year=2022).sum()).transpose(),
            ).sum()
            * 1e6
        ).round(1)
        future_data = (
            (
                calculations.calculate_capita_for_value(
                    pd.DataFrame(
                        calculations.heat_demand_per_municipality_2045(self.user_settings).sum(),
                    ).transpose(),
                ).sum()
                * 1e6
            )
            .astype(float)
            .round(1)
        )
        return list(zip(status_quo_data, future_data))

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("kWh")
        chart_options["xAxis"]["data"] = ["2022", "Dein\nSzenario"]
        return chart_options


class BatteriesRegionChart(Chart):
    """Chart for regional battery count."""

    lookup = "wind_turbines"

    def get_chart_data(self) -> list:
        """Calculate population for whole region."""
        return [int(calculations.batteries_per_municipality().sum())]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("Anzahl")
        del chart_options["series"][0]["name"]
        return chart_options


class BatteriesCapacityRegionChart(Chart):
    """Chart for regional battery capacity."""

    lookup = "wind_turbines"

    def get_chart_data(self) -> list:
        """Calculate population for whole region."""
        return [calculations.battery_capacities_per_municipality().sum().round(1)]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = "Region OLS"
        chart_options["yAxis"]["name"] = _("MWh")
        del chart_options["series"][0]["name"]
        return chart_options


class WindCapacityChart(PreResultsChart):
    """Chart for wind capacity shown on diagram results page."""

    lookup = "wind_capacity"

    def get_chart_data(self) -> dict:
        """Calculate population for whole region."""
        return {
            "capacity": calculations.capacities_per_municipality_2045(self.user_settings)["wind"].sum(),
            "turbines": calculations.wind_turbines_per_municipality_2045(self.user_settings).sum(),
        }

    def render(self) -> dict:
        """Place results from user settings into related chart entries."""
        self.chart_options["series"][0]["data"][4]["value"] = self.chart_data["capacity"].round()
        self.chart_options["series"][3]["data"][4]["value"] = self.chart_data["turbines"].round()
        return self.chart_options


class PVGroundCapacityChart(PreResultsChart):
    """Chart for pv ground capacity shown on diagram results page."""

    lookup = "pv_ground_capacity"

    def get_chart_data(self) -> dict:
        """Calculate population for whole region."""
        return calculations.capacities_per_municipality_2045(self.user_settings, aggregate_pv_ground=True)[
            "pv_ground"
        ].sum()

    def render(self) -> dict:
        """Place results from user settings into related chart entries."""
        self.chart_options["series"][0]["data"][4]["value"] = self.chart_data.round()
        return self.chart_options


class PVRoofCapacityChart(PreResultsChart):
    """Chart for pv roof capacity shown on diagram results page."""

    lookup = "pv_roof_capacity"

    def get_chart_data(self) -> dict:
        """Calculate population for whole region."""
        return calculations.capacities_per_municipality_2045(self.user_settings)["pv_roof"].sum()

    def render(self) -> dict:
        """Place results from user settings into related chart entries."""
        self.chart_options["series"][0]["data"][4]["value"] = self.chart_data.round()
        return self.chart_options


class WindAreaChart(PreResultsChart):
    """Chart for wind capacity shown on diagram results page."""

    lookup = "wind_areas"

    def get_chart_data(self) -> dict:
        """Calculate population for whole region."""
        area = calculations.areas_per_municipality_2045(self.user_settings)["wind"].sum()  # in km2
        region_area = models.Municipality.objects.values("area").aggregate(Sum("area"))["area__sum"]  # in km2
        area_percentage = area / region_area * 100
        return {"area": (area * 100).round(), "area_percentage": area_percentage.round(2)}  # in ha

    def render(self) -> dict:
        """Place results from user settings into related chart entries."""
        self.chart_options["series"][0]["data"][2]["value"] = self.chart_data["area"]
        self.chart_options["series"][1]["data"][2]["value"] = self.chart_data["area_percentage"]
        return self.chart_options


class PVGroundAreaChart(PreResultsChart):
    """Chart for pv ground areas shown on diagram results page."""

    lookup = "pv_ground_areas"

    def get_chart_data(self) -> dict:
        """Calculate population for whole region."""
        areas = calculations.areas_per_municipality_2045(self.user_settings, aggregate_pv_ground=False).sum()
        region_area = models.Municipality.objects.values("area").aggregate(Sum("area"))["area__sum"]
        areas_percentage = areas / region_area * 100
        return {"areas": (areas * 100).round(), "areas_percentage": areas_percentage.round(2)}  # in ha

    def render(self) -> dict:
        """Place results from user settings into related chart entries."""
        for i, area in enumerate(("pv_soil_quality_low", "pv_soil_quality_medium", "pv_permanent_crops")):
            self.chart_options["series"][0]["data"][i] = self.chart_data["areas"][area]
            self.chart_options["series"][1]["data"][i] = self.chart_data["areas_percentage"][area]
        return self.chart_options


class PVRoofAreaChart(PreResultsChart):
    """Chart for pv roof capacity shown on diagram results page."""

    lookup = "pv_roof_areas"

    def get_chart_data(self) -> dict:
        """Calculate population for whole region."""
        area = calculations.areas_per_municipality_2045(self.user_settings, aggregate_pv_ground=False)["pv_roof"].sum()
        potential_area = datapackage.get_potential_areas("pv_roof").sum()
        area_percentage = area / potential_area * 100
        return {"area": (area * 100).round(), "area_percentage": area_percentage.round(2)}  # in ha

    def render(self) -> dict:
        """Place results from user settings into related chart entries."""
        self.chart_options["series"][0]["data"][0] = self.chart_data["area"]
        self.chart_options["series"][1]["data"][0] = self.chart_data["area_percentage"]
        return self.chart_options


CHARTS: dict[str, Union[type[PreResultsChart], type[SimulationChart]]] = {
    "detailed_overview": DetailedOverviewChart,
    "electricity_overview": ElectricityOverviewChart,
    "electricity_autarky": ElectricityAutarkyChart,
    "heat_decentralized": HeatStructureDecentralChart,
    "heat_centralized": HeatStructureCentralChart,
    "population_statusquo_region": PopulationRegionChart,
    "population_density_statusquo_region": PopulationDensityRegionChart,
    "employees_statusquo_region": EmployeesRegionChart,
    "companies_statusquo_region": CompaniesRegionChart,
    "capacity_statusquo_region": CapacityRegionChart,
    "capacity_square_statusquo_region": CapacitySquareRegionChart,
    "capacity_2045_region": Capacity2045RegionChart,
    "capacity_square_2045_region": CapacitySquare2045RegionChart,
    "energy_statusquo_region": EnergyRegionChart,
    "energy_2045_region": Energy2045RegionChart,
    "energy_share_statusquo_region": EnergyShareRegionChart,
    "energy_share_2045_region": EnergyShare2045RegionChart,
    "energy_capita_statusquo_region": EnergyCapitaRegionChart,
    "energy_capita_2045_region": EnergyCapita2045RegionChart,
    "energy_square_statusquo_region": EnergySquareRegionChart,
    "energy_square_2045_region": EnergySquare2045RegionChart,
    "wind_areas": WindAreaChart,
    "wind_capacity": WindCapacityChart,
    "pv_ground_capacity": PVGroundCapacityChart,
    "pv_ground_areas": PVGroundAreaChart,
    "pv_roof_capacity": PVRoofCapacityChart,
    "pv_roof_areas": PVRoofAreaChart,
    "wind_turbines_statusquo_region": WindTurbinesRegionChart,
    "wind_turbines_2045_region": WindTurbines2045RegionChart,
    "wind_turbines_square_statusquo_region": WindTurbinesSquareRegionChart,
    "wind_turbines_square_2045_region": WindTurbinesSquare2045RegionChart,
    "electricity_demand_statusquo_region": ElectricityDemandRegionChart,
    "electricity_demand_2045_region": ElectricityDemand2045RegionChart,
    "electricity_demand_capita_statusquo_region": ElectricityDemandCapitaRegionChart,
    "electricity_demand_capita_2045_region": ElectricityDemandCapita2045RegionChart,
    "heat_demand_statusquo_region": HeatDemandRegionChart,
    "heat_demand_2045_region": HeatDemand2045RegionChart,
    "heat_demand_capita_statusquo_region": HeatDemandCapitaRegionChart,
    "heat_demand_capita_2045_region": HeatDemandCapita2045RegionChart,
    "batteries_statusquo_region": BatteriesRegionChart,
    "batteries_capacity_statusquo_region": BatteriesCapacityRegionChart,
}

PRE_RESULTS = (
    "electricity_demand_2045_region",
    "electricity_demand_capita_2045_region",
    "heat_demand_2045_region",
    "heat_demand_capita_2045_region",
)


def create_chart(lookup: str, chart_data: Optional[Any] = None) -> dict:
    """
    Return chart for given lookup.

    If chart is listed in CHARTS, specific chart is returned. Otherwise, generic chart is returned.
    """
    if lookup in CHARTS:
        return CHARTS[lookup](lookup, chart_data).render()
    return Chart(lookup, chart_data).render()

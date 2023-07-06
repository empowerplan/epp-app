"""Provide popups for digiplan."""

import abc
from collections import namedtuple
from collections.abc import Iterable
from typing import Optional, Union

import pandas as pd
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from django_mapengine import popups
from django_oemof import results
from oemof.tabular.postprocessing import core

from . import calculations, charts, models

Source = namedtuple("Source", ("name", "url"))


class RegionPopup(popups.ChartPopup):
    """Popup containing values for municipality and region in header."""

    lookup: Optional[str] = None
    title: str = None
    description: str = None
    unit: str = None
    sources: Optional[list[Source]] = None

    def __init__(
        self,
        lookup: str,
        selected_id: int,
        map_state: Optional[dict] = None,
        template: Optional[str] = None,
    ) -> None:
        """Initialize parent popup class and adds initialization of detailed data."""
        if self.lookup:
            lookup = self.lookup
        super().__init__(lookup, selected_id, map_state, template)
        self.detailed_data = self.get_detailed_data()

    def get_context_data(self) -> dict:
        """
        Set up context data including municipality and region values.

        Returns
        -------
        dict
            context dict including region and municipality data
        """
        return {
            "id": self.selected_id,
            "title": self.title,
            "description": self.description,
            "unit": self.unit,
            "region_value": self.get_region_value(),
            "municipality_value": self.get_municipality_value(),
            "municipality": models.Municipality.objects.get(pk=self.selected_id),
        }

    def get_chart_options(self) -> dict:
        """
        Return chart data to build chart from in JS.

        Returns
        -------
        dict
            chart data ready to use in ECharts in JS
        """
        chart_data = self.get_chart_data()
        return charts.create_chart(self.lookup, chart_data)

    @abc.abstractmethod
    def get_detailed_data(self) -> pd.DataFrame:
        """
        Return detailed data for each municipality and technology/component.

        Municipality IDs are stored in index, components/technologies/etc. are stored in columns
        """

    def get_region_value(self) -> float:
        """Return aggregated data of all municipalities and technologies."""
        return self.detailed_data.sum().sum()

    def get_municipality_value(self) -> Optional[float]:
        """Return aggregated data for all technologies for given municipality ID."""
        if self.selected_id not in self.detailed_data.index:
            return 0
        return self.detailed_data.loc[self.selected_id].sum()

    def get_chart_data(self) -> Iterable:
        """Return data for given municipality ID."""
        if self.selected_id not in self.detailed_data.index:
            msg = "No chart data available for given ID"
            raise KeyError(msg)
        return self.detailed_data.loc[self.selected_id]


class SimulationPopup(RegionPopup, abc.ABC):
    """Popup with simulation based context."""

    calculation: Union[core.Calculation, core.ParametrizedCalculation] = None

    def __init__(
        self,
        lookup: str,
        selected_id: int,
        map_state: Optional[dict] = None,
        template: Optional[str] = None,
    ) -> None:
        """
        Init simulation popup.

        Parameters
        ----------
        lookup: str
            Lookup name
        selected_id: int
            ID of selected feature
        map_state: Optional[dict]
            Current state of map. Includes current simulation ID
        template: Optional[str]
            Template to render popup. If not given template using lookup name is used
        """
        super().__init__(lookup, selected_id, map_state, template)
        self.simulation_id = map_state["simulation_id"]
        self.result = list(results.get_results(self.simulation_id, [self.calculation]).values())[0]


class ClusterPopup(popups.Popup):
    """Popup for clusters."""

    def __init__(self, lookup: str, selected_id: int, **kwargs) -> None:  # noqa: ARG002
        """Initialize popup with default cluster template."""
        self.model_lookup = lookup
        super().__init__(lookup="cluster", selected_id=selected_id)

    def get_context_data(self) -> dict:
        """Return cluster data as context data."""
        model = {
            "wind": models.WindTurbine,
            "pvroof": models.PVroof,
            "pvground": models.PVground,
            "hydro": models.Hydro,
            "biomass": models.Biomass,
            "combustion": models.Combustion,
            "gsgk": models.GSGK,
            "storage": models.Storage,
        }[self.model_lookup]
        # TODO(Hendrik Huyskens): Add mapping
        # https://github.com/rl-institut-private/digiplan/issues/153
        default_attributes = {
            "name": "Name",
            "mun_name": "Gemeindename",
            "zip_code": "Postleitzahl",
            "geometry_approximated": "Geschätzt",
            "unit_count": "Anzahl",
            "capacity_net": "Kapazität",
        }
        instance = model.objects.annotate(mun_name=F("mun_id__name")).get(pk=self.selected_id)
        return {
            "title": model._meta.verbose_name,  # noqa: SLF001
            "data": {name: getattr(instance, key) for key, name in default_attributes.items()},
        }


class CapacityPopup(RegionPopup):
    """Popup to show capacities."""

    lookup = "capacity"

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.capacities_per_municipality()


class CapacitySquarePopup(RegionPopup):
    """Popup to show capacities per km²."""

    lookup = "capacity"

    def get_detailed_data(self) -> pd.DataFrame:
        """Return capacities per square kilometer."""
        capacities = calculations.capacities_per_municipality()
        return calculations.calculate_square_for_value(capacities)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Installed capacities per square meter")
        chart_options["yAxis"]["name"] = _("MW/km²")
        return chart_options


class EnergyPopup(RegionPopup):
    """Popup to show energies."""

    lookup = "capacity"
    title = _("Energies")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.energies_per_municipality()

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Energies per technology")
        chart_options["yAxis"]["name"] = _("GWh")
        return chart_options


class Energy2045Popup(RegionPopup):
    """Popup to show energies."""

    lookup = "capacity"
    title = _("Energies")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.energies_per_municipality_2045(self.map_state["simulation_id"])

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Energies per technology")
        chart_options["yAxis"]["name"] = _("GWh")
        chart_options["xAxis"]["data"] = ["Status Quo", "Mein Szenario"]
        return chart_options

    def get_chart_data(self) -> Iterable:
        """Create capacity chart data for SQ and future scenario."""
        status_quo_data = calculations.energies_per_municipality().loc[self.selected_id]
        future_data = super().get_chart_data()
        return list(zip(status_quo_data, future_data))


class EnergySharePopup(RegionPopup):
    """Popup to show energy shares."""

    lookup = "capacity"
    title = _("Energie Shares")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.energy_shares_per_municipality()

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Energy shares per technology")
        chart_options["yAxis"]["name"] = _("%")
        return chart_options


class EnergyCapitaPopup(RegionPopup):
    """Popup to show energy shares per population."""

    lookup = "capacity"
    title = _("Gewonnene Energie pro EW")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.calculate_capita_for_value(calculations.energies_per_municipality()) * 1e3

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Energy per capita per technology")
        chart_options["yAxis"]["name"] = _("MWh")
        return chart_options


class EnergyCapita2045Popup(RegionPopup):
    """Popup to show energies."""

    lookup = "capacity"
    title = _("Gewonnene Energie pro EW")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.calculate_capita_for_value(
            calculations.energies_per_municipality_2045(self.map_state["simulation_id"]),
        )

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Energies per capita per technology")
        chart_options["yAxis"]["name"] = _("GWh")
        chart_options["xAxis"]["data"] = ["Status Quo", "Mein Szenario"]
        return chart_options

    def get_chart_data(self) -> Iterable:
        """Create capacity chart data for SQ and future scenario."""
        status_quo_data = calculations.calculate_capita_for_value(calculations.energies_per_municipality()).loc[
            self.selected_id
        ]
        future_data = super().get_chart_data()
        return list(zip(status_quo_data, future_data))


class EnergySquarePopup(RegionPopup):
    """Popup to show energy shares per km²."""

    lookup = "capacity"
    title = _("Gewonnene Energie pro km²")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.calculate_square_for_value(calculations.energies_per_municipality()) * 1e3

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Energie pro km²")
        chart_options["yAxis"]["name"] = _("MWh")
        return chart_options


class EnergySquare2045Popup(RegionPopup):
    """Popup to show energies."""

    lookup = "capacity"
    title = _("Gewonnene Energie pro km²")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.calculate_square_for_value(
            calculations.energies_per_municipality_2045(self.map_state["simulation_id"]),
        )

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Gewonnene Energie pro km²")
        chart_options["yAxis"]["name"] = _("MWh")
        chart_options["xAxis"]["data"] = ["Status Quo", "Mein Szenario"]
        return chart_options

    def get_chart_data(self) -> Iterable:
        """Create capacity chart data for SQ and future scenario."""
        status_quo_data = calculations.calculate_square_for_value(calculations.energies_per_municipality()).loc[
            self.selected_id
        ]
        future_data = super().get_chart_data()
        return list(zip(status_quo_data, future_data))


class PopulationPopup(RegionPopup):
    """Popup to show Population."""

    lookup = "population"

    def get_detailed_data(self) -> pd.DataFrame:
        """Return population data."""
        return models.Population.quantity_per_municipality_per_year()


class PopulationDensityPopup(RegionPopup):
    """Popup to show Population Density."""

    lookup = "population"

    def get_detailed_data(self) -> pd.DataFrame:
        """Return population data squared."""
        population = models.Population.quantity_per_municipality_per_year()
        return calculations.calculate_square_for_value(population)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Population density per year")
        chart_options["yAxis"]["name"] = _("Pop/km²")
        return chart_options


class EmployeesPopup(RegionPopup):
    """Popup to show employees."""

    lookup = "wind_turbines"
    title = _("Beschäftigte")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.employment_per_municipality()

    def get_chart_data(self) -> Iterable:
        """Return single value for employeess in current municipality."""
        return [int(self.detailed_data.loc[self.selected_id])]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Beschäftigte")
        chart_options["yAxis"]["name"] = "#"
        del chart_options["series"][0]["name"]
        return chart_options


class CompaniesPopup(RegionPopup):
    """Popup to show companies."""

    lookup = "wind_turbines"
    title = _("Betriebe")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.companies_per_municipality()

    def get_chart_data(self) -> Iterable:
        """Return single value for companies in current municipality."""
        return [int(self.detailed_data.loc[self.selected_id])]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Betriebe")
        chart_options["yAxis"]["name"] = "#"
        del chart_options["series"][0]["name"]
        return chart_options


class NumberWindturbinesPopup(RegionPopup):
    """Popup to show the number of wind turbines."""

    lookup = "wind_turbines"
    title = _("Number of wind turbines")
    description = _("Description for number of wind turbines")
    unit = ""

    def get_detailed_data(self) -> pd.DataFrame:
        """Return quantity of wind turbines per municipality (index)."""
        return models.WindTurbine.quantity_per_municipality()

    def get_chart_data(self) -> Iterable:
        """Return single value for wind turbines in current municipality."""
        return [int(self.detailed_data.loc[self.selected_id])]


class NumberWindturbinesSquarePopup(RegionPopup):
    """Popup to show the number of wind turbines per km²."""

    lookup = "wind_turbines"

    def get_detailed_data(self) -> pd.DataFrame:
        """Return quantity of wind turbines per municipality (index)."""
        wind_turbines = models.WindTurbine.quantity_per_municipality()
        return calculations.calculate_square_for_value(wind_turbines)

    def get_chart_options(self) -> dict:
        """Overwrite title and unit in chart options."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Wind turbines per square meter")
        chart_options["yAxis"]["name"] = _("WT/km²")
        return chart_options

    def get_chart_data(self) -> Iterable:
        """Return single value for wind turbines in current municipality."""
        return [float(self.detailed_data.loc[self.selected_id])]


class ElectricityDemandPopup(RegionPopup):
    """Popup to show electricity demand."""

    lookup = "electricity_demand"
    title = _("Strombedarf")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.electricity_demand_per_municipality()

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Strombedarf")
        chart_options["yAxis"]["name"] = _("ǴWh")
        return chart_options


class ElectricityDemandCapitaPopup(RegionPopup):
    """Popup to show electricity demand capita."""

    lookup = "electricity_demand"
    title = _("Strombedarf je EinwohnerIn")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.calculate_capita_for_value(calculations.electricity_demand_per_municipality())

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Strombedarf je EinwohnerIn")
        chart_options["yAxis"]["name"] = _("kWh")
        return chart_options


class HeatDemandPopup(RegionPopup):
    """Popup to show heat demand."""

    lookup = "heat_demand"
    title = _("Wärmebedarf")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.electricity_demand_per_municipality()

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Wärmebedarf")
        chart_options["yAxis"]["name"] = _("GWh")
        return chart_options


class HeatDemandCapitaPopup(RegionPopup):
    """Popup to show heat demand capita."""

    lookup = "heat_demand"
    title = _("Wärmebedarf je EinwohnerIn")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.calculate_capita_for_value(calculations.electricity_demand_per_municipality())

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Wärmebedarf je EinwohnerIn")
        chart_options["yAxis"]["name"] = _("kWh")
        return chart_options


class BatteriesPopup(RegionPopup):
    """Popup to show battery count."""

    lookup = "wind_turbines"
    title = _("Anzahl Batteriespeicher")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.batteries_per_municipality()

    def get_chart_data(self) -> Iterable:
        """Return single value for employeess in current municipality."""
        return [int(self.detailed_data.loc[self.selected_id])]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Anzahl Batteriespeicher")
        chart_options["yAxis"]["name"] = "#"
        del chart_options["series"][0]["name"]
        return chart_options


class BatteriesCapacityPopup(RegionPopup):
    """Popup to show battery count."""

    lookup = "wind_turbines"
    title = _("Kapazität Batteriespeicher")

    def get_detailed_data(self) -> pd.DataFrame:  # noqa: D102
        return calculations.battery_capacities_per_municipality()

    def get_chart_data(self) -> Iterable:
        """Return single value for employeess in current municipality."""
        return [int(self.detailed_data.loc[self.selected_id])]

    def get_chart_options(self) -> dict:
        """Overwrite title and unit."""
        chart_options = super().get_chart_options()
        chart_options["title"]["text"] = _("Kapazität Batteriespeicher")
        chart_options["yAxis"]["name"] = _("MWh")
        del chart_options["series"][0]["name"]
        return chart_options


POPUPS: dict[str, type(popups.Popup)] = {
    "wind": ClusterPopup,
    "pvroof": ClusterPopup,
    "pvground": ClusterPopup,
    "hydro": ClusterPopup,
    "biomass": ClusterPopup,
    "combustion": ClusterPopup,
    "gsgk": ClusterPopup,
    "storage": ClusterPopup,
    "population_statusquo": PopulationPopup,
    "population_density_statusquo": PopulationDensityPopup,
    "employees_statusquo": EmployeesPopup,
    "companies_statusquo": CompaniesPopup,
    "energy_statusquo": EnergyPopup,
    "energy_2045": Energy2045Popup,
    "energy_share_statusquo": EnergySharePopup,
    "energy_capita_statusquo": EnergyCapitaPopup,
    "energy_capita_2045": EnergyCapita2045Popup,
    "energy_square_statusquo": EnergySquarePopup,
    "energy_square_2045": EnergySquare2045Popup,
    "capacity_statusquo": CapacityPopup,
    "capacity_square_statusquo": CapacitySquarePopup,
    "wind_turbines_statusquo": NumberWindturbinesPopup,
    "wind_turbines_square_statusquo": NumberWindturbinesSquarePopup,
    "electricity_demand_statusquo": ElectricityDemandPopup,
    "electricity_demand_capita_statusquo": ElectricityDemandCapitaPopup,
    "heat_demand_statusquo": HeatDemandPopup,
    "heat_demand_capita_statusquo": HeatDemandCapitaPopup,
    "batteries_statusquo": BatteriesPopup,
    "batteries_capacity_statusquo": BatteriesCapacityPopup,
}
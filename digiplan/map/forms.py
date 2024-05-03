"""Module containing django forms."""
from __future__ import annotations

from abc import abstractmethod
from itertools import count
from typing import TYPE_CHECKING

from django.forms import (
    BooleanField,
    CharField,
    FloatField,
    Form,
    HiddenInput,
    TextInput,
    renderers,
)
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from . import calculations, charts, config, datapackage, menu
from .widgets import SwitchWidget

if TYPE_CHECKING:
    from django_mapengine import legend


class TemplateForm(Form):  # noqa: D101
    template_name = None
    extra_content = {}

    def __str__(self) -> str:  # noqa: D105
        if self.template_name:
            renderer = renderers.get_default_renderer()
            return mark_safe(renderer.render(self.template_name, {"form": self, **self.extra_content}))  # noqa: S308
        return super().__str__()


class StaticLayerForm(TemplateForm):  # noqa: D101
    template_name = "forms/layer.html"
    switch = BooleanField(
        label=False,
        widget=SwitchWidget(
            attrs={
                "switch_class": "form-check form-switch",
                "switch_input_class": "form-check-input",
            },
        ),
    )
    counter = count()

    def __init__(self, layer: legend.LegendLayer, *args, **kwargs) -> None:  # noqa: ANN002, D107
        super().__init__(*args, **kwargs)
        self.layer = layer


class PanelForm(TemplateForm):  # noqa: D101
    def __init__(self, parameters, additional_parameters=None, **kwargs) -> None:  # noqa: D107, ANN001
        super().__init__(**kwargs)
        self.fields.update(
            {item["name"]: item["field"] for item in self.generate_fields(parameters, additional_parameters)},
        )

    def get_field_attrs(self, name: str, parameters: dict) -> dict:  # noqa: ARG002
        """Set up field attributes from parameters."""
        attrs = {
            "class": parameters["class"],
            "data-min": parameters["min"],
            "data-max": parameters["max"],
            "data-from": parameters["start"],
            "data-grid": "true" if "grid" in parameters and parameters["grid"] else "false",
            "data-has-sidepanel": "true" if "sidepanel" in parameters else "false",
            "data-color": parameters["color"] if "color" in parameters else "",
        }
        if "to" in parameters:
            attrs["data-to"] = parameters["to"]
        if "step" in parameters:
            attrs["data-step"] = parameters["step"]
        if "from-min" in parameters:
            attrs["data-from-min"] = parameters["from-min"]
        if "from-max" in parameters:
            attrs["data-from-max"] = parameters["from-max"]
        return attrs

    def generate_fields(self, parameters: dict, additional_parameters: dict | None = None) -> dict:
        """Create fields from config parameters."""
        if additional_parameters is not None:
            charts.merge_dicts(parameters, additional_parameters)
        for name, item in parameters.items():
            if item["type"] == "slider":
                field = FloatField(
                    label=item["label"],
                    widget=TextInput(attrs=self.get_field_attrs(name, item)),
                    help_text=item["tooltip"],
                    required=item.get("required", True),
                )
                yield {"name": name, "field": field}
            elif item["type"] == "switch":
                attrs = {
                    "class": item["class"],
                }
                field = BooleanField(
                    label=item["label"],
                    widget=SwitchWidget(attrs=attrs),
                    help_text=item["tooltip"],
                    required=False,
                )
                yield {"name": name, "field": field}
            else:
                raise ValueError(f"Unknown parameter type '{item['type']}'")


class EnergyPanelForm(PanelForm):  # noqa: D101
    template_name = "forms/panel_energy.html"

    wind_year = CharField(initial="wind_2024", max_length=9, widget=HiddenInput)

    def __init__(self, parameters, additional_parameters=None, **kwargs) -> None:  # noqa: ANN001
        """Overwrite init function to add initial key results for detail panels."""
        super().__init__(parameters, additional_parameters, **kwargs)
        key_results = {}
        for wind_year in ("wind_2018", "wind_2024", "wind_2027"):
            # get initial slider values for wind and pv:
            key_results[wind_year] = menu.detail_key_results(
                wind_year=wind_year,
                s_w_6=parameters["s_w_6"]["start"],
                s_w_7=parameters["s_w_7"]["start"],
            )
        key_results["pv_ground"] = menu.detail_key_results(
            s_pv_ff_3=parameters["s_pv_ff_3"]["start"],
            s_pv_ff_4=parameters["s_pv_ff_4"]["start"],
            s_pv_ff_5=parameters["s_pv_ff_5"]["start"],
        )
        key_results["pv_roof"] = menu.detail_key_results(s_pv_d_3=parameters["s_pv_d_3"]["start"])
        for technology, key_result in key_results.items():
            for key, value in key_result.items():
                self.extra_content[f"{technology}_key_result_{key}"] = value

    def get_field_attrs(self, name: str, parameters: dict) -> dict:
        """Add HTMX attributes to wind and pv detail sliders."""
        detail_slider_targets = {"s_w_6": "wind_key_results_2024", "s_w_7": "wind_key_results_2027"}
        attrs = super().get_field_attrs(name, parameters)
        if name in detail_slider_targets:
            attrs["hx-get"] = reverse("map:detail_key_results")
            attrs["hx-target"] = detail_slider_targets[name]
        return attrs


class HeatPanelForm(PanelForm):  # noqa: D101
    template_name = "forms/panel_heat.html"


class TrafficPanelForm(PanelForm):  # noqa: D101
    template_name = "forms/panel_traffic.html"


class ResultsBox(TemplateForm):
    """Shows a result summary for a given category in a box."""

    template_name = "widgets/result_box.html"
    category: str = ""
    text: str = ""
    unit: str = ""

    def __init__(self, parameters: dict) -> None:
        """Initialize parameters for result box widget."""
        super().__init__()
        self.value = self.calculate_value(parameters)

    @abstractmethod
    def calculate_value(self, parameters: dict) -> float:
        """Calculate result based on parameters. Abstract."""
        msg = "Please implement value calculation."
        raise NotImplementedError(msg)


class ElectricityWindPVResultsBox(ResultsBox):  # noqa: D101
    category = "electricity"
    text = "<span>Strom</span> werden aus Wind und Photovoltaik erzeugt"
    unit = "TWh"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        energies = (
            calculations.energies_per_municipality_2045(parameters)[["wind", "pv_ground", "pv_roof"]].sum().sum() * 1e-6
        )
        return energies.round(1)


class ElectricityAutarkyResultsBox(ResultsBox):  # noqa: D101
    category = "electricity"
    text = "<span>der Zeit wird der Strombedarf</span> komplett aus regionalen erneuerbaren Quellen gedeckt"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        pass


class ElectricityAreaResultsBox(ResultsBox):  # noqa: D101
    category = "electricity"
    text = "der <span>Regionsfläche</span> werden für Windenergie und Photovoltaik verwendet"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        region_area = datapackage.get_region_area()
        wind_pv_area = (
            calculations.areas_per_municipality_2045(parameters)[["wind", "pv_ground", "pv_roof"]].sum().sum()
        )
        return (wind_pv_area / region_area * 100).round(1)


class HeatResultsBox(ResultsBox):  # noqa: D101
    category = "heat"
    text = "..."
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        pass


class WindGoalResultsBox(ResultsBox):  # noqa: D101
    category = "wind"
    text = "der <span>Brandenburger Ausbauziele 2040</span> werden erreicht"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        goal = config.ADDITIONAL_ENERGY_SETTINGS["s_w_1"]["future_scenario_2040"]
        wind_capacity = calculations.capacities_per_municipality_2045(parameters)["wind"].sum()
        return (wind_capacity / goal * 100).round(1)


class WindAreaResultsBox(ResultsBox):  # noqa: D101
    category = "wind"
    text = "der <span>Regionsfläche</span> werden für die Windenergie verwendet"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        region_area = datapackage.get_region_area()
        wind_area = calculations.areas_per_municipality_2045(parameters)["wind"].sum()
        return (wind_area / region_area * 100).round(1)


class WindDemandShareResultsBox(ResultsBox):  # noqa: D101
    category = "wind"
    text = "des <span>Strombedarfs</span> werden durch Windstrom gedeckt"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        electricity_demand = calculations.electricity_demand_per_municipality_2045(parameters).sum().sum()  # in GWh
        wind_energy = calculations.energies_per_municipality_2045(parameters)["wind"].sum()  # in MWh
        return (wind_energy * 1e-3 / electricity_demand * 100).round(1)


class PVGoalResultsBox(ResultsBox):  # noqa: D101
    category = "pv"
    text = "der <span>Brandenburger Ausbauziele 2040</span> werden erreicht"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        goal_pf_ground = config.ADDITIONAL_ENERGY_SETTINGS["s_pv_ff_1"]["future_scenario_2040"]
        goal_pf_roof = config.ADDITIONAL_ENERGY_SETTINGS["s_pv_d_1"]["future_scenario_2040"]
        goal = goal_pf_ground + goal_pf_roof
        pv_capacity = calculations.capacities_per_municipality_2045(parameters)[["pv_ground", "pv_roof"]].sum().sum()
        return (pv_capacity / goal * 100).round(1)


class PVAreaResultsBox(ResultsBox):  # noqa: D101
    category = "pv"
    text = "der <span>Regionsfläche</span> werden für Freiflächen-PV verwendet"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        region_area = datapackage.get_region_area()
        pv_area = calculations.areas_per_municipality_2045(parameters)["pv_ground"].sum()
        return (pv_area / region_area * 100).round(1)


class PVDemandShareResultsBox(ResultsBox):  # noqa: D101
    category = "pv"
    text = "des <span>Strombedarfs</span> werden durch PV-Strom gedeckt"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        electricity_demand = calculations.electricity_demand_per_municipality_2045(parameters).sum().sum()  # in GWh
        pv_energy = (
            calculations.energies_per_municipality_2045(parameters)[["pv_ground", "pv_roof"]].sum().sum()
        )  # in MWh
        return (pv_energy * 1e-3 / electricity_demand * 100).round(1)


class MobilityResultsBox(ResultsBox):  # noqa: D101
    category = "mobility"
    text = "..."
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        pass


class H2ResultsBox(ResultsBox):  # noqa: D101
    category = "h2"
    text = "..."
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        pass


class CO2ResultsBox(ResultsBox):  # noqa: D101
    category = "co2"
    text = "Reduktion der <span>Treibhausgasemissionen</span> in 2040"
    unit = "%"

    def calculate_value(self, parameters: dict) -> float:  # noqa: D102
        pass


SUMMARY_RESULTS = {
    "summary_electricity_wind_pv": ElectricityWindPVResultsBox,
    "summary_electricity_area": ElectricityAreaResultsBox,
    "summary_wind_goal": WindGoalResultsBox,
    "summary_wind_area": WindAreaResultsBox,
    "summary_wind_demand_share": WindDemandShareResultsBox,
    "summary_pv_goal": PVGoalResultsBox,
    "summary_pv_area": PVAreaResultsBox,
    "summary_pv_demand_share": PVDemandShareResultsBox,
}

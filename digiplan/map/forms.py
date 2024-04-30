"""Module containing django forms."""
from __future__ import annotations

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

from . import charts, menu
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


class ResultsBox(TemplateForm):
    """Shows a result summary for a given category in a box."""

    template_name = "widgets/result_box.html"

    def __init__(self, value: str, text: str, category: str) -> None:
        """Initialize parameters for result box widget."""
        super().__init__()
        self.value = value
        self.text = text
        self.category = category


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
                id_s_w_6=parameters["s_w_6"]["start"],
                id_s_w_7=parameters["s_w_7"]["start"],
            )
        key_results["pv_ground"] = menu.detail_key_results(
            id_s_pv_ff_3=parameters["s_pv_ff_3"]["start"],
            id_s_pv_ff_4=parameters["s_pv_ff_4"]["start"],
            id_s_pv_ff_5=parameters["s_pv_ff_5"]["start"],
        )
        key_results["pv_roof"] = menu.detail_key_results(id_s_pv_d_3=parameters["s_pv_d_3"]["start"])
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

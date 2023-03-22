"""Views for map app.

As map app is SPA, this module contains main view and various API points.
"""
import json

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django_mapengine import views

from digiplan.map import config
from digiplan.map.results import core

from . import forms, map_config
from .results import calculations


class MapGLView(TemplateView, views.MapEngineMixin):
    """Main view for map app (SPA)."""

    template_name = "map.html"
    extra_context = {
        "debug": settings.DEBUG,
        "password_protected": settings.PASSWORD_PROTECTION,
        "password": settings.PASSWORD,
        "area_switches": {
            category: [forms.StaticLayerForm(layer) for layer in layers]
            for category, layers in map_config.LEGEND.items()
        },
        "energy_settings_panel": forms.PanelForm(config.ENERGY_SETTINGS_PANEL),
        "heat_settings_panel": forms.PanelForm(config.HEAT_SETTINGS_PANEL),
        "traffic_settings_panel": forms.PanelForm(config.TRAFFIC_SETTINGS_PANEL),
        "use_distilled_mvts": settings.MAP_ENGINE_USE_DISTILLED_MVTS,
        "store_hot_init": config.STORE_HOT_INIT,
    }

    def get_context_data(self, **kwargs) -> dict:
        """Context data for main view.

        Parameters
        ----------
        kwargs
            Optional kwargs

        Returns
        -------
        dict
            context for main view
        """
        # Add unique session ID
        context = super().get_context_data(**kwargs)

        context["settings_parameters"] = config.ENERGY_SETTINGS_PANEL
        context["settings_dependency_map"] = config.SETTINGS_DEPENDENCY_MAP
        context["dependency_parameters"] = config.DEPENDENCY_PARAMETERS

        # Categorize sources
        categorized_sources = {
            category: [
                config.SOURCES[layer.get_layer_id()] for layer in layers if layer.get_layer_id() in config.SOURCES
            ]
            for category, layers in map_config.LEGEND.items()
        }
        context["sources"] = categorized_sources
        context["store_cold_init"] = config.STORE_COLD_INIT

        return context


def get_popup(request: HttpRequest, lookup: str, region: int) -> JsonResponse:  # noqa: ARG001
    """Return popup as html and chart options to render chart on popup.

    Parameters
    ----------
    request : HttpRequest
        Request from app, can hold option for different language
    lookup: str
        Name is used to lookup data and chart functions
    region: int
        ID of region selected on map. Data and chart for popup is calculated for related region.

    Returns
    -------
    JsonResponse
        containing HTML to render popup and chart options to be used in E-Chart.
    """
    data = calculations.create_data(lookup, region)
    chart = calculations.create_chart(lookup, region)

    try:
        html = render_to_string(f"popups/{lookup}.html", context=data)
    except TemplateDoesNotExist:
        html = render_to_string("popups/default.html", context=data)
    return JsonResponse({"html": html, "chart": chart})


# pylint: disable=W0613
def get_choropleth(request: HttpRequest, lookup: str, scenario: str) -> JsonResponse:  # noqa: ARG001
    """Read scenario results from database, aggregate data and send back data.

    Parameters
    ----------
    request : HttpRequest
        Request can contain optional values (i.e. language)
    lookup : str
        which result/calculation shall be shown in choropleth?
    scenario : str
        defines the scenario to look up values for (i.e. status quo or user scenario)

    Returns
    -------
    JsonResponse
        Containing key-value pairs of municipality_ids and values and related color style
    """
    values = calculations.create_choropleth_data(lookup)
    fill_color = settings.MAP_ENGINE_CHOROPLETHS.get_fill_color(lookup, list(values.values()))
    return JsonResponse({"values": values, "fill_color": fill_color})


def get_visualization(request: HttpRequest) -> JsonResponse:
    """Return visualization from oemof simulation result.

    Parameters
    ----------
    request : HttpRequest
        Request for visualization

    Returns
    -------
    JsonResponse
        Visualization of simulation result
    """
    scenario_name = request.GET["scenario"]
    parameters_raw = request.GET.get("parameters")
    parameters = json.loads(parameters_raw) if parameters_raw else {}
    visualization = request.GET["visualization"]
    scenario = core.Scenario(scenario_name, parameters)
    vh = core.VisualizationHandler([scenario])
    vh.add(visualization)
    vh.run()
    return JsonResponse(vh[visualization])

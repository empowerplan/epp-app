"""
Views for map app.

As map app is SPA, this module contains main view and various API points.
"""
import json

from django.conf import settings
from django.http import HttpRequest, response
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_mapengine import views

from digiplan import __version__
from digiplan.map import config, menu

from . import charts, choropleths, forms, map_config, popups, utils


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
        "pv_map_control": _("Negativkriterien PV"),
        "store_hot_init": config.STORE_HOT_INIT,
        "oemof_scenario": settings.OEMOF_SCENARIO,
        "markdown": {"reveal_equity": config.REVEAL_EQUITY_MD},
    }

    def get_context_data(self, **kwargs) -> dict:
        """
        Context data for main view.

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

        # Move region_boundaries layer to bottom:
        context["mapengine_layers"].insert(
            0,
            context["mapengine_layers"].pop(
                next(
                    i
                    for i, element in enumerate(context["mapengine_layers"])
                    if element["id"] == "region_boundaries" or element["id"] == "region_boundaries_distilled"
                ),
            ),
        )

        context["panels"] = [
            forms.EnergyPanelForm(
                utils.get_translated_json_from_file(config.ENERGY_SETTINGS_PANEL_FILE, self.request),
                additional_parameters=utils.get_translated_json_from_file(config.ADDITIONAL_ENERGY_SETTINGS_FILE),
            ),
            forms.HeatPanelForm(
                utils.get_translated_json_from_file(config.HEAT_SETTINGS_PANEL_FILE, self.request),
                additional_parameters=utils.get_translated_json_from_file(config.ADDITIONAL_HEAT_SETTINGS_FILE),
            ),
            forms.TrafficPanelForm(
                utils.get_translated_json_from_file(config.TRAFFIC_SETTINGS_PANEL_FILE, self.request),
                additional_parameters=utils.get_translated_json_from_file(config.ADDITIONAL_TRAFFIC_SETTINGS_FILE),
            ),
        ]

        context["settings_parameters"] = config.ENERGY_SETTINGS_PANEL
        context["scenario_settings"] = config.SCENARIO_SETTINGS

        # Categorize sources
        categorized_sources = {
            category: [config.SOURCES[layer.layer_id] for layer in layers if layer.layer_id in config.SOURCES]
            for category, layers in map_config.LEGEND.items()
        }
        context["sources"] = categorized_sources
        context["store_cold_init"] = config.STORE_COLD_INIT

        context["wind_capacity"] = charts.Chart("wind_capacity").render()
        context["wind_areas"] = charts.Chart("wind_areas").render()
        context["pv_ground_capacity"] = charts.Chart("pv_ground_capacity").render()
        context["pv_ground_areas"] = charts.Chart("pv_ground_areas").render()
        context["pv_roof_capacity"] = charts.Chart("pv_roof_capacity").render()
        context["pv_roof_areas"] = charts.Chart("pv_roof_areas").render()
        context["detailed_overview"] = charts.Chart("detailed_overview").render()
        context["electricity_overview"] = charts.Chart("electricity_overview").render()
        context["electricity_autarky"] = charts.Chart("electricity_autarky").render()
        context["heat_decentralized"] = charts.Chart("heat_decentralized").render()
        context["heat_centralized"] = charts.Chart("heat_centralized").render()
        context["onboarding_wind"] = charts.Chart("onboarding_wind").render()
        context["onboarding_pv_ground"] = charts.Chart("onboarding_pv_ground").render()
        context["onboarding_pv_roof"] = charts.Chart("onboarding_pv_roof").render()

        context["app_version"] = str(__version__)

        return context


def get_popup(request: HttpRequest, lookup: str, region: int) -> response.JsonResponse:
    """
    Return popup as html and chart options to render chart on popup.

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
    map_state = request.GET.dict()
    lookup = lookup.removesuffix("_distilled")
    popup = popups.POPUPS[lookup](lookup, region, map_state=map_state)
    return popup.render()


# pylint: disable=W0613
def get_choropleth(request: HttpRequest, lookup: str, layer_id: str) -> response.JsonResponse:  # noqa: ARG001
    """
    Read scenario results from database, aggregate data and send back data.

    Parameters
    ----------
    request : HttpRequest
        Request can contain optional values (i.e. language)
    lookup : str
        which result/calculation shall be shown in choropleth?
    layer_id : str
        layer ID of given choropleth

    Returns
    -------
    JsonResponse
        Containing key-value pairs of municipality_ids and values and related color style
    """
    map_state = request.GET.dict()
    return choropleths.CHOROPLETHS[lookup](lookup, map_state)


def get_charts(request: HttpRequest) -> response.JsonResponse:
    """
    Return all result charts at once.

    Parameters
    ----------
    request: HttpRequest
        request holding simulation ID in map_state dict

    Returns
    -------
    JsonResponse
        holding dict with `div_id` as keys and chart options as values.
        `div_id` is used in frontend to detect chart container.
    """
    lookups = request.GET.getlist("charts[]")
    map_state = json.loads(request.GET.get("map_state", "{}"))
    return response.JsonResponse(
        {lookup: charts.CHARTS[lookup](user_settings=map_state).render() for lookup in lookups},
    )


def get_summary_results(request: HttpRequest) -> response.JsonResponse:
    """
    Return all summary results as HTMLs with related div ID.

    Parameters
    ----------
    request: HttpRequest
        holding user settings

    Returns
    -------
    JsonResponse
        holding dict containing div IDs as key and summary results as HTML as values
    """
    lookups = request.GET.getlist("summaries[]")
    map_state = json.loads(request.GET.get("map_state", "{}"))
    return response.JsonResponse(
        {lookup: forms.SUMMARY_RESULTS[lookup](parameters=map_state).render() for lookup in lookups},
    )


class DetailKeyResultsView(TemplateView):
    """Return HTMX-partial for requested detail key results."""

    template_name = "forms/panel_energy.html#key_results"

    def get_context_data(self, **kwargs) -> dict:  # noqa: ARG002
        """Get detail key results for requested technology."""
        # Cut off leading "id_" from form field id
        parameters = {
            key[3:] if key.startswith("id_") else key: value for key, value in self.request.GET.dict().items()
        }
        return {f"key_result_{key}": value for key, value in menu.detail_key_results(**parameters).items()}

"""
Application settings for digiplan's map app.

Ready function is used to register hooks in django-oemof.
This is necessary, as django otherwise complains about "app not ready".
"""

from django.apps import AppConfig


class MapConfig(AppConfig):
    """Config for digiplan map app."""

    name = "digiplan.map"

    def ready(self) -> None:
        """Content in here is run when app is ready."""
        # pylint: disable=C0415
        from django_oemof import hooks  # noqa: PLC0415

        # pylint: disable=C0415
        from digiplan.map import hooks as digiplan_hooks  # noqa: PLC0415

        hooks.register_hook(
            hooks.HookType.SETUP,
            hooks.Hook(scenario=hooks.ALL_SCENARIOS, function=digiplan_hooks.read_parameters),
        )

        hooks.register_hook(
            hooks.HookType.PARAMETER,
            hooks.Hook(scenario=hooks.ALL_SCENARIOS, function=digiplan_hooks.adapt_electricity_demand),
        )

        hooks.register_hook(
            hooks.HookType.PARAMETER,
            hooks.Hook(scenario=hooks.ALL_SCENARIOS, function=digiplan_hooks.adapt_heat_demand),
        )

        hooks.register_hook(
            hooks.HookType.PARAMETER,
            hooks.Hook(scenario=hooks.ALL_SCENARIOS, function=digiplan_hooks.adapt_heatpumps),
        )

        hooks.register_hook(
            hooks.HookType.PARAMETER,
            hooks.Hook(scenario=hooks.ALL_SCENARIOS, function=digiplan_hooks.adapt_heat_components),
        )

        hooks.register_hook(
            hooks.HookType.PARAMETER,
            hooks.Hook(scenario=hooks.ALL_SCENARIOS, function=digiplan_hooks.adapt_storages),
        )

        hooks.register_hook(
            hooks.HookType.PARAMETER,
            hooks.Hook(scenario=hooks.ALL_SCENARIOS, function=digiplan_hooks.adapt_renewable_capacities),
        )

        hooks.register_hook(
            hooks.HookType.ENERGYSYSTEM,
            hooks.Hook(scenario=hooks.ALL_SCENARIOS, function=digiplan_hooks.adapt_extraction_turbines),
        )

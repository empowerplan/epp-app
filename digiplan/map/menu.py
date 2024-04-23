"""Add calculations for menu items."""

from . import config, datapackage


def detail_key_results(technology: str, **kwargs: dict) -> dict:
    """Calculate detail key results for given technology."""
    areas = datapackage.get_potential_areas()
    potential_capacities = datapackage.get_potential_values()  # in MW
    full_load_hours = datapackage.get_full_load_hours(2045)
    nominal_power_per_unit = config.TECHNOLOGY_DATA["nominal_power_per_unit"]["wind"]

    if technology.startswith("wind"):
        percentage = 1
        if technology == "wind_2024":
            percentage = float(kwargs["id_s_w_6"]) / float(config.ENERGY_SETTINGS_PANEL["s_w_6"]["max"])
        if technology == "wind_2027":
            percentage = float(kwargs["id_s_w_7"]) / 100
        return {
            "area": areas[technology] * 100 * percentage,
            "turbines": potential_capacities[technology] / nominal_power_per_unit * percentage,
            "energy": potential_capacities[technology] * full_load_hours["wind"] * percentage * 1e-6,
        }
    if technology == "pv_ground":
        percentages = {
            "pv_soil_quality_low": int(kwargs["id_s_pv_ff_3"]) / 100,
            "pv_soil_quality_medium": int(kwargs["id_s_pv_ff_4"]) / 100,
            "pv_permanent_crops": int(kwargs["id_s_pv_ff_5"]) / 100,
        }
        flh_mapping = {
            "pv_soil_quality_low": "pv_ground",
            "pv_soil_quality_medium": "pv_ground_vertical_bifacial",
            "pv_permanent_crops": "pv_ground_elevated",
        }
        return {
            "area": sum(areas[pv_type] * 100 * percentages[pv_type] for pv_type in percentages),
            "energy": sum(
                potential_capacities[pv_type] * full_load_hours[flh_mapping[pv_type]] * percentages[pv_type]
                for pv_type in percentages
            )
            * 1e-6,
        }
    if technology == "pv_roof":
        percentage = int(kwargs["id_s_pv_d_3"]) / 100
        return {
            "area": areas[technology] * 100 * percentage,
            "energy": potential_capacities[technology] * full_load_hours[technology] * percentage * 1e-6,
        }
    raise KeyError(f"Unknown technology '{technology}'.")

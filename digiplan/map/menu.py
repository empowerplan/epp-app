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
            percentage = int(kwargs["id_s_w_6"]) / 100
        if technology == "wind_2027":
            percentage = int(kwargs["id_s_w_7"]) / 100
        return {
            "area": areas[technology] / 100 * percentage,
            "turbines": potential_capacities[technology] / nominal_power_per_unit * percentage,
            "energy": potential_capacities[technology] * full_load_hours["wind"] * percentage * 1e-6,
        }
    if technology == "pv_ground":
        return {"area": 33, "energy": 2001}
    if technology == "pv_roof":
        return {"area": 34, "energy": 2002}
    raise KeyError(f"Unknown technology '{technology}'.")

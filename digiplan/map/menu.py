"""Add calculations for menu items."""

from . import calculations, config, datapackage


def detail_key_results(**kwargs: dict) -> dict:
    """Calculate detail key results for given technology."""
    shares = calculations.calculate_potential_shares(kwargs)
    areas = datapackage.get_potential_areas().sum()  # in km2
    potential_capacities = datapackage.get_potential_capacities().sum()  # in MW
    full_load_hours = datapackage.get_full_load_hours(2045)
    nominal_power_per_unit = config.TECHNOLOGY_DATA["nominal_power_per_unit"]["wind"]

    if "wind_year" in kwargs:
        wind_year = kwargs["wind_year"]
        share = shares["wind"]
        return {
            "area": areas[wind_year] * 100 * share,
            "turbines": potential_capacities[wind_year] / nominal_power_per_unit * share,
            "energy": potential_capacities[wind_year] * full_load_hours["wind"] * share * 1e-6,
        }
    if "s_pv_ff_3" in kwargs:
        flh_mapping = {
            "pv_soil_quality_low": "pv_ground",
            "pv_soil_quality_medium": "pv_ground_vertical_bifacial",
            "pv_permanent_crops": "pv_ground_elevated",
        }
        return {
            "area": sum(areas[pv_type] * 100 * shares[pv_type] for pv_type in shares),
            "energy": sum(
                potential_capacities[pv_type] * full_load_hours[flh_mapping[pv_type]] * shares[pv_type]
                for pv_type in shares
            )
            * 1e-6,
        }
    if "s_pv_d_3" in kwargs:
        return {
            "area": areas["pv_roof"] * 100 * shares["pv_roof"],
            "energy": potential_capacities["pv_roof"] * full_load_hours["pv_roof"] * shares["pv_roof"] * 1e-6,
        }
    raise KeyError(f"Unknown parameters ({kwargs}).")

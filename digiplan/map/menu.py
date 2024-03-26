"""Add calculations for menu items."""


def detail_key_results(technology: str, **kwargs: dict) -> dict:  # noqa: ARG001
    """Calculate detail key results for given technology."""
    if technology == "wind_2018":
        return {"area": 300, "turbines": 20, "energy": 2000}
    if technology == "wind_2024":
        return {"area": 400, "turbines": 30, "energy": 3000}
    if technology == "wind_2027":
        return {"area": 500, "turbines": 50, "energy": 4000}
    if technology == "pv_ground":
        return {"area": 33, "energy": 2001}
    if technology == "pv_roof":
        return {"area": 34, "energy": 2002}
    raise KeyError(f"Unknown technology '{technology}'.")

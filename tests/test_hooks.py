"""Test hooks."""

import pandas as pd

from digiplan.map import hooks


def test_adapt_electricity_demand(monkeypatch):  # noqa: ANN001
    """Test electricity demand setup."""

    def fake_get_power_demand(sector: str) -> dict:
        """Return dummy data for electricity demand."""
        # returns dict-like with DataFrame under sector name
        sector_data = pd.DataFrame({"2022": [1.0, 2.0, 3.0]})
        return {sector: sector_data}

    monkeypatch.setattr(hooks.datapackage, "get_power_demand", fake_get_power_demand)

    data = {"s_v_1": 0, "s_v_3": 50, "s_v_4": 100, "s_v_5": 0}
    out = hooks.adapt_electricity_demand("scenario", data)
    # hh: sum 6 * 0.5
    assert out["ABW-electricity-demand_hh"]["amount"] == 3.0
    # cts: sum 6 * 1.0
    assert out["ABW-electricity-demand_cts"]["amount"] == 6.0
    # ind: sum 6 * 0.0
    assert out["ABW-electricity-demand_ind"]["amount"] == 0.0


def test_adapt_renewable_capacities(monkeypatch):  # noqa: ANN001
    """Test adaptation of renewable capacities."""
    # profiles and flh
    monkeypatch.setattr(
        hooks.datapackage,
        "get_full_load_hours",
        lambda _: {
            "wind": 2.0,
            "pv_ground": 1.0,
            "pv_roof": 1.0,
            "ror": 1.0,
        },
    )

    # simple profile series of ones
    monkeypatch.setattr(hooks.datapackage, "get_profile", lambda _, __: pd.Series([1, 1, 1, 1]))

    tech = {
        "batteries": {
            "large": {"nominal_power_per_storage_capacity": 0.5},
            "small": {
                "nominal_power_per_storage_capacity": 0.25,
                "storage_capacity_per_pv_power": 2.0,
            },
        },
    }
    monkeypatch.setattr(hooks.config, "TECHNOLOGY_DATA", tech)

    data = {
        "s_w_1": 10.0,
        "s_pv_ff_1": 5.0,
        "s_pv_d_1": 3.0,
        "s_h_1": 1.0,
        "s_s_g_1": 100,  # percent of daily energy
        "s_pv_d_4": 50,  # percent of pv rooftop power to small batteries
        # keys to be removed
        "s_pv_ff_3": 0,
        "s_pv_ff_4": 0,
        "s_pv_ff_5": 0,
        "s_pv_d_3": 0,
    }

    out = hooks.adapt_renewable_capacities("scenario", data)
    # profiles added
    assert "profile" in out["ABW-wind-onshore"]
    # large scale battery size > 0
    assert out["ABW-electricity-large_scale_battery"]["storage_capacity"] > 0
    # small scale battery depends on rooftop pv
    assert out["ABW-electricity-small_scale_battery"]["storage_capacity"] == 0.5 * 3.0 * 2.0

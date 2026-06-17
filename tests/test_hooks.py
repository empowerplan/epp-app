"""Test hooks."""

import pandas as pd
import pytest

from digiplan.map import hooks


def test_adapt_heatpumps():
    """Test adaptation of heatpumps."""
    data = {
        "w_d_wp_3": 10.0,
        "w_d_wp_4": 11.0,
        "w_d_wp_5": 12.0,
        "w_z_wp_1": 13.0,
        "ABW-heat_decentral-demand_hh": {"amount": 100},
        "ABW-heat_decentral-demand_cts": {"amount": 120},
        "ABW-heat_decentral-demand_ind": {"amount": 130},
        "ABW-heat_central-demand_hh": {"amount": 140},
        "ABW-heat_central-demand_cts": {"amount": 150},
        "ABW-heat_central-demand_ind": {"amount": 160},
    }
    out = hooks.adapt_heatpumps("tsam_40_24_1_cost_0", data)

    # Energies from heatpumps
    assert out["hp_energy"]["decentral"] == 100 * 0.10 + 120 * 0.11 + 130 * 0.12
    assert out["hp_energy"]["central"] == (140 + 150 + 160) * 0.13

    data = {
        "w_d_wp_3": 50.0,
        "w_d_wp_4": 50.0,
        "w_d_wp_5": 50.0,
        "w_z_wp_1": 50.0,
        "ABW-heat_decentral-demand_hh": {"amount": 100},
        "ABW-heat_decentral-demand_cts": {"amount": 120},
        "ABW-heat_decentral-demand_ind": {"amount": 130},
        "ABW-heat_central-demand_hh": {"amount": 140},
        "ABW-heat_central-demand_cts": {"amount": 150},
        "ABW-heat_central-demand_ind": {"amount": 160},
    }
    out = hooks.adapt_heatpumps("tsam_40_24_1_cost_0", data)

    # Energies from heatpumps
    assert out["hp_energy"]["decentral"] == 100 * 0.50 + 120 * 0.50 + 130 * 0.50
    assert out["hp_energy"]["central"] == (140 + 150 + 160) * 0.50


def test_adapt_heat_components():
    """Test adaptation of heat components."""
    data = {
        "w_d_wp_3": 10.0,
        "w_d_wp_4": 11.0,
        "w_d_wp_5": 12.0,
        "w_z_wp_1": 13.0,
        "ABW-heat_decentral-demand_hh": {"amount": 100},
        "ABW-heat_decentral-demand_cts": {"amount": 120},
        "ABW-heat_decentral-demand_ind": {"amount": 130},
        "hp_energy": {"decentral": 100 * 0.10 + 120 * 0.11 + 130 * 0.12, "central": (140 + 150 + 160) * 0.13},
        "ABW-heat_central-demand_hh": {"amount": 140},
        "ABW-heat_central-demand_cts": {"amount": 150},
        "ABW-heat_central-demand_ind": {"amount": 160},
        "ABW-electricity-heatpump_central": {
            "capacity": 0.01799216699276035,
        },
        "ABW-electricity-heatpump_decentral": {
            "capacity": 0.011535782344309641,
        },
    }
    out = hooks.adapt_heat_components("tsam_40_24_1_cost_0", data)

    hp_dec_share = 0.8876581123758391
    boiler_dec_share = 0.056497203680542236 / (1 - hp_dec_share)
    ch4ext_dec_share = 0.009995754184134148 / (1 - hp_dec_share)
    remaining_demand_dec = 100 + 120 + 130 - data["hp_energy"]["decentral"]

    assert out["ABW-electricity-pth_decentral"]["output_parameters"]["full_load_time_max"] == pytest.approx(
        remaining_demand_dec * boiler_dec_share,
    )
    assert out["turbines"]["ABW-ch4-extchp_decentral"][0] == pytest.approx(remaining_demand_dec * ch4ext_dec_share)

    data = {
        "w_d_wp_3": 50.0,
        "w_d_wp_4": 50.0,
        "w_d_wp_5": 50.0,
        "w_z_wp_1": 13.0,
        "ABW-heat_decentral-demand_hh": {"amount": 100},
        "ABW-heat_decentral-demand_cts": {"amount": 120},
        "ABW-heat_decentral-demand_ind": {"amount": 130},
        "hp_energy": {"decentral": 100 * 0.50 + 120 * 0.50 + 130 * 0.50, "central": (140 + 150 + 160) * 0.13},
        "ABW-heat_central-demand_hh": {"amount": 140},
        "ABW-heat_central-demand_cts": {"amount": 150},
        "ABW-heat_central-demand_ind": {"amount": 160},
        "ABW-electricity-heatpump_central": {"capacity": 0.0692006422798475},
        "ABW-electricity-heatpump_decentral": {"capacity": 0.05333784493663601},
    }
    out = hooks.adapt_heat_components("tsam_40_24_1_cost_0", data)

    hp_dec_share = 0.8876581123758391
    boiler_dec_share = 0.056497203680542236 / (1 - hp_dec_share)
    ch4ext_dec_share = 0.009995754184134148 / (1 - hp_dec_share)
    remaining_demand_dec = 100 + 120 + 130 - data["hp_energy"]["decentral"]

    assert out["ABW-electricity-pth_decentral"]["output_parameters"]["full_load_time_max"] == pytest.approx(
        remaining_demand_dec * boiler_dec_share,
    )
    assert out["turbines"]["ABW-ch4-extchp_decentral"][0] == pytest.approx(remaining_demand_dec * ch4ext_dec_share)


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

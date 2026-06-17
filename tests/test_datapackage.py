"""Module to test datapackage functions."""

import pytest

from digiplan.map import datapackage


def test_heat_capacity_shares():
    """Test reading heat structure shares from digipipe datapackage."""
    shares = datapackage.get_heat_capacity_shares("dec")
    hp_dec_share = 0.8876581123758391
    assert shares["electricity_direct_heating"] == pytest.approx(0.056497203680542236 / (1 - hp_dec_share))
    assert shares["solar_thermal"] == pytest.approx(0.004739072023327305 / (1 - hp_dec_share))

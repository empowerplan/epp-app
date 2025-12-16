"""Module to test utils."""

import pandas as pd

from digiplan.map.utils import interpolate_year_from_dataframe


def test_interpolate_year_from_dataframe() -> None:
    """Test interpolation and extrapolation."""
    df = pd.DataFrame({2020: [3, 3, 3], 2040: [5, 5, 5]})

    interpolated_df = interpolate_year_from_dataframe(df, 2030)
    pd.testing.assert_series_equal(interpolated_df, pd.Series([4, 4, 4], name=2030, dtype=float))

    interpolated_df = interpolate_year_from_dataframe(df, 2050)
    pd.testing.assert_series_equal(interpolated_df, pd.Series([6, 6, 6], name=2050, dtype=float))

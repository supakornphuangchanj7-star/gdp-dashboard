import math
import pandas as pd
import pytest
from pathlib import Path
from streamlit_app import get_gdp_data


def test_get_gdp_data_structure():
    """Verify get_gdp_data loads and pivots expected columns and years."""
    df = get_gdp_data()
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == {"Country Code", "Year", "GDP"}
    assert df["Year"].min() == 1960
    assert df["Year"].max() == 2022


def test_indexed_gdp_lookup_accuracy():
    """Verify indexed lookup produces identical GDP values to original boolean mask filtering."""
    gdp_df = get_gdp_data()
    from_year = 1960
    to_year = 2022
    selected_countries = ["DEU", "FRA", "GBR", "BRA", "MEX", "JPN", "USA", "CHN"]

    # Original method
    first_year_orig = gdp_df[gdp_df["Year"] == from_year]
    last_year_orig = gdp_df[gdp_df["Year"] == to_year]

    # Optimized indexed method
    first_year_opt = gdp_df[gdp_df["Year"] == from_year].set_index("Country Code")["GDP"]
    last_year_opt = gdp_df[gdp_df["Year"] == to_year].set_index("Country Code")["GDP"]

    for country in selected_countries:
        first_gdp_orig = first_year_orig[first_year_orig["Country Code"] == country]["GDP"].iat[0] / 1e9
        last_gdp_orig = last_year_orig[last_year_orig["Country Code"] == country]["GDP"].iat[0] / 1e9

        first_gdp_opt = first_year_opt.get(country, math.nan) / 1e9
        last_gdp_opt = last_year_opt.get(country, math.nan) / 1e9

        assert first_gdp_orig == first_gdp_opt or (math.isnan(first_gdp_orig) and math.isnan(first_gdp_opt))
        assert last_gdp_orig == last_gdp_opt or (math.isnan(last_gdp_orig) and math.isnan(last_gdp_opt))


def test_indexed_gdp_lookup_missing_country():
    """Verify indexed lookup gracefully handles missing or invalid country codes."""
    gdp_df = get_gdp_data()
    from_year = 1990
    first_year = gdp_df[gdp_df["Year"] == from_year].set_index("Country Code")["GDP"]

    missing_val = first_year.get("NON_EXISTENT_COUNTRY", math.nan)
    assert math.isnan(missing_val)

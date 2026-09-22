import pandas as pd
import math

from streamlit_app import get_gdp_data

def test_get_gdp_data():
    df = get_gdp_data()
    assert not df.empty
    assert 'Country Code' in df.columns
    assert 'Year' in df.columns
    assert 'GDP' in df.columns
    assert df['Year'].min() == 1960
    assert df['Year'].max() == 2022

def test_gdp_metric_calculation():
    gdp_df = get_gdp_data()
    from_year, to_year = 1990, 2022
    selected_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']

    first_year_gdp = gdp_df[gdp_df['Year'] == from_year].set_index('Country Code')['GDP']
    last_year_gdp = gdp_df[gdp_df['Year'] == to_year].set_index('Country Code')['GDP']

    for country in selected_countries:
        first_gdp_val = first_year_gdp.get(country)
        last_gdp_val = last_year_gdp.get(country)

        first_gdp = (first_gdp_val / 1000000000) if first_gdp_val is not None else float('nan')
        last_gdp = (last_gdp_val / 1000000000) if last_gdp_val is not None else float('nan')

        assert not math.isnan(first_gdp)
        assert not math.isnan(last_gdp)
        assert last_gdp > 0

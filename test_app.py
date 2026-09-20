import math
import pandas as pd
import pytest
from streamlit_app import get_gdp_data

def test_get_gdp_data():
    df = get_gdp_data()
    assert isinstance(df, pd.DataFrame)
    assert set(['Country Code', 'Year', 'GDP']).issubset(df.columns)
    assert not df.empty

def test_gdp_metric_calculation_logic():
    gdp_df = get_gdp_data()
    selected_countries = ['DEU', 'FRA', 'USA']
    from_year, to_year = 1990, 2020

    filtered_gdp_df = gdp_df[
        (gdp_df['Country Code'].isin(selected_countries))
        & (gdp_df['Year'] <= to_year)
        & (from_year <= gdp_df['Year'])
    ]

    # Original algorithm
    first_year = gdp_df[gdp_df['Year'] == from_year]
    last_year = gdp_df[gdp_df['Year'] == to_year]

    orig_results = {}
    for country in selected_countries:
        first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
        last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
        orig_results[country] = (first_gdp, last_gdp)

    # Optimized algorithm
    first_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == from_year]
    last_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == to_year]
    first_gdp_map = dict(zip(first_year_df['Country Code'], first_year_df['GDP']))
    last_gdp_map = dict(zip(last_year_df['Country Code'], last_year_df['GDP']))

    opt_results = {}
    for country in selected_countries:
        first_gdp = first_gdp_map.get(country, math.nan) / 1000000000
        last_gdp = last_gdp_map.get(country, math.nan) / 1000000000
        opt_results[country] = (first_gdp, last_gdp)

    assert orig_results == opt_results

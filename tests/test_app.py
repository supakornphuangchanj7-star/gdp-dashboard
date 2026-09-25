import math
import pandas as pd
from pathlib import Path
from streamlit_app import get_gdp_data

def test_get_gdp_data():
    df = get_gdp_data()
    assert isinstance(df, pd.DataFrame)
    assert 'Country Code' in df.columns
    assert 'Year' in df.columns
    assert 'GDP' in df.columns
    assert df['Year'].min() == 1960
    assert df['Year'].max() == 2022

def test_metric_calculation_correctness():
    df = get_gdp_data()
    selected_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
    from_year, to_year = 1960, 2022

    filtered_gdp_df = df[
        (df['Country Code'].isin(selected_countries))
        & (df['Year'] <= to_year)
        & (from_year <= df['Year'])
    ]

    first_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == from_year]
    last_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == to_year]
    first_gdp_map = dict(zip(first_year_df['Country Code'], first_year_df['GDP']))
    last_gdp_map = dict(zip(last_year_df['Country Code'], last_year_df['GDP']))

    for country in selected_countries:
        first_gdp = first_gdp_map.get(country, float('nan')) / 1000000000
        last_gdp = last_gdp_map.get(country, float('nan')) / 1000000000

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        if country == 'FRA':
            assert growth != 'n/a'
            assert delta_color == 'normal'
        elif country == 'DEU':
            assert growth == 'n/a'
            assert delta_color == 'off'

def test_metric_calculation_missing_or_nan_country():
    df = get_gdp_data()
    selected_countries = ['NON_EXISTENT_COUNTRY']
    from_year, to_year = 1960, 2022

    filtered_gdp_df = df[
        (df['Country Code'].isin(selected_countries))
        & (df['Year'] <= to_year)
        & (from_year <= df['Year'])
    ]

    first_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == from_year]
    last_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == to_year]
    first_gdp_map = dict(zip(first_year_df['Country Code'], first_year_df['GDP']))
    last_gdp_map = dict(zip(last_year_df['Country Code'], last_year_df['GDP']))

    first_gdp = first_gdp_map.get('NON_EXISTENT_COUNTRY', float('nan')) / 1000000000
    assert math.isnan(first_gdp)

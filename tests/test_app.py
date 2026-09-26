import math
import pandas as pd
from streamlit_app import get_gdp_data

def test_get_gdp_data():
    df = get_gdp_data()
    assert isinstance(df, pd.DataFrame)
    assert 'Country Code' in df.columns
    assert 'Year' in df.columns
    assert 'GDP' in df.columns
    assert df['Year'].min() == 1960
    assert df['Year'].max() == 2022

def test_indexed_gdp_lookup():
    df = get_gdp_data()
    from_year = 1960
    to_year = 2022
    selected_countries = ['DEU', 'FRA', 'GBR', 'USA', 'NONEXISTENT']

    first_year_gdp = df[df['Year'] == from_year].set_index('Country Code')['GDP']
    last_year_gdp = df[df['Year'] == to_year].set_index('Country Code')['GDP']

    for country in selected_countries:
        first_gdp = first_year_gdp.get(country, math.nan) / 1000000000
        last_gdp = last_year_gdp.get(country, math.nan) / 1000000000

        # Check against direct filtering
        f_sub = df[(df['Year'] == from_year) & (df['Country Code'] == country)]
        l_sub = df[(df['Year'] == to_year) & (df['Country Code'] == country)]

        orig_first = f_sub['GDP'].iat[0] / 1000000000 if len(f_sub) > 0 else math.nan
        orig_last = l_sub['GDP'].iat[0] / 1000000000 if len(l_sub) > 0 else math.nan

        if math.isnan(orig_first):
            assert math.isnan(first_gdp)
        else:
            assert first_gdp == orig_first

        if math.isnan(orig_last):
            assert math.isnan(last_gdp)
        else:
            assert last_gdp == orig_last

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

def test_gdp_lookup_logic():
    df = get_gdp_data()
    from_year = 1960
    to_year = 2022
    selected_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']

    first_year = df[df['Year'] == from_year]
    last_year = df[df['Year'] == to_year]

    first_gdp_map = dict(zip(first_year['Country Code'], first_year['GDP']))
    last_gdp_map = dict(zip(last_year['Country Code'], last_year['GDP']))

    for country in selected_countries:
        # Check original baseline lookup
        orig_first = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1e9
        orig_last = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1e9

        # Check map lookup
        map_first = first_gdp_map.get(country, math.nan) / 1e9
        map_last = last_gdp_map.get(country, math.nan) / 1e9

        if math.isnan(orig_first):
            assert math.isnan(map_first)
        else:
            assert orig_first == map_first

        if math.isnan(orig_last):
            assert math.isnan(map_last)
        else:
            assert orig_last == map_last

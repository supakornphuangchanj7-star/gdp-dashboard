import math
import unittest
from streamlit_app import get_gdp_data

class TestGdpDashboard(unittest.TestCase):
    def setUp(self):
        self.gdp_df = get_gdp_data()

    def test_get_gdp_data_structure(self):
        """Test that get_gdp_data returns expected columns and year range."""
        self.assertIn('Country Code', self.gdp_df.columns)
        self.assertIn('Year', self.gdp_df.columns)
        self.assertIn('GDP', self.gdp_df.columns)

        min_year = self.gdp_df['Year'].min()
        max_year = self.gdp_df['Year'].max()
        self.assertEqual(min_year, 1960)
        self.assertEqual(max_year, 2022)

    def test_filtered_gdp_lookup(self):
        """Test the dictionary lookup logic used for GDP metrics calculation."""
        selected_countries = ['DEU', 'FRA', 'JPN']
        from_year, to_year = 1990, 2020

        filtered_gdp_df = self.gdp_df[
            (self.gdp_df['Country Code'].isin(selected_countries))
            & (self.gdp_df['Year'] <= to_year)
            & (from_year <= self.gdp_df['Year'])
        ]

        first_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == from_year]
        last_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == to_year]

        first_gdp_map = dict(zip(first_year_df['Country Code'], first_year_df['GDP']))
        last_gdp_map = dict(zip(last_year_df['Country Code'], last_year_df['GDP']))

        for country in selected_countries:
            self.assertIn(country, first_gdp_map)
            self.assertIn(country, last_gdp_map)
            first_gdp = first_gdp_map.get(country, math.nan) / 1e9
            last_gdp = last_gdp_map.get(country, math.nan) / 1e9
            self.assertFalse(math.isnan(first_gdp))
            self.assertFalse(math.isnan(last_gdp))

    def test_empty_countries_lookup(self):
        """Test lookup behavior when no countries are selected."""
        selected_countries = []
        from_year, to_year = 1990, 2020

        filtered_gdp_df = self.gdp_df[
            (self.gdp_df['Country Code'].isin(selected_countries))
            & (self.gdp_df['Year'] <= to_year)
            & (from_year <= self.gdp_df['Year'])
        ]

        first_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == from_year]
        first_gdp_map = dict(zip(first_year_df['Country Code'], first_year_df['GDP']))

        self.assertEqual(len(first_gdp_map), 0)
        missing_val = first_gdp_map.get('UNKNOWN', math.nan)
        self.assertTrue(math.isnan(missing_val))

if __name__ == '__main__':
    unittest.main()

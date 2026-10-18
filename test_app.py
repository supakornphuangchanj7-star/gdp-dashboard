import math
import unittest
from streamlit_app import get_gdp_data


class TestGdpDashboard(unittest.TestCase):
    def test_get_gdp_data(self):
        gdp_df = get_gdp_data()
        self.assertIn('Country Code', gdp_df.columns)
        self.assertIn('Year', gdp_df.columns)
        self.assertIn('GDP', gdp_df.columns)
        self.assertGreater(len(gdp_df), 0)

    def test_gdp_dict_lookup(self):
        gdp_df = get_gdp_data()
        from_year = 1990
        to_year = 2022

        first_year_gdp = gdp_df[gdp_df['Year'] == from_year].set_index('Country Code')['GDP'].to_dict()
        last_year_gdp = gdp_df[gdp_df['Year'] == to_year].set_index('Country Code')['GDP'].to_dict()

        selected_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
        for country in selected_countries:
            self.assertIn(country, first_year_gdp)
            self.assertIn(country, last_year_gdp)

            fg = first_year_gdp.get(country, float('nan')) / 1000000000
            lg = last_year_gdp.get(country, float('nan')) / 1000000000

            self.assertFalse(math.isnan(fg))
            self.assertFalse(math.isnan(lg))
            self.assertGreater(fg, 0)
            self.assertGreater(lg, 0)


if __name__ == '__main__':
    unittest.main()

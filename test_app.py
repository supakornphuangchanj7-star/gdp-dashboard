import math
import unittest

from streamlit_app import get_gdp_data


class TestGDPAppPerformanceAndEquivalence(unittest.TestCase):
    def test_gdp_indexing_equivalence(self):
        gdp_df = get_gdp_data()
        from_year = 1960
        to_year = 2022
        all_countries = list(gdp_df['Country Code'].unique())

        first_year = gdp_df[gdp_df['Year'] == from_year]
        last_year = gdp_df[gdp_df['Year'] == to_year]

        first_year_gdp = first_year.set_index('Country Code')['GDP']
        last_year_gdp = last_year.set_index('Country Code')['GDP']

        for country in all_countries:
            orig_first = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
            orig_last = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

            opt_first = first_year_gdp.loc[country] / 1000000000
            opt_last = last_year_gdp.loc[country] / 1000000000

            if math.isnan(orig_first):
                self.assertTrue(math.isnan(opt_first))
            else:
                self.assertEqual(orig_first, opt_first)

            if math.isnan(orig_last):
                self.assertTrue(math.isnan(opt_last))
            else:
                self.assertEqual(orig_last, opt_last)

if __name__ == '__main__':
    unittest.main()

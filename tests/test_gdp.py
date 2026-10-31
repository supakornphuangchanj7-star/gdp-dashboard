import unittest
import math
import pandas as pd
from pathlib import Path


class TestGDPLookup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_path = Path(__file__).parent.parent / 'data/gdp_data.csv'
        raw_gdp_df = pd.read_csv(data_path)
        cls.gdp_df = raw_gdp_df.melt(
            ['Country Code'],
            [str(x) for x in range(1960, 2023)],
            'Year',
            'GDP',
        )
        cls.gdp_df['Year'] = pd.to_numeric(cls.gdp_df['Year'])

    def test_lookup_equivalence(self):
        """Verify that dictionary lookup produces identical results to DataFrame filtering."""
        from_year = 1960
        to_year = 2022
        selected_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']

        first_year = self.gdp_df[self.gdp_df['Year'] == from_year]
        last_year = self.gdp_df[self.gdp_df['Year'] == to_year]

        first_gdp_by_country = dict(zip(first_year['Country Code'], first_year['GDP']))
        last_gdp_by_country = dict(zip(last_year['Country Code'], last_year['GDP']))

        for country in selected_countries:
            # Original approach
            orig_first = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1e9
            orig_last = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1e9

            # Optimized approach
            opt_first = first_gdp_by_country.get(country, float('nan')) / 1e9
            opt_last = last_gdp_by_country.get(country, float('nan')) / 1e9

            if math.isnan(orig_first):
                self.assertTrue(math.isnan(opt_first))
            else:
                self.assertEqual(orig_first, opt_first)

            if math.isnan(orig_last):
                self.assertTrue(math.isnan(opt_last))
            else:
                self.assertEqual(orig_last, opt_last)

    def test_missing_country_fallback(self):
        """Verify fallback behavior when country is not present in dictionary."""
        first_gdp_by_country = {'USA': 1000.0}
        self.assertTrue(math.isnan(first_gdp_by_country.get('NON_EXISTENT', float('nan'))))


if __name__ == '__main__':
    unittest.main()

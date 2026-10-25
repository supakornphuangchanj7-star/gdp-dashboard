import unittest
import math
import pandas as pd
from pathlib import Path

class TestGDPExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
        raw_gdp_df = pd.read_csv(DATA_FILENAME)
        MIN_YEAR = 1960
        MAX_YEAR = 2022
        cls.gdp_df = raw_gdp_df.melt(
            ['Country Code'],
            [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
            'Year',
            'GDP',
        )
        cls.gdp_df['Year'] = pd.to_numeric(cls.gdp_df['Year'])

    def test_original_vs_optimized_lookup(self):
        selected_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
        from_year = 1960
        to_year = 2022

        filtered_gdp_df = self.gdp_df[
            (self.gdp_df['Country Code'].isin(selected_countries))
            & (self.gdp_df['Year'] <= to_year)
            & (from_year <= self.gdp_df['Year'])
        ]

        # Original logic
        first_year_orig = self.gdp_df[self.gdp_df['Year'] == from_year]
        last_year_orig = self.gdp_df[self.gdp_df['Year'] == to_year]

        orig_res = {}
        for country in selected_countries:
            f_gdp = first_year_orig[first_year_orig['Country Code'] == country]['GDP'].iat[0] / 1e9
            l_gdp = last_year_orig[last_year_orig['Country Code'] == country]['GDP'].iat[0] / 1e9
            orig_res[country] = (f_gdp, l_gdp)

        # Optimized logic
        first_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == from_year]
        last_year_df = filtered_gdp_df[filtered_gdp_df['Year'] == to_year]
        first_year_gdp = dict(zip(first_year_df['Country Code'], first_year_df['GDP']))
        last_year_gdp = dict(zip(last_year_df['Country Code'], last_year_df['GDP']))

        opt_res = {}
        for country in selected_countries:
            f_gdp = first_year_gdp.get(country, math.nan) / 1e9
            l_gdp = last_year_gdp.get(country, math.nan) / 1e9
            opt_res[country] = (f_gdp, l_gdp)

        for country in selected_countries:
            f1, l1 = orig_res[country]
            f2, l2 = opt_res[country]

            if math.isnan(f1):
                self.assertTrue(math.isnan(f2))
            else:
                self.assertAlmostEqual(f1, f2)

            if math.isnan(l1):
                self.assertTrue(math.isnan(l2))
            else:
                self.assertAlmostEqual(l1, l2)

if __name__ == '__main__':
    unittest.main()

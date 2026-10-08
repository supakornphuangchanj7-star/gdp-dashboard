import unittest
import math
import time
from pathlib import Path
import pandas as pd


class TestGDPLookup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
        raw_gdp_df = pd.read_csv(DATA_FILENAME)
        MIN_YEAR = 1960
        MAX_YEAR = 2022

        gdp_df = raw_gdp_df.melt(
            ['Country Code'],
            [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
            'Year',
            'GDP',
        )
        gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
        cls.gdp_df = gdp_df

    def test_lookup_equivalence(self):
        countries = self.gdp_df['Country Code'].unique()
        for from_year in [1960, 1990, 2010]:
            for to_year in [2000, 2020, 2022]:
                first_year = self.gdp_df[self.gdp_df['Year'] == from_year]
                last_year = self.gdp_df[self.gdp_df['Year'] == to_year]

                first_gdp_map = dict(zip(first_year['Country Code'], first_year['GDP']))
                last_gdp_map = dict(zip(last_year['Country Code'], last_year['GDP']))

                for country in countries:
                    # Original logic
                    orig_first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
                    orig_last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

                    # Optimized logic
                    opt_first_gdp = first_gdp_map.get(country, math.nan) / 1000000000
                    opt_last_gdp = last_gdp_map.get(country, math.nan) / 1000000000

                    if math.isnan(orig_first_gdp):
                        self.assertTrue(math.isnan(opt_first_gdp))
                    else:
                        self.assertEqual(orig_first_gdp, opt_first_gdp)

                    if math.isnan(orig_last_gdp):
                        self.assertTrue(math.isnan(opt_last_gdp))
                    else:
                        self.assertEqual(orig_last_gdp, opt_last_gdp)

    def test_performance_improvement(self):
        selected_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN', 'USA', 'CHN', 'IND', 'CAN']
        from_year = 1990
        to_year = 2020

        # Benchmark original logic
        t0 = time.perf_counter()
        for _ in range(200):
            first_year = self.gdp_df[self.gdp_df['Year'] == from_year]
            last_year = self.gdp_df[self.gdp_df['Year'] == to_year]
            for country in selected_countries:
                first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
                last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
        orig_time = time.perf_counter() - t0

        # Benchmark optimized logic
        t0 = time.perf_counter()
        for _ in range(200):
            first_year = self.gdp_df[self.gdp_df['Year'] == from_year]
            last_year = self.gdp_df[self.gdp_df['Year'] == to_year]
            first_gdp_map = dict(zip(first_year['Country Code'], first_year['GDP']))
            last_gdp_map = dict(zip(last_year['Country Code'], last_year['GDP']))
            for country in selected_countries:
                first_gdp = first_gdp_map.get(country, math.nan) / 1000000000
                last_gdp = last_gdp_map.get(country, math.nan) / 1000000000
        opt_time = time.perf_counter() - t0

        speedup = orig_time / opt_time
        print(f"\nOriginal time: {orig_time*1000:.2f}ms, Optimized time: {opt_time*1000:.2f}ms (Speedup: {speedup:.2f}x)")
        self.assertGreater(speedup, 2.0, "Expected at least 2x speedup for dictionary lookup vs repeated dataframe filtering")


if __name__ == '__main__':
    unittest.main()

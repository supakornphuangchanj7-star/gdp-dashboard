import unittest
import math
import pandas as pd
from pathlib import Path


class TestGDPMetrics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_path = Path(__file__).parent / 'data/gdp_data.csv'
        raw_gdp_df = pd.read_csv(data_path)
        cls.gdp_df = raw_gdp_df.melt(
            ['Country Code'],
            [str(x) for x in range(1960, 2023)],
            'Year',
            'GDP',
        )
        cls.gdp_df['Year'] = pd.to_numeric(cls.gdp_df['Year'])

    def test_optimized_lookup_matches_original_baseline(self):
        test_cases = [
            (['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'], 1960, 2022),
            (['USA', 'CHN', 'IND', 'DEU'], 1970, 2020),
            (['ABW', 'AFE', 'AFG'], 1990, 2015),
            (list(self.gdp_df['Country Code'].unique()[:30]), 1980, 2010),
            (list(self.gdp_df['Country Code'].unique()), 1960, 2022),
        ]

        for selected_countries, from_year, to_year in test_cases:
            filtered_gdp_df = self.gdp_df[
                (self.gdp_df['Country Code'].isin(selected_countries))
                & (self.gdp_df['Year'] <= to_year)
                & (from_year <= self.gdp_df['Year'])
            ]

            # Original baseline logic
            first_year_orig = self.gdp_df[self.gdp_df['Year'] == from_year]
            last_year_orig = self.gdp_df[self.gdp_df['Year'] == to_year]

            # Optimized logic
            first_year_gdp = (
                filtered_gdp_df[filtered_gdp_df['Year'] == from_year]
                .set_index('Country Code')['GDP']
            )
            last_year_gdp = (
                filtered_gdp_df[filtered_gdp_df['Year'] == to_year]
                .set_index('Country Code')['GDP']
            )

            for country in selected_countries:
                first_gdp_orig = first_year_orig[first_year_orig['Country Code'] == country]['GDP'].iat[0] / 1e9
                last_gdp_orig = last_year_orig[last_year_orig['Country Code'] == country]['GDP'].iat[0] / 1e9

                first_gdp_opt = first_year_gdp.get(country, float('nan')) / 1e9
                last_gdp_opt = last_year_gdp.get(country, float('nan')) / 1e9

                if math.isnan(first_gdp_orig):
                    self.assertTrue(math.isnan(first_gdp_opt))
                else:
                    self.assertEqual(first_gdp_orig, first_gdp_opt)

                if math.isnan(last_gdp_orig):
                    self.assertTrue(math.isnan(last_gdp_opt))
                else:
                    self.assertEqual(last_gdp_orig, last_gdp_opt)

    def test_missing_country_fallback(self):
        filtered_gdp_df = self.gdp_df[
            (self.gdp_df['Country Code'].isin(['DEU']))
            & (self.gdp_df['Year'] <= 2022)
            & (1960 <= self.gdp_df['Year'])
        ]
        first_year_gdp = (
            filtered_gdp_df[filtered_gdp_df['Year'] == 1960]
            .set_index('Country Code')['GDP']
        )
        self.assertTrue(math.isnan(first_year_gdp.get('NONEXISTENT_COUNTRY', float('nan'))))


if __name__ == '__main__':
    unittest.main()

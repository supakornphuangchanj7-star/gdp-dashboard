import unittest
import math
import pandas as pd
from pathlib import Path


def load_gdp_data():
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
    return gdp_df


def compute_metrics(gdp_df, selected_countries, from_year, to_year):
    filtered_gdp_df = gdp_df[
        (gdp_df['Country Code'].isin(selected_countries))
        & (gdp_df['Year'] <= to_year)
        & (from_year <= gdp_df['Year'])
    ]
    first_year_gdp_dict = filtered_gdp_df[filtered_gdp_df['Year'] == from_year].set_index('Country Code')['GDP'].to_dict()
    last_year_gdp_dict = filtered_gdp_df[filtered_gdp_df['Year'] == to_year].set_index('Country Code')['GDP'].to_dict()

    metrics = {}
    for country in selected_countries:
        first_gdp_val = first_year_gdp_dict.get(country, math.nan)
        last_gdp_val = last_year_gdp_dict.get(country, math.nan)

        first_gdp = first_gdp_val / 1000000000
        last_gdp = last_gdp_val / 1000000000

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        metrics[country] = {
            'first_gdp': first_gdp,
            'last_gdp': last_gdp,
            'growth': growth,
            'delta_color': delta_color,
        }
    return metrics


class TestGDPDashboard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gdp_df = load_gdp_data()

    def test_data_loading(self):
        self.assertIn('Country Code', self.gdp_df.columns)
        self.assertIn('Year', self.gdp_df.columns)
        self.assertIn('GDP', self.gdp_df.columns)
        self.assertEqual(self.gdp_df['Year'].min(), 1960)
        self.assertEqual(self.gdp_df['Year'].max(), 2022)

    def test_compute_metrics_valid(self):
        selected = ['DEU', 'FRA', 'USA']
        metrics = compute_metrics(self.gdp_df, selected, 1990, 2022)
        for country in selected:
            self.assertIn(country, metrics)
            self.assertFalse(math.isnan(metrics[country]['last_gdp']))
            self.assertEqual(metrics[country]['delta_color'], 'normal')

    def test_compute_metrics_missing_start_year(self):
        # AFG (Afghanistan) has missing GDP in 1990
        selected = ['AFG']
        metrics = compute_metrics(self.gdp_df, selected, 1990, 2022)
        self.assertEqual(metrics['AFG']['growth'], 'n/a')
        self.assertEqual(metrics['AFG']['delta_color'], 'off')


if __name__ == '__main__':
    unittest.main()

import unittest
import math
import pandas as pd

class TestGdpMetricOptimization(unittest.TestCase):
    def test_dict_lookup_equivalent_to_dataframe_filtering(self):
        # Sample data mimicking gdp_df
        data = {
            'Country Code': ['USA', 'DEU', 'FRA', 'JPN', 'XYZ'],
            'Year': [1960, 1960, 1960, 1960, 1960],
            'GDP': [5.43e11, 2.15e11, 6.22e10, 4.43e10, float('nan')]
        }
        df = pd.DataFrame(data)

        # Original method
        def orig_lookup(country):
            sub = df[df['Country Code'] == country]
            if len(sub) == 0:
                return float('nan')
            return sub['GDP'].iat[0] / 1e9

        # Optimized method
        gdp_dict = dict(zip(df['Country Code'], df['GDP']))
        def opt_lookup(country):
            val = gdp_dict.get(country, float('nan'))
            return val / 1e9

        test_countries = ['USA', 'DEU', 'FRA', 'JPN', 'XYZ', 'NONEXISTENT']
        for c in test_countries:
            orig_val = orig_lookup(c)
            opt_val = opt_lookup(c)

            if math.isnan(orig_val):
                self.assertTrue(math.isnan(opt_val), f"Expected NaN for {c}")
            else:
                self.assertEqual(orig_val, opt_val, f"Mismatch for {c}")

if __name__ == '__main__':
    unittest.main()

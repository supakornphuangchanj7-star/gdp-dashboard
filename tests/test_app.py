import unittest
from pathlib import Path
import pandas as pd
from streamlit.testing.v1 import AppTest
import streamlit_app


class TestGDPDashboard(unittest.TestCase):
    def test_get_gdp_data(self):
        """Test that get_gdp_data returns expected dataframe structure."""
        df = streamlit_app.get_gdp_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("Country Code", df.columns)
        self.assertIn("Year", df.columns)
        self.assertIn("GDP", df.columns)
        self.assertGreater(len(df), 0)
        self.assertEqual(df["Year"].min(), 1960)
        self.assertEqual(df["Year"].max(), 2022)

    def test_app_rendering_metrics(self):
        """Test that the Streamlit app runs and produces metrics correctly."""
        script_path = str(Path(__file__).parent.parent / "streamlit_app.py")
        at = AppTest.from_file(script_path).run()
        self.assertFalse(at.exception)

        # Default selection has 6 countries
        default_countries = ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
        metric_labels = [m.label for m in at.metric]
        for country in default_countries:
            self.assertIn(f"{country} GDP", metric_labels)

        # Verify values for a known country (e.g. FRA, MEX, JPN)
        fra_metric = next(m for m in at.metric if m.label == "FRA GDP")
        self.assertEqual(fra_metric.value, "2,779B")
        self.assertEqual(fra_metric.delta, "44.66x")


if __name__ == "__main__":
    unittest.main()

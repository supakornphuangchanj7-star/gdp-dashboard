import unittest
from streamlit.testing.v1 import AppTest


class TestGDPDashboard(unittest.TestCase):
    def test_default_load(self):
        """Test default load of the app and check metrics rendered."""
        at = AppTest.from_file("streamlit_app.py").run()
        self.assertFalse(at.exception)

        # Default countries: ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']
        metric_labels = [m.label for m in at.metric]
        self.assertEqual(len(metric_labels), 6)
        self.assertIn("DEU GDP", metric_labels)
        self.assertIn("FRA GDP", metric_labels)
        self.assertIn("GBR GDP", metric_labels)
        self.assertIn("BRA GDP", metric_labels)
        self.assertIn("MEX GDP", metric_labels)
        self.assertIn("JPN GDP", metric_labels)

        # Check a specific metric value
        deu_metric = next(m for m in at.metric if m.label == "DEU GDP")
        self.assertEqual(deu_metric.value, "4,082B")
        self.assertEqual(deu_metric.delta, "n/a")

    def test_filter_countries_and_years(self):
        """Test changing years and countries via AppTest widgets."""
        at = AppTest.from_file("streamlit_app.py").run()
        self.assertFalse(at.exception)

        # Update year range slider to (1990, 2020)
        at.slider[0].set_value((1990, 2020)).run()
        self.assertFalse(at.exception)

        # Update selected countries multiselect to ['USA', 'CAN']
        at.multiselect[0].set_value(["USA", "CAN"]).run()
        self.assertFalse(at.exception)

        metric_labels = [m.label for m in at.metric]
        self.assertEqual(metric_labels, ["USA GDP", "CAN GDP"])

        usa_metric = next(m for m in at.metric if m.label == "USA GDP")
        self.assertIn("B", usa_metric.value)
        self.assertNotEqual(usa_metric.delta, "n/a")


if __name__ == "__main__":
    unittest.main()

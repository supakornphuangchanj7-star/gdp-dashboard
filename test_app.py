import unittest

from streamlit.testing.v1 import AppTest


class TestGDPDashboardApp(unittest.TestCase):
    def test_app_smoke_and_defaults(self):
        """Verify the app loads successfully with default parameters."""
        at = AppTest.from_file("streamlit_app.py")
        at.run()
        self.assertFalse(at.exception)

        # Check default slider values (returns tuple)
        self.assertEqual(len(at.slider), 1)
        self.assertEqual(tuple(at.slider[0].value), (1960, 2022))

        # Check default multiselect values
        self.assertEqual(len(at.multiselect), 1)
        self.assertEqual(
            at.multiselect[0].value,
            ["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"],
        )

        # Check metrics rendered for each selected country
        self.assertEqual(len(at.metric), 6)
        labels = [m.label for m in at.metric]
        self.assertIn("DEU GDP", labels)
        self.assertIn("FRA GDP", labels)
        self.assertIn("GBR GDP", labels)
        self.assertIn("BRA GDP", labels)
        self.assertIn("MEX GDP", labels)
        self.assertIn("JPN GDP", labels)

    def test_slider_filtering(self):
        """Verify changing slider year range updates metrics correctly."""
        at = AppTest.from_file("streamlit_app.py")
        at.run()

        # Update year range
        at.slider[0].set_value([1980, 2010]).run()
        self.assertFalse(at.exception)
        self.assertEqual(tuple(at.slider[0].value), (1980, 2010))
        self.assertEqual(len(at.metric), 6)

    def test_country_selection(self):
        """Verify selecting a custom subset of countries works properly."""
        at = AppTest.from_file("streamlit_app.py")
        at.run()

        # Select only FRA and JPN
        at.multiselect[0].set_value(["FRA", "JPN"]).run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.metric), 2)
        labels = [m.label for m in at.metric]
        self.assertEqual(labels, ["FRA GDP", "JPN GDP"])


if __name__ == "__main__":
    unittest.main()

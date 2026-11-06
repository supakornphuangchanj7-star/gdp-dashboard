import unittest
from streamlit.testing.v1 import AppTest


class TestGDPDashboard(unittest.TestCase):
    def test_default_rendering(self):
        """Verify the dashboard renders with default settings without exceptions."""
        at = AppTest.from_file("streamlit_app.py")
        at.run()
        self.assertFalse(at.exception)
        # Check metrics generated for default 6 countries
        self.assertEqual(len(at.metric), 6)
        labels = [m.label for m in at.metric]
        for country in ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']:
            self.assertIn(f'{country} GDP', labels)

    def test_custom_selection(self):
        """Verify custom country selection and year range."""
        at = AppTest.from_file("streamlit_app.py")
        at.run()
        # Change slider and multiselect
        at.slider[0].set_value((2000, 2020)).run()
        at.multiselect[0].select("USA").run()
        self.assertFalse(at.exception)
        self.assertIn("USA GDP", [m.label for m in at.metric])

    def test_empty_country_selection(self):
        """Verify empty country selection displays warning without crashing."""
        at = AppTest.from_file("streamlit_app.py")
        at.run()
        at.multiselect[0].unselect("DEU").unselect("FRA").unselect("GBR").unselect("BRA").unselect("MEX").unselect("JPN").run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.metric), 0)


if __name__ == "__main__":
    unittest.main()

import unittest
from streamlit.testing.v1 import AppTest


class TestGDPApp(unittest.TestCase):
    def test_default_run(self):
        at = AppTest.from_file("streamlit_app.py")
        at.run()
        self.assertFalse(at.exception)
        # Check default metrics rendered
        self.assertEqual(len(at.metric), 6)
        labels = [m.label for m in at.metric]
        expected_countries = ["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"]
        for country in expected_countries:
            self.assertIn(f"{country} GDP", labels)

    def test_country_selection(self):
        at = AppTest.from_file("streamlit_app.py")
        at.run()
        # Change multiselect
        at.multiselect[0].select("USA").run()
        labels = [m.label for m in at.metric]
        self.assertIn("USA GDP", labels)
        self.assertFalse(at.exception)


if __name__ == "__main__":
    unittest.main()

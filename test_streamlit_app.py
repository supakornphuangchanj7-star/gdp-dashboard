import unittest
from streamlit.testing.v1 import AppTest


class TestStreamlitApp(unittest.TestCase):
    def test_default_run(self):
        at = AppTest.from_file("streamlit_app.py").run()
        self.assertFalse(at.exception)

        # 6 default selected countries: DEU, FRA, GBR, BRA, MEX, JPN
        self.assertEqual(len(at.metric), 6)

        metrics_by_label = {m.label: m for m in at.metric}
        self.assertIn("DEU GDP", metrics_by_label)
        self.assertIn("FRA GDP", metrics_by_label)
        self.assertIn("GBR GDP", metrics_by_label)
        self.assertIn("BRA GDP", metrics_by_label)
        self.assertIn("MEX GDP", metrics_by_label)
        self.assertIn("JPN GDP", metrics_by_label)

        # Check values and deltas for known countries
        self.assertEqual(metrics_by_label["DEU GDP"].value, "4,082B")
        self.assertEqual(metrics_by_label["DEU GDP"].delta, "n/a")

        self.assertEqual(metrics_by_label["FRA GDP"].value, "2,779B")
        self.assertEqual(metrics_by_label["FRA GDP"].delta, "44.66x")

        self.assertEqual(metrics_by_label["GBR GDP"].value, "3,089B")
        self.assertEqual(metrics_by_label["GBR GDP"].delta, "42.18x")

        self.assertEqual(metrics_by_label["USA GDP" if "USA GDP" in metrics_by_label else "JPN GDP"].value, "4,232B")

    def test_custom_selection(self):
        at = AppTest.from_file("streamlit_app.py").run()
        self.assertFalse(at.exception)

        # Change selection to USA and CAN, and years to [2000, 2020]
        at.slider[0].set_value([2000, 2020]).run()
        at.multiselect[0].set_value(["USA", "CAN"]).run()
        self.assertFalse(at.exception)

        self.assertEqual(len(at.metric), 2)
        metrics_by_label = {m.label: m for m in at.metric}
        self.assertIn("USA GDP", metrics_by_label)
        self.assertIn("CAN GDP", metrics_by_label)


if __name__ == "__main__":
    unittest.main()

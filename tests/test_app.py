import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).parent.parent / "streamlit_app.py")


class TestGDPDashboard(unittest.TestCase):
    def test_default_load(self):
        at = AppTest.from_file(APP_PATH).run()
        self.assertFalse(at.exception)
        # Should render 6 default selected countries
        self.assertEqual(len(at.metric), 6)
        labels = set(m.label for m in at.metric)
        expected_labels = {
            "DEU GDP",
            "FRA GDP",
            "GBR GDP",
            "BRA GDP",
            "MEX GDP",
            "JPN GDP",
        }
        self.assertEqual(labels, expected_labels)

        # Verify values and deltas for specific countries
        metric_by_country = {m.label: m for m in at.metric}
        deu_metric = metric_by_country["DEU GDP"]
        self.assertEqual(deu_metric.value, "4,082B")
        self.assertEqual(deu_metric.delta, "n/a")

        mex_metric = metric_by_country["MEX GDP"]
        self.assertEqual(mex_metric.value, "1,466B")
        self.assertEqual(mex_metric.delta, "112.41x")

    def test_slider_and_multiselect_interactions(self):
        at = AppTest.from_file(APP_PATH).run()
        # Change slider year range
        at.slider[0].set_value((1990, 2020)).run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.metric), 6)

        # Change selected countries
        at.multiselect[0].set_value(["USA", "CAN"]).run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.metric), 2)
        labels = set(m.label for m in at.metric)
        self.assertEqual(labels, {"USA GDP", "CAN GDP"})


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).parent.parent / "streamlit_app.py")


class TestStreamlitApp(unittest.TestCase):
    def test_app_default_run(self):
        """Test default app run renders metrics correctly without exceptions."""
        at = AppTest.from_file(APP_PATH)
        at.run()

        self.assertEqual(len(at.exception), 0)
        self.assertEqual(len(at.metric), 6)

        metrics = {m.label: (m.value, m.delta) for m in at.metric}
        self.assertEqual(metrics["DEU GDP"], ("4,082B", "n/a"))
        self.assertEqual(metrics["FRA GDP"], ("2,779B", "44.66x"))
        self.assertEqual(metrics["GBR GDP"], ("3,089B", "42.18x"))
        self.assertEqual(metrics["BRA GDP"], ("1,920B", "n/a"))
        self.assertEqual(metrics["MEX GDP"], ("1,466B", "112.41x"))
        self.assertEqual(metrics["JPN GDP"], ("4,232B", "95.52x"))

    def test_app_with_custom_selection_and_slider(self):
        """Test app with custom country multiselect and slider years."""
        at = AppTest.from_file(APP_PATH)
        at.run()

        # Modify slider to 1990 - 2020
        at.slider[0].set_value((1990, 2020)).run()
        self.assertEqual(len(at.exception), 0)

        # Modify selected countries to USA, CHN
        at.multiselect[0].set_value(["USA", "CHN"]).run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(len(at.metric), 2)

        metric_labels = [m.label for m in at.metric]
        self.assertIn("USA GDP", metric_labels)
        self.assertIn("CHN GDP", metric_labels)


if __name__ == "__main__":
    unittest.main()

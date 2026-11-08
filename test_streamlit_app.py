import unittest
from streamlit.testing.v1 import AppTest


class TestStreamlitApp(unittest.TestCase):
    def test_default_run(self):
        """Test default dashboard rendering with initial selections."""
        at = AppTest.from_file('streamlit_app.py')
        at.run()
        self.assertFalse(at.exception)

        # Default countries are DEU, FRA, GBR, BRA, MEX, JPN
        metrics = at.metric
        self.assertEqual(len(metrics), 6)

        metric_dict = {m.label: m for m in metrics}
        self.assertIn('DEU GDP', metric_dict)
        self.assertEqual(metric_dict['DEU GDP'].value, '4,082B')
        self.assertEqual(metric_dict['DEU GDP'].delta, 'n/a')

        self.assertIn('FRA GDP', metric_dict)
        self.assertEqual(metric_dict['FRA GDP'].value, '2,779B')
        self.assertEqual(metric_dict['FRA GDP'].delta, '44.66x')

        self.assertIn('MEX GDP', metric_dict)
        self.assertEqual(metric_dict['MEX GDP'].value, '1,466B')
        self.assertEqual(metric_dict['MEX GDP'].delta, '112.41x')

    def test_custom_selection(self):
        """Test selecting a single country and customized year range."""
        at = AppTest.from_file('streamlit_app.py')
        at.run()

        # Update multiselect to a single country: USA
        at.multiselect[0].set_value(['USA']).run()
        self.assertFalse(at.exception)

        metrics = at.metric
        self.assertEqual(len(metrics), 1)
        self.assertEqual(metrics[0].label, 'USA GDP')
        self.assertEqual(metrics[0].value, '25,440B')
        self.assertEqual(metrics[0].delta, '46.82x')

    def test_empty_selection(self):
        """Test app behaviour when no countries are selected."""
        at = AppTest.from_file('streamlit_app.py')
        at.run()

        # Deselect all countries
        at.multiselect[0].set_value([]).run()
        self.assertFalse(at.exception)

        # There should be 0 metrics
        self.assertEqual(len(at.metric), 0)


if __name__ == '__main__':
    unittest.main()

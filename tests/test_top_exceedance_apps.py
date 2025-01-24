import unittest
from metrics_manager import MetricsManager
from config import THRESHOLD, TOP_X_APPS

class TestTopExceedanceApps(unittest.TestCase):
    def setUp(self):
        self.metrics_manager = MetricsManager()

    def test_no_exceedance(self):
        top_apps = self.metrics_manager.get_top_exceedance_apps(TOP_X_APPS)
        self.assertEqual(len(top_apps), 0)

    def test_tie_in_exceedance(self):
        metrics = [
            {"app1": THRESHOLD + 1, "app2": THRESHOLD + 1},
            {"app1": THRESHOLD + 1, "app2": THRESHOLD + 1},
        ]
        for metric in metrics:
            self.metrics_manager.process_metrics(metric, THRESHOLD)
        top_apps = self.metrics_manager.get_top_exceedance_apps(TOP_X_APPS)
        self.assertEqual(top_apps, [("app1", 2), ("app2", 2)])

    def test_get_top_exceedance_apps_single_app(self):
        """Test get_top_exceedance_apps with a single app."""
        self.metrics_manager.exceedance_count = {"app1": 5}
        top_apps = self.metrics_manager.get_top_exceedance_apps(TOP_X_APPS)
        self.assertEqual(top_apps, [("app1", 5)])

if __name__ == "__main__":
    unittest.main()
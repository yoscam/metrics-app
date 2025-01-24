import unittest
from metrics_manager import MetricsManager
from config import TOP_X_APPS

class TestMetricsManager(unittest.TestCase):
    def setUp(self):
        self.metrics_manager = MetricsManager()

    def test_get_top_exceedance_apps(self):
        """Test the get_top_exceedance_apps method."""
        # Simulate exceedance counts
        self.metrics_manager.exceedance_count = {"app1": 5, "app2": 3, "app3": 1}

        # Set TOP_X_APPS explicitly for the test
        top_x_apps = 2

        # Get the top apps
        top_apps = self.metrics_manager.get_top_exceedance_apps(top_x_apps)

        # Verify the result
        self.assertEqual(top_apps, [("app1", 5), ("app2", 3)])

    def test_get_top_exceedance_apps_empty(self):
        """Test the get_top_exceedance_apps method with no exceedances."""
        # Simulate no exceedances
        self.metrics_manager.exceedance_count = {}

        # Set TOP_X_APPS explicitly for the test
        top_x_apps = 2

        # Get the top apps
        top_apps = self.metrics_manager.get_top_exceedance_apps(top_x_apps)

        # Verify the result
        self.assertEqual(top_apps, [])

    def test_get_top_exceedance_apps_less_than_top_x(self):
        """Test get_top_exceedance_apps when fewer apps exceed the threshold than TOP_X_APPS."""
        self.metrics_manager.exceedance_count = {"app1": 5}
        top_apps = self.metrics_manager.get_top_exceedance_apps(TOP_X_APPS)
        self.assertEqual(top_apps, [("app1", 5)])

if __name__ == "__main__":
    unittest.main()
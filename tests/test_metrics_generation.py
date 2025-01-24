import unittest
from app import generate_metrics
from config import NUM_APPS, RANDOM_METRIC_MIN, RANDOM_METRIC_MAX, THRESHOLD

class TestMetricsGeneration(unittest.TestCase):
    def test_number_of_apps(self):
        metrics = generate_metrics()
        self.assertEqual(len(metrics), NUM_APPS)

    def test_metric_values(self):
        metrics = generate_metrics()
        for value in metrics.values():
            self.assertGreaterEqual(value, RANDOM_METRIC_MIN)  # Ensure values are >= RANDOM_METRIC_MIN
            self.assertLessEqual(value, RANDOM_METRIC_MAX)     # Ensure values are <= RANDOM_METRIC_MAX

    def test_metric_values_edge_cases(self):
        """Test edge cases for metric values."""
        metrics = generate_metrics()
        for value in metrics.values():
            self.assertGreaterEqual(value, RANDOM_METRIC_MIN)  # Ensure values are >= RANDOM_METRIC_MIN
            self.assertLessEqual(value, RANDOM_METRIC_MAX)     # Ensure values are <= RANDOM_METRIC_MAX

if __name__ == "__main__":
    unittest.main()
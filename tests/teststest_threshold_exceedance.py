import unittest
from metrics_manager import MetricsManager
from config import THRESHOLD

class TestThresholdExceedance(unittest.TestCase):
    def setUp(self):
        self.metrics_manager = MetricsManager()

    def test_metric_at_threshold(self):
        metrics = {"app1": THRESHOLD}
        self.metrics_manager.process_metrics(metrics, THRESHOLD)
        self.assertEqual(self.metrics_manager.exceedance_count["app1"], 0)

    def test_metric_just_below_threshold(self):
        metrics = {"app1": THRESHOLD - 1}
        self.metrics_manager.process_metrics(metrics, THRESHOLD)
        self.assertEqual(self.metrics_manager.exceedance_count["app1"], 0)

    def test_metric_just_above_threshold(self):
        metrics = {"app1": THRESHOLD + 1}
        self.metrics_manager.process_metrics(metrics, THRESHOLD)
        self.assertEqual(self.metrics_manager.exceedance_count["app1"], 1)

    def test_metric_exactly_at_threshold(self):
        """Test process_metrics when a metric is exactly at the threshold."""
        metrics = {"app1": THRESHOLD}
        self.metrics_manager.process_metrics(metrics, THRESHOLD)
        self.assertEqual(self.metrics_manager.exceedance_count["app1"], 0)

if __name__ == "__main__":
    unittest.main()
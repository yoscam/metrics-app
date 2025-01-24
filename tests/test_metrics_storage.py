import unittest
from metrics_manager import MetricsManager
from app import generate_metrics
from config import WRITE_METRICS_TO_FILE, RANDOM_METRIC_MIN, RANDOM_METRIC_MAX

class TestMetricsStorage(unittest.TestCase):
    def setUp(self):
        self.metrics_manager = MetricsManager()
        self.metrics = generate_metrics()

    def test_store_metrics_with_file_writing(self):
        if WRITE_METRICS_TO_FILE:
            self.metrics_manager.store_metrics(self.metrics)
            self.assertEqual(len(self.metrics_manager.metrics_history), 1)
            self.assertEqual(self.metrics_manager.metrics_history[0][1], self.metrics)

    def test_store_metrics_without_file_writing(self):
        # Temporarily disable file writing
        original_write_to_file = self.metrics_manager.write_to_file
        self.metrics_manager.write_to_file = False

        self.metrics_manager.store_metrics(self.metrics)
        self.assertEqual(len(self.metrics_manager.metrics_history), 1)
        self.assertEqual(self.metrics_manager.metrics_history[0][1], self.metrics)

        # Restore the original value
        self.metrics_manager.write_to_file = original_write_to_file

    def test_store_metrics_empty(self):
        """Test storing empty metrics."""
        self.metrics_manager.store_metrics({})
        self.assertEqual(len(self.metrics_manager.metrics_history), 1)
        self.assertEqual(self.metrics_manager.metrics_history[0][1], {})

if __name__ == "__main__":
    unittest.main()
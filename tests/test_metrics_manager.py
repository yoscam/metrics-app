import os
import json
import unittest
from metrics_manager import MetricsManager
from config import METRICS_FILE_PATH, DELETE_PREVIOUS_METRICS_FILE

class TestMetricsManagerFileWriting(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for testing
        self.temp_file_path = METRICS_FILE_PATH + ".tmp"

        # Create a MetricsManager instance with the temporary file path
        self.metrics_manager = MetricsManager(metrics_file=self.temp_file_path)

    def tearDown(self):
        # Clean up the temporary file if it exists
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)

    def test_write_json_enabled(self):
        """Test file writing when WRITE_METRICS_TO_FILE is True."""
        # Enable file writing
        self.metrics_manager.write_to_file = True

        metrics = {"app1": 1000, "app2": 2000}
        self.metrics_manager._write_json(123456789, metrics)

        # Verify the file was created and contains the correct data
        self.assertTrue(os.path.exists(self.temp_file_path))
        with open(self.temp_file_path, "r") as file:
            data = json.load(file)
            self.assertEqual(data["timestamp"], 123456789)
            self.assertEqual(data["metrics"], metrics)

    def test_write_json_disabled(self):
        """Test file writing when WRITE_METRICS_TO_FILE is False."""
        # Disable file writing
        self.metrics_manager.write_to_file = False

        metrics = {"app1": 1000, "app2": 2000}
        self.metrics_manager._write_json(123456789, metrics)

        # Verify the file was not created
        self.assertFalse(os.path.exists(self.temp_file_path))

    def test_store_metrics_with_file_writing_enabled(self):
        """Test store_metrics when WRITE_METRICS_TO_FILE is True."""
        # Enable file writing
        self.metrics_manager.write_to_file = True

        metrics = {"app1": 1000, "app2": 2000}
        self.metrics_manager.store_metrics(metrics)

        # Verify the file was created and contains the correct data
        self.assertTrue(os.path.exists(self.temp_file_path))
        with open(self.temp_file_path, "r") as file:
            data = json.load(file)
            self.assertEqual(data["timestamp"], self.metrics_manager.metrics_history[-1][0])
            self.assertEqual(data["metrics"], metrics)

    def test_store_metrics_with_file_writing_disabled(self):
        """Test store_metrics when WRITE_METRICS_TO_FILE is False."""
        # Disable file writing
        self.metrics_manager.write_to_file = False

        metrics = {"app1": 1000, "app2": 2000}
        self.metrics_manager.store_metrics(metrics)

        # Verify the file was not created
        self.assertFalse(os.path.exists(self.temp_file_path))

        # Verify the metrics are still stored in memory
        self.assertEqual(len(self.metrics_manager.metrics_history), 1)
        self.assertEqual(self.metrics_manager.metrics_history[0][1], metrics)

    def test_delete_previous_metrics_file(self):
        """Test that the previous metrics file is deleted if DELETE_PREVIOUS_METRICS_FILE is True."""
        # Create a dummy file to simulate a previous metrics file
        with open(self.temp_file_path, "w") as file:
            file.write("dummy content")

        # Verify the file exists
        self.assertTrue(os.path.exists(self.temp_file_path))

        # Reinitialize MetricsManager with DELETE_PREVIOUS_METRICS_FILE set to True
        self.metrics_manager = MetricsManager(metrics_file=self.temp_file_path)

        # Verify the file was deleted
        self.assertFalse(os.path.exists(self.temp_file_path))

if __name__ == "__main__":
    unittest.main()
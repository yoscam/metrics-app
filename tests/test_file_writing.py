import unittest
import os
import json
from metrics_manager import MetricsManager
from config import WRITE_METRICS_TO_FILE

class TestFileWriting(unittest.TestCase):
    def setUp(self):
        self.metrics_manager = MetricsManager()
        self.metrics = {"app1": 1000, "app2": 2000}

        # Define the temporary file path
        self.temp_dir = "Temp"
        self.temp_file_path = os.path.join(self.temp_dir, "metrics_log.txt")

        # Create the Temp directory if it doesn't exist
        os.makedirs(self.temp_dir, exist_ok=True)

        # Override the METRICS_FILE_PATH in the MetricsManager
        self.metrics_manager.metrics_file = self.temp_file_path

    def tearDown(self):
        # Clean up the temporary file and directory
        if os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)
        if os.path.exists(self.temp_dir) and not os.listdir(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_file_writing(self):
        if WRITE_METRICS_TO_FILE:
            # Store metrics to test writing to a new file
            self.metrics_manager.store_metrics(self.metrics)

            # Verify the file exists
            self.assertTrue(os.path.exists(self.temp_file_path))

            # Read the file and verify its content
            with open(self.temp_file_path, "r") as file:
                lines = file.readlines()
                self.assertEqual(len(lines), 1)
                data = json.loads(lines[0])
                self.assertEqual(data["metrics"], self.metrics)

    def test_file_appending(self):
        if WRITE_METRICS_TO_FILE:
            # Store metrics twice to test appending
            self.metrics_manager.store_metrics(self.metrics)
            self.metrics_manager.store_metrics(self.metrics)

            # Verify the file exists
            self.assertTrue(os.path.exists(self.temp_file_path))

            # Read the file and verify its content
            with open(self.temp_file_path, "r") as file:
                lines = file.readlines()
                self.assertEqual(len(lines), 2)
                for line in lines:
                    data = json.loads(line)
                    self.assertEqual(data["metrics"], self.metrics)

    def test_file_writing_disabled(self):
        """Test file writing when WRITE_METRICS_TO_FILE is False."""
        # Temporarily disable file writing
        original_write_to_file = self.metrics_manager.write_to_file
        self.metrics_manager.write_to_file = False

        # Store metrics
        self.metrics_manager.store_metrics(self.metrics)

        # Verify the file was not written
        self.assertFalse(os.path.exists(self.temp_file_path))

        # Restore the original value
        self.metrics_manager.write_to_file = original_write_to_file

if __name__ == "__main__":
    unittest.main()
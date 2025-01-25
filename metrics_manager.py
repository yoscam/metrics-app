import time
import os
import json
from collections import defaultdict
from config import WRITE_METRICS_TO_FILE, METRICS_FILE_PATH, DELETE_PREVIOUS_METRICS_FILE

class MetricsManager:
    def __init__(self, metrics_file=None):
        self.metrics_history = []  # List to store all metrics with timestamps
        self.exceedance_count = defaultdict(int)  # Track threshold exceedances per app
        self.write_to_file = WRITE_METRICS_TO_FILE
        self.metrics_file = metrics_file if metrics_file is not None else METRICS_FILE_PATH  # Use custom file path if provided

        # Delete the previous metrics file if the option is enabled
        if DELETE_PREVIOUS_METRICS_FILE and os.path.exists(self.metrics_file):
            os.remove(self.metrics_file)

    def store_metrics(self, metrics):
        """Store metrics with a timestamp and optionally save them to a JSON file."""
        timestamp = int(time.time())
        self.metrics_history.append((timestamp, metrics))

        # Save metrics to the JSON file if enabled
        if self.write_to_file:
            self._write_json(timestamp, metrics)

    def _write_json(self, timestamp, metrics):
        """Write metrics to the file in JSON format if write_to_file is True."""
        if not self.write_to_file:
            return  # Do not write to file if write_to_file is False

        data = {
            "timestamp": timestamp,
            "metrics": metrics
        }
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.metrics_file), exist_ok=True)
        with open(self.metrics_file, "a") as file:
            json.dump(data, file)
            file.write("\n")  # Add a newline for readability

    def process_metrics(self, metrics, threshold):
        """Process metrics to check for threshold exceedances."""
        for app_name, value in metrics.items():
            if value > threshold:
                self.exceedance_count[app_name] += 1

    def get_top_exceedance_apps(self, top_x):
        """Retrieve the top X apps with the most threshold exceedances."""
        sorted_apps = sorted(self.exceedance_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_apps[:top_x]
# Configuration file for the metrics application

# Number of app_names to generate metrics for
NUM_APPS = 10000

# Threshold value for metrics
THRESHOLD = 10000

# Interval (in seconds) for generating and storing metrics
METRICS_INTERVAL = 3

# Number of top apps to display for threshold exceedance
TOP_X_APPS = 3

# File storage configuration
WRITE_METRICS_TO_FILE = True  # Set to False to disable writing to a file
METRICS_FILE_PATH = "data/metrics_log.txt"  # Custom file path
DELETE_PREVIOUS_METRICS_FILE = True  # Set to False to keep the previous file

# Display mode for top apps exceeding the threshold
# Options: "console", "page", "both"
DISPLAY_MODE = "both"  # Change to "console" or "page" as needed

# Configuration for random metric generation
RANDOM_METRIC_MIN = 1  # Minimum value for random metrics
RANDOM_METRIC_MAX = 12000          # Maximum value for random metrics

# Metric name to use in Prometheus format
METRIC_NAME = "bigquery_written_bytes"  # Change this to your desired metric name

# Flask server configuration
FLASK_HOST = "0.0.0.0"  # Host to run the Flask app (e.g., "0.0.0.0" for all interfaces)
FLASK_PORT = 5000       # Port to run the Flask app
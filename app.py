import os
import logging
from flask import Flask, Response, render_template
import random
import time
import threading
import json
from config import *
from metrics_manager import MetricsManager
import atexit  # Import atexit to handle cleanup

# Initialize Flask app
app = Flask(__name__)

# Disable Werkzeug's request logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Optionally, disable Flask's built-in request logging
from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.log_request = lambda *args, **kwargs: None

# Configure logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)  # Convert LOG_LEVEL string to logging level

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Add console handler if LOG_TO_CONSOLE is True and LOG_TO_CONSOLE_ONLY_EXCEEDINGS is False
if LOG_TO_CONSOLE and not LOG_TO_CONSOLE_ONLY_EXCEEDINGS:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

# Add file handler if LOG_TO_FILE is True
if LOG_TO_FILE:
    # Create the logs directory if it doesn't exist
    log_dir = os.path.dirname(LOG_FILE_NAME)
    os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.FileHandler(LOG_FILE_NAME, mode='a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    # Register a cleanup function to close the file handler on application exit
    atexit.register(file_handler.close)

# Initialize MetricsManager
metrics_manager = MetricsManager()

# Delete the previous exceedings file if the option is enabled
if DELETE_PREVIOUS_EXCEEDINGS_FILE and os.path.exists(EXCEEDINGS_FILE_PATH):
    os.remove(EXCEEDINGS_FILE_PATH)

def generate_metrics():
    """Generate random metrics for each app."""
    metrics = {
        f"app{i+1}": random.randint(RANDOM_METRIC_MIN, RANDOM_METRIC_MAX)
        for i in range(NUM_APPS)
    }
    return metrics

def format_prometheus_metrics(metrics):
    """Format metrics in Prometheus format."""
    prometheus_metrics = []
    for app_name, value in metrics.items():
        prometheus_metrics.append(f'{METRIC_NAME}{{app_name="{app_name}"}} {value}')
    return "\n".join(prometheus_metrics)

def log_exceedings(top_apps):
    """Log the top apps exceeding the threshold to the exceedings_log.txt file."""
    if WRITE_EXCEEDINGS_TO_FILE and isinstance(top_apps, list):  # Ensure top_apps is a list
        timestamp = int(time.time())
        data = {
            "timestamp": timestamp,
            "top_apps": top_apps
        }
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(EXCEEDINGS_FILE_PATH), exist_ok=True)
        with open(EXCEEDINGS_FILE_PATH, "a") as file:
            json.dump(data, file)
            file.write("\n")  # Add a newline for readability
            file.flush()  # Force flush to ensure data is written

def display_top_apps(top_apps):
    """Display the top apps based on the configured DISPLAY_MODE."""
    if DISPLAY_MODE in ["console", "both"]:
        if LOG_TO_CONSOLE_ONLY_EXCEEDINGS:
            # Print directly to the console if only exceedance logs are allowed
            print(f"Top {TOP_X_APPS} apps exceeding threshold: {top_apps}")
        else:
            # Use the logger if all logs are allowed
            logger.info(f"Top {TOP_X_APPS} apps exceeding threshold: {top_apps}")

    # Log the top apps to the exceedings_log.txt file
    log_exceedings(top_apps)

def periodic_metrics_generation(max_iterations=None):
    """Periodically generate, store, and process metrics."""
    iteration = 0
    while True:
        try:
            if max_iterations is not None and iteration >= max_iterations:
                break  # Stop after max_iterations

            metrics = generate_metrics()
            metrics_manager.store_metrics(metrics)
            metrics_manager.process_metrics(metrics, THRESHOLD)
            top_apps = metrics_manager.get_top_exceedance_apps(TOP_X_APPS)
            display_top_apps(top_apps)

            # Log the iteration message to the file handler only
            logger.info(f"Iteration {iteration}: Metrics processed and logged.")

            time.sleep(METRICS_INTERVAL)
            iteration += 1
        except Exception as e:
            logger.error(f"Error in periodic_metrics_generation: {e}", exc_info=True)
            time.sleep(METRICS_INTERVAL)  # Wait before retrying

@app.route('/metrics')
def metrics():
    """Endpoint to serve the last collected metrics in Prometheus format."""
    if metrics_manager.metrics_history:
        last_metrics = metrics_manager.metrics_history[-1][1]  # Get the latest metrics
    else:
        last_metrics = generate_metrics()  # Fallback if no metrics are available

    # Format the metrics in Prometheus format
    prometheus_metrics = format_prometheus_metrics(last_metrics)
    logger.info("Serving metrics in Prometheus format")  # Log the request
    return Response(prometheus_metrics, mimetype="text/plain")

@app.route('/exceeding')
def exceeding():
    """Endpoint to display the top apps exceeding the threshold."""
    if DISPLAY_MODE not in ["page", "both"]:
        logger.warning("Display mode is not set to 'page' or 'both'")  # Log the warning
        return "Display mode is not set to 'page' or 'both'.", 404

    top_apps = metrics_manager.get_top_exceedance_apps(TOP_X_APPS)
    logger.info("Serving top apps exceeding threshold")  # Log the request
    return render_template('exceeding.html', top_apps=top_apps)

def main():
    """Main function to start the metrics generation and Flask app."""
    # Start the periodic metrics generation in a separate thread
    threading.Thread(target=periodic_metrics_generation, daemon=True).start()
    # Run the Flask app
    logger.info(f"Starting Flask app on {FLASK_HOST}:{FLASK_PORT}")  # Log the app start
    app.run(host=FLASK_HOST, port=FLASK_PORT)

if __name__ == "__main__":
    main()
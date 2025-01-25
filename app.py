import logging
from flask import Flask, Response, render_template
import random
import time
import threading
from config import (
    NUM_APPS, THRESHOLD, METRICS_INTERVAL, TOP_X_APPS, DISPLAY_MODE,
    RANDOM_METRIC_MIN, RANDOM_METRIC_MAX, METRIC_NAME, FLASK_HOST, FLASK_PORT,
    LOG_TO_CONSOLE, LOG_TO_FILE, LOG_FILE_NAME, LOG_LEVEL, LOG_HTTP_REQUESTS
)
from metrics_manager import MetricsManager

# Initialize Flask app
app = Flask(__name__)

# Configure logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)  # Convert LOG_LEVEL string to logging level

# Create a logger
logger = logging.getLogger()
logger.setLevel(log_level)

# Add console handler if LOG_TO_CONSOLE is True
if LOG_TO_CONSOLE:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

# Add file handler if LOG_TO_FILE is True
if LOG_TO_FILE:
    file_handler = logging.FileHandler(LOG_FILE_NAME)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

# Disable Flask's default HTTP request logging if LOG_HTTP_REQUESTS is False
if not LOG_HTTP_REQUESTS:
    logging.getLogger('werkzeug').setLevel(logging.ERROR)  # Suppress HTTP request logs

# Initialize MetricsManager
metrics_manager = MetricsManager()

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

def display_top_apps(top_apps):
    """Display the top apps based on the configured DISPLAY_MODE."""
    if DISPLAY_MODE in ["console", "both"]:
        print(f"Top {TOP_X_APPS} apps exceeding threshold: {top_apps}")

    if DISPLAY_MODE in ["page", "both"]:
        # The /exceeding route will handle displaying the top apps on the page
        pass

def periodic_metrics_generation(max_iterations=None):
    """Periodically generate, store, and process metrics."""
    iteration = 0
    while True:
        if max_iterations is not None and iteration >= max_iterations:
            break  # Stop after max_iterations

        metrics = generate_metrics()
        metrics_manager.store_metrics(metrics)
        metrics_manager.process_metrics(metrics, THRESHOLD)
        top_apps = metrics_manager.get_top_exceedance_apps(TOP_X_APPS)
        display_top_apps(top_apps)
        time.sleep(METRICS_INTERVAL)
        iteration += 1

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
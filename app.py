from flask import Flask, Response, render_template
import random
import time
import threading
from config import (
    NUM_APPS, THRESHOLD, METRICS_INTERVAL, TOP_X_APPS, DISPLAY_MODE,
    RANDOM_METRIC_MIN, RANDOM_METRIC_MAX, METRIC_NAME, FLASK_HOST, FLASK_PORT
)
from metrics_manager import MetricsManager

app = Flask(__name__)
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
    return Response(prometheus_metrics, mimetype="text/plain")

@app.route('/exceeding')
def exceeding():
    """Endpoint to display the top apps exceeding the threshold."""
    if DISPLAY_MODE not in ["page", "both"]:
        return "Display mode is not set to 'page' or 'both'.", 404

    top_apps = metrics_manager.get_top_exceedance_apps(TOP_X_APPS)
    return render_template('exceeding.html', top_apps=top_apps)

def main():
    """Main function to start the metrics generation and Flask app."""
    # Start the periodic metrics generation in a separate thread
    threading.Thread(target=periodic_metrics_generation, daemon=True).start()
    # Run the Flask app
    app.run(host=FLASK_HOST, port=FLASK_PORT)

if __name__ == "__main__":
    main()
<h1>Metrics Monitoring Application</h1>
This Python-based web application generates and monitors metrics for multiple applications, exposing them in <strong>Prometheus</strong> format. It includes a Flask web server with a <code>/metrics</code> endpoint, which serves randomly generated metrics for a configurable number of applications. The application also processes these metrics to track threshold exceedances and displays the top applications that exceed the threshold the most.

<h2>Key Features:</h2>
<strong>Prometheus Metrics:</strong> Generates random metrics (between 1 and 12,000) for a configurable number of applications and serves them in Prometheus format.

<strong>Threshold Monitoring:</strong> Tracks how many times each application exceeds a defined threshold value.

<strong>Top Exceedance Display:</strong> Periodically displays the top X applications that have exceeded the threshold the most.

<strong>Configurable Parameters:</strong> All settings (e.g., number of apps, threshold, interval) are configurable via a config.py file.

<strong>Web Interface:</strong> Includes a /metrics endpoint for Prometheus and an /exceeding endpoint to display top exceedances in a web page.

<h2>Technologies Used:</h2>
<strong>Flask</strong>: For the web server and endpoints.

<strong>Prometheus Format:</strong> For serving metrics.

<strong>Python:</strong> For backend logic and data processing.

<h2>How to Run:</h2>
Clone the repository.

Install dependencies: pip install -r requirements.txt.

Run the application: python app.py.

Access the /metrics endpoint at http://localhost:5000/metrics and the /exceeding endpoint at http://localhost:5000/exceeding.

Configuration:
Modify the config.py file to adjust:

Number of applications (NUM_APPS).

Threshold value (THRESHOLD).

Metrics generation interval (METRICS_INTERVAL).

Display mode (DISPLAY_MODE).

Use Cases:
Monitoring application performance metrics.

Simulating and testing Prometheus-based monitoring systems.

Demonstrating threshold-based alerting and reporting.

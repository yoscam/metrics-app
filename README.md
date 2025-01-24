<h1>Metrics Monitoring Application</h1>
This Python-based web application generates and monitors metrics for multiple applications, exposing them in <h2>Prometheus</h2> format. It includes a Flask web server with a <code>/metrics</code> endpoint, which serves randomly generated metrics for a configurable number of applications. The application also processes these metrics to track threshold exceedances and displays the top applications that exceed the threshold the most.

<h2>Key Features:</h2>
Prometheus Metrics: Generates random metrics (between 1 and 12,000) for a configurable number of applications and serves them in Prometheus format.

Threshold Monitoring: Tracks how many times each application exceeds a defined threshold value.

Top Exceedance Display: Periodically displays the top X applications that have exceeded the threshold the most.

Configurable Parameters: All settings (e.g., number of apps, threshold, interval) are configurable via a config.py file.

Web Interface: Includes a /metrics endpoint for Prometheus and an /exceeding endpoint to display top exceedances in a web page.

Technologies Used:
Flask: For the web server and endpoints.

Prometheus Format: For serving metrics.

Python: For backend logic and data processing.

How to Run:
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

<h1>Metrics Monitoring Application</h1>
This Python-based web application generates and monitors metrics for multiple applications, exposing them in <strong>Prometheus</strong> format. It includes a Flask web server with a <code>/metrics</code> endpoint, which serves randomly generated metrics for a configurable number of applications. The application also processes these metrics to track threshold exceedances and displays the top applications that exceed the threshold the most.

<h2>Key Features:</h2>
<strong>Prometheus Metrics:</strong> Generates random metrics (between 1 and 12,000) for a configurable number of applications and serves them in Prometheus format.<br/>
<strong>Threshold Monitoring:</strong> Tracks how many times each application exceeds a defined threshold value.<br/>
<strong>Top Exceedance Display:</strong> Periodically displays the top X applications that have exceeded the threshold the most.<br/>
<strong>Configurable Parameters:</strong> All settings (e.g., number of apps, threshold, interval) are configurable via a config.py file.<br/>
<strong>Web Interface:</strong> Includes a <code>/metrics</code> endpoint for Prometheus and an <code>/exceeding</code> endpoint to display top exceedances in a web page.<br/>

<h2>Technologies Used:</h2>
<strong>Flask</strong>: For the web server and endpoints.<br/>
<strong>Prometheus Format:</strong> For serving metrics.<br/>  
<strong>Python:</strong> For backend logic and data processing.<br/>

<h2>How to Run:</h2>
Clone the repository.<br/>
Install dependencies: <code>pip install -r requirements.txt</code>.<br/>  
Run the application: <code>python app.py</code>.<br/>
Access the <code>/metrics</code> endpoint at <code>http://localhost:5000/metrics</code> and the <code>/exceeding</code> endpoint at <code>http://localhost:5000/exceeding</code>.<br/>

<h2>Running with Docker:</h2>
<strong>To pull and run the Docker image, follow these steps</strong>:<br/>
<code>docker pull yoscam2/metrics-app:latest<br/>
docker run -p 5000:5000 yoscam2/metrics-app</code><br/>

<h2>Configuration:</h2>
<h3>Application Settings</h3>
<code>NUM_APPS</code>: Number of app names to generate metrics for.<br/>
<code>THRESHOLD</code>: Threshold value for metrics. Apps exceeding this value will be tracked.<br/>
<code>METRICS_INTERVAL</code>: Interval (in seconds) for generating and storing metrics.<br/>
<code>TOP_X_APPS</code>: Number of top apps to display for threshold exceedance.<br/>
<code>DISPLAY_MODE</code>: Display mode for top apps exceeding the threshold. Options: "console", "page", or "both".<br/>
<code>METRIC_NAME</code>: Name of the metric to use in Prometheus format.<br/>
<h3>File Storage Settings</h3>
<code>WRITE_METRICS_TO_FILE</code>: Set to True to enable writing metrics to a file, or False to disable.<br/>
<code>METRICS_FILE_PATH</code>: Path to the file where metrics will be stored.<br/>
<code>DELETE_PREVIOUS_METRICS_FILE</code>: Set to True to delete the previous metrics file before starting, or False to keep it.<br/>
<code>WRITE_EXCEEDINGS_TO_FILE</code>: Set to True to enable writing top exceedances to a file, or False to disable.<br/>
<code>EXCEEDINGS_FILE_PATH</code>: Path to the file where top exceedances will be stored (default: data/exceedings_log.txt).<br/>
<code>DELETE_PREVIOUS_EXCEEDINGS_FILE</code>: Set to True to delete the previous exceedances file before starting, or False to keep it.<br/>
<h3>Flask Server Settings</h3>
<code>FLASK_HOST</code>: Host to run the Flask app. Use "0.0.0.0" to allow access from all interfaces or "127.0.0.1" for local access only.<br/>
<code>FLASK_PORT</code>: Port to run the Flask app.<br/>
<h3>Logging Configuration</h3>
<code>LOG_TO_CONSOLE</code>: Set to True to print logs to the console.<br/>
<code>LOG_TO_FILE</code>: Set to True to write logs to a file.<br/>
<code>LOG_FILE_NAME</code>: Name of the log file (default: app.log).<br/>
<code>LOG_LEVEL</code>: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).<br/>
<code>LOG_HTTP_REQUESTS</code>: Set to False to disable HTTP request logs on the console.<br/>

<h2>Use Cases:</h2>
Monitoring application performance metrics.<br/>
Simulating and testing Prometheus-based monitoring systems.<br/>
Demonstrating threshold-based alerting and reporting.<br/>

<h2>Repository Structure:</h2>
<code>metrics-app/<br/>
├── app.py                # Flask application and endpoints<br/>
├── config.py             # Configuration file<br/>
├── metrics_manager.py    # Metrics storage and processing logic<br/>
├── requirements.txt      # Dependencies<br/>
├── README.md             # Project documentation<br/>
├── tests/                # Unit tests<br/>
│   ├── test_app.py<br/>
│   ├── test_metrics_generation.py<br/>
│   ├── test_metrics_manager.py<br/>
│   └── ...<br/>
├── templates/            # HTML templates<br/>
│   └── exceeding.html<br/>
├── data/                 # Data and log files<br/>
│   ├── metrics_log.txt   # Metrics log file<br/>
└── └── exceedings_log.txt</code> # Exceedings log file<br/>

<h2>Example Metrics Output:</h2><code>
bigquery_written_bytes{app_name="app1"} 8581<br/>
bigquery_written_bytes{app_name="app2"} 3000<br/>
bigquery_written_bytes{app_name="app3"} 4000<br/>
bigquery_written_bytes{app_name="app4"} 5000<br/>
bigquery_written_bytes{app_name="app5"} 12000<br/>
bigquery_written_bytes{app_name="app6"} 566</code><br/>

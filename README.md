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

<h2>Configuration:</h2>
Modify the <code>config.py</code> file to adjust:<br/>
Number of applications (<code>NUM_APPS</code>).<br/>
Threshold value (<code>THRESHOLD</code>).<br/>
Metrics generation interval (<code>METRICS_INTERVAL</code>).<br/>
Display mode (<code>DISPLAY_MODE</code>).<br/>

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
├── templates/            # HTML templates (if applicable)<br/>
│   └── exceeding.html</code><br/>

<h2>Example Metrics Output:</h2><code>
bigquery_written_bytes{app_name="app1"} 8581<br/>
bigquery_written_bytes{app_name="app2"} 3000<br/>
bigquery_written_bytes{app_name="app3"} 4000<br/>
bigquery_written_bytes{app_name="app4"} 5000<br/>
bigquery_written_bytes{app_name="app5"} 12000<br/>
bigquery_written_bytes{app_name="app6"} 566</code><br/>

<h2>Running with Docker:</h2>
<strong>To pull and run the Docker image, follow these steps</strong>:<br/>
<code>docker pull yoscam2/metrics-app:latest<br/>
docker run -p 5000:5000 yoscam2/metrics-app</code><br/>

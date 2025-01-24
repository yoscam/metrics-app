<h1>Metrics Monitoring Application</h1>
This Python-based web application generates and monitors metrics for multiple applications, exposing them in <strong>Prometheus</strong> format. It includes a Flask web server with a <code>/metrics</code> endpoint, which serves randomly generated metrics for a configurable number of applications. The application also processes these metrics to track threshold exceedances and displays the top applications that exceed the threshold the most.

<h2>Key Features:</h2>
<strong>Prometheus Metrics:</strong> Generates random metrics (between 1 and 12,000) for a configurable number of applications and serves them in Prometheus format.<br/>
<strong>Threshold Monitoring:</strong> Tracks how many times each application exceeds a defined threshold value.<br/>
<strong>Top Exceedance Display:</strong> Periodically displays the top X applications that have exceeded the threshold the most.  
<strong>Configurable Parameters:</strong> All settings (e.g., number of apps, threshold, interval) are configurable via a config.py file.  
<strong>Web Interface:</strong> Includes a <code>/metrics</code> endpoint for Prometheus and an <code>/exceeding</code> endpoint to display top exceedances in a web page.  

<h2>Technologies Used:</h2>
<strong>Flask</strong>: For the web server and endpoints.  
<strong>Prometheus Format:</strong> For serving metrics.  
<strong>Python:</strong> For backend logic and data processing.  

<h2>How to Run:</h2>
Clone the repository.  
Install dependencies: <code>pip install -r requirements.txt</code>.  
Run the application: <code>python app.py</code>.  
Access the <code>/metrics</code> endpoint at <code>http://localhost:5000/metrics</code> and the <code>/exceeding</code> endpoint at <code>http://localhost:5000/exceeding</code>.  

<h2>Configuration:</h2>
Modify the <code>config.py</code> file to adjust:  
Number of applications (<code>NUM_APPS</code>).  
Threshold value (<code>THRESHOLD</code>).  
Metrics generation interval (<code>METRICS_INTERVAL</code>).  
Display mode (<code>DISPLAY_MODE</code>).  

<h2>Use Cases:</h2>
Monitoring application performance metrics.  
Simulating and testing Prometheus-based monitoring systems.  
Demonstrating threshold-based alerting and reporting.  

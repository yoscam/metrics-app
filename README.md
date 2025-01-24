# Metrics Application

This is a Python web application that generates metrics and exposes them in Prometheus format. It also processes the metrics to track threshold exceedances and displays the top apps that exceed the threshold the most.

## How to Run

1.	Clone the repository or download the files.
2.	Install the required dependencies:
	bash / cmd
	cd {application folder}
	pip install -r requirements.txt
3.	Run the application:
	python app.py
4.	Access the application:
	http://localhost:5000/metrics
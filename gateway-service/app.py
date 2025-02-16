from flask import Flask, jsonify, request
import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# List of storage service URLs
storage_services = [
    "http://storage_service_1:5000",
    "http://storage_service_2:5000",
    "http://storage_service_3:5000",
]

# Status of each storage service
service_statuses = {url: {"status": "unknown", "failures": 0, "state": "CLOSED"} for url in storage_services}

# Cached data
cached_data = None

# Round-robin counter
current_service = 0

# Connection pooling
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

# Circuit breaker thresholds
FAILURE_THRESHOLD = 3
RECOVERY_TIMEOUT = 30  # seconds

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "sparksailor7@gmail.com"
SMTP_PASSWORD = ""
EMAIL_FROM = "sparksailor7@gmail.com"
EMAIL_TO = "zvenczel@kx.com"

def send_email_notification(subject, message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)
        server.quit()
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def health_check():
    while True:
        for service_url in storage_services:
            if service_statuses[service_url]["state"] == "OPEN":
                # Skip health check if the circuit is open
                continue

            try:
                response = session.get(f"{service_url}/health", timeout=2)
                response.raise_for_status()
                service_statuses[service_url] = {"status": "running", "failures": 0, "state": "CLOSED"}
                logging.info(f"{service_url} is running")
            except requests.exceptions.RequestException:
                service_statuses[service_url]["failures"] += 1
                logging.error(f"{service_url} is unavailable (failure count: {service_statuses[service_url]['failures']})")
                if service_statuses[service_url]["failures"] >= FAILURE_THRESHOLD:
                    service_statuses[service_url]["state"] = "OPEN"
                    logging.error(f"{service_url} circuit breaker opened")
                    send_email_notification(f"Alert: {service_url} is down", f"The storage service at {service_url} is down and the circuit breaker is open.")
                service_statuses[service_url]["status"] = "unavailable"

        time.sleep(10)  # Check every 10 seconds

def circuit_breaker_recovery():
    while True:
        for service_url in storage_services:
            if service_statuses[service_url]["state"] == "OPEN":
                time.sleep(RECOVERY_TIMEOUT)
                service_statuses[service_url]["state"] = "HALF-OPEN"
                logging.info(f"{service_url} circuit breaker half-open (testing recovery)")
                try:
                    response = session.get(f"{service_url}/health", timeout=2)
                    response.raise_for_status()
                    service_statuses[service_url] = {"status": "running", "failures": 0, "state": "CLOSED"}
                    logging.info(f"{service_url} has recovered and is running")
                    send_email_notification(f"Info: {service_url} has recovered", f"The storage service at {service_url} has recovered and is running.")
                except requests.exceptions.RequestException:
                    service_statuses[service_url]["state"] = "OPEN"
                    logging.error(f"{service_url} is still unavailable, circuit breaker remains open")

        time.sleep(10)  # Check every 10 seconds

@app.route('/status', methods=['GET'])
def status():
    return jsonify(service_statuses)

@app.route('/data', methods=['GET'])
def data():
    global current_service, cached_data
    available_services = [url for url, status in service_statuses.items() if status["status"] == "running"]
    if not available_services:
        if cached_data:
            return jsonify(cached_data), 200
        else:
            return jsonify({'error': 'No Storage Services are available and no cached data is available'}), 503
    service_url = available_services[current_service % len(available_services)]
    current_service += 1
    try:
        response = session.get(f"{service_url}/data", timeout=2)
        response.raise_for_status()
        cached_data = response.json()  # Update cached data
        return jsonify(cached_data), response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {service_url}: {e}")
        if cached_data:
            return jsonify(cached_data), 200
        else:
            return jsonify({'error': 'Storage Service is not available and no cached data is available'}), 503

@app.route('/health', methods=['GET'])
def health_check_endpoint():
    return jsonify({"status": "Gateway service is running"}), 200

if __name__ == '__main__':
    logging.info("Starting gateway service...")
    threading.Thread(target=health_check, daemon=True).start()
    threading.Thread(target=circuit_breaker_recovery, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
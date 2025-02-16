from flask import Flask, jsonify, request, render_template
import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading
import time
import psutil
import signal
from routes.service1 import service1_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(service1_bp)

# Configure logging
logging.basicConfig(level=logging.INFO)

# List of storage service URLs
storage_services = [
    "http://storage_service_1:5000",
    "http://storage_service_2:5000",
    "http://storage_service_3:5000",
]

# Round-robin counter
current_service = 0

# Connection pooling
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

@app.route('/service1/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def service1_proxy(path):
    global current_service
    service_url = storage_services[current_service]
    current_service = (current_service + 1) % len(storage_services)
    try:
        response = session.request(
            method=request.method,
            url=f"{service_url}/{path}",
            json=request.get_json(),
            headers={key: value for (key, value) in request.headers if key != 'Host'}
        )
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        logging.error(f"Storage Service is not available at {service_url}")
        return jsonify({'error': 'Storage Service is not available'}), 503
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {service_url}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check_endpoint():
    return jsonify({"status": "Gateway service is running"}), 200

if __name__ == '__main__':
    logging.info("Starting gateway service...")
    app.run(host='0.0.0.0', port=5000)
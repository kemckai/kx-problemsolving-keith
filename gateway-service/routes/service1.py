# filepath: /Users/spectorclef/Documents/Keith/distributed_service/distributed-service-assembly/gateway-service/routes/service1.py
from flask import Blueprint, render_template, jsonify, request
import requests
import logging

service1_bp = Blueprint('service1', __name__)

@service1_bp.route('/service1', methods=['GET'])
def service1():
    return render_template('service1.html')

@service1_bp.route('/service1/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def service1_proxy(path):
    logging.info(f"Received request for /service1/{path}")
    url = f'http://storage-service:5000/{path}'
    try:
        response = requests.request(
            method=request.method,
            url=url,
            json=request.get_json(),
            headers={key: value for (key, value) in request.headers if key != 'Host'}
        )
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        logging.error(f"Storage Service is not available at {url}")
        return jsonify({'error': 'Storage Service is not available'}), 503
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return jsonify({'error': str(e)}), 500
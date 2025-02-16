from flask import Flask, jsonify, render_template
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Dummy data for the storage service
dummy_data = {
    "service_1": {"id": 1, "message": "Hello from Service 1"},
    "service_2": {"id": 2, "message": "Hello from Service 2"},
    "service_3": {"id": 3, "message": "Hello from Service 3"},
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    try:
        logging.info("Status endpoint called")
        return jsonify({"status": "running"})
    except Exception as e:
        logging.error(f"Error in status endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=['GET'])
def data():
    try:
        logging.info("Data endpoint called")
        return jsonify(dummy_data)
    except Exception as e:
        logging.error(f"Error in data endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        logging.info("Health check endpoint called")
        return jsonify({"status": "Storage service is running"}), 200
    except Exception as e:
        logging.error(f"Error in health check endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting storage service...")
    app.run(host='0.0.0.0', port=5000)
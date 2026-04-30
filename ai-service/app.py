import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import routes
from routes.health import get_health

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    health_data = get_health()
    return jsonify({
        "status": "healthy" if "error" not in health_data else "unhealthy",
        "timestamp": time.time(),
        "data": health_data
    })

@app.route('/describe', methods=['POST'])
def describe():
    return jsonify({"message": "Endpoint not yet implemented"}), 501

@app.route('/recommend', methods=['POST'])
def recommend():
    return jsonify({"message": "Endpoint not yet implemented"}), 501

@app.route('/categorise', methods=['POST'])
def categorise():
    return jsonify({"message": "Endpoint not yet implemented"}), 501

@app.route('/generate-report', methods=['POST'])
def generate_report():
    return jsonify({"message": "Endpoint not yet implemented"}), 501

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

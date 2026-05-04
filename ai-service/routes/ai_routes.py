from flask import Blueprint, request, jsonify, g
import time
import json
from services.groq_client import GroqClient

ai_bp = Blueprint('ai', __name__)
client = GroqClient()

def get_request_data():
    return getattr(g, 'sanitized_data', request.get_json())

@ai_bp.route('/describe', methods=['POST'])
def describe():
    data = get_request_data()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    user_input = data['text']
    prompt = f"Describe the following security incident or log entry in detail:\n\n{user_input}"
    
    start_time = time.time()
    response = client.generate_response(prompt)
    end_time = time.time()
    
    return jsonify({
        "result": response,
        "metadata": {
            "confidence": 0.85,  # Mocked for now
            "model_used": "llama-3.3-70b-versatile",
            "response_time_ms": int((end_time - start_time) * 1000),
            "cached": False  # Handled by GroqClient but we can refine this later
        }
    })

@ai_bp.route('/recommend', methods=['POST'])
def recommend():
    data = get_request_data()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    user_input = data['text']
    prompt = f"Provide security recommendations for the following scenario:\n\n{user_input}"
    
    start_time = time.time()
    response = client.generate_response(prompt)
    end_time = time.time()
    
    return jsonify({
        "result": response,
        "metadata": {
            "confidence": 0.90,  # Mocked for now
            "model_used": "llama-3.3-70b-versatile",
            "response_time_ms": int((end_time - start_time) * 1000),
            "cached": False
        }
    })

@ai_bp.route('/categorise', methods=['POST'])
def categorise():
    return jsonify({"message": "Endpoint not yet implemented"}), 501

@ai_bp.route('/generate-report', methods=['POST'])
def generate_report():
    return jsonify({"message": "Endpoint not yet implemented"}), 501

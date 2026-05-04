from flask import Blueprint, request, jsonify, g
import time
import json
from services.groq_client import GroqClient
from extensions.limiter import limiter

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
    response, is_cached = client.generate_response(prompt)
    end_time = time.time()
    
    return jsonify({
        "result": response,
        "metadata": {
            "confidence": 0.85,
            "model_used": "llama-3.3-70b-versatile",
            "response_time_ms": int((end_time - start_time) * 1000),
            "cached": is_cached
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
    response, is_cached = client.generate_response(prompt)
    end_time = time.time()
    
    return jsonify({
        "result": response,
        "metadata": {
            "confidence": 0.90,
            "model_used": "llama-3.3-70b-versatile",
            "response_time_ms": int((end_time - start_time) * 1000),
            "cached": is_cached
        }
    })

@ai_bp.route('/categorise', methods=['POST'])
def categorise():
    data = get_request_data()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    user_input = data['text']
    prompt = f"""
Classify the following text into EXACTLY ONE category:
Categories: [Bug, Feature Request, Feedback, Other]
Return ONLY JSON: {{"category": "", "confidence": 0.0, "reasoning": ""}}
Text: {user_input}
"""
    
    start_time = time.time()
    response, is_cached = client.generate_response(prompt)
    end_time = time.time()
    
    try:
        parsed = json.loads(response)
    except:
        parsed = {"category": "Other", "confidence": 0.5, "reasoning": "Failed to parse AI response", "raw_response": response}

    return jsonify({
        "result": parsed,
        "metadata": {
            "confidence": parsed.get("confidence", 0.0),
            "model_used": "llama-3.3-70b-versatile",
            "response_time_ms": int((end_time - start_time) * 1000),
            "cached": is_cached
        }
    })

@ai_bp.route('/generate-report', methods=['POST'])
@limiter.limit("10 per minute")
def generate_report():
    data = get_request_data()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    user_input = data['text']
    prompt = f"Generate a comprehensive security report based on the following logs/events:\n\n{user_input}\n\nInclude: Summary, Risk Level, and Action Plan."
    
    start_time = time.time()
    response, is_cached = client.generate_response(prompt)
    end_time = time.time()
    
    return jsonify({
        "result": response,
        "metadata": {
            "confidence": 0.95,
            "model_used": "llama-3.3-70b-versatile",
            "response_time_ms": int((end_time - start_time) * 1000),
            "cached": is_cached
        }
    })

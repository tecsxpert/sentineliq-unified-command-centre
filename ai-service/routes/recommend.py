"""
Recommend Route - Actionable recommendation generation
"""
from flask import Blueprint, jsonify, request
import json
from services.groq_client import GroqClient
from prompts.recommend_prompt import RECOMMEND_PROMPT

# Create blueprint
recommend_bp = Blueprint('recommend', __name__)

client = GroqClient()


def validate_recommend_input(text):
    """Validate and clean input for recommendation generation."""
    if not text or not isinstance(text, str):
        return False, "Text must be a non-empty string", None

    cleaned = text.strip()

    if len(cleaned) < 5:
        return False, "Text must be at least 5 characters long", None

    if len(cleaned) > 5000:
        return False, "Text exceeds maximum length of 5000 characters", None

    invalid_chars = cleaned.count('$') + cleaned.count('^') + cleaned.count('\\')
    if invalid_chars > 5:
        return False, "Text contains excessive special characters", None

    return True, None, cleaned


def normalize_recommendation(item):
    """Normalize a recommendation object and enforce valid fields."""
    if not isinstance(item, dict):
        return {
            "action_type": "investigate",
            "description": "Review the input and identify an improvement opportunity.",
            "priority": "medium"
        }

    action_type = str(item.get("action_type", "investigate")).strip().lower()
    if action_type not in ["fix", "improve", "investigate", "document", "communicate"]:
        action_type = "investigate"

    description = str(item.get("description", "Create a recommendation based on the input.")).strip()
    if not description:
        description = "Create a recommendation based on the input."

    priority = str(item.get("priority", "medium")).strip().lower()
    if priority not in ["high", "medium", "low"]:
        priority = "medium"

    return {
        "action_type": action_type,
        "description": description,
        "priority": priority
    }


def recommend_text(user_input, use_cache=True):
    """Generate 3 actionable recommendations from user input."""
    prompt = RECOMMEND_PROMPT.format(input_text=user_input)
    response = client.generate_response(prompt, use_cache=use_cache)

    try:
        parsed = json.loads(response)
    except json.JSONDecodeError:
        parsed = None

    recommendations = []
    if isinstance(parsed, list):
        recommendations = [normalize_recommendation(item) for item in parsed[:3]]
    elif isinstance(parsed, dict) and "recommendations" in parsed and isinstance(parsed["recommendations"], list):
        recommendations = [normalize_recommendation(item) for item in parsed["recommendations"][:3]]
    else:
        recommendations = [
            {
                "action_type": "investigate",
                "description": "Review the submission and identify the top three improvement actions.",
                "priority": "medium"
            },
            {
                "action_type": "improve",
                "description": "Improve the user experience by addressing the main usability issue.",
                "priority": "medium"
            },
            {
                "action_type": "document",
                "description": "Document the issue and communicate recommended next steps to the team.",
                "priority": "low"
            }
        ]

    if len(recommendations) < 3:
        while len(recommendations) < 3:
            recommendations.append({
                "action_type": "investigate",
                "description": "Identify an additional recommendation from the input.",
                "priority": "low"
            })

    return recommendations


@recommend_bp.route('/recommend', methods=['POST'])
def recommend_endpoint():
    """Generate actionable recommendations from raw user input."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body must be JSON",
                "required_fields": ["text"]
            }), 400

        if 'text' not in data:
            return jsonify({
                "error": "Missing required field: 'text'",
                "required_fields": ["text"],
                "optional_fields": ["use_cache"]
            }), 400

        is_valid, error_msg, cleaned_text = validate_recommend_input(data['text'])
        if not is_valid:
            return jsonify({
                "error": error_msg
            }), 400

        use_cache = data.get('use_cache', True)
        if not isinstance(use_cache, bool):
            use_cache = True

        recommendations = recommend_text(cleaned_text, use_cache=use_cache)
        return jsonify(recommendations), 200

    except json.JSONDecodeError:
        return jsonify({
            "error": "Invalid JSON in request body"
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": "server_error"
        }), 500

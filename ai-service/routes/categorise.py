from flask import Blueprint, jsonify, request
from services.groq_client import GroqClient

# Create blueprint
categorise_bp = Blueprint('categorise', __name__)

client = GroqClient()

def categorise_text(user_input):
    try:
        prompt = f"""
Classify the following text into EXACTLY ONE category:

Categories:
- Bug
- Feature Request
- Feedback
- Other

STRICT RULES:
- Do NOT use markdown
- Do NOT use ```
- Return ONLY valid JSON
- Do NOT add any extra text

Format:
{{
    "category": "",
    "confidence": 0.0,
    "reasoning": ""
}}

Text:
{user_input}
"""

        response = client.generate_response(prompt)

        return response

    except Exception as e:
        return {
            "error": str(e)
        }


@categorise_bp.route('/categorise', methods=['POST'])
def categorise_endpoint():
    """
    Text categorisation endpoint
    
    Request JSON:
    {
        "text": "Text to categorise"
    }
    
    Response JSON:
    {
        "category": "Bug|Feature Request|Feedback|Other",
        "confidence": 0.0-1.0,
        "reasoning": "Explanation of categorisation"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        
        result = categorise_text(text)
        
        # Try to parse JSON response
        import json
        try:
            parsed = json.loads(result)
            return jsonify(parsed), 200
        except:
            return jsonify({"category": result}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
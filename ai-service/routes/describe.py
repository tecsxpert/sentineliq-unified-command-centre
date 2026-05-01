"""
Describe Route - Professional text description generation
Transforms raw user input into standardized, professional descriptions
"""
from flask import Blueprint, jsonify, request
import json
from datetime import datetime, timezone
from services.groq_client import GroqClient
from prompts.describe_prompt import DESCRIBE_PROMPT

# Create blueprint
describe_bp = Blueprint('describe', __name__)

client = GroqClient()


def validate_describe_input(text):
    """
    Validate and clean describe endpoint input
    
    Args:
        text: Input text to validate
        
    Returns:
        tuple: (is_valid, error_message, cleaned_text)
    """
    if not text or not isinstance(text, str):
        return False, "Text must be a non-empty string", None
    
    cleaned = text.strip()
    
    if len(cleaned) < 5:
        return False, "Text must be at least 5 characters long", None
    
    if len(cleaned) > 5000:
        return False, "Text exceeds maximum length of 5000 characters", None
    
    # Check for valid characters (no excessive special characters)
    invalid_chars = cleaned.count('$') + cleaned.count('^') + cleaned.count('\\')
    if invalid_chars > 5:
        return False, "Text contains excessive special characters", None
    
    return True, None, cleaned


def describe_text(user_input, use_cache=True):
    """
    Generate professional description from user input
    
    Args:
        user_input: Text to describe (issue, feature, feedback)
        use_cache: Whether to use cached responses
        
    Returns:
        dict: JSON object with title, description, severity, type, key_points, and metadata
    """
    start_time = datetime.now(timezone.utc)
    
    try:
        # Format prompt with user input
        prompt = DESCRIBE_PROMPT.format(input_text=user_input)
        
        # Call Groq with caching and retries
        response = client.generate_response(prompt, use_cache=use_cache)
        
        # Parse JSON response
        try:
            parsed = json.loads(response)
            
            # Validate response structure
            required_fields = ['title', 'description', 'severity', 'type', 'key_points']
            if not all(field in parsed for field in required_fields):
                # Add missing fields with defaults
                parsed.setdefault('title', 'Description Generated')
                parsed.setdefault('description', response)
                parsed.setdefault('severity', 'medium')
                parsed.setdefault('type', 'feedback')
                parsed.setdefault('key_points', [])
            
            # Add metadata
            end_time = datetime.now(timezone.utc)
            parsed['metadata'] = {
                'generated_at': start_time.isoformat(),
                'processing_ms': int((end_time - start_time).total_seconds() * 1000),
                'cached': False
            }
            
            return parsed
            
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return structured error
            end_time = datetime.now(timezone.utc)
            return {
                "title": "Parsing Error",
                "description": f"Invalid JSON response from LLM. Raw: {response[:100]}",
                "severity": "low",
                "type": "feedback",
                "key_points": [],
                "metadata": {
                    'generated_at': start_time.isoformat(),
                    'processing_ms': int((end_time - start_time).total_seconds() * 1000),
                    'error': 'json_decode_error'
                }
            }
            
    except Exception as e:
        end_time = datetime.now(timezone.utc)
        return {
            "error": str(e),
            "title": "Generation Error",
            "description": f"Failed to generate description: {str(e)}",
            "severity": "high",
            "type": "error",
            "key_points": [],
            "metadata": {
                'generated_at': start_time.isoformat(),
                'processing_ms': int((end_time - start_time).total_seconds() * 1000),
                'error': 'processing_error'
            }
        }


@describe_bp.route('/describe', methods=['POST'])
def describe_endpoint():
    """
    Describe endpoint - Generate professional descriptions
    
    Request JSON:
    {
        "text": "Raw user input to describe",
        "use_cache": true (optional, default: true)
    }
    
    Response JSON:
    {
        "title": "Professional title",
        "description": "Detailed description",
        "severity": "low|medium|high|critical",
        "type": "bug|feature|feedback|enhancement|documentation|error",
        "key_points": ["point 1", "point 2", "point 3"],
        "metadata": {
            "generated_at": "2026-05-01T10:30:45.123456+00:00",
            "processing_ms": 1234,
            "cached": false
        }
    }
    
    Status Codes:
    - 200: Success
    - 400: Invalid input (missing text, too short, too long)
    - 413: Payload too large
    - 500: Server error
    """
    request_time = datetime.now(timezone.utc)
    
    try:
        # Get JSON payload
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "Request body must be JSON",
                "received_at": request_time.isoformat(),
                "required_fields": ["text"]
            }), 400
        
        # Validate input presence
        if 'text' not in data:
            return jsonify({
                "error": "Missing required field: 'text'",
                "received_at": request_time.isoformat(),
                "required_fields": ["text"],
                "optional_fields": ["use_cache"]
            }), 400
        
        # Validate input content
        is_valid, error_msg, cleaned_text = validate_describe_input(data['text'])
        if not is_valid:
            return jsonify({
                "error": error_msg,
                "received_at": request_time.isoformat()
            }), 400
        
        # Get cache preference (default: true)
        use_cache = data.get('use_cache', True)
        if not isinstance(use_cache, bool):
            use_cache = True
        
        # Generate description
        result = describe_text(cleaned_text, use_cache=use_cache)
        
        return jsonify(result), 200
        
    except json.JSONDecodeError:
        return jsonify({
            "error": "Invalid JSON in request body",
            "received_at": request_time.isoformat()
        }), 400
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": "server_error",
            "received_at": request_time.isoformat()
        }), 500

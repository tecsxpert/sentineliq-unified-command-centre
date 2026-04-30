import re
from flask import request, jsonify

# Characters to strip
STRIP_CHARS = r'[<>"\'\(\);&]'

# Prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore previous",
    r"system:",
    r"assistant:",
    r"you are now",
    r"new instructions"
]

def sanitize_input(text):
    if not isinstance(text, str):
        return text
    # Strip dangerous characters
    return re.sub(STRIP_CHARS, '', text)

def detect_injection(text):
    if not isinstance(text, str):
        return False
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False

def security_middleware():
    if request.method == 'POST':
        if not request.is_json:
            return
            
        data = request.get_json(silent=True)
        if not data:
            return

        modified = False
        for key, value in data.items():
            if isinstance(value, str):
                if detect_injection(value):
                    return jsonify({
                        "error": "Security Alert: Potential prompt injection detected",
                        "status": 400
                    }), 400
                
                sanitized = sanitize_input(value)
                
                # Apply PII scrubbing
                from middleware.pii_scrubber import scrub_pii
                scrubbed = scrub_pii(sanitized)
                
                if scrubbed != value:
                    data[key] = scrubbed
                    modified = True
        
        if modified:
            # We can't easily re-assign request.json in Flask, 
            # but we can use a custom property or just rely on the route getting the data again.
            # However, since we've already parsed it, we can store it in g.
            from flask import g
            g.sanitized_data = data

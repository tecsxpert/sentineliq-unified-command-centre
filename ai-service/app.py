import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import routes
from routes.health import get_health
from routes.ai_routes import ai_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Limiter
from extensions.limiter import limiter
limiter.init_app(app)

# Register Blueprints
app.register_blueprint(ai_bp)

# Register Middleware
from middleware.security import security_middleware
app.before_request(security_middleware)

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route('/health', methods=['GET'])
def health_check():
    health_data = get_health()
    return jsonify({
        "status": "healthy" if "error" not in health_data else "unhealthy",
        "timestamp": time.time(),
        "data": health_data
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

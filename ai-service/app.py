"""
Flask AI Service Entry Point
Unified Command Centre - AI Microservice
"""
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend communication
CORS(app)

# Configure app
app.config['JSON_SORT_KEYS'] = False


# ==================== BLUEPRINT REGISTRATION ====================

# Import and register route blueprints
from routes.health import health_bp
from routes.query import query_bp
from routes.categorise import categorise_bp
from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.rag import rag_bp
from routes.report import report_bp
from routes.analyse import analyse_bp
from routes.batch_process import batch_bp

app.register_blueprint(health_bp, url_prefix='/api/ai')
app.register_blueprint(query_bp, url_prefix='/api/ai')
app.register_blueprint(categorise_bp, url_prefix='/api/ai')
app.register_blueprint(describe_bp, url_prefix='/api/ai')
app.register_blueprint(recommend_bp, url_prefix='/api/ai')
app.register_blueprint(rag_bp, url_prefix='/api/ai')
app.register_blueprint(report_bp, url_prefix='/api/ai')
app.register_blueprint(analyse_bp, url_prefix='/api/ai')
app.register_blueprint(batch_bp, url_prefix='/api/ai')


# ==================== ROOT ENDPOINT ====================

@app.route('/api/ai', methods=['GET'])
def root():
    """Root endpoint for API verification"""
    return jsonify({
        "service": "Sentiment IQ AI Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "GET /api/ai/health",
            "query": "POST /api/ai/query",
            "categorise": "POST /api/ai/categorise",
            "describe": "POST /api/ai/describe",
            "recommend": "POST /api/ai/recommend",
            "rag": {
                "health": "GET /api/ai/rag/health",
                "upload": "POST /api/ai/rag/upload",
                "retrieve": "POST /api/ai/rag/retrieve",
                "stats": "GET /api/ai/rag/stats",
                "clear": "DELETE /api/ai/rag/clear",
                "export": "GET /api/ai/rag/export"
            },
            "report": {
                "generate": "POST /api/ai/generate-report",
                "template": "GET /api/ai/generate-report/template",
                "types": "GET /api/ai/generate-report/types",
                "preview": "POST /api/ai/generate-report/preview",
                "compare": "POST /api/ai/generate-report/compare"
            }
        }
    })


# ==================== ERROR HANDLING ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": str(error)
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500


# ==================== APP STARTUP ====================

if __name__ == '__main__':
    port = os.getenv('AI_SERVICE_PORT', 5000)
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting AI Service on port {port}...")
    app.run(
        host='0.0.0.0',
        port=int(port),
        debug=debug
    )

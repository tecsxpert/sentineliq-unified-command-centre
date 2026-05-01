"""
AI Service Quick Start Guide

This file provides a quick reference for getting the AI service up and running.
"""

# ==================== SETUP ====================

# 1. Install dependencies

# pip install -r requirements.txt

# 2. Create .env file

# Copy .env.example to .env

# Add your GROQ_API_KEY

# 3. Run the service

# python app.py

# ==================== FILE STRUCTURE ====================

"""
ai-service/
├── app.py # Flask application entry point
├── requirements.txt # Python dependencies
├── Dockerfile # Docker containerization
├── .env.example # Environment variables template
├── README.md # Full documentation
│
├── routes/ # Flask blueprints (API endpoints)
│ ├── **init**.py
│ ├── health.py # GET /api/ai/health
│ ├── query.py # POST /api/ai/query
│ └── categorise.py # POST /api/ai/categorise
│
├── services/ # Business logic & external integrations
│ ├── **init**.py
│ ├── groq_client.py # Groq LLM API client
│ ├── chroma_service.py # Vector database (Chroma)
│ └── cache_service.py # Response caching
│
├── prompts/ # LLM prompt templates
│ ├── **init**.py
│ ├── query_prompt.py # RAG query prompt
│ ├── categorise_prompt.py # Categorization prompt
│ └── health_prompt.py # Health check prompt
│
└── tests/ # Test files (existing)
├── test_health.py
├── test_query.py
├── test_categorise.py
└── ...
"""

# ==================== API ENDPOINTS ====================

"""

1. HEALTH CHECK
   GET http://localhost:5000/api/ai/health

   Response:
   {
   "model": "llama-3.3-70b-versatile",
   "avg_response_time": 0.5234,
   "chroma_docs": 150,
   "uptime_seconds": 3600.32,
   "cache": { "cached_items": 42 }
   }

2. QUERY (RAG)
   POST http://localhost:5000/api/ai/query

   Body:
   {
   "question": "What can the app do?"
   }

   Response:
   {
   "answer": "The app can...",
   "sources": ["source 1", "source 2"]
   }

3. CATEGORISE
   POST http://localhost:5000/api/ai/categorise
   Body:
   {
   "text": "The app crashes when I login"
   }
   Response:
   {
   "category": "Bug",
   "confidence": 0.95,
   "reasoning": "System failure reported during login"
   }
   """

# ==================== TESTING ====================

"""
Test individual endpoints:

# Test health

curl http://localhost:5000/api/ai/health

# Test query

curl -X POST http://localhost:5000/api/ai/query \
 -H "Content-Type: application/json" \
 -d '{"question": "What is the app?"}'

# Test categorise

curl -X POST http://localhost:5000/api/ai/categorise \
 -H "Content-Type: application/json" \
 -d '{"text": "The app crashes on startup"}'

Or run existing test files:
python test_health.py
python test_query.py
python test_categorise.py
"""

# ==================== DEVELOPMENT ====================

"""
Adding a new endpoint:

1. Create route file (routes/new_feature.py):
   from flask import Blueprint, jsonify, request

   bp = Blueprint('feature', **name**)

   @bp.route('/feature', methods=['POST'])
   def feature_endpoint():
   data = request.get_json() # Your logic here
   return jsonify({"result": "data"})

2. Create service if needed (services/feature_service.py)

3. Register in app.py:
   from routes.new_feature import bp as feature_bp
   app.register_blueprint(feature_bp, url_prefix='/api/ai')

4. Test your endpoint
   """

# ==================== ENVIRONMENT VARIABLES ====================

"""
Required:

- GROQ_API_KEY: Your Groq API key

Optional:

- FLASK_ENV: development or production (default: development)
- AI_SERVICE_PORT: Service port (default: 5000)
- REDIS_URL: Redis connection (if using Redis cache)
  """

# ==================== DEPLOYMENT ====================

"""
Docker:
docker build -t sentineliq-ai-service .
docker run -p 5000:5000 --env-file .env sentineliq-ai-service

With docker-compose (from root):
docker-compose up ai-service
"""

# ==================== TROUBLESHOOTING ====================

"""
Issue: "GROQ_API_KEY not found"
Fix: Create .env file with GROQ_API_KEY=your_key

Issue: "ModuleNotFoundError: No module named 'routes'"
Fix: Ensure you're running from ai-service directory
Or use: python -m app (not: python app.py)

Issue: "CORS error from frontend"
Fix: CORS is enabled in app.py, check network request

Issue: "Chroma collection is empty"
Fix: Run a query to initialize the collection
"""

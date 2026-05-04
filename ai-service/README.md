# AI Service - README

Flask-based AI microservice for the Sentinel IQ Unified Command Centre providing RAG (Retrieval-Augmented Generation) query answering and text categorization.

## Features

- **Query Endpoint**: RAG-based question answering using Groq LLM + Chroma vector DB
- **Categorise Endpoint**: Text classification using Groq LLM
- **Health Check**: System diagnostics including response times and cache stats
- **Caching**: Response caching via Redis/local storage
- **CORS Support**: Frontend communication enabled
- **Error Handling**: Comprehensive error responses and logging

## Project Structure

```
ai-service/
├── app.py                    # Flask entry point
├── requirements.txt          # Python dependencies
├── routes/                   # Flask blueprints
│   ├── health.py            # Health check endpoint
│   ├── query.py             # RAG query endpoint
│   └── categorise.py        # Text categorisation endpoint
├── services/                # Business logic
│   ├── groq_client.py       # Groq LLM client with caching
│   ├── chroma_service.py    # Vector database integration
│   └── cache_service.py     # Response caching
└── prompts/                 # LLM prompt templates
    ├── query_prompt.py
    ├── categorise_prompt.py
    └── health_prompt.py
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file (use `.env.example` as template):

```bash
GROQ_API_KEY=your_groq_api_key
FLASK_ENV=development
AI_SERVICE_PORT=5000
```

### 3. Run the Service

**Development:**

```bash
python app.py
```

**Production (with Gunicorn):**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### 1. Health Check

```
GET /api/ai/health

Response:
{
    "model": "llama-3.3-70b-versatile",
    "avg_response_time": 0.5234,
    "chroma_docs": 150,
    "uptime_seconds": 3600.32,
    "cache": {
        "cached_items": 42
    }
}
```

### 2. Query (RAG)

```
POST /api/ai/query

Request:
{
    "question": "What features does the app have?"
}

Response:
{
    "answer": "The app has the following features...",
    "sources": [
        "Context source 1",
        "Context source 2"
    ]
}
```

### 3. Categorise

```
POST /api/ai/categorise

Request:
{
    "text": "The app crashes when I login"
}

Response:
{
    "category": "Bug",
    "confidence": 0.95,
    "reasoning": "User reported system failure during authentication"
}
```

## Configuration

### Environment Variables

| Variable          | Default     | Purpose                 |
| ----------------- | ----------- | ----------------------- |
| `GROQ_API_KEY`    | -           | Groq API authentication |
| `FLASK_ENV`       | development | Environment mode        |
| `AI_SERVICE_PORT` | 5000        | Service port            |

### Cache Strategy

- **Type**: In-memory (Redis ready)
- **TTL**: Configurable per request
- **Strategy**: LRU eviction

## Development Guidelines

### Adding a New Endpoint

1. Create route file in `routes/` with Flask blueprint
2. Create service logic in `services/` if needed
3. Create prompt template in `prompts/` if using LLM
4. Register blueprint in `app.py`

### Example Route:

```python
from flask import Blueprint, jsonify, request

bp = Blueprint('feature', __name__)

@bp.route('/feature', methods=['POST'])
def feature_endpoint():
    data = request.get_json()
    # Process request
    return jsonify(result)
```

## Testing

Run existing test files:

```bash
python test_health.py
python test_query.py
python test_categorise.py
```

## Docker Deployment

```bash
docker build -t sentineliq-ai-service .
docker run -p 5000:5000 --env-file .env sentineliq-ai-service
```

## Common Issues

### Issue: "GROQ_API_KEY not found"

**Solution**: Ensure `.env` file exists in project root with valid API key

### Issue: "Chroma collection empty"

**Solution**: Call query endpoint first to initialize data via `add_data()`

### Issue: "CORS error from frontend"

**Solution**: Verify Flask-CORS is installed and app is configured with `CORS(app)`

## Performance Notes

- Average response time: 500-1000ms per query
- Chroma supports up to 100K+ documents
- Groq API has rate limits (see documentation)
- Caching reduces latency by 90%+ for repeated queries

## Contributing

1. Create a new feature branch
2. Follow existing code style (PEP 8)
3. Add tests for new endpoints
4. Update README with new endpoints/config options

## License

Internal - Sentinel IQ

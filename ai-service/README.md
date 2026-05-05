# AI Service - Sentinel IQ Unified Command Centre

A production-ready Flask microservice providing 9 AI-powered endpoints for the Sentinel IQ Unified Command Centre. Combines Groq LLM, ChromaDB vector search, concurrent batch processing, and streaming capabilities with comprehensive testing framework.

**Status**: 🚀 Production Ready | **Day 12**: Complete Documentation | **Test Coverage**: 50+ pytest tests  
**Python**: 3.13.1 | **Framework**: Flask 2.3.3 | **LLM**: Groq llama-3.3-70b | **Vector DB**: ChromaDB 0.3.21

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Service](#running-the-service)
- [API Reference](#api-reference)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Architecture](#architecture)

---

## Prerequisites

### System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.9+ (tested with 3.13.1)
- **Memory**: 2GB minimum (4GB+ recommended for ChromaDB)
- **Disk Space**: 1GB for dependencies + ChromaDB vector store
- **Network**: Outbound HTTPS for Groq API (groq.com)

### External Dependencies

- **Groq API**: Free tier available at [groq.com](https://groq.com)
- **Python Package Manager**: pip 24.0+

---

## Installation

### 1. Clone and Navigate

```bash
cd c:\Users\Polic\OneDrive\Desktop\SAINATH\ PATIL\sentineliq-unified-command-centre\ai-service
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies**:

```
Flask==2.3.3              # Web framework
Flask-CORS==4.0.0         # Cross-origin resource sharing
groq==0.4.2               # Groq LLM API client
chromadb==0.3.21          # Vector database
sentence-transformers==2.2.2  # Embeddings
langchain==0.1.16         # LLM orchestration
python-dotenv==1.0.0      # Environment variables
pytest==7.4.3             # Testing framework
pytest-mock==3.12.0       # Test mocking
gunicorn==21.2.0          # Production WSGI server
```

---

## Configuration

### Environment Variables

Create a `.env` file in the `ai-service` directory with the following variables:

```bash
# ==================== REQUIRED ====================

# Groq API Authentication (get from https://groq.com)
GROQ_API_KEY=your_groq_api_key_here

# Flask Configuration
FLASK_ENV=development

# ==================== OPTIONAL ====================

# Server Configuration
AI_SERVICE_PORT=5000                    # Default: 5000
AI_SERVICE_HOST=0.0.0.0                # Default: 0.0.0.0 (all interfaces)

# ChromaDB Configuration
CHROMA_DB_PATH=./chroma_db              # Default: ./chroma_db
CHROMA_COLLECTION_NAME=AI-Documents    # Default: AI-Documents

# Groq Model Configuration
GROQ_MODEL=llama-3.3-70b               # Default: llama-3.3-70b
GROQ_TEMPERATURE=0.3                   # Default: 0.3 (0.0-1.0)
GROQ_MAX_TOKENS=2000                   # Default: 2000

# Caching Configuration
CACHE_ENABLED=true                     # Default: true
CACHE_TTL_SECONDS=3600                 # Default: 3600 (1 hour)

# Batch Processing Configuration
BATCH_PROCESSOR_WORKERS=5              # Default: 5 (concurrent workers)
BATCH_PROCESSOR_ITEM_DELAY_MS=100      # Default: 100ms per item
BATCH_PROCESSOR_MAX_ITEMS=20           # Default: 20 items per batch

# Groq Retry Configuration
GROQ_RETRY_ATTEMPTS=3                  # Default: 3
GROQ_RETRY_DELAY=1                     # Default: 1 second

# Logging Configuration (optional)
LOG_LEVEL=INFO                         # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/ai-service.log
```

---

## Running the Service

### Development Mode (Flask Development Server)

```bash
# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Run development server
python app.py
```

**Output**:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

Service available at: `http://localhost:5000/api/ai`

### Production Mode (Gunicorn)

```bash
# Single worker process
gunicorn -w 1 -b 0.0.0.0:5000 app:app

# Multiple workers (production recommended)
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Health Check

```bash
# Verify service is running
curl http://localhost:5000/api/ai
```

---

## API Reference

Base URL: `http://localhost:5000/api/ai`

### 1. Health Check Endpoint

Get service status, metrics, and diagnostics.

```http
POST /api/ai/health
Content-Type: application/json

{}
```

**Response** (200 OK):

```json
{
  "status": "healthy",
  "service": "Sentinel IQ AI Service",
  "cache_stats": {
    "hit_rate": 0.82,
    "total_requests": 156
  },
  "model_info": {
    "model": "llama-3.3-70b"
  },
  "uptime_seconds": 3661,
  "timestamp": "2026-05-05T10:30:45Z"
}
```

### 2. Query Endpoint (RAG)

Retrieve answers using Retrieval-Augmented Generation.

```http
POST /api/ai/query
Content-Type: application/json

{
  "question": "What are the main features?",
  "use_cache": true
}
```

**Response** (200 OK):

```json
{
  "status": "success",
  "question": "What are the main features?",
  "answer": "The main features include health monitoring, RAG-based Q&A, batch processing...",
  "sources": [
    {
      "document": "System Overview",
      "relevance": 0.95
    }
  ],
  "response_time_ms": 287,
  "timestamp": "2026-05-05T10:30:45Z"
}
```

### 3. Categorise Endpoint

Classify text into predefined categories.

```http
POST /api/ai/categorise
Content-Type: application/json

{
  "text": "The database is running slow",
  "use_cache": true
}
```

**Response** (200 OK):

```json
{
  "status": "success",
  "category": "Performance Issue",
  "confidence": 0.94,
  "related_categories": [
    {
      "name": "Infrastructure",
      "confidence": 0.08
    }
  ],
  "timestamp": "2026-05-05T10:30:45Z"
}
```

### 4. Describe Endpoint

Generate professional descriptions.

```http
POST /api/ai/describe
Content-Type: application/json

{
  "text": "Users can't login since the auth service went down"
}
```

**Response** (200 OK):

```json
{
  "status": "success",
  "title": "Authentication Service Outage",
  "description": "Complete loss of user authentication functionality...",
  "severity": "critical",
  "type": "incident",
  "key_points": ["Authentication service unavailable", "All users locked out"],
  "timestamp": "2026-05-05T10:30:45Z"
}
```

### 5. Recommend Endpoint

Generate actionable recommendations.

```http
POST /api/ai/recommend
Content-Type: application/json

{
  "context": "The system is experiencing high memory usage"
}
```

**Response** (200 OK):

```json
{
  "status": "success",
  "recommendations": [
    {
      "priority": "high",
      "action": "Implement memory pooling to reduce allocation overhead",
      "benefit": "Can reduce peak memory by 20-30%",
      "effort": "medium",
      "timeline_days": 3
    }
  ],
  "timestamp": "2026-05-05T10:30:45Z"
}
```

### 6. Report Endpoint (Streaming)

Generate structured reports with SSE streaming.

```http
POST /api/ai/report
Content-Type: application/json

{
  "title": "System Performance Analysis",
  "sections": ["Executive Summary", "Recommendations"]
}
```

**Response** (200 OK, Content-Type: text/event-stream):

```
data: {"type": "start", "title": "System Performance Analysis"}
data: {"type": "token", "content": "The"}
data: {"type": "token", "content": " system"}
...
data: {"type": "end", "metadata": {"total_tokens": 456}}
```

### 7. Analyse Endpoint

Perform deep document analysis.

```http
POST /api/ai/analyse
Content-Type: application/json

{
  "document": "2-hour outage due to database connection pool exhaustion"
}
```

**Response** (200 OK):

```json
{
  "status": "success",
  "insights": [
    {
      "type": "root_cause",
      "text": "Memory leak in database connection handling",
      "confidence": 0.96
    }
  ],
  "risks": [
    {
      "level": "critical",
      "description": "Memory leak will cause recurring failures",
      "mitigation": "Deploy code fix and implement monitoring"
    }
  ],
  "timestamp": "2026-05-05T10:30:45Z"
}
```

### 8. RAG Pipeline Endpoint

Manage documents for RAG system.

```http
POST /api/ai/rag/add-document
Content-Type: application/json

{
  "title": "User Guide",
  "content": "Welcome to Sentinel IQ...",
  "category": "documentation"
}
```

**Response** (201 Created):

```json
{
  "status": "success",
  "document": {
    "id": "doc_abc123",
    "title": "User Guide",
    "category": "documentation"
  }
}
```

### 9. Batch Process Endpoint

Process up to 20 items concurrently.

```http
POST /api/ai/batch-process
Content-Type: application/json

{
  "items": [
    {"text": "First item"},
    {"text": "Second item"},
    {"text": "Third item"}
  ]
}
```

**Response** (200 OK):

```json
{
  "status": "success",
  "total_items": 3,
  "processed": 3,
  "results": [
    {
      "id": 0,
      "text": "First item",
      "word_count": 2,
      "char_count": 10,
      "processed": true
    },
    {
      "id": 1,
      "text": "Second item",
      "word_count": 2,
      "char_count": 11,
      "processed": true
    },
    {
      "id": 2,
      "text": "Third item",
      "word_count": 2,
      "char_count": 10,
      "processed": true
    }
  ],
  "total_time": 0.324,
  "timestamp": "2026-05-05T10:30:45Z"
}
```

**Batch Status**:

```http
GET /api/ai/batch-process/status
```

**Response** (200 OK):

```json
{
  "status": "ready",
  "total_processed": 45,
  "total_batches": 15,
  "concurrent_workers": 5
}
```

---

## Development

### Project Structure

```
ai-service/
├── app.py                          # Flask entry point
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (not in git)
├── README.md                      # This file
├── routes/                        # AI endpoints (9 total)
│   ├── health.py                 # Health check
│   ├── query.py                  # RAG query
│   ├── categorise.py             # Text categorization
│   ├── describe.py               # Description generation
│   ├── recommend.py              # Recommendations
│   ├── report.py                 # Report generation
│   ├── analyse.py                # Document analysis
│   ├── rag.py                    # RAG pipeline
│   └── batch_process.py          # Batch processing
├── services/                      # Business logic
│   ├── groq_client.py            # Groq LLM client
│   ├── chroma_service.py         # Vector database
│   ├── cache_service.py          # Response caching
│   ├── batch_service.py          # Batch processor
│   └── report_service.py         # Report generation
├── prompts/                       # LLM prompt templates
│   ├── health_prompt.py
│   ├── query_prompt.py
│   ├── categorise_prompt.py
│   ├── describe_prompt.py
│   ├── recommend_prompt.py
│   ├── report_prompt.py
│   └── analyse_prompt.py
└── chroma_db/                     # Vector store (auto-created)
```

---

## Testing

### Run All Tests

```bash
# Run all tests
python -m pytest -v

# Run specific test file
python -m pytest test_batch_process.py -v

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

**Total Test Coverage**: 50+ pytest tests across all 9 endpoints

---

## Deployment

### Docker

```bash
docker build -t sentineliq-ai-service .
docker run -p 5000:5000 \
  -e GROQ_API_KEY=your_key \
  sentineliq-ai-service
```

### Production Checklist

- [ ] Set FLASK_ENV=production
- [ ] Configure valid GROQ_API_KEY
- [ ] Enable CACHE_ENABLED=true
- [ ] Use Gunicorn with 4+ workers
- [ ] Configure logging and monitoring
- [ ] Run full test suite successfully

---

## Architecture

### Technology Stack

| Component             | Version       | Purpose            |
| --------------------- | ------------- | ------------------ |
| Flask                 | 2.3.3         | REST API framework |
| Groq LLM              | Latest        | Text generation    |
| ChromaDB              | 0.3.21        | Vector search      |
| Sentence-Transformers | 2.2.2         | Embeddings         |
| ThreadPoolExecutor    | Python stdlib | Batch processing   |
| Pytest                | 7.4.3         | Unit testing       |
| Gunicorn              | 21.2.0        | Production server  |

### Performance

- **Health Check**: 50-100ms
- **Query (RAG)**: 300-800ms
- **Batch Processing**: 3-5x faster vs sequential (100-600ms for 20 items)
- **Caching Impact**: 50-70% latency reduction for cached responses

---

## Support

### Common Issues

| Issue                         | Solution                              |
| ----------------------------- | ------------------------------------- |
| GROQ_API_KEY not found        | Create .env file with valid key       |
| ChromaDB collection not found | First request auto-creates collection |
| Connection timeout            | Check internet, verify firewall       |
| Port 5000 in use              | Change AI_SERVICE_PORT in .env        |

---

**Last Updated**: May 5, 2026 | **Status**: Production Ready ✅

1. Create a new feature branch
2. Follow existing code style (PEP 8)
3. Add tests for new endpoints
4. Update README with new endpoints/config options

## License

Internal - Sentinel IQ

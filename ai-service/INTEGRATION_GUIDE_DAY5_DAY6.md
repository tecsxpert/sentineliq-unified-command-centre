# Integration Guide: RAG Pipeline + Report Generation

## Overview

Day 5 (RAG) + Day 6 (Report Generation) create a powerful system for document-based intelligent report generation.

## Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│           AI Service Flask App                  │
└─────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
    ┌────────┐    ┌──────────┐    ┌──────────┐
    │  RAG   │    │ Groq     │    │  Report  │
    │Service │    │ LLM API  │    │ Service  │
    └────────┘    └──────────┘    └──────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
    ┌─────────┐                   ┌──────────┐
    │ChromaDB │                   │REST API  │
    │(Vectors)│                   │Endpoints │
    └─────────┘                   └──────────┘
```

## Workflow: Document → Report

### Step 1: Upload Documents (Day 5 - RAG)

```python
# Request
POST /api/ai/rag/upload
{
  "file_paths": [
    "docs/user_guide.txt",
    "docs/api_spec.pdf",
    "docs/faq.docx"
  ],
  "metadata": {"category": "product_docs"}
}

# What happens:
1. Documents loaded (TXT/PDF/DOCX)
2. Text split into 500-char chunks with 50-char overlap
3. Embeddings generated (384-dim vectors)
4. Stored in ChromaDB with metadata
```

### Step 2: Generate Report (Day 6 - Report Generation)

```python
# Request
POST /api/ai/generate-report
{
  "topic": "Product Documentation Overview",
  "report_type": "general",
  "use_rag": true,
  "top_items_count": 5
}

# What happens:
1. ReportService receives request
2. RAG retrieves similar chunks: "retrieve: 'Product Documentation...'"
3. Groq LLM synthesizes:
   - Title (from topic + context)
   - Executive Summary (2-3 sentences)
   - Overview (3-4 paragraphs)
   - Top Items (5 findings)
   - Recommendations (actionable steps)
4. Returns structured JSON report
```

### Step 3: Use the Report

```python
# Access generated report
{
  "title": "Product Documentation Comprehensive Overview",
  "executive_summary": "...",
  "overview": "...",
  "top_items": [
    {
      "item_number": 1,
      "title": "API Endpoint Coverage",
      "description": "System documents 50+ REST API endpoints",
      "impact": "high",
      "priority": 1
    },
    ...
  ],
  "recommendations": [
    {
      "recommendation": "Create API v2 migration guide",
      "action": "1. Document breaking changes\n2. Provide examples\n3. Release timeline",
      "timeline": "short-term",
      "effort": "medium"
    },
    ...
  ]
}
```

## Use Cases

### Use Case 1: Knowledge Base Analysis

```python
# Scenario: Analyze company knowledge base

# Day 5: Upload all documentation
rag.add_documents([
  "docs/policies.docx",
  "docs/procedures.pdf",
  "docs/guidelines.txt"
])

# Day 6: Generate comprehensive analysis
report = report_service.generate_report(
  topic="Knowledge Base Organization",
  report_type="executive"
)
# Result: Executive summary with key findings and recommendations
```

### Use Case 2: On-Demand Reports

```python
# Scenario: Sales team needs quick competitive analysis

# Day 6: No RAG needed, just custom context
report = report_service.generate_report(
  topic="Competitor Landscape",
  use_rag=False,
  custom_context="Our competitors: A (pricing $X), B (pricing $Y), C (pricing $Z)"
)
# Result: Instant comparative analysis without document upload
```

### Use Case 3: Document Summarization

```python
# Scenario: Summarize specific PDF documents

# Day 5: Upload documents
rag.add_documents(["research_paper.pdf", "whitepaper.pdf"])

# Day 6: Generate summary report
report = report_service.generate_report(
  topic="Research Summary",
  use_rag=True  # Uses uploaded documents
)
# Result: Concise summary with key takeaways
```

### Use Case 4: Bulk Analysis

```python
# Scenario: Generate monthly reports on multiple topics

topics = [
  "Product Performance Metrics",
  "Customer Feedback Analysis",
  "Infrastructure Health",
  "Team Productivity Trends"
]

reports = []
for topic in topics:
  report = report_service.generate_report(topic)
  reports.append(report)
  # Save or process each report
```

### Use Case 5: Decision Support

```python
# Scenario: Compare three implementation options

comparison = report_service.generate_comparative_report(
  items_to_compare=[
    "Microservices Architecture",
    "Monolithic Architecture",
    "Serverless Architecture"
  ]
)
# Result: Structured comparison with pros/cons and recommendations
```

## API Request Examples

### Example 1: Basic Report with RAG

```bash
curl -X POST http://localhost:5000/api/ai/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Cloud Migration Strategy",
    "report_type": "technical"
  }'
```

### Example 2: Report Preview (Fast)

```bash
curl -X POST http://localhost:5000/api/ai/generate-report/preview \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Security Audit Results"
  }'
```

### Example 3: Comparative Report

```bash
curl -X POST http://localhost:5000/api/ai/generate-report/compare \
  -H "Content-Type: application/json" \
  -d '{
    "items": ["Framework A", "Framework B", "Framework C"]
  }'
```

### Example 4: Custom Context Report

```bash
curl -X POST http://localhost:5000/api/ai/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Q2 Business Review",
    "custom_context": "Revenue: $5M (+20% YoY), Customers: 500 (+100), Team: 25",
    "use_rag": false
  }'
```

## Configuration Reference

### RAG Configuration (Day 5)

```python
# services/rag_service.py

chunk_size = 500       # Characters per chunk
chunk_overlap = 50     # Character overlap
embedding_model = "all-MiniLM-L6-v2"  # 384-dimensional vectors
database = "ChromaDB"  # Vector storage
```

### Report Configuration (Day 6)

```python
# services/report_service.py

report_types = [
  "general",
  "technical",
  "executive",
  "comparative",
  "analysis"
]

top_items_count_default = 5
top_items_count_range = (1, 15)

timelines = ["immediate", "short-term", "long-term"]
effort_levels = ["low", "medium", "high"]
impact_levels = ["high", "medium", "low"]
```

## Performance Metrics

### RAG Pipeline (Day 5)

| Operation       | Time              | Notes                |
| --------------- | ----------------- | -------------------- |
| Document Upload | 2-3s per 100 docs | Embedding generation |
| Retrieval       | <100ms            | Vector search        |
| Storage         | ~1KB per chunk    | ChromaDB             |

### Report Generation (Day 6)

| Operation    | Time  | Tokens   |
| ------------ | ----- | -------- |
| Basic Report | 5-10s | 600-800  |
| With RAG     | 6-12s | 700-900  |
| Preview      | 3-5s  | 300-400  |
| Comparison   | 6-12s | 800-1200 |

## Data Flow Examples

### Flow 1: Enhanced Report with RAG Context

```
User Request:
└─→ Topic: "Infrastructure Optimization"
    └─→ use_rag: true

Report Service:
├─→ Call RAG: retrieve_documents("Infrastructure Optimization")
│   └─→ ChromaDB Vector Search
│       └─→ Returns 5 most similar chunks from uploaded docs
│
├─→ Call Groq LLM with:
│   ├─ Topic
│   ├─ Retrieved context (500-1000 chars)
│   └─ Report template
│
└─→ Generate sections:
    ├─ Title (from topic + context)
    ├─ Executive Summary (context-aware)
    ├─ Overview (expanded with details)
    ├─ Top Items (from context)
    └─ Recommendations (based on findings)

Result: Context-enriched report
```

### Flow 2: Fast Report without RAG

```
User Request:
└─→ Topic: "Q2 Results"
    └─→ use_rag: false

Report Service:
├─→ Skip RAG retrieval (saves 1-2 seconds)
│
├─→ Call Groq LLM with:
│   ├─ Topic only
│   └─ Report template
│
└─→ Generate sections:
    ├─ Title
    ├─ Executive Summary (generic)
    ├─ Overview (standard)
    ├─ Top Items (generated)
    └─ Recommendations

Result: Instant report (3-5 seconds total)
```

### Flow 3: Document-based Report

```
User Request:
└─→ context_documents: ["doc1", "doc2", "doc3"]

Report Service:
├─→ Skip RAG (using provided docs)
│
├─→ Call Groq LLM with:
│   ├─ Topic
│   ├─ Documents content
│   └─ Report template
│
└─→ Generate report from specific content

Result: Targeted report from specific sources
```

## Error Handling & Recovery

### Scenario 1: RAG Unavailable

```python
# If RAG service fails:
report_service.generate_report(
    topic="Topic",
    use_rag=False  # Falls back to generic report
)
# Returns report without context
```

### Scenario 2: Groq API Error

```python
# Service handles JSON parsing failures:
# - Fallback items generated
# - Recommendations provided
# - Report structure maintained
# Status: 200 (partial failure handled gracefully)
```

### Scenario 3: Invalid Parameters

```python
# Request validation happens first:
# - Missing topic: 400 Bad Request
# - Invalid report_type: 400
# - Invalid top_items_count: 400
# - Timeout: 500
```

## Integration Checklist

- [x] RAG Service deployed (Day 5)
- [x] ChromaDB initialized
- [x] Documents uploaded to RAG
- [x] Report Service deployed (Day 6)
- [x] Groq API key configured
- [x] Flask app integrated with both services
- [x] API endpoints registered
- [x] Tests passing
- [x] Documentation complete
- [x] Examples provided

## Production Deployment

### Environment Variables Required

```
GROQ_API_KEY=your_groq_api_key
FLASK_ENV=production
AI_SERVICE_PORT=5000
```

### Health Checks

```bash
# RAG Service
GET /api/ai/rag/health
→ Checks: ChromaDB connection, document count

# Report Service (via RAG health)
GET /api/ai/health
→ Overall service status
```

### Monitoring

- Track report generation times
- Monitor Groq API quota usage
- Log failed requests with context
- Alert on timeouts

## Scaling Considerations

### Horizontal Scaling

- Each instance maintains own RAG service
- Shared Groq API key
- Document sync required across instances

### Vertical Scaling

- Increase embedding batch size
- Optimize chunk size for your content
- Use faster embedding model if needed

### Optimization

- Cache frequently generated reports
- Implement queue for bulk operations
- Pre-warm embeddings for common queries

## Next Steps

1. **Upload Documents**

   ```bash
   POST /api/ai/rag/upload
   ```

2. **Test Report Generation**

   ```bash
   POST /api/ai/generate-report
   ```

3. **Explore Report Types**

   ```bash
   GET /api/ai/generate-report/types
   ```

4. **Build Custom Workflows**
   - Combine with existing services
   - Add caching layer
   - Implement scheduling

5. **Optimize Based on Usage**
   - Monitor performance
   - Adjust chunk sizes
   - Fine-tune parameters

---

## Summary

| Day      | Feature                        | Purpose                         | Key Output                       |
| -------- | ------------------------------ | ------------------------------- | -------------------------------- |
| 5        | RAG Pipeline                   | Document management & retrieval | Vector embeddings in ChromaDB    |
| 6        | Report Generation              | Intelligent synthesis           | Structured JSON reports          |
| Together | Document → Analysis → Insights | End-to-end intelligence         | Automatically generated analysis |

This integration provides a complete pipeline for converting documents into intelligent, actionable reports.

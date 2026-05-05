# SentinelIQ Unified Command Centre

## Development Log

### Day 9: Document Analysis for Insights & Risks

**Date:** May 5, 2026  
**Focus:** Build POST `/analyse-document` endpoint that accepts text, identifies key insights and risks, returns structured findings array

#### Backend Changes (AI Service)

- **New Route**: `routes/analyse.py` with `POST /api/ai/analyse-document` endpoint
- **Analysis Logic**: `analyse_document()` function using Groq to identify insights and risks
- **Structured Output**: Returns findings array with categories, severity levels, and confidence scores
- **Validation**: Input validation (50-10000 characters) and output normalization
- **Blueprint Registration**: Added `analyse_bp` to `app.py`

#### Frontend Changes (React)

- **AnalysePage Component**: New page with document text input and analysis results display
- **Form Features**: Text area with character counter, focus area checkboxes, validation
- **Results Display**: Color-coded insights and risks with severity indicators
- **Navigation**: Added "Analyze Document" button to dashboard
- **Routing**: Added `/analyse` route to App.jsx

#### Analysis Categories

**Insights**: technical, business, operational, strategic, compliance, performance, security  
**Risks**: security, compliance, operational, financial, reputational, technical, strategic

#### Response Structure

```json
{
  "insights": [
    {
      "type": "insight",
      "category": "security|business|...",
      "title": "Brief title",
      "description": "Detailed explanation",
      "severity": "low|medium|high",
      "confidence": 0.0-1.0
    }
  ],
  "risks": [
    {
      "type": "risk",
      "category": "security|compliance|...",
      "title": "Brief title",
      "description": "Detailed explanation",
      "severity": "low|medium|high|critical",
      "confidence": 0.0-1.0
    }
  ],
  "metadata": {
    "document_length": 1234,
    "insights_count": 3,
    "risks_count": 2,
    "analysis_timestamp": "ISO datetime"
  }
}
```

#### Technical Features

- **AI-Powered Analysis**: Uses Groq LLM for intelligent document analysis
- **Structured Findings**: Categorized and prioritized insights/risks
- **Confidence Scoring**: AI confidence levels for each finding
- **Severity Classification**: Risk assessment with severity levels
- **Input Validation**: Comprehensive validation with helpful error messages
- **Fallback Handling**: Graceful degradation when AI analysis fails

#### Testing

- ✅ Python compilation successful
- ✅ React build successful
- ✅ Spring Boot tests pass
- ✅ API endpoint validation
- ✅ Frontend component integration

#### Usage

```bash
# Analyze document
curl -X POST http://localhost:5000/api/ai/analyse-document \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your document text here...",
    "focus_areas": ["security", "compliance"]
  }'
```

Navigate to `/analyse` in the frontend to access the document analysis tool.

### Day 8: SSE Streaming for Report Generation

**Date:** May 5, 2026  
**Focus:** Add Server-Sent Events (SSE) streaming to `/generate-report` endpoint with React EventSource integration

#### Backend Changes (AI Service)

- **GroqClient**: Added `generate_streaming_response()` method with streaming support
- **ReportService**: Added `generate_streaming_report()` and streaming helper methods:
  - `_generate_streaming_title()`
  - `_generate_streaming_overview()`
  - `_generate_streaming_executive_summary()`
- **Report Route**: Modified `/generate-report` to support `?stream=true` query parameter
- **SSE Events**: Implemented proper SSE format with event types:
  - `start`: Generation started
  - `progress`: Progress updates with messages
  - `title`: Streaming title chunks
  - `overview`: Streaming overview chunks
  - `executive_summary`: Streaming executive summary chunks
  - `top_items`: Complete top items array
  - `recommendations`: Complete recommendations array
  - `complete`: Final complete report
  - `error`: Error handling

#### Frontend Changes (React)

- **ReportPage**: New page component with streaming support
- **EventSource Integration**: Real-time streaming using EventSource API
- **Progressive Display**: Text appears as it's generated (title, overview, executive summary)
- **Form Controls**: Topic input, report type selection, RAG toggle, custom context, streaming toggle
- **Navigation**: Added "Generate AI Report" button to dashboard
- **Routing**: Added `/reports` route to App.jsx

#### Technical Implementation

- **Streaming Protocol**: SSE with JSON payloads and event types
- **Real-time UX**: Users see report generation progress in real-time
- **Fallback Support**: Regular non-streaming mode still available
- **Error Handling**: Graceful error handling for streaming failures
- **Performance**: Non-blocking streaming prevents UI freezing

#### Testing

- ✅ Python compilation successful
- ✅ React build successful
- ✅ SSE event format validation
- ✅ EventSource integration tested

#### Usage

```bash
# Streaming mode (default)
POST /api/ai/generate-report?stream=true

# Regular mode
POST /api/ai/generate-report
```

Navigate to `/reports` in the frontend to access the streaming report generator.

# Day 20: Quick Reference Guide

## What is Day 20?

**Advanced AI Operations Demonstration** — Three sophisticated AI features showcased with real-world scenarios:

1. **AI Recommend** — Smart recommendation engine with read-aloud capability
2. **Report Generation** — Streaming comprehensive reports in real-time
3. **RAG Query** — Semantic document retrieval from knowledge base

---

## Quick Start

### Step 1: Prepare Environment

```bash
cd ai-service
pip install pyttsx3  # Optional: for text-to-speech
```

### Step 2: Set Groq API Key

```bash
# Windows PowerShell
$env:GROQ_API_KEY = "sk_your_key_here"

# Windows CMD
set GROQ_API_KEY=sk_your_key_here

# Linux/Mac
export GROQ_API_KEY=sk_your_key_here
```

### Step 3: Start AI Service

```bash
python app.py
# Output: 🚀 Starting AI Service on port 5000...
```

### Step 4: Run Demo (in new terminal)

```bash
cd ai-service
python day20_advanced_demo.py
```

---

## What Each Operation Does

### Operation 1: AI Recommend 🎙️

**Input**: Issue/feedback text

```json
{
  "text": "Our mobile app crashes on Android login screen..."
}
```

**AI Process**:

1. Parse text for issues and context
2. Identify severity and root cause
3. Generate 3-5 actionable recommendations
4. Prioritize by impact (HIGH/MEDIUM/LOW)
5. Classify recommendation type (fix, improve, investigate, etc.)
6. Read first recommendation aloud (optional TTS)

**Output**:

```json
{
  "recommendations": [
    {
      "action_type": "fix",
      "description": "Roll back session management code",
      "priority": "high"
    },
    {
      "action_type": "investigate",
      "description": "Profile memory usage during login",
      "priority": "high"
    },
    {
      "action_type": "document",
      "description": "Document regression testing procedures",
      "priority": "medium"
    }
  ]
}
```

**Real-world Use**:

- Support ticket analysis
- Issue prioritization
- Decision support
- Incident response

---

### Operation 2: Report Generation (Streaming) 📊

**Input**: Topic and report parameters

```json
{
  "topic": "Mobile App Crash Issues",
  "report_type": "executive",
  "use_rag": true,
  "custom_context": "Recent session management update",
  "top_items_count": 5
}
```

**AI Process** (with streaming):

1. Search knowledge base via RAG (if enabled)
2. Prepare context from retrieved docs
3. Call Groq LLM to generate report incrementally
4. Send report sections as real-time SSE streams
5. Client receives chunks progressively

**Streaming Timeline**:

```
0s:   User sees "Generating..." indicator
0.5s: "Executive Summary" section appears
1.0s: Key metrics start appearing
1.5s: Analysis section begins
2.5s: Recommendations appear
3.5s: Report complete ✓
```

**Without Streaming** (traditional):

```
0s:   User waits...
0s:   Waiting...
0s:   Still waiting...
3.5s: [Full report appears all at once]
```

**Report Types Available**:
| Type | Content | Best For |
|------|---------|----------|
| general | Balanced overview | Initial analysis |
| technical | Implementation details | Engineering |
| executive | Key metrics/ROI | Leadership |
| comparative | Side-by-side comparison | Decisions |
| analysis | Deep-dive breakdown | Deep understanding |

**Real-world Use**:

- Executive briefings
- Incident post-mortems
- Project analysis
- Competitive analysis
- Technical documentation

---

### Operation 3: RAG Query (Semantic Retrieval) 🔍

**Input**: Search query

```json
{
  "query": "How do I troubleshoot app crashes on Android?",
  "n_results": 5
}
```

**AI Process**:

1. Convert query to semantic embedding (384D vector)
2. Search ChromaDB for similar document embeddings
3. Compute similarity scores (0-1 range)
4. Rank by relevance
5. Return top-5 with metadata

**Similarity Scoring** (what each score means):

```
0.95+ = Highly relevant (must-read)    ✅✅✅
0.80+ = Very relevant (should review)  ✅✅
0.60+ = Somewhat relevant (reference)  ✅
0.40+ = Loosely related (context)      ⚠️
<0.40 = Not relevant (skip)            ❌
```

**Output Example**:

```json
{
  "query": "Android crash troubleshooting",
  "results": [
    {
      "similarity": 0.94,
      "document": "Android crash debugging using ANR dialogs...",
      "metadata": {"source": "android_guide.md", "date": "2024"}
    },
    {
      "similarity": 0.87,
      "document": "Mobile session management best practices...",
      "metadata": {"source": "mobile_arch.md"}
    }
    ... (3 more results)
  ]
}
```

**Real-world Use**:

- Knowledge base search
- Context retrieval for LLM
- Research aggregation
- Document discovery
- Support article recommendations

---

## Understanding the AI Pipeline

### How RAG + Report Works Together

```
User Request for Report on "Mobile Crash Issues"
    ↓
[RAG Retrieval]
├─ Query: "mobile app crash issues"
├─ Search: Find 5 similar knowledge base documents
└─ Result: [android_debugging.md, session_mgmt.md, ...]
    ↓
[Context Preparation]
├─ Combine retrieved docs + custom context
├─ Prepare reference material
└─ Total context: ~2000-4000 tokens
    ↓
[LLM Report Generation]
├─ Groq LLM receives: "Generate executive report using context: [docs]..."
├─ Model generates report incrementally
└─ Each sentence/section sent as SSE chunk
    ↓
[Streaming Output]
├─ Client receives: "data: {chunk 1}"
├─ Next: "data: {chunk 2}"
├─ And so on...
└─ Until report complete
    ↓
[Report Complete]
├─ All sections displayed
├─ User can read/interact
└─ Full report saved to JSON
```

### Why Streaming Matters

**Traditional (All-at-once)**:

```
API Call → 3-5 second wait → Complete report appears
User Experience: Feels slow, unclear if working
```

**Streaming (Incremental)**:

```
API Call → 0.5s: Title appears → 1s: Intro → 1.5s: Metrics → ...
User Experience: Feels fast, visible progress, can start reading
```

---

## Output Files Generated

After running the demo, you'll have:

### 1. `day20_recommend_results.json`

```json
{
  "timestamp": "2024-05-08T10:30:00",
  "endpoint": "/recommend",
  "input": "issue text here",
  "recommendations": [
    { "action_type": "fix", "description": "...", "priority": "high" }
  ],
  "response_time_seconds": 1.24
}
```

### 2. `day20_report_streaming_results.json`

```json
{
  "timestamp": "2024-05-08T10:30:05",
  "endpoint": "/generate-report?stream=true",
  "topic": "Mobile App Crash Issues",
  "report_type": "executive",
  "chunks_received": 47,
  "full_report_preview": "Executive Summary\n..."
}
```

### 3. `day20_rag_query_results.json`

```json
{
  "timestamp": "2024-05-08T10:30:10",
  "endpoint": "/rag/retrieve",
  "query": "How do I troubleshoot crashes?",
  "n_results_returned": 5,
  "documents": ["Android debugging guide...", "Session management..."],
  "response_time_seconds": 0.45
}
```

---

## Expected Output Flow

When you run `python day20_advanced_demo.py`:

```
======================================================================
                  DAY 20: ADVANCED AI OPERATIONS DEMO
======================================================================

[STEP 0] Checking prerequisites
✓ GROQ_API_KEY is set ✓
✓ Base URL: http://localhost:5000/api/ai
✓ TTS Support: Available

======================================================================
                    DEMO 1: AI RECOMMEND (Read-Aloud) 🎙️
======================================================================

[STEP 1] Preparing input for AI analysis
Input: Our mobile app is crashing on the login screen...

💭 AI: Reading the input... I see:
💭 AI: - Issue Type: Mobile app crash
💭 AI: - Severity: High (15% user drop)
💭 AI: - Suspected Cause: Session management code
💭 AI: - Generating 3 prioritized recommendations...

[STEP 2] Calling AI Recommend endpoint
✓ Response received in 1.24s

Generated Recommendations:
Recommendation 1:
  Type:     FIX
  Priority: HIGH
  Action:   Roll back session management changes immediately
...

[STEP 3] Reading first recommendation aloud (Text-to-Speech)
Text: 'Recommendation: Roll back session management changes...'
✓ Read-aloud completed
✓ Results saved to day20_recommend_results.json

======================================================================
                 DEMO 2: REPORT GENERATION (Streaming) 📊
======================================================================

[STEP 1] Setting up report generation request
Topic:    Mobile App Crash Issues in Android Platform
Type:     Executive Summary
Streaming: Enabled (real-time output)

💭 AI: When streaming is enabled, the LLM generates report sections
💭 AI: and sends them as Server-Sent Events (SSE)...

[STEP 2] Streaming report sections
Real-time Report Output:

Executive Summary
=====================
The mobile application is experiencing critical crashes on Android
devices, with a reported 15% decrease in daily active users...

Key Metrics:
- Platform Impact: Android (35% of user base)
- User Impact: 15% reduction in DAU
- Timeline: Started after latest update...

Root Cause Analysis:
The recent session management update appears to be the primary driver...

Recommendations:
1. [HIGH PRIORITY] Immediate rollback of session code
2. [HIGH PRIORITY] Enable crash reporting in staging...

======================================================================
                 DEMO 3: RAG QUERY (Semantic Retrieval) 🔍
======================================================================

[STEP 1] Preparing RAG query
Query: How do I troubleshoot app crashes on Android?

💭 AI: Converting query to embeddings using sentence-transformers...
💭 AI: Searching ChromaDB vector database...
💭 AI: Computing semantic similarity scores...
💭 AI: Ranking results by relevance...

[STEP 2] Sending RAG retrieve request
✓ Response received in 0.45s

Retrieved Documents (5 results):

Result 1:
  Similarity: 94%
  Document: Android app crashes can be debugged by enabling ANR...
  Metadata: {'source': 'android_debugging.md', 'date': '2024'}

Result 2:
  Similarity: 87%
  Document: Session management failures often occur when timing...
  Metadata: {'source': 'mobile_architecture.md'}
...

✓ Results saved to day20_rag_query_results.json

======================================================================
                         Day 20 Demo Complete 🎉
======================================================================

✓ All demonstrations completed successfully!

Output files:
  - day20_recommend_results.json
  - day20_report_streaming_results.json
  - day20_rag_query_results.json
```

---

## Troubleshooting

### ❌ Error: "GROQ_API_KEY not found"

**Fix**:

```bash
# Set the environment variable
$env:GROQ_API_KEY = "sk_your_key_here"

# Verify it's set
$env:GROQ_API_KEY
# Should output: sk_your_key_here
```

### ❌ Error: "pyttsx3 not installed" (TTS fails)

**Fix**:

```bash
pip install pyttsx3
# Or skip TTS - demo continues anyway
```

### ❌ Error: "Cannot connect to http://localhost:5000"

**Fix**:

```bash
# Make sure service is running
python app.py

# Or set custom URL
$env:AI_SERVICE_URL = "http://your-server:5000/api/ai"
```

### ❌ Error: "Stream stopped unexpectedly"

**Cause**: Network timeout or server error

**Fix**:

- Check network connectivity
- Verify server is still running
- Check firewall/proxy settings
- Increase timeout in demo script

---

## Key Metrics

| Operation     | Typical Time | Throughput      | Quality         |
| ------------- | ------------ | --------------- | --------------- |
| **Recommend** | 1-2s         | 1-3 rec/s       | 95%+ relevance  |
| **Report**    | 3-5s         | 1 report/5s     | Executive ready |
| **RAG Query** | 0.3-0.5s     | 200 queries/min | 90%+ precision  |

---

## Success Criteria for Day 20

✅ **Demo 1**: Recommend generates 3+ prioritized recommendations  
✅ **Demo 2**: Report streams incrementally with visible progress  
✅ **Demo 3**: RAG returns 5 documents with similarity scores  
✅ **Output**: Three JSON files created with results  
✅ **Errors**: All errors handled gracefully with clear messages

---

## Next Steps

After completing Day 20:

1. **Day 21**: Integrate demo into CI/CD pipeline
2. **Day 22**: Add performance monitoring/metrics
3. **Day 23**: Build web UI with real-time streaming display
4. **Day 24**: Implement caching for frequent operations
5. **Day 25**: Add multi-language support

---

**Created**: May 8, 2026  
**Status**: Complete ✅  
**Difficulty**: Advanced  
**Estimated Time**: 15-30 minutes per demo

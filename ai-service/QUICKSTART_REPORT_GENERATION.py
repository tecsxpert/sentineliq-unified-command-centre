"""
Quick Start: Report Generation API
Day 6 - Get Started in 5 Minutes
"""

# ==================== INSTALLATION ====================

"""
1. Install dependencies:
   pip install -r requirements.txt

2. Ensure GROQ_API_KEY environment variable is set:
   set GROQ_API_KEY=your_key_here  (Windows)
   export GROQ_API_KEY=your_key_here  (Linux/Mac)

3. Ensure RAG pipeline is initialized (loads documents):
   See DAY5_RAG_PIPELINE.md for RAG setup

4. Start the AI service:
   python app.py
"""

# ==================== BASIC USAGE - PYTHON ====================

# Option 1: Using the Service Directly
from services.report_service import get_report_service

service = get_report_service()

# Generate a simple report
report = service.generate_report(topic="Cloud Security")

# Access the report
print(f"Title: {report['title']}")
print(f"Summary: {report['executive_summary']}")
print(f"Items: {len(report['top_items'])}")
print(f"Recommendations: {len(report['recommendations'])}")


# Option 2: With Custom Parameters
report = service.generate_report(
    topic="DevOps Implementation",
    report_type="technical",
    top_items_count=8,
    use_rag=True
)


# ==================== BASIC USAGE - REST API ====================

# Using curl (Windows PowerShell)
"""
$body = @{
    topic = "System Architecture"
    report_type = "executive"
    top_items_count = 5
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

$response = Invoke-WebRequest `
    -Uri "http://localhost:5000/api/ai/generate-report" `
    -Method POST `
    -Body $body `
    -Headers $headers

$response.Content | ConvertFrom-Json | ConvertTo-Json
"""

# Or using Python requests:
import requests
import json

url = "http://localhost:5000/api/ai/generate-report"
payload = {
    "topic": "Machine Learning Pipeline",
    "report_type": "technical",
    "top_items_count": 5
}

response = requests.post(url, json=payload)
report = response.json()['data']

print(json.dumps(report['title'], indent=2))


# ==================== COMMON SCENARIOS ====================

# SCENARIO 1: Quick Report
print("📋 Scenario 1: Quick Report (1 minute)")
report = get_report_service().generate_report(
    topic="API Security",
    top_items_count=3  # Fewer items = faster
)
print(f"Generated: {report['title']}")


# SCENARIO 2: Executive Summary
print("\n📊 Scenario 2: Executive Report")
report = get_report_service().generate_report(
    topic="Q2 Performance Review",
    report_type="executive"
)
print(f"Executive Summary: {report['executive_summary']}")


# SCENARIO 3: Product Comparison
print("\n⚖️ Scenario 3: Comparison Report")
comparison = get_report_service().generate_comparative_report(
    items_to_compare=["PostgreSQL", "MongoDB", "DynamoDB"]
)
print(f"Comparing: {comparison['metadata']['topic']}")


# SCENARIO 4: Document-Based Analysis
print("\n📚 Scenario 4: From Specific Documents")
documents = [
    "Our system handles 1M requests per day with 99.9% uptime",
    "Infrastructure cost is $50k per month",
    "Current team size: 8 engineers"
]

report = get_report_service().generate_summarized_report(
    topic="Infrastructure Assessment",
    context_docs=documents
)
print(f"Generated: {report['title']}")


# SCENARIO 5: Without RAG (Faster)
print("\n⚡ Scenario 5: Fast Report (No RAG Context)")
report = get_report_service().generate_report(
    topic="Process Improvement",
    use_rag=False,  # Skip RAG retrieval
    top_items_count=3
)
print(f"Generated in ~3-5 seconds")


# ==================== API ENDPOINTS REFERENCE ====================

print("\n" + "="*60)
print("ENDPOINTS SUMMARY")
print("="*60)

endpoints = {
    "POST /api/ai/generate-report": {
        "Purpose": "Generate structured report",
        "Key Params": ["topic (required)", "report_type", "use_rag"],
        "Time": "5-10 seconds"
    },
    "GET /api/ai/generate-report/template": {
        "Purpose": "Get empty report structure",
        "Key Params": "None",
        "Time": "<100ms"
    },
    "GET /api/ai/generate-report/types": {
        "Purpose": "List supported report types",
        "Key Params": "None",
        "Time": "<100ms"
    },
    "POST /api/ai/generate-report/preview": {
        "Purpose": "Quick preview (3 items)",
        "Key Params": ["topic", "report_type"],
        "Time": "3-5 seconds"
    },
    "POST /api/ai/generate-report/compare": {
        "Purpose": "Comparative report",
        "Key Params": ["items (array, min 2)"],
        "Time": "5-10 seconds"
    }
}

for endpoint, info in endpoints.items():
    print(f"\n{endpoint}")
    for key, val in info.items():
        print(f"  {key}: {val}")


# ==================== RESPONSE STRUCTURE ====================

print("\n" + "="*60)
print("RESPONSE STRUCTURE")
print("="*60)

sample_response = {
    "status": "success",
    "data": {
        "title": "Cloud Security Best Practices",
        "executive_summary": "...(2-3 sentences)...",
        "overview": "...(3-4 paragraphs)...",
        "top_items": [
            {
                "item_number": 1,
                "title": "Multi-Factor Authentication",
                "description": "Implement MFA across systems",
                "impact": "high",
                "priority": 1
            }
        ],
        "recommendations": [
            {
                "recommendation": "Deploy MFA",
                "action": "1. Choose provider\n2. Configure\n3. Deploy",
                "timeline": "immediate",
                "effort": "medium"
            }
        ],
        "metadata": {
            "generated_at": "2026-05-05T10:30:00",
            "report_type": "general",
            "topic": "Cloud Security",
            "items_count": 5,
            "recommendations_count": 3,
            "context_used": "rag"
        }
    }
}

print("\nStructure shown above (truncated for brevity)")


# ==================== ERROR HANDLING ====================

print("\n" + "="*60)
print("ERROR HANDLING")
print("="*60)

def safe_generate_report(topic):
    """Generate report with error handling"""
    try:
        response = requests.post(
            "http://localhost:5000/api/ai/generate-report",
            json={"topic": topic},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['data']
        else:
            error_info = response.json()
            print(f"Error: {error_info['message']}")
            return None
            
    except requests.exceptions.Timeout:
        print("Request timeout - report generation took too long")
        return None
    except requests.exceptions.ConnectionError:
        print("Cannot connect to AI service - is it running?")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None


# Usage
report = safe_generate_report("Test Topic")


# ==================== BEST PRACTICES ====================

print("\n" + "="*60)
print("BEST PRACTICES")
print("="*60)

practice_tips = """
✓ Caching
  - Cache frequently generated reports
  - TTL: 1 hour for most topics
  
✓ Batch Processing
  - Generate multiple reports sequentially
  - Implement retry logic for failures

✓ Performance
  - Use preview endpoint for quick checks
  - Reduce top_items_count for speed
  - Set appropriate timeouts

✓ Context
  - Provide custom_context for domain-specific reports
  - Use RAG for knowledge base queries
  - Document-based for specific analysis

✓ Error Handling
  - Always wrap API calls in try/except
  - Check response status codes
  - Implement fallback strategies

✓ Integration
  - Use report outputs in dashboards
  - Export to PDF/HTML for sharing
  - Archive for compliance
  - Version control for tracking changes
"""

print(practice_tips)


# ==================== TROUBLESHOOTING ====================

print("\n" + "="*60)
print("TROUBLESHOOTING")
print("="*60)

troubleshooting = """
Problem: Report generation is slow
  ✓ Check Groq API status
  ✓ Use preview endpoint instead
  ✓ Reduce top_items_count
  ✓ Skip RAG context with use_rag=false

Problem: Getting JSON parsing errors
  ✓ Service has built-in fallback
  ✓ Reduce topic length/complexity
  ✓ Check GROQ_API_KEY is set correctly

Problem: Empty recommendations
  ✓ Provide custom_context
  ✓ Try different report_type
  ✓ Include RAG context

Problem: Connection refused
  ✓ Ensure Flask app is running
  ✓ Check port 5000 is not blocked
  ✓ Verify localhost is accessible

Problem: Timeout errors
  ✓ Increase timeout to 30+ seconds
  ✓ Check network connection
  ✓ Reduce top_items_count
"""

print(troubleshooting)


# ==================== NEXT STEPS ====================

print("\n" + "="*60)
print("NEXT STEPS")
print("="*60)

next_steps = """
1. Start the service:
   python app.py

2. Try a basic request:
   curl -X POST http://localhost:5000/api/ai/generate-report \\
     -H "Content-Type: application/json" \\
     -d '{"topic": "Your Topic"}'

3. Explore report types:
   curl http://localhost:5000/api/ai/generate-report/types

4. Check the documentation:
   - DAY6_REPORT_GENERATION.md (comprehensive)
   - REPORT_GENERATION_EXAMPLES.py (14 examples)

5. Run tests:
   pytest test_report_generation.py -v

6. Integrate into your application:
   - Use the API endpoints directly
   - Or use the Python service class
   - Add caching for frequently used reports

7. Customize and extend:
   - Add export to PDF
   - Implement email delivery
   - Build report scheduling
   - Create report templates
"""

print(next_steps)

if __name__ == "__main__":
    print("\n✅ Report Generation Service - Ready to Use!")
    print("📖 For more examples, see REPORT_GENERATION_EXAMPLES.py")
    print("📚 For full documentation, see DAY6_REPORT_GENERATION.md")

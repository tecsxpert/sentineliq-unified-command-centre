"""
Report Generation Usage Examples
Day 6 - Practical demonstrations
"""

# ==================== EXAMPLE 1: BASIC REPORT ====================

from services.report_service import get_report_service

# Initialize
report_service = get_report_service()

# Generate a simple report
report = report_service.generate_report(
    topic="Cloud Security Best Practices",
    report_type="general"
)

print("Generated Report:")
print(f"Title: {report['title']}")
print(f"Summary: {report['executive_summary']}")
print(f"Items: {len(report['top_items'])}")
print(f"Recommendations: {len(report['recommendations'])}")


# ==================== EXAMPLE 2: API USAGE ====================

import requests
import json

# Example: POST /generate-report
url = "http://localhost:5000/api/ai/generate-report"

payload = {
    "topic": "Machine Learning Implementation Strategy",
    "report_type": "technical",
    "use_rag": True,
    "top_items_count": 5
}

response = requests.post(url, json=payload)
report = response.json()['data']

print("\n📄 Report Generated via API:")
print(json.dumps({
    "title": report['title'],
    "items_count": len(report['top_items']),
    "recommendations": len(report['recommendations'])
}, indent=2))


# ==================== EXAMPLE 3: STRUCTURED REPORT ACCESS ====================

# Access each section
report = report_service.generate_report(
    topic="Data Privacy Compliance",
    report_type="executive"
)

# Executive Summary
print(f"\n=== EXECUTIVE SUMMARY ===")
print(report['executive_summary'])

# Overview
print(f"\n=== OVERVIEW ===")
print(report['overview'])

# Top Items with Details
print(f"\n=== TOP ITEMS ({len(report['top_items'])} items) ===")
for item in report['top_items']:
    print(f"\n{item['priority']}. {item['title']} [{item['impact'].upper()}]")
    print(f"   Description: {item['description']}")

# Recommendations with Actions
print(f"\n=== RECOMMENDATIONS ===")
for i, rec in enumerate(report['recommendations'], 1):
    print(f"\n{i}. {rec['recommendation']}")
    print(f"   Timeline: {rec['timeline']}")
    print(f"   Effort: {rec['effort']}")
    print(f"   Actions:\n{rec['action']}")

# Metadata
print(f"\n=== METADATA ===")
for key, value in report['metadata'].items():
    print(f"{key}: {value}")


# ==================== EXAMPLE 4: CUSTOM CONTEXT REPORT ====================

# Generate report with custom documentation
report = report_service.generate_report(
    topic="Product Documentation Review",
    custom_context="""
    Our product includes:
    - REST API with 50+ endpoints
    - WebSocket support for real-time updates
    - GraphQL interface
    - Mobile SDK for iOS/Android
    """,
    use_rag=False
)

print(f"\nReport with Custom Context:")
print(f"Title: {report['title']}")
print(f"Context Used: {report['metadata']['context_used']}")


# ==================== EXAMPLE 5: RAPID PREVIEW ====================

import requests

# Quick preview endpoint - faster response
preview_response = requests.post(
    "http://localhost:5000/api/ai/generate-report/preview",
    json={"topic": "Quick Analysis", "report_type": "general"}
)

preview = preview_response.json()['data']
print(f"\n⚡ Quick Preview Generated:")
print(f"  Items: {len(preview['top_items'])}")
print(f"  Recommendations: {len(preview['recommendations'])}")


# ==================== EXAMPLE 6: COMPARATIVE ANALYSIS ====================

# Generate comparison report
comparison_report = report_service.generate_comparative_report(
    items_to_compare=["Python", "Java", "Go", "Rust"]
)

print(f"\n📊 Comparative Report:")
print(f"Title: {comparison_report['title']}")
print(f"Comparing: {comparison_report['metadata']['topic']}")


# ==================== EXAMPLE 7: DOCUMENT-BASED REPORT ====================

# Generate report from specific documents
documents = [
    "Document 1: Features and capabilities...",
    "Document 2: Performance benchmarks...",
    "Document 3: User feedback and reviews..."
]

doc_report = report_service.generate_summarized_report(
    topic="Product Analysis",
    context_docs=documents
)

print(f"\n📚 Document-Based Report:")
print(f"Generated from {len(documents)} documents")
print(f"Title: {doc_report['title']}")


# ==================== EXAMPLE 8: REPORT TEMPLATES ====================

# Get report template structure
template = report_service.get_report_template()

print("\n🏗️ Report Template Structure:")
print(f"Fields: {list(template.keys())}")

# Populate template manually if needed
template['title'] = "Custom Report"
template['executive_summary'] = "..."
template['top_items'] = [
    {
        "item_number": 1,
        "title": "First Item",
        "description": "Description here",
        "impact": "high",
        "priority": 1
    }
]


# ==================== EXAMPLE 9: BATCH REPORT GENERATION ====================

# Generate multiple reports efficiently
topics = [
    "AI Implementation Strategy",
    "DevOps Best Practices",
    "Database Optimization",
    "Security Hardening"
]

reports = []
for topic in topics:
    report = report_service.generate_report(
        topic=topic,
        top_items_count=3
    )
    reports.append(report)
    print(f"✓ Generated: {report['title']}")

# Aggregate findings
all_items = []
for report in reports:
    all_items.extend(report['top_items'])

print(f"\n📈 Total Items Across All Reports: {len(all_items)}")


# ==================== EXAMPLE 10: API WITH ERROR HANDLING ====================

import requests
from requests.exceptions import RequestException

def generate_report_safely(topic, report_type="general"):
    """Generate report with error handling"""
    try:
        response = requests.post(
            "http://localhost:5000/api/ai/generate-report",
            json={
                "topic": topic,
                "report_type": report_type,
                "top_items_count": 5
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Error: {response.status_code} - {response.json().get('message')}")
            return None
            
    except RequestException as e:
        print(f"Connection error: {str(e)}")
        return None


# Usage
report = generate_report_safely("Enterprise Architecture")
if report:
    print(f"✓ Successfully generated: {report['title']}")
else:
    print("✗ Failed to generate report")


# ==================== EXAMPLE 11: EXPORT REPORT TO JSON ====================

import json
from datetime import datetime

def save_report_to_file(report, filename=None):
    """Save report to JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Report saved to {filename}")
    return filename


# Usage
report = report_service.generate_report("System Architecture")
save_report_to_file(report)


# ==================== EXAMPLE 12: PARSE REPORT SECTIONS ====================

def get_high_priority_items(report):
    """Extract high priority items"""
    return [item for item in report['top_items'] 
            if item['impact'] == 'high']

def get_immediate_actions(report):
    """Extract immediate actions"""
    return [rec for rec in report['recommendations'] 
            if rec['timeline'] == 'immediate']

def get_low_effort_recommendations(report):
    """Extract low effort recommendations"""
    return [rec for rec in report['recommendations'] 
            if rec['effort'] == 'low']

# Usage
report = report_service.generate_report("Process Optimization")
high_priority = get_high_priority_items(report)
immediate = get_immediate_actions(report)
easy_wins = get_low_effort_recommendations(report)

print(f"\n🎯 Analysis:")
print(f"  High Priority Items: {len(high_priority)}")
print(f"  Immediate Actions: {len(immediate)}")
print(f"  Low Effort Wins: {len(easy_wins)}")


# ==================== EXAMPLE 13: GET REPORT TYPES ====================

import requests

# Get supported report types
types_response = requests.get("http://localhost:5000/api/ai/generate-report/types")
report_types = types_response.json()['data']

print("\n📋 Supported Report Types:")
for report_type, description in report_types.items():
    print(f"  • {report_type}: {description}")


# ==================== EXAMPLE 14: PARAMETERS VALIDATION ====================

# Helper function to validate report parameters
def validate_report_params(topic, report_type, top_items_count):
    """Validate report generation parameters"""
    valid_types = ["general", "technical", "executive", "comparative", "analysis"]
    
    if not topic or not isinstance(topic, str):
        return False, "Topic must be a non-empty string"
    
    if report_type not in valid_types:
        return False, f"Report type must be one of: {valid_types}"
    
    if not isinstance(top_items_count, int) or top_items_count < 1 or top_items_count > 15:
        return False, "Top items count must be between 1 and 15"
    
    return True, "Parameters valid"

# Usage
valid, message = validate_report_params("Security Review", "technical", 5)
print(f"\n✓ Validation: {message}" if valid else f"\n✗ Validation: {message}")


# ==================== PERFORMANCE TIPS ====================

"""
Performance Optimization Tips:

1. Use RAG Strategically:
   - use_rag=True for knowledge base queries
   - use_rag=False for faster reports with custom context

2. Adjust Item Counts:
   - Fewer items (3) for quick reports
   - More items (10) for comprehensive analysis

3. Caching:
   - Cache frequently generated reports
   - Reuse comparisons when possible

4. Batch Processing:
   - Generate multiple reports in sequence
   - Process results together for aggregation

5. Error Handling:
   - Set appropriate timeouts (30s default)
   - Implement retry logic for failed requests
   - Validate parameters before sending

6. Memory Management:
   - Stream large reports if needed
   - Export to file for archival
   - Cleanup old reports periodically
"""

# ==================== USE CASES ====================

"""
Real-World Use Cases:

1. Executive Summaries:
   - Daily strategic reports
   - Board meeting materials
   - Decision support documents

2. Technical Analysis:
   - Architecture reviews
   - Performance analysis
   - Security audits

3. Comparative Studies:
   - Product comparisons
   - Vendor evaluation
   - Technology assessment

4. Compliance Reporting:
   - Audit trail documentation
   - Regulatory compliance reports
   - Risk assessment documents

5. Knowledge Base:
   - FAQ generation
   - Documentation summaries
   - Learning materials

6. Decision Making:
   - Pro/con analysis
   - Option evaluation
   - Risk analysis
"""

if __name__ == "__main__":
    print("✓ Report Generation Examples - Ready to use")

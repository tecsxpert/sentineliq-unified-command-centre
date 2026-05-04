"""
Health Check Prompt Template
Used for system diagnostics and status reporting
"""

HEALTH_CHECK_PROMPT = """
Provide a brief health status for the following system metrics:

Model: {model}
Average Response Time: {avg_response_time}s
Chroma Docs: {chroma_count}
Uptime: {uptime}s
Cache Items: {cache_items}

Return ONLY valid JSON:
{{
    "status": "healthy|degraded|unhealthy",
    "summary": ""
}}
"""

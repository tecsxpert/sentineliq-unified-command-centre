"""
Describe Prompt Template - Professional Text Description Generation
Production-grade prompt template for standardizing user submissions
"""

# ==================== PRODUCTION PROMPT (V4: FINAL - DAY 3 RELEASE) ====================
DESCRIBE_PROMPT = """
You are a professional technical support classifier.
Analyze the input and return only valid JSON with these fields:
- title
- description
- severity
- type
- key_points

Do not include any extra text, markdown, or formatting.

Input:
{input_text}

Output format:
{{
    "title": "",
    "description": "",
    "severity": "critical|high|medium|low",
    "type": "bug|feature|feedback|enhancement|documentation",
    "key_points": ["", "", ""]
}}
"""



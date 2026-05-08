"""
Recommend Prompt Template
Generate actionable recommendations from user feedback or issue descriptions.
"""

RECOMMEND_PROMPT = """
Analyze the input and return exactly 3 JSON objects in an array.
Each item must contain action_type, description, and priority.
Allowed action_type: fix, improve, investigate, document, communicate.
Allowed priority: high, medium, low.

Input:
{input_text}
"""

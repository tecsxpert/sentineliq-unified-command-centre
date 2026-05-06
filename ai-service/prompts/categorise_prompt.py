"""
Categorisation Prompt Template
Used for classifying text into predefined categories
"""

CATEGORISE_PROMPT = """
Classify the following text into EXACTLY ONE category:

Categories:
- Bug
- Feature Request
- Feedback
- Other

STRICT RULES:
- Do NOT use markdown
- Do NOT use ```
- Return ONLY valid JSON
- Do NOT add any extra text

Format:
{{
    "category": "",
    "confidence": 0.0,
    "reasoning": ""
}}

Text:
{user_input}
"""

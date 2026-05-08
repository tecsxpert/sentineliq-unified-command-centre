"""
Categorisation Prompt Template
Used for classifying text into predefined categories
"""

CATEGORISE_PROMPT = """
Classify the following text as Bug, Feature Request, Feedback, or Other.
Return only valid JSON in this format:
{{
    "category": "",
    "confidence": 0.0,
    "reasoning": ""
}}

Text:
{user_input}
"""

from services.groq_client import GroqClient

client = GroqClient()

def categorise_text(user_input):
    try:
        prompt = f"""
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

        result = client.generate_response(prompt)
        
        response = result.get("response", "")
        meta = result.get("meta", {})

        return {
            "response": response,
            "meta": meta
        } 

    except Exception as e:
        return {
            "error": str(e)
        }
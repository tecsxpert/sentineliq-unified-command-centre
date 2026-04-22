from services.groq_client import GroqClient

client = GroqClient()

def categorise_text(user_input):
    try:
        prompt = f"""
        Classify the following text into one of these categories:
        Bug, Feature Request, Feedback, Other.

        Also provide:
        - confidence (between 0 and 1)
        - reasoning

        Return ONLY in this JSON format:
        {{
            "category": "",
            "confidence": 0.0,
            "reasoning": ""
        }}

        Text:
        {user_input}
        """

        response = client.generate_response(prompt)

        return response

    except Exception as e:
        return {
            "error": str(e)
        }
import os
import time
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GroqClient:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)

    def generate_response(self, prompt):
        retries = 3

        for attempt in range(retries):
            try:
                start_time = time.time()

                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                end_time = time.time()

                return {
                    "response": response.choices[0].message.content,
                    "meta": {
                        "is_fallback": False,
                        "response_time_ms": round((end_time - start_time) * 1000, 2)
                    }
                }

            except Exception as e:
                print(f"Error: {e}")

                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    # Fallback response
                    return {
                        "response": "Sorry, the system is currently busy. Please try again later.",
                        "meta": {
                            "is_fallback": True,
                            "error": str(e)
                        }
                    }
import os
import time
from groq import Groq
from dotenv import load_dotenv
from routes.health import record_response_time
from services.cache_service import get_cache, set_cache

load_dotenv()


class GroqClient:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)

    def generate_response(self, prompt, use_cache=True):
        retries = 3

        # STEP 1: Check cache
        if use_cache:
            cached = get_cache(prompt)
            if cached:
                return {
                    "response": cached,
                    "meta": {
                        "confidence": 0.9,
                        "model_used": "llama-3.3-70b-versatile",
                        "tokens_used": 0,
                        "response_time_ms": 0,
                        "cached": True
                    }
                }

        # STEP 2: Call Groq
        for attempt in range(retries):
            try:
                start_time = time.time()

                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )

                end_time = time.time()

                duration = (end_time - start_time) * 1000

                record_response_time(end_time - start_time)

                result = response.choices[0].message.content

                # STEP 3: Store in cache
                if use_cache:
                    set_cache(prompt, result)

                return {
                    "response": result,
                    "meta": {
                        "confidence": 0.9,
                        "model_used": "llama-3.3-70b-versatile",
                        "tokens_used": len(prompt.split()),
                        "response_time_ms": round(duration, 2),
                        "cached": False
                    }
                }

            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    return {"error": str(e)}
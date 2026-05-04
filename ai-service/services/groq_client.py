import os
import time
from groq import Groq
from dotenv import load_dotenv
from routes.health import record_response_time
from services.cache_service import get_cache, set_cache

# Load env
load_dotenv()


class GroqClient:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def generate_response(self, prompt, use_cache=True):
        if not self.api_key:
            return f"[MOCK RESPONSE] Since GROQ_API_KEY is missing, here is a placeholder for: {prompt[:50]}...", False

        retries = 3

        # 🔥 STEP 1: Check cache
        if use_cache:
            cached = get_cache(prompt)
            if cached:
                return cached, True

        # 🔥 STEP 2: Call Groq if not cached
        for attempt in range(retries):
            try:
                start_time = time.time()

                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )

                end_time = time.time()

                record_response_time(end_time - start_time)

                result = response.choices[0].message.content

                # 🔥 STEP 3: Store in cache
                if use_cache:
                    set_cache(prompt, result)

                return result, False

            except Exception as e:
                print(f"Error: {e}")

                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(2)
                else:
                    return "Error: Unable to get response", False
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
        self.client = Groq(api_key=self.api_key)

    def generate_response(self, prompt, use_cache=True):
        retries = 3

        # 🔥 STEP 1: Check cache
        if use_cache:
            cached = get_cache(prompt)
            if cached:
                return cached

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

                return result

            except Exception as e:
                print(f"Error generating response: {e}")
                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(2)
                else:
                    return "Error: Unable to generate response"

    def generate_streaming_response(self, prompt, use_cache=True):
        """
        Generate streaming response from Groq API
        Yields chunks of text as they arrive
        """
        retries = 3

        # 🔥 STEP 1: Check cache (for streaming, we'll return cached content as single chunk)
        if use_cache:
            cached = get_cache(prompt)
            if cached:
                yield cached
                return

        # 🔥 STEP 2: Call Groq with streaming
        for attempt in range(retries):
            try:
                start_time = time.time()

                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True  # Enable streaming
                )

                full_content = ""
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        full_content += content
                        yield content

                end_time = time.time()
                record_response_time(end_time - start_time)

                # 🔥 STEP 3: Store in cache
                if use_cache:
                    set_cache(prompt, full_content)

            except Exception as e:
                print(f"Streaming error: {e}")
                if attempt < retries - 1:
                    print("Retrying streaming...")
                    time.sleep(2)
                else:
                    yield "Error: Unable to get streaming response"
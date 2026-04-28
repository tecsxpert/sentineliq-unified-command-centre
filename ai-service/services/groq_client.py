import os
import time
from groq import Groq
from dotenv import load_dotenv
from routes.health import record_response_time

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
                start_time = time.time()  # start timer

                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                end_time = time.time()  # end timer

                # record response time
                record_response_time(end_time - start_time)

                return response.choices[0].message.content

            except Exception as e:
                print(f"Error: {e}")

                if attempt < retries - 1:
                    print("Retrying...")
                    time.sleep(2)  # wait before retry
                else:
                    return "Error: Unable to get response from AI"
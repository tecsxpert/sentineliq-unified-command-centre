from services.groq_client import GroqClient

client = GroqClient()

response = client.generate_response("Explain machine learning in simple terms")

print(response)
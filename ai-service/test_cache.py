from services.groq_client import GroqClient
from services.cache_service import get_cache_stats

client = GroqClient()

prompt = "App crashes when login"

print("First call (MISS):")
print(client.generate_response(prompt))

print("\nSecond call (HIT):")
print(client.generate_response(prompt))

print("\nThird call (SKIP CACHE):")
print(client.generate_response(prompt, use_cache=False))

print("\nCache Stats:")
print(get_cache_stats())
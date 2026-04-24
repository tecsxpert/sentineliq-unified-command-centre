from services.chroma_service import add_data
from routes.query import query_with_context

# Add data (important)
add_data()

# Ask question
question = "Why is my app crashing?"

result = query_with_context(question)

print(result)
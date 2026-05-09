from routes.health import get_health
from routes.query import query_with_context
from services.chroma_service import add_data

# Load DB
add_data()

# Call query to generate response time
query_with_context("App crashes when login")

# Now check health
result = get_health()
print(result)
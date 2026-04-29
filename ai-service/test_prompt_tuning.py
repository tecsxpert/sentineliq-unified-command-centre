from routes.categorise import categorise_text
from routes.query import query_with_context
from services.chroma_service import add_data

# Load DB data
add_data()

# 10 test inputs
inputs = [
    "App crashes when login",
    "Add dark mode feature",
    "UI looks very nice",
    "App is slow and laggy",
    "Feature request for notifications",
    "Login page not working",
    "Improve dashboard design",
    "App freezes sometimes",
    "Add multi-language support",
    "Performance is very bad"
]

print("\n===== CATEGORY TEST =====")

for text in inputs:
    result = categorise_text(text)
    print("\nInput:", text)
    print("Output:", result)

print("\n===== QUERY TEST =====")

for text in inputs:
    result = query_with_context(text)
    print("\nQuestion:", text)
    print("Output:", result)
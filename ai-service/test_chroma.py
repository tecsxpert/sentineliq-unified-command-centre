from services.chroma_service import add_data, query_data

# Step 1: Add data
add_data()

# Step 2: Query similar text
result = query_data("App crashing issue")

print(result)
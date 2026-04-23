import chromadb

# Create persistent database (saved locally)
client = chromadb.Client()

# Create or get collection
collection = client.get_or_create_collection(name="test_collection")

def add_data():
    collection.add(
        documents=[
            "The app crashes when I login",
            "The UI looks clean and modern",
            "Feature request: add dark mode"
        ],
        ids=["1", "2", "3"]
    )

def query_data(query_text):
    results = collection.query(
        query_texts=[query_text],
        n_results=1
    )
    return results
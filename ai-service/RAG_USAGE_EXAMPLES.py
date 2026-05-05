"""
Quick Start Examples for RAG Pipeline
Day 5 - Practical usage demonstrations
"""

# ==================== EXAMPLE 1: BASIC USAGE ====================

from services.rag_service import get_rag_service

# Initialize RAG service (singleton)
rag = get_rag_service()

# Load and process documents
stats = rag.add_documents([
    "support_docs/faq.txt",
    "support_docs/installation_guide.pdf"
])

print(f"✓ Loaded {stats['documents_loaded']} documents")
print(f"✓ Created {stats['chunks_created']} chunks")
print(f"✓ Generated embeddings for {stats['chunks_embedded']} chunks")


# ==================== EXAMPLE 2: SEMANTIC SEARCH ====================

# Retrieve relevant documents based on query
query = "How do I install the software?"
results = rag.retrieve_documents(query, n_results=5)

print(f"\nQuery: {query}")
print("Top Results:")
for i, (doc, doc_id, distance, metadata) in enumerate(zip(
    results['results']['documents'],
    results['results']['ids'],
    results['results']['distances'],
    results['results']['metadatas']
)):
    relevance = 1 - distance  # Convert distance to similarity (0-1)
    print(f"\n{i+1}. Relevance: {relevance:.2%}")
    print(f"   Document ID: {doc_id}")
    print(f"   Source: {metadata.get('source', 'unknown')}")
    print(f"   Preview: {doc[:150]}...")


# ==================== EXAMPLE 3: BATCH OPERATIONS ====================

# Add multiple documents with metadata
import os

docs_dir = "knowledge_base/"
doc_files = [
    os.path.join(docs_dir, f)
    for f in os.listdir(docs_dir)
    if f.endswith(('.txt', '.pdf', '.docx'))
]

metadata = {
    "knowledge_base": "product_docs",
    "version": "2.0",
    "language": "en"
}

stats = rag.add_documents(doc_files, metadata=metadata)
print(f"Batch upload complete: {stats['documents_loaded']} documents processed")


# ==================== EXAMPLE 4: COLLECTION MANAGEMENT ====================

# Get collection statistics
stats = rag.get_collection_stats()
print(f"\nCollection Statistics:")
print(f"  Name: {stats['collection_name']}")
print(f"  Total Chunks: {stats['document_count']}")
print(f"  Embedding Model: {stats['embedding_model']}")
print(f"  Chunk Config: {stats['chunk_size']} chars, {stats['chunk_overlap']} overlap")


# ==================== EXAMPLE 5: EXPORT FOR BACKUP ====================

# Export collection to JSON
rag.export_collection("backup_$(datetime).json")
print("✓ Collection exported for backup")


# ==================== EXAMPLE 6: RAG WITH GROQ LLM ====================

from services.groq_client import GroqClient
from config import GROQ_API_KEY

# Retrieve context
context_results = rag.retrieve_documents("How does authentication work?", n_results=3)
context = "\n\n".join(context_results['results']['documents'])

# Use context with LLM
groq_client = GroqClient(api_key=GROQ_API_KEY)
prompt = f"""Based on the following documentation, answer the question:

Documentation:
{context}

Question: How does authentication work?
"""

response = groq_client.chat(prompt)
print(f"\nAI Response with RAG Context:\n{response}")


# ==================== EXAMPLE 7: ADVANCED QUERYING ====================

# Different query types
queries = [
    "troubleshooting common errors",
    "API rate limits",
    "database configuration",
    "security best practices"
]

for query in queries:
    results = rag.retrieve_documents(query, n_results=1)
    if results['results']['documents']:
        best_match = results['results']['documents'][0]
        relevance = 1 - results['results']['distances'][0]
        print(f"\n'{query}' → Relevance: {relevance:.1%}")


# ==================== EXAMPLE 8: CLEAR AND RESET ====================

# Clear all documents and start fresh
rag.delete_all_documents()
print("✓ Collection cleared")

# Verify it's empty
stats = rag.get_collection_stats()
assert stats['document_count'] == 0
print("✓ Verified: Collection is empty")


# ==================== EXAMPLE 9: PROGRAMMATIC WORKFLOW ====================

def setup_rag_pipeline(doc_files: list, collection_name: str = "rag_documents"):
    """Setup complete RAG pipeline"""
    # Initialize service
    rag = get_rag_service(collection_name)
    
    # Clear any existing data
    rag.delete_all_documents()
    
    # Load documents
    stats = rag.add_documents(doc_files)
    
    # Export initial state
    rag.export_collection(f"{collection_name}_init.json")
    
    # Verify
    final_stats = rag.get_collection_stats()
    print(f"✓ RAG Pipeline Ready")
    print(f"  Documents: {final_stats['document_count']} chunks")
    print(f"  Model: {final_stats['embedding_model']}")
    
    return rag


def query_rag_pipeline(rag, query: str, top_k: int = 3):
    """Query the RAG pipeline and format results"""
    results = rag.retrieve_documents(query, n_results=top_k)
    
    formatted = {
        "query": query,
        "results": []
    }
    
    for doc, doc_id, distance, metadata in zip(
        results['results']['documents'],
        results['results']['ids'],
        results['results']['distances'],
        results['results']['metadatas']
    ):
        formatted["results"].append({
            "relevance": round(1 - distance, 3),
            "source": metadata.get('source'),
            "preview": doc[:200]
        })
    
    return formatted


# Usage
if __name__ == "__main__":
    # Setup
    rag = setup_rag_pipeline([
        "docs/guide.txt",
        "docs/api_reference.pdf",
        "docs/faq.docx"
    ])
    
    # Query
    result = query_rag_pipeline(rag, "How to get started?", top_k=5)
    print("\nQuery Result:")
    print(f"Query: {result['query']}")
    for i, r in enumerate(result['results'], 1):
        print(f"  {i}. ({r['relevance']:.1%}) {r['source']}")


# ==================== EXAMPLE 10: ERROR HANDLING ====================

def safe_rag_retrieve(rag, query: str, max_retries: int = 1):
    """Safe retrieval with error handling"""
    try:
        results = rag.retrieve_documents(query, n_results=5)
        if not results['results']['documents']:
            print(f"⚠ No results found for: {query}")
            return None
        return results
    except Exception as e:
        print(f"✗ Error during retrieval: {str(e)}")
        return None


# ==================== NOTES ====================
"""
Performance Tips:
1. Use batch processing for multiple documents
2. Cache frequent queries
3. Adjust chunk_size based on document type
4. Use appropriate embedding model for your domain
5. Export regularly for backup

Customization:
- Change chunk_size/overlap for different content types
- Use domain-specific embedding models
- Add custom metadata for filtering
- Implement caching layer for production

Integration:
- Use with Describe service for enhanced summaries
- Combine with Groq for few-shot learning
- Add to Query service for similarity search
- Implement in Recommend service for context
"""

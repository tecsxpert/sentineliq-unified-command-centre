"""
Comprehensive RAG Pipeline Tests
Test document loading, chunking, embedding, and retrieval
"""
import pytest
import os
import tempfile
from pathlib import Path
from services.rag_service import RAGService, get_rag_service


class TestRAGService:
    """Test RAG Service functionality"""
    
    @pytest.fixture
    def rag_service(self):
        """Create a test RAG service"""
        service = RAGService(collection_name="test_rag_collection")
        yield service
        # Cleanup
        service.delete_all_documents()
    
    @pytest.fixture
    def sample_text_file(self):
        """Create a sample text file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            content = """
            Sentiment Analysis in NLP:
            Sentiment analysis is the process of determining the emotional tone or sentiment 
            expressed in a piece of text. It's a crucial Natural Language Processing (NLP) task 
            used extensively in business intelligence, social media monitoring, product reviews, 
            and customer feedback analysis.
            
            Common approaches include:
            1. Lexicon-based methods using sentiment dictionaries
            2. Machine learning classifiers trained on labeled data
            3. Deep learning models like transformer networks
            4. Hybrid approaches combining multiple techniques
            
            Applications of sentiment analysis span many domains including brand monitoring, 
            customer support, market research, and political opinion tracking.
            """
            f.write(content)
            return f.name
    
    @pytest.fixture
    def sample_docs_dir(self):
        """Create sample documents directory"""
        temp_dir = tempfile.mkdtemp()
        
        # Create multiple text files
        for i in range(3):
            file_path = os.path.join(temp_dir, f"doc_{i}.txt")
            with open(file_path, 'w') as f:
                f.write(f"Document {i}: This is sample content for testing RAG pipeline. " * 20)
        
        yield temp_dir
        
        # Cleanup
        for file_path in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file_path))
        os.rmdir(temp_dir)
    
    # ==================== TEXT LOADING TESTS ====================
    
    def test_load_text_file(self, rag_service, sample_text_file):
        """Test loading text file"""
        text = rag_service.load_text_file(sample_text_file)
        assert isinstance(text, str)
        assert len(text) > 0
        assert "Sentiment Analysis" in text
    
    def test_load_nonexistent_file(self, rag_service):
        """Test loading non-existent file"""
        with pytest.raises(FileNotFoundError):
            rag_service.load_text_file("/nonexistent/path/file.txt")
    
    def test_load_document_txt(self, rag_service, sample_text_file):
        """Test load_document with txt file"""
        text = rag_service.load_document(sample_text_file)
        assert isinstance(text, str)
        assert len(text) > 0
    
    # ==================== CHUNKING TESTS ====================
    
    def test_chunk_text_default_params(self, rag_service):
        """Test text chunking with default parameters"""
        text = "A" * 1000  # 1000 char string
        chunks = rag_service.chunk_text(text)
        
        assert len(chunks) > 1
        # First chunk should be 500 chars
        assert len(chunks[0]) == 500
        # Overlap between chunks
        assert chunks[1][:50] == chunks[0][-50:]
    
    def test_chunk_text_custom_params(self, rag_service):
        """Test text chunking with custom parameters"""
        text = "B" * 500
        chunks = rag_service.chunk_text(text, chunk_size=100, overlap=20)
        
        assert len(chunks) > 1
        assert len(chunks[0]) == 100
    
    def test_chunk_text_overlap(self, rag_service):
        """Test that chunks have proper overlap"""
        text = "0123456789" * 100  # 1000 chars
        chunks = rag_service.chunk_text(text, chunk_size=200, overlap=50)
        
        # Check overlap between consecutive chunks
        for i in range(len(chunks) - 1):
            assert chunks[i+1][:50] == chunks[i][-50:]
    
    def test_chunk_small_text(self, rag_service):
        """Test chunking text smaller than chunk size"""
        text = "Small text"
        chunks = rag_service.chunk_text(text, chunk_size=100, overlap=10)
        
        assert len(chunks) == 1
        assert chunks[0] == text
    
    # ==================== EMBEDDING TESTS ====================
    
    def test_embed_single_text(self, rag_service):
        """Test embedding a single text"""
        text = "This is a test sentence for embedding"
        embedding = rag_service.embed_text(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) == 384  # all-MiniLM-L6-v2 produces 384-dim vectors
        assert all(isinstance(x, float) for x in embedding)
    
    def test_embed_multiple_texts(self, rag_service):
        """Test embedding multiple texts"""
        texts = [
            "First test sentence",
            "Second test sentence",
            "Third test sentence"
        ]
        embeddings = rag_service.embed_texts(texts)
        
        assert len(embeddings) == 3
        assert all(isinstance(e, list) for e in embeddings)
        assert all(len(e) == 384 for e in embeddings)
    
    def test_embedding_semantic_similarity(self, rag_service):
        """Test that similar texts have similar embeddings"""
        from scipy.spatial.distance import cosine
        
        text1 = "The cat sat on the mat"
        text2 = "The dog sat on the floor"
        text3 = "Machine learning is fascinating"
        
        emb1 = rag_service.embed_text(text1)
        emb2 = rag_service.embed_text(text2)
        emb3 = rag_service.embed_text(text3)
        
        # Similar texts should have lower distance
        dist_1_2 = cosine(emb1, emb2)
        dist_1_3 = cosine(emb1, emb3)
        
        assert dist_1_2 < dist_1_3  # First pair should be more similar
    
    # ==================== DOCUMENT STORAGE TESTS ====================
    
    def test_add_single_document(self, rag_service, sample_text_file):
        """Test adding a single document"""
        stats = rag_service.add_documents([sample_text_file])
        
        assert stats['documents_loaded'] == 1
        assert stats['chunks_created'] > 0
        assert stats['chunks_embedded'] > 0
        assert stats['documents_loaded'] == stats['chunks_embedded']
    
    def test_add_multiple_documents(self, rag_service, sample_docs_dir):
        """Test adding multiple documents"""
        doc_paths = [
            os.path.join(sample_docs_dir, f"doc_{i}.txt")
            for i in range(3)
        ]
        
        stats = rag_service.add_documents(doc_paths)
        
        assert stats['documents_loaded'] == 3
        assert stats['chunks_created'] > 0
        assert stats['chunks_embedded'] > 0
    
    def test_add_documents_with_metadata(self, rag_service, sample_text_file):
        """Test adding documents with metadata"""
        metadata = {
            "category": "test",
            "author": "test_user",
            "version": "1.0"
        }
        
        stats = rag_service.add_documents([sample_text_file], metadata)
        assert stats['documents_loaded'] == 1
        
        # Verify metadata is stored
        results = rag_service.collection.get()
        for meta in results['metadatas']:
            assert meta['category'] == "test"
            assert meta['author'] == "test_user"
    
    # ==================== RETRIEVAL TESTS ====================
    
    def test_retrieve_documents(self, rag_service, sample_text_file):
        """Test retrieving documents"""
        rag_service.add_documents([sample_text_file])
        
        results = rag_service.retrieve_documents("sentiment analysis")
        
        assert results['query'] == "sentiment analysis"
        assert len(results['results']['documents']) > 0
        assert len(results['results']['ids']) > 0
        assert len(results['results']['distances']) > 0
    
    def test_retrieve_with_custom_n_results(self, rag_service, sample_text_file):
        """Test retrieve with custom number of results"""
        rag_service.add_documents([sample_text_file])
        
        results = rag_service.retrieve_documents("sentiment", n_results=2)
        assert len(results['results']['documents']) <= 2
    
    def test_retrieve_empty_collection(self, rag_service):
        """Test retrieval on empty collection"""
        results = rag_service.retrieve_documents("test query")
        assert results['results']['documents'] == []
    
    def test_retrieve_relevance_ranking(self, rag_service, sample_text_file):
        """Test that retrieval returns ranked results by relevance"""
        rag_service.add_documents([sample_text_file])
        
        results = rag_service.retrieve_documents("machine learning")
        distances = results['results']['distances']
        
        # Distances should be sorted (lower is better)
        assert distances == sorted(distances)
    
    # ==================== COLLECTION MANAGEMENT TESTS ====================
    
    def test_get_collection_stats(self, rag_service, sample_text_file):
        """Test getting collection statistics"""
        rag_service.add_documents([sample_text_file])
        
        stats = rag_service.get_collection_stats()
        
        assert stats['collection_name'] == "test_rag_collection"
        assert stats['document_count'] > 0
        assert stats['chunk_size'] == 500
        assert stats['chunk_overlap'] == 50
    
    def test_delete_all_documents(self, rag_service, sample_text_file):
        """Test deleting all documents"""
        rag_service.add_documents([sample_text_file])
        assert rag_service.get_collection_stats()['document_count'] > 0
        
        rag_service.delete_all_documents()
        assert rag_service.get_collection_stats()['document_count'] == 0
    
    def test_export_collection(self, rag_service, sample_text_file):
        """Test exporting collection"""
        rag_service.add_documents([sample_text_file])
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_file = f.name
        
        try:
            export_data = rag_service.export_collection(export_file)
            
            assert 'metadata' in export_data
            assert 'data' in export_data
            assert export_data['metadata']['collection_name'] == "test_rag_collection"
            assert os.path.exists(export_file)
        finally:
            if os.path.exists(export_file):
                os.remove(export_file)
    
    # ==================== INTEGRATION TESTS ====================
    
    def test_full_rag_pipeline(self, rag_service, sample_text_file):
        """Test complete RAG pipeline: load -> chunk -> embed -> store -> retrieve"""
        # Add document
        add_stats = rag_service.add_documents([sample_text_file])
        assert add_stats['documents_loaded'] == 1
        assert add_stats['chunks_created'] > 0
        
        # Retrieve
        results = rag_service.retrieve_documents("sentiment analysis")
        assert len(results['results']['documents']) > 0
        
        # Check stats
        stats = rag_service.get_collection_stats()
        assert stats['document_count'] == add_stats['chunks_created']
    
    def test_singleton_instance(self):
        """Test that singleton instance works correctly"""
        service1 = get_rag_service()
        service2 = get_rag_service()
        
        assert service1 is service2  # Same instance


class TestRAGChunking:
    """Focused tests for chunking behavior"""
    
    @pytest.fixture
    def rag_service(self):
        return RAGService(collection_name="test_chunking")
    
    def test_chunk_size_500_exactly(self, rag_service):
        """Test that chunks are exactly 500 chars"""
        text = "X" * 1500
        chunks = rag_service.chunk_text(text)
        
        # First and middle chunk should be exactly 500
        assert len(chunks[0]) == 500
        assert len(chunks[1]) == 500
    
    def test_overlap_50_chars(self, rag_service):
        """Test that overlap is exactly 50 chars"""
        text = "0123456789" * 100
        chunks = rag_service.chunk_text(text)
        
        for i in range(len(chunks) - 1):
            overlap = chunks[i][-50:]
            assert overlap == chunks[i+1][:50]


class TestEmbeddingModel:
    """Test embedding model selection"""
    
    def test_default_model_initialized(self):
        """Test that default model is initialized"""
        service = RAGService()
        assert service.embedding_model is not None
        assert service.embedding_model_name == "all-MiniLM-L6-v2"
    
    def test_custom_embedding_model(self):
        """Test initialization with custom embedding model"""
        service = RAGService(embedding_model="all-MiniLM-L6-v2")
        assert service.embedding_model_name == "all-MiniLM-L6-v2"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

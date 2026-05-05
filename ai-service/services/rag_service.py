"""
RAG (Retrieval-Augmented Generation) Service
Handles document loading, chunking, embedding, and storage in ChromaDB
"""
import os
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
import subprocess
import json
from datetime import datetime


class RAGService:
    """RAG Pipeline Service with ChromaDB"""
    
    def __init__(self, collection_name="rag_documents", embedding_model="all-MiniLM-L6-v2"):
        """
        Initialize RAG Service
        
        Args:
            collection_name: ChromaDB collection name
            embedding_model: Sentence transformer model name
        """
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        self.chunk_size = 500
        self.chunk_overlap = 50
        
        # Initialize ChromaDB client
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        
        # Initialize embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
    def load_text_file(self, file_path: str) -> str:
        """Load text from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
    
    def load_pdf_file(self, file_path: str) -> str:
        """Load text from PDF file"""
        try:
            from pypdf import PdfReader
            text = ""
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def load_docx_file(self, file_path: str) -> str:
        """Load text from DOCX file"""
        try:
            from docx import Document
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def load_document(self, file_path: str) -> str:
        """Load document based on file type"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.txt':
            return self.load_text_file(file_path)
        elif file_ext == '.pdf':
            return self.load_pdf_file(file_path)
        elif file_ext == '.docx':
            return self.load_docx_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> list:
        """
        Chunk text with specified size and overlap
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk (default 500)
            overlap: Overlap between chunks (default 50)
            
        Returns:
            List of text chunks
        """
        if chunk_size is None:
            chunk_size = self.chunk_size
        if overlap is None:
            overlap = self.chunk_overlap
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        
        return chunks
    
    def embed_text(self, text: str) -> list:
        """Generate embedding for text"""
        return self.embedding_model.encode(text).tolist()
    
    def embed_texts(self, texts: list) -> list:
        """Generate embeddings for multiple texts"""
        return self.embedding_model.encode(texts).tolist()
    
    def add_documents(self, file_paths: list, metadata: dict = None) -> dict:
        """
        Add documents to RAG pipeline
        
        Args:
            file_paths: List of file paths to load
            metadata: Optional metadata for documents
            
        Returns:
            Dictionary with statistics
        """
        stats = {
            "documents_loaded": 0,
            "chunks_created": 0,
            "chunks_embedded": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        all_chunks = []
        all_ids = []
        all_metadatas = []
        all_embeddings = []
        
        for file_path in file_paths:
            try:
                # Load document
                print(f"Loading document: {file_path}")
                text = self.load_document(file_path)
                stats["documents_loaded"] += 1
                
                # Chunk text
                chunks = self.chunk_text(text)
                print(f"Created {len(chunks)} chunks from {file_path}")
                stats["chunks_created"] += len(chunks)
                
                # Create embeddings
                embeddings = self.embed_texts(chunks)
                stats["chunks_embedded"] += len(embeddings)
                
                # Prepare data for storage
                for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    chunk_id = f"{Path(file_path).stem}_chunk_{i}"
                    all_chunks.append(chunk)
                    all_ids.append(chunk_id)
                    all_embeddings.append(embedding)
                    
                    # Create metadata
                    chunk_metadata = {
                        "source": file_path,
                        "chunk_index": i,
                        "chunk_size": len(chunk)
                    }
                    if metadata:
                        chunk_metadata.update(metadata)
                    all_metadatas.append(chunk_metadata)
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                raise
        
        # Store in ChromaDB
        if all_chunks:
            self.collection.add(
                documents=all_chunks,
                ids=all_ids,
                embeddings=all_embeddings,
                metadatas=all_metadatas
            )
            print(f"Stored {len(all_chunks)} chunks in ChromaDB")
        
        return stats
    
    def retrieve_documents(self, query: str, n_results: int = 5) -> dict:
        """
        Retrieve relevant documents for query
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Retrieved documents with metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return {
            "query": query,
            "results": {
                "documents": results['documents'][0] if results['documents'] else [],
                "ids": results['ids'][0] if results['ids'] else [],
                "distances": results['distances'][0] if results['distances'] else [],
                "metadatas": results['metadatas'][0] if results['metadatas'] else []
            }
        }
    
    def get_collection_stats(self) -> dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
            "embedding_model": self.embedding_model_name,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }
    
    def delete_all_documents(self):
        """Delete all documents from collection"""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )
        print(f"Cleared collection: {self.collection_name}")
    
    def export_collection(self, output_file: str):
        """Export collection data"""
        try:
            data = self.collection.get()
            
            export_data = {
                "metadata": {
                    "collection_name": self.collection_name,
                    "embedding_model": self.embedding_model_name,
                    "chunk_size": self.chunk_size,
                    "chunk_overlap": self.chunk_overlap,
                    "export_timestamp": datetime.now().isoformat()
                },
                "data": {
                    "ids": data.get("ids", []),
                    "documents": data.get("documents", []),
                    "metadatas": data.get("metadatas", [])
                }
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"Collection exported to {output_file}")
            return export_data
        except Exception as e:
            raise Exception(f"Error exporting collection: {str(e)}")


# Singleton instance
_rag_service = None

def get_rag_service(collection_name="rag_documents", embedding_model="all-MiniLM-L6-v2") -> RAGService:
    """Get or create RAG service singleton"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService(collection_name, embedding_model)
    return _rag_service

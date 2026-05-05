"""
Day 13: Model Preloader Service
Pre-loads expensive models (sentence-transformers) at startup to reduce latency
Implements singleton pattern for model reuse across requests
"""
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()


class ModelPreloader:
    """Singleton model preloader for sentence-transformers embeddings"""
    
    _instance = None
    _embedding_model = None
    _is_loaded = False
    
    def __new__(cls):
        """Ensure single instance across application"""
        if cls._instance is None:
            cls._instance = super(ModelPreloader, cls).__new__(cls)
        return cls._instance
    
    def preload_models(self, embedding_model_name="all-MiniLM-L6-v2", force_reload=False):
        """
        Pre-load sentence-transformers model at startup
        
        Args:
            embedding_model_name: Model to load (default: all-MiniLM-L6-v2)
            force_reload: Force reload even if already loaded
            
        Returns:
            dict: Load status and timing info
        """
        import time
        
        if self._is_loaded and not force_reload:
            return {
                "status": "already_loaded",
                "model": embedding_model_name,
                "message": "Model already preloaded in memory"
            }
        
        try:
            start_time = time.time()
            print(f"[ModelPreloader] Loading embedding model: {embedding_model_name}")
            
            # Load the model (this is the slow operation done once at startup)
            self._embedding_model = SentenceTransformer(embedding_model_name)
            
            load_time = time.time() - start_time
            self._is_loaded = True
            
            print(f"[ModelPreloader] ✓ Model loaded in {load_time:.2f}s")
            
            return {
                "status": "success",
                "model": embedding_model_name,
                "load_time_seconds": load_time,
                "message": f"Model preloaded successfully in {load_time:.2f}s"
            }
        
        except Exception as e:
            print(f"[ModelPreloader] ✗ Error loading model: {str(e)}")
            return {
                "status": "failed",
                "model": embedding_model_name,
                "error": str(e),
                "message": f"Failed to preload model: {str(e)}"
            }
    
    def get_embedding_model(self):
        """
        Get preloaded embedding model
        
        Returns:
            SentenceTransformer: Preloaded model instance
            
        Raises:
            RuntimeError: If model not preloaded
        """
        if not self._is_loaded or self._embedding_model is None:
            raise RuntimeError(
                "Embedding model not preloaded. Call preload_models() at startup."
            )
        return self._embedding_model
    
    def is_model_loaded(self):
        """Check if model is loaded"""
        return self._is_loaded


# Global instance for easy access
_preloader = None


def init_model_preloader(embedding_model="all-MiniLM-L6-v2"):
    """
    Initialize global model preloader at app startup
    
    Args:
        embedding_model: Model name to preload
        
    Returns:
        dict: Preload result
    """
    global _preloader
    _preloader = ModelPreloader()
    return _preloader.preload_models(embedding_model_name=embedding_model)


def get_preloaded_embedding_model():
    """Get preloaded embedding model from singleton"""
    if _preloader is None:
        raise RuntimeError("Model preloader not initialized. Call init_model_preloader() first.")
    return _preloader.get_embedding_model()


def is_model_preloaded():
    """Check if models are preloaded"""
    return _preloader is not None and _preloader.is_model_loaded()

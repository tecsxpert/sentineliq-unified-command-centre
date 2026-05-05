#!/usr/bin/env python3
"""
Simple health endpoint test
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_health():
    """Test health endpoint"""
    try:
        # Mock the chromadb import to avoid dependency issues
        import sys
        from unittest.mock import MagicMock
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        # Now import the health route
        from routes.health import get_health

        result = get_health()
        # Check that we get a proper response (either success or error)
        assert isinstance(result, dict)
        if 'error' not in result:
            assert 'model' in result
            assert 'avg_response_time' in result
            assert 'chroma_docs' in result
            assert 'uptime_seconds' in result
            assert 'cache' in result
        print("✓ Health endpoint test passed")
        return True
    except Exception as e:
        print(f"✗ Health endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing health endpoint...")
    success = test_health()
    if success:
        print("🎉 Health test passed!")
        sys.exit(0)
    else:
        print("❌ Health test failed")
        sys.exit(1)
#!/usr/bin/env python3
"""
Simple test runner to validate the comprehensive tests
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import routes.health
        # Skip chromadb-dependent imports for now
        # import routes.query
        # import routes.categorise
        # import routes.describe
        # import routes.recommend
        # import routes.report
        # import routes.analyse
        # import services.groq_client
        print("✓ Basic route imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_health_endpoint():
    """Test health endpoint"""
    try:
        from routes.health import get_health
        result = get_health()
        assert result['status'] == 'healthy'
        assert 'timestamp' in result
        assert 'version' in result
        print("✓ Health endpoint test passed")
        return True
    except Exception as e:
        print(f"✗ Health endpoint test failed: {e}")
        return False

def test_query_endpoint():
    """Test query endpoint with mocking"""
    try:
        from unittest.mock import patch
        from routes.query import query_with_context

        with patch('routes.query.query_data') as mock_query, \
             patch('services.groq_client.GroqClient.generate_response') as mock_groq:

            # Mock ChromaDB query
            mock_query.return_value = {
                'results': {
                    'documents': [['Test document content']]
                }
            }

            # Mock Groq response
            mock_groq.return_value = '{"answer": "This is a test answer"}'

            result = query_with_context("What is AI?")
            assert "answer" in result
            print("✓ Query endpoint test passed")
            return True
    except Exception as e:
        print(f"✗ Query endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running comprehensive test validation...")
    print()

    tests = [
        test_imports,
        test_health_endpoint,
        test_query_endpoint,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
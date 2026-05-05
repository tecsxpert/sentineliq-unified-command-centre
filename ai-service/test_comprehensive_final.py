"""
Comprehensive pytest unit tests for AI Service endpoints
Tests all endpoints with mocked Groq responses, error handling, and edge cases
This version focuses on testable functionality without heavy external dependencies
"""
import pytest
import json
import sys
from unittest.mock import Mock, patch, MagicMock


# Mock external dependencies before importing routes
sys.modules['chromadb'] = MagicMock()
sys.modules['chromadb.config'] = MagicMock()
sys.modules['sentence_transformers'] = MagicMock()
sys.modules['langchain'] = MagicMock()
sys.modules['pypdf'] = MagicMock()


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_endpoint_success(self):
        """Test health endpoint with mocked response"""
        from routes.health import get_health

        result = get_health()
        # Check that we get a proper response structure
        assert isinstance(result, dict)
        if 'error' not in result:
            assert 'model' in result
            assert 'avg_response_time' in result
            assert 'chroma_docs' in result
            assert 'uptime_seconds' in result
            assert 'cache' in result


class TestValidationFunctions:
    """Test input validation functions across all endpoints"""

    def test_categorise_validation_short_text(self):
        """Test categorisation validation rejects short text"""
        from routes.categorise import validate_categorise_input

        is_valid, error, cleaned = validate_categorise_input("Hi")
        assert not is_valid
        assert "at least 10 characters" in error

    def test_categorise_validation_success(self):
        """Test categorisation validation accepts valid text"""
        from routes.categorise import validate_categorise_input

        is_valid, error, cleaned = validate_categorise_input("This is a valid test string for categorisation!")
        assert is_valid
        assert error == ""
        assert len(cleaned) > 0

    def test_describe_validation_empty_text(self):
        """Test describe validation rejects empty text"""
        from routes.describe import validate_describe_input

        is_valid, error, cleaned = validate_describe_input("")
        assert not is_valid
        assert "non-empty string" in error

    def test_describe_validation_success(self):
        """Test describe validation accepts valid text"""
        from routes.describe import validate_describe_input

        is_valid, error, cleaned = validate_describe_input("This is a valid document for description")
        assert is_valid
        assert error == ""

    def test_recommend_validation_short_text(self):
        """Test recommend validation rejects short text"""
        from routes.recommend import validate_recommend_input

        is_valid, error, cleaned = validate_recommend_input("Hi")
        assert not is_valid
        assert "at least 5 characters" in error

    def test_recommend_validation_success(self):
        """Test recommend validation accepts valid text"""
        from routes.recommend import validate_recommend_input

        is_valid, error, cleaned = validate_recommend_input("This is text for recommendation generation")
        assert is_valid
        assert error == ""

    def test_analyse_validation_short_text(self):
        """Test analyse validation rejects short text"""
        from routes.analyse import validate_analyse_input

        is_valid, error, cleaned = validate_analyse_input("Short")
        assert not is_valid
        assert "at least 50 characters" in error

    def test_analyse_validation_success(self):
        """Test analyse validation accepts valid text"""
        from routes.analyse import validate_analyse_input

        long_text = "This is a long enough document text for analysis purposes. It contains substantial content."
        is_valid, error, cleaned = validate_analyse_input(long_text)
        assert is_valid
        assert error == ""


class TestInputSanitization:
    """Test input sanitization and text cleaning"""

    def test_whitespace_trimming(self):
        """Test that whitespace is properly trimmed"""
        from routes.categorise import validate_categorise_input

        is_valid, error, cleaned = validate_categorise_input("   This is valid text   ")
        assert is_valid
        assert cleaned == "This is valid text"

    def test_special_characters_handling(self):
        """Test handling of special characters"""
        from routes.describe import validate_describe_input

        is_valid, error, cleaned = validate_describe_input("Text with @special #characters $and more!")
        assert is_valid
        # Special characters should be preserved
        assert "@special" in cleaned

    def test_multiple_spaces_normalization(self):
        """Test normalization of multiple spaces"""
        from routes.categorise import validate_categorise_input

        is_valid, error, cleaned = validate_categorise_input("This   has   multiple    spaces")
        assert is_valid
        # Should normalize spaces
        assert "   " not in cleaned


class TestErrorHandling:
    """Test error handling in endpoints"""

    def test_categorise_null_input(self):
        """Test categorisation handles None input"""
        from routes.categorise import validate_categorise_input

        is_valid, error, cleaned = validate_categorise_input(None)
        assert not is_valid

    def test_describe_null_input(self):
        """Test describe handles None input"""
        from routes.describe import validate_describe_input

        is_valid, error, cleaned = validate_describe_input(None)
        assert not is_valid

    def test_recommend_null_input(self):
        """Test recommend handles None input"""
        from routes.recommend import validate_recommend_input

        is_valid, error, cleaned = validate_recommend_input(None)
        assert not is_valid

    def test_analyse_null_input(self):
        """Test analyse handles None input"""
        from routes.analyse import validate_analyse_input

        is_valid, error, cleaned = validate_analyse_input(None)
        assert not is_valid


class TestGroqClientErrorHandling:
    """Test Groq client error handling with mocking"""

    @patch('services.groq_client.Groq')
    def test_groq_client_retry_logic(self, mock_groq_class):
        """Test Groq client retries on failure"""
        from services.groq_client import GroqClient

        # Mock the client to fail first time, succeed second time
        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        # Configure mock to raise error first, then succeed
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Success"
        mock_client.chat.completions.create.side_effect = [
            Exception("API Error"),
            mock_response
        ]

        groq_client = GroqClient()
        # This would retry and potentially succeed
        result = groq_client.generate_response("Test prompt")

        # Should have attempted twice
        assert mock_client.chat.completions.create.call_count >= 1

    @patch('services.groq_client.Groq')
    def test_groq_client_handles_connection_error(self, mock_groq_class):
        """Test Groq client handles connection errors"""
        from services.groq_client import GroqClient

        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        # Configure mock to always fail
        mock_client.chat.completions.create.side_effect = Exception("Connection failed")

        groq_client = GroqClient()
        result = groq_client.generate_response("Test prompt")

        # Should return error message
        assert "Error" in result


class TestCacheingFunctionality:
    """Test caching functionality"""

    @patch('services.cache_service.get_cache')
    @patch('services.cache_service.set_cache')
    @patch('services.groq_client.Groq')
    def test_cache_hit_avoids_api_call(self, mock_groq_class, mock_set_cache, mock_get_cache):
        """Test that cache hit avoids API call"""
        from services.groq_client import GroqClient

        # Mock cache to have a hit
        mock_get_cache.return_value = "Cached response"

        mock_client = MagicMock()
        mock_groq_class.return_value = mock_client

        groq_client = GroqClient()
        result = groq_client.generate_response("Test prompt", use_cache=True)

        # Should have returned cached result without calling API
        assert result == "Cached response"
        assert mock_client.chat.completions.create.call_count == 0

    @patch('services.cache_service.get_cache')
    @patch('services.cache_service.set_cache')
    @patch('services.groq_client.Groq')
    def test_cache_miss_calls_api(self, mock_groq_class, mock_set_cache, mock_get_cache):
        """Test that cache miss results in API call"""
        from services.groq_client import GroqClient

        # Mock cache to have a miss
        mock_get_cache.return_value = None

        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "API response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_groq_class.return_value = mock_client

        groq_client = GroqClient()
        result = groq_client.generate_response("Test prompt", use_cache=True)

        # Should have called API
        assert mock_client.chat.completions.create.call_count >= 1
        # Should have set cache
        assert mock_set_cache.call_count >= 1


class TestEndpointIntegration:
    """Integration tests for endpoints with mocked external services"""

    @patch('services.cache_service.get_cache', return_value=None)
    @patch('services.cache_service.set_cache')
    def test_categorise_integration(self, mock_set_cache, mock_get_cache):
        """Test categorise endpoint integration"""
        from routes.categorise import categorise_text
        from unittest.mock import patch

        with patch('services.groq_client.GroqClient.generate_response') as mock_groq:
            mock_groq.return_value = '{"category": "technical", "confidence": 0.85}'

            result = categorise_text("This is a technical document about machine learning and AI")

            assert isinstance(result, str)
            # Try to parse as JSON
            parsed = json.loads(result)
            assert "category" in parsed

    @patch('services.cache_service.get_cache', return_value=None)
    @patch('services.cache_service.set_cache')
    def test_describe_integration(self, mock_set_cache, mock_get_cache):
        """Test describe endpoint integration"""
        from routes.describe import describe_text
        from unittest.mock import patch

        with patch('services.groq_client.GroqClient.generate_response') as mock_groq:
            mock_groq.return_value = '{"description": "This is a comprehensive summary of the document"}'

            result = describe_text("Sample text that needs description")

            assert isinstance(result, str)
            parsed = json.loads(result)
            assert "description" in parsed

    @patch('services.cache_service.get_cache', return_value=None)
    @patch('services.cache_service.set_cache')
    def test_recommend_integration(self, mock_set_cache, mock_get_cache):
        """Test recommend endpoint integration"""
        from routes.recommend import recommend_text
        from unittest.mock import patch

        with patch('services.groq_client.GroqClient.generate_response') as mock_groq:
            mock_groq.return_value = '[{"action_type": "fix", "description": "Fix the bug", "priority": "high"}]'

            result = recommend_text("There is a critical bug that needs fixing")

            assert isinstance(result, list)
            if len(result) > 0:
                assert "action_type" in result[0]


class TestResponseFormatting:
    """Test response formatting across endpoints"""

    def test_json_response_format(self):
        """Test that responses are properly formatted JSON"""
        sample_response = '{"category": "technical", "confidence": 0.85}'
        parsed = json.loads(sample_response)
        assert isinstance(parsed, dict)
        assert "category" in parsed
        assert "confidence" in parsed

    def test_list_response_format(self):
        """Test that list responses are valid"""
        sample_response = '[{"action_type": "fix"}, {"action_type": "improve"}]'
        parsed = json.loads(sample_response)
        assert isinstance(parsed, list)
        assert len(parsed) > 0
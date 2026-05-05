"""
Comprehensive pytest unit tests for AI Service endpoints
Tests all endpoints with mocked Groq responses, error handling, and edge cases
"""
import pytest
import json
import sys
from unittest.mock import Mock, patch, MagicMock


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_endpoint_mock(self):
        """Test health endpoint with mocked response"""
        # Mock chromadb and sentence_transformers to avoid import issues
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

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


class TestQueryEndpoint:
    """Test query endpoint with mocked responses"""

    @patch('routes.query.query_data')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_query_success_mock(self, mock_groq, mock_query_data):
        """Test successful query with mocked data"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.query import query_with_context

        # Mock ChromaDB query
        mock_query_data.return_value = {
            'results': {
                'documents': [['Test document content']]
            }
        }

        # Mock Groq response
        mock_groq.return_value = '{"answer": "This is a test answer"}'

        result = query_with_context("What is AI?")
        assert "answer" in result
        parsed = json.loads(result)
        assert parsed['answer'] == "This is a test answer"

    @patch('routes.query.query_data')
    def test_query_empty_input_mock(self, mock_query_data):
        """Test query with empty input"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.query import query_with_context

        # Should handle empty input gracefully
        result = query_with_context("")
        assert isinstance(result, str)


class TestCategoriseEndpoint:
    """Test categorisation endpoint"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_categorise_success_mock(self, mock_groq):
        """Test successful categorisation"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.categorise import categorise_text

        mock_groq.return_value = '{"category": "technical", "confidence": 0.85}'

        result = categorise_text("This is a technical document about APIs")
        assert "category" in result
        parsed = json.loads(result)
        assert parsed['category'] == 'technical'

    @patch('services.groq_client.GroqClient.generate_response')
    def test_categorise_short_text_mock(self, mock_groq):
        """Test categorisation with text too short"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.categorise import validate_categorise_input

        is_valid, error, cleaned = validate_categorise_input("Hi")
        assert not is_valid
        assert "at least 10 characters" in error


class TestDescribeEndpoint:
    """Test description endpoint"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_describe_success_mock(self, mock_groq):
        """Test successful description generation"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.describe import describe_text

        mock_groq.return_value = '{"description": "This is a comprehensive description"}'

        result = describe_text("Sample text for description")
        assert "description" in result
        parsed = json.loads(result)
        assert "description" in parsed

    @patch('services.groq_client.GroqClient.generate_response')
    def test_describe_empty_text_mock(self, mock_groq):
        """Test description with empty text"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.describe import validate_describe_input

        is_valid, error, cleaned = validate_describe_input("")
        assert not is_valid
        assert "non-empty string" in error


class TestRecommendEndpoint:
    """Test recommendation endpoint"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_recommend_success_mock(self, mock_groq):
        """Test successful recommendation generation"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.recommend import recommend_text

        mock_groq.return_value = '[{"action_type": "fix", "description": "Fix the issue", "priority": "high"}]'

        result = recommend_text("There is a bug in the system")
        assert isinstance(result, list)
        assert len(result) > 0
        assert "action_type" in result[0]

    @patch('services.groq_client.GroqClient.generate_response')
    def test_recommend_text_too_short_mock(self, mock_groq):
        """Test recommendation with text too short"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.recommend import validate_recommend_input

        is_valid, error, cleaned = validate_recommend_input("Hi")
        assert not is_valid
        assert "at least 5 characters" in error


class TestReportEndpoint:
    """Test report generation endpoint"""

    @patch('services.report_service.ReportService._retrieve_context')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_generate_report_success_mock(self, mock_groq, mock_retrieve):
        """Test successful report generation"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from services.report_service import ReportService

        mock_retrieve.return_value = "Sample context"

        # Mock all the Groq calls for report generation
        mock_groq.side_effect = [
            "Sample Report Title",  # Title
            "Sample overview text",  # Overview
            "Sample executive summary",  # Executive summary
            '[{"item_number": 1, "title": "Item 1", "description": "Desc", "impact": "high", "priority": 1}]',  # Top items
            '[{"recommendation": "Rec 1", "action": "Action", "timeline": "immediate", "effort": "low"}]'  # Recommendations
        ]

        service = ReportService()
        result = service.generate_report("Test Topic")

        assert "title" in result
        assert "overview" in result
        assert "executive_summary" in result
        assert "top_items" in result
        assert "recommendations" in result
        assert "metadata" in result

    @patch('services.report_service.ReportService._retrieve_context')
    def test_generate_report_empty_topic_mock(self, mock_retrieve):
        """Test report generation with empty topic"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from services.report_service import ReportService

        service = ReportService()

        with pytest.raises(ValueError):
            service.generate_report("")


class TestAnalyseEndpoint:
    """Test document analysis endpoint"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_analyse_document_success_mock(self, mock_groq):
        """Test successful document analysis"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.analyse import analyse_document

        mock_groq.return_value = '{"insights": [{"type": "insight", "category": "technical", "title": "Test insight", "description": "Test desc", "severity": "medium", "confidence": 0.8}], "risks": []}'

        result = analyse_document("This is a long enough document text for analysis purposes.")

        assert "insights" in result
        assert "risks" in result
        assert "metadata" in result
        assert len(result["insights"]) > 0

    @patch('services.groq_client.GroqClient.generate_response')
    def test_analyse_document_text_too_short_mock(self, mock_groq):
        """Test document analysis with text too short"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.analyse import validate_analyse_input

        is_valid, error, cleaned = validate_analyse_input("Short")
        assert not is_valid
        assert "at least 50 characters" in error

    @patch('services.groq_client.GroqClient.generate_response')
    def test_analyse_document_json_error_mock(self, mock_groq):
        """Test document analysis with invalid JSON response"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from routes.analyse import analyse_document

        mock_groq.return_value = 'Invalid JSON response from Groq'

        result = analyse_document("This is a valid length document for testing error handling.")

        # Should handle JSON error gracefully with fallback
        assert "insights" in result
        assert "risks" in result
        assert "metadata" in result


class TestGroqClientMocking:
    """Test Groq client mocking and error handling"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_groq_client_exception_handling_mock(self, mock_groq):
        """Test Groq client handles exceptions properly"""
        # Mock dependencies
        sys.modules['chromadb'] = MagicMock()
        sys.modules['chromadb.config'] = MagicMock()
        sys.modules['sentence_transformers'] = MagicMock()

        from services.groq_client import GroqClient

        mock_groq.side_effect = Exception("API Error")

        client = GroqClient()
        result = client.generate_response("Test prompt")

        # Should return error message on exception
        assert "Error" in result

    @patch('services.cache_service.get_cache')
    @patch('services.cache_service.set_cache')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_cache_integration_mock(self, mock_groq, mock_set_cache, mock_get_cache):
        """Test cache integration works properly"""
        from services.groq_client import GroqClient

        # Test cache hit
        mock_get_cache.return_value = "Cached response"
        client = GroqClient()
        result = client.generate_response("Test prompt")
        assert result == "Cached response"
        mock_groq.assert_not_called()

        # Test cache miss
        mock_get_cache.return_value = None
        mock_groq.return_value = "New response"
        result = client.generate_response("Test prompt")
        assert result == "New response"
        mock_set_cache.assert_called_once()


class TestInputValidation:
    """Test input validation across endpoints"""

    def test_validate_categorise_input_edge_cases(self):
        """Test categorise input validation edge cases"""
        from routes.categorise import validate_categorise_input

        # Valid input
        is_valid, error, cleaned = validate_categorise_input("This is a valid text for categorisation")
        assert is_valid
        assert error is None
        assert cleaned == "This is a valid text for categorisation"

        # Empty input
        is_valid, error, cleaned = validate_categorise_input("")
        assert not is_valid
        assert "non-empty string" in error

        # Too short
        is_valid, error, cleaned = validate_categorise_input("Hi")
        assert not is_valid
        assert "at least 10 characters" in error

        # Too long
        long_text = "A" * 10001
        is_valid, error, cleaned = validate_categorise_input(long_text)
        assert not is_valid
        assert "exceeds maximum length" in error

    def test_validate_describe_input_edge_cases(self):
        """Test describe input validation edge cases"""
        from routes.describe import validate_describe_input

        # Valid input
        is_valid, error, cleaned = validate_describe_input("This is a valid text for description")
        assert is_valid

        # Empty input
        is_valid, error, cleaned = validate_describe_input("")
        assert not is_valid

        # Too long
        long_text = "A" * 10001
        is_valid, error, cleaned = validate_describe_input(long_text)
        assert not is_valid


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
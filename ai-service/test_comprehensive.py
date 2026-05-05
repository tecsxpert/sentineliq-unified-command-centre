"""
Comprehensive pytest unit tests for AI Service endpoints
Tests all endpoints with mocked Groq responses, error handling, and edge cases
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from routes.health import health_bp, get_health
from routes.query import query_bp, query_with_context
from routes.categorise import categorise_bp, categorise_text
from routes.describe import describe_bp, describe_text
from routes.recommend import recommend_bp, recommend_text
from routes.report import report_bp, generate_report
from routes.analyse import analyse_bp, analyse_document
from services.groq_client import GroqClient
from services.cache_service import get_cache, set_cache


@pytest.fixture
def app():
    """Create Flask test app"""
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Register all blueprints
    app.register_blueprint(health_bp, url_prefix='/api/ai')
    app.register_blueprint(query_bp, url_prefix='/api/ai')
    app.register_blueprint(categorise_bp, url_prefix='/api/ai')
    app.register_blueprint(describe_bp, url_prefix='/api/ai')
    app.register_blueprint(recommend_bp, url_prefix='/api/ai')
    app.register_blueprint(report_bp, url_prefix='/api/ai')
    app.register_blueprint(analyse_bp, url_prefix='/api/ai')

    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def mock_groq_response():
    """Mock successful Groq response"""
    return {
        "choices": [
            {
                "message": {
                    "content": '{"answer": "Test response"}'
                }
            }
        ]
    }


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_endpoint_success(self, client):
        """Test successful health check"""
        response = client.get('/api/ai/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'version' in data

    def test_get_health_function(self):
        """Test get_health function directly"""
        result = get_health()
        assert result['status'] == 'healthy'
        assert 'timestamp' in result
        assert 'version' in result


class TestQueryEndpoint:
    """Test query endpoint with mocked responses"""

    @patch('routes.query.query_data')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_query_success(self, mock_groq, mock_query_data, client):
        """Test successful query with mocked data"""
        # Mock ChromaDB query
        mock_query_data.return_value = {
            'results': {
                'documents': [['Test document content']]
            }
        }

        # Mock Groq response
        mock_groq.return_value = '{"answer": "This is a test answer"}'

        response = client.post('/api/ai/query',
                             json={'question': 'What is AI?'},
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'answer' in data['data']

    @patch('routes.query.query_data')
    def test_query_missing_question(self, mock_query_data, client):
        """Test query with missing question"""
        response = client.post('/api/ai/query',
                             json={},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'question' in data['message']

    @patch('routes.query.query_data')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_query_empty_question(self, mock_groq, mock_query_data, client):
        """Test query with empty question"""
        response = client.post('/api/ai/query',
                             json={'question': ''},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestCategoriseEndpoint:
    """Test categorisation endpoint"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_categorise_success(self, mock_groq, client):
        """Test successful categorisation"""
        mock_groq.return_value = '{"category": "technical", "confidence": 0.85}'

        response = client.post('/api/ai/categorise',
                             json={'text': 'This is a technical document about APIs'},
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['data']['category'] == 'technical'

    @patch('services.groq_client.GroqClient.generate_response')
    def test_categorise_short_text(self, mock_groq, client):
        """Test categorisation with text too short"""
        response = client.post('/api/ai/categorise',
                             json={'text': 'Hi'},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    @patch('services.groq_client.GroqClient.generate_response')
    def test_categorise_json_error(self, mock_groq, client):
        """Test categorisation with invalid JSON response"""
        mock_groq.return_value = 'Invalid JSON response'

        response = client.post('/api/ai/categorise',
                             json={'text': 'This is a valid length text for testing'},
                             content_type='application/json')

        assert response.status_code == 200
        # Should handle JSON error gracefully with fallback


class TestDescribeEndpoint:
    """Test description endpoint"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_describe_success(self, mock_groq, client):
        """Test successful description generation"""
        mock_groq.return_value = '{"description": "This is a comprehensive description"}'

        response = client.post('/api/ai/describe',
                             json={'text': 'Sample text for description'},
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'description' in data['data']

    @patch('services.groq_client.GroqClient.generate_response')
    def test_describe_empty_text(self, mock_groq, client):
        """Test description with empty text"""
        response = client.post('/api/ai/describe',
                             json={'text': ''},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestRecommendEndpoint:
    """Test recommendation endpoint"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_recommend_success(self, mock_groq, client):
        """Test successful recommendation generation"""
        mock_groq.return_value = '[{"action_type": "fix", "description": "Fix the issue", "priority": "high"}]'

        response = client.post('/api/ai/recommend',
                             json={'text': 'There is a bug in the system'},
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert isinstance(data['data'], list)

    @patch('services.groq_client.GroqClient.generate_response')
    def test_recommend_text_too_short(self, mock_groq, client):
        """Test recommendation with text too short"""
        response = client.post('/api/ai/recommend',
                             json={'text': 'Hi'},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestReportEndpoint:
    """Test report generation endpoint"""

    @patch('services.report_service.ReportService._retrieve_context')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_generate_report_success(self, mock_groq, mock_retrieve, client):
        """Test successful report generation"""
        mock_retrieve.return_value = "Sample context"

        # Mock all the Groq calls for report generation
        mock_groq.side_effect = [
            "Sample Report Title",  # Title
            "Sample overview text",  # Overview
            "Sample executive summary",  # Executive summary
            '[{"item_number": 1, "title": "Item 1", "description": "Desc", "impact": "high", "priority": 1}]',  # Top items
            '[{"recommendation": "Rec 1", "action": "Action", "timeline": "immediate", "effort": "low"}]'  # Recommendations
        ]

        response = client.post('/api/ai/generate-report',
                             json={'topic': 'Test Report Topic'},
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'title' in data['data']
        assert 'overview' in data['data']

    @patch('services.report_service.ReportService._retrieve_context')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_generate_report_missing_topic(self, mock_groq, mock_retrieve, client):
        """Test report generation with missing topic"""
        response = client.post('/api/ai/generate-report',
                             json={},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'topic' in data['message']

    @patch('services.report_service.ReportService._retrieve_context')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_generate_report_empty_topic(self, mock_groq, mock_retrieve, client):
        """Test report generation with empty topic"""
        response = client.post('/api/ai/generate-report',
                             json={'topic': ''},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestAnalyseEndpoint:
    """Test document analysis endpoint"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_analyse_document_success(self, mock_groq, client):
        """Test successful document analysis"""
        mock_groq.return_value = '{"insights": [{"type": "insight", "category": "technical", "title": "Test insight", "description": "Test desc", "severity": "medium", "confidence": 0.8}], "risks": []}'

        response = client.post('/api/ai/analyse-document',
                             json={'text': 'This is a long enough document text for analysis purposes.'},
                             content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'insights' in data['data']
        assert 'risks' in data['data']

    @patch('services.groq_client.GroqClient.generate_response')
    def test_analyse_document_text_too_short(self, mock_groq, client):
        """Test document analysis with text too short"""
        response = client.post('/api/ai/analyse-document',
                             json={'text': 'Short'},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    @patch('services.groq_client.GroqClient.generate_response')
    def test_analyse_document_missing_text(self, mock_groq, client):
        """Test document analysis with missing text"""
        response = client.post('/api/ai/analyse-document',
                             json={},
                             content_type='application/json')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    @patch('services.groq_client.GroqClient.generate_response')
    def test_analyse_document_json_error_handling(self, mock_groq, client):
        """Test document analysis with invalid JSON response"""
        mock_groq.return_value = 'Invalid JSON response from Groq'

        response = client.post('/api/ai/analyse-document',
                             json={'text': 'This is a valid length document for testing error handling.'},
                             content_type='application/json')

        assert response.status_code == 200
        # Should handle JSON error gracefully with fallback response


class TestGroqClientMocking:
    """Test Groq client mocking and error handling"""

    @patch('services.groq_client.GroqClient.generate_response')
    def test_groq_client_exception_handling(self, mock_groq):
        """Test Groq client handles exceptions properly"""
        mock_groq.side_effect = Exception("API Error")

        client = GroqClient()
        result = client.generate_response("Test prompt")

        # Should return error message on exception
        assert "Error" in result

    @patch('services.cache_service.get_cache')
    @patch('services.cache_service.set_cache')
    @patch('services.groq_client.GroqClient.generate_response')
    def test_cache_integration(self, mock_groq, mock_set_cache, mock_get_cache):
        """Test cache integration works properly"""
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


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
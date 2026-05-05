"""
Comprehensive Report Generation Tests
Test report service with various configurations and scenarios
"""
import pytest
import json
from datetime import datetime
from services.report_service import ReportService, get_report_service
from unittest.mock import Mock, patch, MagicMock


class TestReportService:
    """Test ReportService functionality"""
    
    @pytest.fixture
    def report_service(self):
        """Create a test report service"""
        with patch('services.report_service.GroqClient'):
            service = ReportService(groq_api_key="test_key")
            return service
    
    @pytest.fixture
    def mock_groq_responses(self):
        """Create mock responses for Groq"""
        return {
            "title": "Comprehensive Security Analysis Report",
            "executive_summary": "This report provides a thorough analysis of security measures and recommendations for improving system protection.",
            "overview": "Security is a critical aspect of any organization. This report examines current practices and identifies areas for improvement.",
            "top_items": json.dumps([
                {
                    "item_number": 1,
                    "title": "Authentication Enhancement",
                    "description": "Implement multi-factor authentication across all systems.",
                    "impact": "high",
                    "priority": 1
                },
                {
                    "item_number": 2,
                    "title": "Data Encryption",
                    "description": "Enable end-to-end encryption for sensitive data.",
                    "impact": "high",
                    "priority": 2
                }
            ]),
            "recommendations": json.dumps([
                {
                    "recommendation": "Deploy MFA system across all user accounts",
                    "action": "1. Configure MFA provider\n2. Enable for all accounts\n3. Train users",
                    "timeline": "immediate",
                    "effort": "medium"
                }
            ])
        }
    
    # ==================== REPORT GENERATION TESTS ====================
    
    def test_generate_report_basic(self, report_service, mock_groq_responses):
        """Test basic report generation"""
        # Mock Groq responses
        report_service.groq_client.chat = Mock(side_effect=lambda x: mock_groq_responses.get(
            "title" if "title" in x else 
            "executive_summary" if "summary" in x else 
            "overview" if "overview" in x else
            "top_items",
            "mocked response"
        ))
        
        report = report_service.generate_report(
            topic="Security Analysis",
            use_rag=False
        )
        
        assert report is not None
        assert "title" in report
        assert "executive_summary" in report
        assert "overview" in report
        assert "top_items" in report
        assert "recommendations" in report
        assert "metadata" in report
    
    def test_report_structure(self, report_service, mock_groq_responses):
        """Test report JSON structure is valid"""
        report_service.groq_client.chat = Mock(return_value="mocked response")
        
        report = report_service.generate_report(
            topic="Test Topic",
            use_rag=False
        )
        
        # Verify structure
        assert isinstance(report, dict)
        assert isinstance(report['title'], str)
        assert isinstance(report['executive_summary'], str)
        assert isinstance(report['overview'], str)
        assert isinstance(report['top_items'], list)
        assert isinstance(report['recommendations'], list)
        assert isinstance(report['metadata'], dict)
    
    def test_metadata_contains_required_fields(self, report_service):
        """Test that metadata contains all required fields"""
        report_service.groq_client.chat = Mock(return_value="mocked")
        
        report = report_service.generate_report(
            topic="Test",
            report_type="technical",
            use_rag=False
        )
        
        metadata = report['metadata']
        assert 'generated_at' in metadata
        assert 'report_type' in metadata
        assert 'topic' in metadata
        assert 'items_count' in metadata
        assert 'recommendations_count' in metadata
        assert 'context_used' in metadata
        
        assert metadata['report_type'] == 'technical'
        assert metadata['topic'] == 'Test'
    
    def test_top_items_count_custom(self, report_service):
        """Test generating specific number of top items"""
        report_service.groq_client.chat = Mock(return_value=json.dumps([
            {
                "item_number": i,
                "title": f"Item {i}",
                "description": f"Description {i}",
                "impact": "high",
                "priority": i
            } for i in range(1, 4)
        ]))
        
        report = report_service.generate_report(
            topic="Test",
            top_items_count=3,
            use_rag=False
        )
        
        assert len(report['top_items']) > 0
    
    def test_bottom_items_validation(self, report_service):
        """Test that top items have required fields"""
        items_json = json.dumps([
            {
                "item_number": 1,
                "title": "Test Item",
                "description": "Test description",
                "impact": "high",
                "priority": 1
            }
        ])
        
        report_service.groq_client.chat = Mock(return_value=items_json)
        
        report = report_service.generate_report(
            topic="Test",
            use_rag=False
        )
        
        if report['top_items']:
            item = report['top_items'][0]
            assert 'item_number' in item
            assert 'title' in item
            assert 'description' in item
            assert 'impact' in item
            assert 'priority' in item
    
    def test_recommendations_validation(self, report_service):
        """Test that recommendations have required fields"""
        recs_json = json.dumps([
            {
                "recommendation": "Test recommendation",
                "action": "Do this 1. Step 1\n2. Step 2",
                "timeline": "short-term",
                "effort": "low"
            }
        ])
        
        report_service.groq_client.chat = Mock(return_value=recs_json)
        
        report = report_service.generate_report(
            topic="Test",
            use_rag=False
        )
        
        if report['recommendations']:
            rec = report['recommendations'][0]
            assert 'recommendation' in rec
            assert 'action' in rec
            assert 'timeline' in rec
            assert 'effort' in rec
    
    # ==================== REPORT TYPE TESTS ====================
    
    def test_report_types_supported(self, report_service):
        """Test different report types"""
        report_service.groq_client.chat = Mock(return_value="mocked")
        
        for report_type in ["general", "technical", "executive", "comparative"]:
            report = report_service.generate_report(
                topic="Test",
                report_type=report_type,
                use_rag=False
            )
            
            assert report['metadata']['report_type'] == report_type
    
    # ==================== RAG CONTEXT TESTS ====================
    
    def test_generate_with_custom_context(self, report_service):
        """Test report generation with custom context"""
        report_service.groq_client.chat = Mock(return_value="mocked response")
        
        report = report_service.generate_report(
            topic="Test",
            custom_context="Important: This is custom context",
            use_rag=False
        )
        
        assert report['metadata']['context_used'] == 'custom'
    
    def test_rag_context_flag(self, report_service):
        """Test RAG context flag in metadata"""
        report_service.groq_client.chat = Mock(return_value="mocked")
        
        report_with_rag = report_service.generate_report(
            topic="Test",
            use_rag=True,
            custom_context=""
        )
        
        report_without_rag = report_service.generate_report(
            topic="Test",
            use_rag=False,
            custom_context=""
        )
        
        # Context should be tracked
        assert report_with_rag['metadata']['context_used'] in ['rag', 'none', 'custom']
        assert report_without_rag['metadata']['context_used'] == 'none'
    
    # ==================== SPECIAL REPORT TYPES ====================
    
    def test_summarized_report_from_docs(self, report_service):
        """Test generating report from specific context documents"""
        report_service.groq_client.chat = Mock(return_value="mocked")
        
        docs = ["Document 1 content", "Document 2 content"]
        report = report_service.generate_summarized_report(
            topic="Test Summary",
            context_docs=docs
        )
        
        assert report['metadata']['topic'] == "Test Summary"
        assert report['metadata']['context_used'] == 'custom'
    
    def test_comparative_report(self, report_service):
        """Test generating comparative report"""
        report_service.groq_client.chat = Mock(return_value="mocked")
        
        items = ["Product A", "Product B", "Product C"]
        report = report_service.generate_comparative_report(items_to_compare=items)
        
        assert "Comparison" in report['metadata']['topic']
        assert report['metadata']['report_type'] == 'comparative'
    
    # ==================== TEMPLATE TESTS ====================
    
    def test_get_report_template(self, report_service):
        """Test getting empty report template"""
        template = report_service.get_report_template()
        
        assert template is not None
        assert 'title' in template
        assert 'executive_summary' in template
        assert 'overview' in template
        assert 'top_items' in template
        assert 'recommendations' in template
        assert 'metadata' in template
        
        # Verify initial values
        assert template['title'] == ""
        assert template['top_items'] == []
        assert template['recommendations'] == []
    
    # ==================== ERROR HANDLING TESTS ====================
    
    def test_json_parse_error_handling(self, report_service):
        """Test handling of invalid JSON from Groq"""
        # Mock invalid JSON response
        report_service.groq_client.chat = Mock(return_value="Invalid JSON {{{")
        
        report = report_service.generate_report(
            topic="Test",
            use_rag=False
        )
        
        # Should still return valid report structure even with parse errors
        assert report is not None
        assert 'title' in report
        assert 'top_items' in report
    
    def test_groq_connection_error(self, report_service):
        """Test handling of Groq connection errors"""
        report_service.groq_client.chat = Mock(side_effect=Exception("Connection failed"))
        
        with pytest.raises(Exception):
            report_service.generate_report(
                topic="Test",
                use_rag=False
            )
    
    # ==================== SINGLETON TESTS ====================
    
    def test_singleton_instance(self):
        """Test that singleton instance works"""
        with patch('services.report_service.GroqClient'):
            service1 = get_report_service()
            service2 = get_report_service()
            
            assert service1 is service2


class TestReportEndpoint:
    """Test Report REST API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create Flask test client"""
        from ai_service.app import app
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            yield client
    
    def test_generate_report_endpoint_success(self, client):
        """Test POST /generate-report success"""
        with patch('routes.report.report_service.generate_report') as mock_gen:
            mock_gen.return_value = {
                "title": "Test Report",
                "executive_summary": "Summary",
                "overview": "Overview",
                "top_items": [],
                "recommendations": [],
                "metadata": {}
            }
            
            response = client.post('/api/ai/generate-report', 
                json={"topic": "Test Topic"}
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert 'data' in data
    
    def test_generate_report_missing_topic(self, client):
        """Test POST /generate-report without topic"""
        response = client.post('/api/ai/generate-report',
            json={}
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'topic' in data['message'].lower()
    
    def test_generate_report_invalid_topic(self, client):
        """Test POST /generate-report with invalid topic"""
        response = client.post('/api/ai/generate-report',
            json={"topic": ""}
        )
        
        assert response.status_code == 400
    
    def test_report_types_endpoint(self, client):
        """Test GET /generate-report/types"""
        response = client.get('/api/ai/generate-report/types')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'data' in data
        assert isinstance(data['data'], dict)
    
    def test_report_template_endpoint(self, client):
        """Test GET /generate-report/template"""
        response = client.get('/api/ai/generate-report/template')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'data' in data
    
    def test_compare_report_endpoint(self, client):
        """Test POST /generate-report/compare"""
        with patch('routes.report.report_service.generate_comparative_report') as mock_gen:
            mock_gen.return_value = {
                "title": "Comparison",
                "executive_summary": "Summary",
                "overview": "Overview",
                "top_items": [],
                "recommendations": [],
                "metadata": {}
            }
            
            response = client.post('/api/ai/generate-report/compare',
                json={"items": ["Item A", "Item B"]}
            )
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'success'
    
    def test_compare_report_minimum_items(self, client):
        """Test compare report requires at least 2 items"""
        response = client.post('/api/ai/generate-report/compare',
            json={"items": ["Item A"]}
        )
        
        assert response.status_code == 400
    
    def test_invalid_top_items_count(self, client):
        """Test validation of top_items_count parameter"""
        response = client.post('/api/ai/generate-report',
            json={"topic": "Test", "top_items_count": 100}
        )
        
        assert response.status_code == 400


class TestReportContent:
    """Test generated report content quality"""
    
    @pytest.fixture
    def report_service(self):
        """Create a test report service"""
        with patch('services.report_service.GroqClient'):
            service = ReportService(groq_api_key="test_key")
            return service
    
    def test_timestamp_format(self, report_service):
        """Test that timestamp is valid ISO format"""
        report_service.groq_client.chat = Mock(return_value="mocked")
        
        report = report_service.generate_report(topic="Test", use_rag=False)
        
        timestamp = report['metadata']['generated_at']
        try:
            datetime.fromisoformat(timestamp)
        except ValueError:
            pytest.fail(f"Invalid timestamp format: {timestamp}")
    
    def test_impact_values(self, report_service):
        """Test that impact values are valid"""
        items_json = json.dumps([
            {
                "item_number": 1,
                "title": "Item",
                "description": "Desc",
                "impact": "high",
                "priority": 1
            }
        ])
        
        report_service.groq_client.chat = Mock(return_value=items_json)
        
        report = report_service.generate_report(topic="Test", use_rag=False)
        
        valid_impacts = ["high", "medium", "low"]
        for item in report['top_items']:
            assert item['impact'] in valid_impacts
    
    def test_timeline_values(self, report_service):
        """Test that timeline values are valid"""
        recs_json = json.dumps([
            {
                "recommendation": "Test",
                "action": "Do it",
                "timeline": "immediate",
                "effort": "low"
            }
        ])
        
        report_service.groq_client.chat = Mock(return_value=recs_json)
        
        report = report_service.generate_report(topic="Test", use_rag=False)
        
        valid_timelines = ["immediate", "short-term", "long-term"]
        for rec in report['recommendations']:
            assert rec['timeline'] in valid_timelines


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

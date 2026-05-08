import json
from unittest.mock import patch

import pytest

from app import app as flask_app


@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get('/api/ai/health')
    assert response.status_code == 200
    payload = response.get_json()

    assert payload is not None
    assert payload.get('model') == 'llama-3.3-70b-versatile'
    assert isinstance(payload.get('chroma_docs'), int)
    assert isinstance(payload.get('uptime_seconds'), float)
    assert payload.get('cache', {}).get('cached_items', 0) >= 0


@patch('routes.query.query_data')
@patch('services.groq_client.GroqClient.generate_response')
def test_query_endpoint(mock_generate_response, mock_query_data, client):
    mock_query_data.return_value = {
        'documents': [['The application crashes when logging in.']]
    }
    mock_generate_response.return_value = json.dumps({'answer': 'The crash occurs during login due to invalid credentials.'})

    response = client.post('/api/ai/query', json={'question': 'Why does the app crash on login?'})
    assert response.status_code == 200

    payload = response.get_json()
    assert payload['answer'] == 'The crash occurs during login due to invalid credentials.'
    assert payload['sources'] == ['The application crashes when logging in.']


@patch('services.groq_client.GroqClient.generate_response')
def test_categorise_endpoint(mock_generate_response, client):
    mock_generate_response.return_value = json.dumps({
        'category': 'Bug',
        'confidence': 0.97,
        'reasoning': 'The text describes an application failure that needs fixing.'
    })

    response = client.post('/api/ai/categorise', json={'text': 'The app crashes after clicking the login button.'})
    assert response.status_code == 200

    payload = response.get_json()
    assert payload['category'] == 'Bug'
    assert payload['confidence'] == 0.97
    assert 'reasoning' in payload


@patch('services.groq_client.GroqClient.generate_response')
def test_describe_endpoint(mock_generate_response, client):
    mock_generate_response.return_value = json.dumps({
        'title': 'Login Workflow Failure',
        'description': 'The application crashes when users attempt to log in, preventing access.',
        'severity': 'high',
        'type': 'bug',
        'key_points': ['Crash during login', 'Blocks user access', 'Requires immediate fix']
    })

    response = client.post('/api/ai/describe', json={'text': 'When users enter credentials, the login screen freezes and the app crashes.'})
    assert response.status_code == 200

    payload = response.get_json()
    assert payload['title'] == 'Login Workflow Failure'
    assert payload['severity'] == 'high'
    assert payload['type'] == 'bug'
    assert isinstance(payload['key_points'], list)
    assert payload['metadata']['cached'] is False


@patch('services.groq_client.GroqClient.generate_response')
def test_recommend_endpoint(mock_generate_response, client):
    mock_generate_response.return_value = json.dumps([
        {
            'action_type': 'fix',
            'description': 'Correct the login validation logic to prevent crashes.',
            'priority': 'high'
        },
        {
            'action_type': 'document',
            'description': 'Record the incident and add a regression test for login flows.',
            'priority': 'medium'
        },
        {
            'action_type': 'communicate',
            'description': 'Notify the team and escalate the bug to the engineering lead.',
            'priority': 'medium'
        }
    ])

    response = client.post('/api/ai/recommend', json={'text': 'The login flow crashes for some users after credential submission.'})
    assert response.status_code == 200

    payload = response.get_json()
    assert isinstance(payload, list)
    assert len(payload) == 3
    assert payload[0]['action_type'] == 'fix'
    assert payload[1]['priority'] == 'medium'


@patch('services.groq_client.GroqClient.generate_response')
def test_analyse_document_endpoint(mock_generate_response, client):
    mock_generate_response.return_value = json.dumps({
        'insights': [
            {
                'type': 'insight',
                'category': 'operational',
                'title': 'Login flow instability',
                'description': 'The login feature causes intermittent crashes, impacting user onboarding.',
                'severity': 'high',
                'confidence': 0.9
            }
        ],
        'risks': [
            {
                'type': 'risk',
                'category': 'operational',
                'title': 'Customer churn risk',
                'description': 'Customers may abandon the product after repeated login failures.',
                'severity': 'high',
                'confidence': 0.88
            }
        ]
    })

    sample_text = (
        'The document describes a recurring failure in the login module that prevents users from successfully signing in. '
        'This issue has caused multiple support tickets and a visible drop in user retention metrics.'
    )
    response = client.post('/api/ai/analyse-document', json={'text': sample_text})
    assert response.status_code == 200

    payload = response.get_json()
    assert payload['status'] == 'success'
    assert 'data' in payload
    assert len(payload['data']['insights']) == 1
    assert len(payload['data']['risks']) == 1
    assert payload['data']['metadata']['document_length'] == len(sample_text)


if __name__ == '__main__':
    pytest.main(['-q', __file__])

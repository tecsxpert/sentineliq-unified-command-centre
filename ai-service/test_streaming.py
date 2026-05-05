"""
Test script for SSE streaming report generation
"""
import requests
import json
import time

def test_streaming_report():
    """Test the streaming report generation endpoint"""

    # Test data
    test_data = {
        "topic": "AI Security Best Practices",
        "report_type": "technical",
        "use_rag": True,
        "custom_context": "",
        "top_items_count": 3
    }

    # API endpoint
    url = "http://localhost:5000/api/ai/generate-report?stream=true"

    print("Testing SSE streaming report generation...")
    print(f"Topic: {test_data['topic']}")
    print("-" * 50)

    try:
        # Make the request
        response = requests.post(url, json=test_data, stream=True)

        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            print(response.text)
            return

        print("Streaming response received. Processing events...")

        # Process the streaming response
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])  # Remove 'data: ' prefix
                        print(f"Event: {data}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse JSON: {line_str[6:]}")

        print("-" * 50)
        print("Streaming test completed!")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_streaming_report()
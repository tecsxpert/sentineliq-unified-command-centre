"""
Test script for document analysis endpoint
"""
import requests
import json

def test_analyse_document():
    """Test the document analysis endpoint"""

    # Sample document text for analysis
    test_data = {
        "text": """
        Company Security Report - Q4 2024

        Executive Summary:
        During Q4 2024, our organization experienced several security incidents that require immediate attention.
        The most critical issue was a data breach affecting 10,000 customer records due to an unpatched vulnerability
        in our legacy payment processing system. This resulted in significant financial losses and reputational damage.

        Key Findings:
        1. Outdated software versions across 40% of our infrastructure
        2. Insufficient access controls leading to privilege escalation
        3. Lack of proper encryption for sensitive data at rest
        4. Delayed security patch deployment processes

        Business Impact:
        The data breach cost approximately $2.5 million in remediation efforts, legal fees, and customer compensation.
        Customer trust has declined by 15% according to recent surveys. Regulatory fines are expected to exceed $500,000.

        Recommendations:
        - Implement automated patch management system
        - Conduct comprehensive security audit within 30 days
        - Enhance employee training programs
        - Deploy multi-factor authentication across all systems
        - Establish incident response team with 24/7 availability

        Risk Assessment:
        High-risk areas include customer data handling, third-party vendor access, and cloud infrastructure security.
        Medium-risk areas involve internal network segmentation and mobile device management.

        Compliance Status:
        Currently compliant with GDPR and CCPA requirements, but SOC 2 Type II certification is pending renewal.
        """,
        "focus_areas": ["security", "compliance", "business"]
    }

    # API endpoint
    url = "http://localhost:5000/api/ai/analyse-document"

    print("Testing document analysis endpoint...")
    print(f"Document length: {len(test_data['text'])} characters")
    print(f"Focus areas: {test_data['focus_areas']}")
    print("-" * 50)

    try:
        # Make the request
        response = requests.post(url, json=test_data)

        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            print(response.text)
            return

        result = response.json()

        if result.get('status') != 'success':
            print(f"API Error: {result.get('message', 'Unknown error')}")
            return

        data = result['data']

        print("✅ Analysis completed successfully!")
        print(f"📊 Insights found: {data['metadata']['insights_count']}")
        print(f"⚠️  Risks identified: {data['metadata']['risks_count']}")
        print()

        # Display insights
        if data.get('insights'):
            print("💡 INSIGHTS:")
            for i, insight in enumerate(data['insights'], 1):
                print(f"  {i}. [{insight['category'].upper()}] {insight['title']}")
                print(f"     Severity: {insight['severity']} | Confidence: {insight['confidence']}")
                print(f"     {insight['description']}")
                print()

        # Display risks
        if data.get('risks'):
            print("🚨 RISKS:")
            for i, risk in enumerate(data['risks'], 1):
                print(f"  {i}. [{risk['category'].upper()}] {risk['title']}")
                print(f"     Severity: {risk['severity']} | Confidence: {risk['confidence']}")
                print(f"     {risk['description']}")
                print()

        print(f"⏰ Analysis timestamp: {data['metadata']['analysis_timestamp']}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_analyse_document()
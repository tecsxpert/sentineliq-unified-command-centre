import os
import time
import json
import argparse
import requests

BASE_URL = os.getenv('AI_SERVICE_URL', 'http://localhost:5000/api/ai')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

DEMO_PAYLOADS = {
    'health': None,
    'query': {'question': 'Why does the app crash on login?'},
    'categorise': {'text': 'The app crashes after clicking login and the user loses their session.'},
    'describe': {'text': 'When users enter credentials, the login screen freezes and the app crashes.'},
    'recommend': {'text': 'The login flow crashes for some users after submitting their password.'},
    'analyse-document': {
        'text': (
            'The login module fails intermittently when users enter credentials. '
            'This failure has generated multiple support tickets and is linked to recurring drops in onboarding. '
            'Developers suspect the issue is caused by session initialization timing and error handling.'
        )
    }
}

EXPECTED_ENDPOINTS = [
    ('health', 'GET', '/health'),
    ('query', 'POST', '/query'),
    ('categorise', 'POST', '/categorise'),
    ('describe', 'POST', '/describe'),
    ('recommend', 'POST', '/recommend'),
    ('analyse-document', 'POST', '/analyse-document')
]


def call_endpoint(session, method, url, json_body=None):
    start = time.monotonic()
    if method == 'GET':
        response = session.get(url, timeout=60)
    else:
        response = session.post(url, json=json_body, timeout=60)
    elapsed = time.monotonic() - start
    return response, elapsed


def run_demo(base_url):
    if not GROQ_API_KEY:
        print('ERROR: GROQ_API_KEY is not set in the environment.')
        print('Set GROQ_API_KEY in your shell or .env before running this script.')
        return 1

    session = requests.Session()
    session.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

    results = []
    for name, method, path in EXPECTED_ENDPOINTS:
        full_url = f'{base_url}{path}'
        payload = DEMO_PAYLOADS.get(name)
        print(f'Calling {name} -> {method} {full_url}')

        try:
            response, elapsed = call_endpoint(session, method, full_url, payload)
            body = None
            try:
                body = response.json()
            except json.JSONDecodeError:
                body = response.text

            success = response.status_code == 200
            results.append({
                'endpoint': name,
                'method': method,
                'url': full_url,
                'status_code': response.status_code,
                'elapsed_seconds': round(elapsed, 4),
                'response_body': body,
                'success': success
            })
            print(f'  status={response.status_code}, time={elapsed:.4f}s')
        except Exception as exc:
            print(f'  ERROR: {exc}')
            results.append({
                'endpoint': name,
                'method': method,
                'url': full_url,
                'status_code': None,
                'elapsed_seconds': None,
                'response_body': str(exc),
                'success': False
            })

    output_file = 'day17_live_dry_run_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'base_url': base_url, 'results': results}, f, indent=2)

    print('\nDry run complete. Results written to', output_file)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Day 17 live AI endpoint dry run.')
    parser.add_argument('--base-url', default=BASE_URL, help='Base API URL for the service')
    args = parser.parse_args()
    exit(run_demo(args.base_url))

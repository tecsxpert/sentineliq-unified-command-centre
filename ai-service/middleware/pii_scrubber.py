import re

# Simple PII patterns
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_PATTERN = r'\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}'
IP_PATTERN = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

def scrub_pii(text):
    if not isinstance(text, str):
        return text
    
    text = re.sub(EMAIL_PATTERN, '[EMAIL]', text)
    text = re.sub(PHONE_PATTERN, '[PHONE]', text)
    # text = re.sub(IP_PATTERN, '[IP]', text) # IPs might be relevant for security analysis
    
    return text

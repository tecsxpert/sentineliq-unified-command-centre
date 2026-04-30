import os
import jwt
from flask import request, jsonify

JWT_SECRET = os.getenv("JWT_SECRET", "sentineliq-secret-key") # Default for dev

def auth_middleware():
    # Allow health check without auth
    if request.path == '/health':
        return

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401

    try:
        token = auth_header.split(" ")[1]
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except Exception as e:
        return jsonify({"error": "Invalid or expired token"}), 401

import json
from flask import Blueprint, jsonify, request
from services.groq_client import GroqClient
from services.chroma_service import query_data

# Create blueprint
query_bp = Blueprint('query', __name__)

client = GroqClient()

def query_with_context(user_question):
    try:
        context = "The app crashes when I login. The UI looks clean and modern. Feature request: add dark mode."

        prompt = f"""
        You are an AI assistant.

        STRICT RULES:
        - Answer ONLY using the provided context
        - If answer is not found, say: "No relevant information found"
        - Do NOT guess or assume
        - Keep answer short and clear

        Context:
        {context}

        Question:
        {user_question}

        Return only the answer.
        """

        result = client.generate_response(prompt)

        answer = result.get("response", "")
        meta = result.get("meta", {})

        sources = [
            "The app crashes when I login",
            "The UI looks clean and modern",
            "Feature request: add dark mode"
        ]

        return {
            "answer": answer,
            "sources": sources,
            "meta": meta
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@query_bp.route('/query', methods=['POST'])
def query_endpoint():
    """
    Query endpoint for RAG-based question answering
    
    Request JSON:
    {
        "question": "Your question here"
    }
    
    Response JSON:
    {
        "answer": "Answer text",
        "sources": ["source 1", "source 2", ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "Missing 'question' field"}), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400
        
        result = query_with_context(question)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        return {"error": str(e)}

import json
from flask import Blueprint, jsonify, request
from services.groq_client import GroqClient
from services.chroma_service import query_data

# Create blueprint
query_bp = Blueprint('query', __name__)

client = GroqClient()

def query_with_context(user_question):
    try:
        #Step 1: Get top 3 results
        results = query_data(user_question)
        documents = results.get("documents", [[]])[0]

        #Step 2: Prepare context
        context = "\n".join(documents)

        #Step 3: Prompt
        prompt = f"""
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{user_question}

STRICT RULES:
- Do NOT use markdown
- Do NOT use ```
- Do NOT add extra explanation
- Use only the context
- Return ONLY valid JSON

Format:
{{
    "answer": ""
}}
"""

        #Step 4: Call Groq
        response = client.generate_response(prompt)

        #Step 5: Extract clean answer
        try:
            parsed = json.loads(response)
            answer_text = parsed.get("answer", response)
        except:
            answer_text = response

        #Step 6: Return final output
        return {
            "answer": answer_text,
            "sources": documents
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
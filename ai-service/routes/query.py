import json
from services.groq_client import GroqClient
from services.chroma_service import query_data

client = GroqClient()

def query_with_context(user_question):
    try:
        # Step 1: Get top results from ChromaDB
        results = query_data(user_question)

        documents = results.get("documents", [[]])[0]

        # Step 2: Prepare context
        context = "\n".join(documents)

        # Step 3: Create prompt
        prompt = f"""
        Use the following context to answer the question.

        Context:
        {context}

        Question:
        {user_question}

        Return ONLY in this JSON format:
        {{
            "answer": ""
        }}
        """

        # Step 4: Call Groq
        response = client.generate_response(prompt)

        # Step 5: Extract clean answer
        try:
            parsed = json.loads(response)
            answer_text = parsed.get("answer", response)
        except:
            answer_text = response

        # Step 6: Return final output
        return {
            "answer": answer_text,
            "sources": documents
        }

    except Exception as e:
        return {
            "error": str(e)
        }
from services.groq_client import GroqClient
from services.chroma_service import query_data

client = GroqClient()


def query_with_context(user_question):
    try:
        results = query_data(user_question)
        documents = results.get("documents", [[]])[0]

        context = "\n".join(documents)

        prompt = f"""
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{user_question}

Return only the answer.
"""

        response = client.generate_response(prompt)

        return {
            "answer": response["response"],
            "sources": documents,
            "meta": response["meta"]
        }

    except Exception as e:
        return {"error": str(e)}
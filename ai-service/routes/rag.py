"""
RAG Route - REST endpoints for RAG pipeline
"""
from flask import Blueprint, request, jsonify
from services.rag_service import get_rag_service
import os

rag_bp = Blueprint('rag', __name__)

# Initialize RAG service
rag_service = get_rag_service()


@rag_bp.route('/rag/health', methods=['GET'])
def rag_health():
    """Check RAG service health"""
    try:
        stats = rag_service.get_collection_stats()
        return jsonify({
            "status": "healthy",
            "service": "RAG Pipeline",
            "collection_stats": stats
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@rag_bp.route('/rag/upload', methods=['POST'])
def upload_documents():
    """
    Upload and process documents
    Expected JSON: {
        "file_paths": ["path/to/doc1.txt", "path/to/doc2.pdf"],
        "metadata": {"category": "support_docs", ...}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'file_paths' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'file_paths' in request"
            }), 400
        
        file_paths = data['file_paths']
        metadata = data.get('metadata', {})
        
        # Verify files exist
        for file_path in file_paths:
            if not os.path.exists(file_path):
                return jsonify({
                    "status": "error",
                    "message": f"File not found: {file_path}"
                }), 400
        
        # Process documents
        stats = rag_service.add_documents(file_paths, metadata)
        
        return jsonify({
            "status": "success",
            "message": "Documents processed and stored",
            "statistics": stats
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@rag_bp.route('/rag/retrieve', methods=['POST'])
def retrieve_documents():
    """
    Retrieve relevant documents for a query
    Expected JSON: {
        "query": "search query text",
        "n_results": 5
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'query' in request"
            }), 400
        
        query = data['query']
        n_results = data.get('n_results', 5)
        
        results = rag_service.retrieve_documents(query, n_results)
        
        return jsonify({
            "status": "success",
            "data": results
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@rag_bp.route('/rag/stats', methods=['GET'])
def get_stats():
    """Get collection statistics"""
    try:
        stats = rag_service.get_collection_stats()
        return jsonify({
            "status": "success",
            "statistics": stats
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@rag_bp.route('/rag/clear', methods=['DELETE'])
def clear_collection():
    """Clear all documents from collection"""
    try:
        rag_service.delete_all_documents()
        return jsonify({
            "status": "success",
            "message": "Collection cleared"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@rag_bp.route('/rag/export', methods=['GET'])
def export_collection():
    """Export collection to JSON file"""
    try:
        output_file = request.args.get('output_file', 'rag_export.json')
        rag_service.export_collection(output_file)
        return jsonify({
            "status": "success",
            "message": f"Collection exported to {output_file}"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

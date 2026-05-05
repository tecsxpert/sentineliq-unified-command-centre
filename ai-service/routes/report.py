"""
Report Generation Route - REST endpoint for report generation
POST /api/ai/generate-report
"""
from flask import Blueprint, request, jsonify, Response, stream_with_context
from services.report_service import get_report_service
import json

report_bp = Blueprint('report', __name__)

# Initialize report service
report_service = get_report_service()


@report_bp.route('/generate-report', methods=['POST'])
def generate_report():
    """
    Generate a comprehensive report

    Query parameters:
    - stream: boolean (optional, default: false) - Enable SSE streaming

    Expected JSON:
    {
        "topic": "string (required) - Report topic",
        "report_type": "string (optional, default: 'general') - Type: general, technical, executive, comparative",
        "use_rag": "boolean (optional, default: true) - Use RAG for context",
        "custom_context": "string (optional) - Custom context to include",
        "top_items_count": "integer (optional, default: 5) - Number of top items",
        "context_documents": "array (optional) - Specific documents for context"
    }

    Returns (regular):
    {
        "status": "success",
        "data": { ... report data ... }
    }

    Returns (streaming): SSE events with different event types
    """
    try:
        # Check if streaming is requested
        stream_param = request.args.get('stream', 'false').lower()
        is_streaming = stream_param in ('true', '1', 'yes')

        data = request.get_json()

        # Validate required fields
        if not data or 'topic' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required field: 'topic'"
            }), 400

        topic = data['topic']
        if not isinstance(topic, str) or len(topic.strip()) == 0:
            return jsonify({
                "status": "error",
                "message": "Topic must be a non-empty string"
            }), 400

        # Extract optional parameters
        report_type = data.get('report_type', 'general')
        use_rag = data.get('use_rag', True)
        custom_context = data.get('custom_context', '')
        top_items_count = data.get('top_items_count', 5)
        context_documents = data.get('context_documents', [])

        # Validate parameters
        if not isinstance(report_type, str):
            return jsonify({
                "status": "error",
                "message": "report_type must be a string"
            }), 400

        if not isinstance(use_rag, bool):
            return jsonify({
                "status": "error",
                "message": "use_rag must be a boolean"
            }), 400

        if not isinstance(top_items_count, int) or top_items_count < 1 or top_items_count > 15:
            return jsonify({
                "status": "error",
                "message": "top_items_count must be an integer between 1 and 15"
            }), 400

        # Handle context documents
        if context_documents:
            if not isinstance(context_documents, list):
                return jsonify({
                    "status": "error",
                    "message": "context_documents must be an array"
                }), 400

            # Use context documents instead of RAG
            if is_streaming:
                return Response(
                    stream_with_context(report_service.generate_streaming_summarized_report(topic, context_documents)),
                    content_type='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}
                )
            else:
                report = report_service.generate_summarized_report(topic, context_documents)
        else:
            # Generate report with specified parameters
            if is_streaming:
                return Response(
                    stream_with_context(report_service.generate_streaming_report(
                        topic=topic,
                        report_type=report_type,
                        use_rag=use_rag,
                        custom_context=custom_context,
                        top_items_count=top_items_count
                    )),
                    content_type='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}
                )
            else:
                report = report_service.generate_report(
                    topic=topic,
                    report_type=report_type,
                    use_rag=use_rag,
                    custom_context=custom_context,
                    top_items_count=top_items_count
                )

        return jsonify({
            "status": "success",
            "data": report
        }), 200

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid parameter: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@report_bp.route('/generate-report/template', methods=['GET'])
def get_report_template():
    """Get empty report template"""
    template = report_service.get_report_template()
    return jsonify({
        "status": "success",
        "data": template
    }), 200


@report_bp.route('/generate-report/types', methods=['GET'])
def get_report_types():
    """Get supported report types"""
    report_types = {
        "general": "General purpose report with overview and recommendations",
        "technical": "Technical report focused on implementation details",
        "executive": "Executive summary with key metrics and decisions",
        "comparative": "Comparison report between multiple items",
        "analysis": "In-depth analysis with detailed breakdown"
    }
    return jsonify({
        "status": "success",
        "data": report_types
    }), 200


@report_bp.route('/generate-report/preview', methods=['POST'])
def generate_report_preview():
    """
    Generate a quick report preview (faster, limited content)
    Useful for progress indication
    """
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required field: 'topic'"
            }), 400
        
        topic = data['topic']
        report_type = data.get('report_type', 'general')
        
        # Generate report with fewer items for preview
        report = report_service.generate_report(
            topic=topic,
            report_type=report_type,
            use_rag=True,
            top_items_count=3
        )
        
        return jsonify({
            "status": "success",
            "data": report
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@report_bp.route('/generate-report/compare', methods=['POST'])
def generate_comparative_report():
    """
    Generate comparative report for multiple items
    
    Expected JSON:
    {
        "items": ["item1", "item2", "item3", ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'items' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required field: 'items'"
            }), 400
        
        items = data['items']
        
        if not isinstance(items, list) or len(items) < 2:
            return jsonify({
                "status": "error",
                "message": "items must be an array with at least 2 elements"
            }), 400
        
        report = report_service.generate_comparative_report(items)
        
        return jsonify({
            "status": "success",
            "data": report
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

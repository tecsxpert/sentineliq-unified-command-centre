"""
Day 11: Batch Processing Endpoint
Processes up to 20 items concurrently with 100ms delay per item
"""
import asyncio
import json
import time
from flask import Blueprint, request, jsonify
from services.batch_service import BatchProcessor

# Create blueprint
batch_bp = Blueprint('batch', __name__)

batch_processor = BatchProcessor()


def validate_batch_input(data):
    """Validate batch processing input"""
    try:
        if not isinstance(data, dict):
            return False, "Request must be JSON object", None
        
        items = data.get('items', [])
        
        if not isinstance(items, list):
            return False, "Items must be an array", None
        
        if len(items) == 0:
            return False, "Items array cannot be empty", None
        
        if len(items) > 20:
            return False, f"Maximum 20 items allowed, got {len(items)}", None
        
        # Validate each item
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                return False, f"Item {idx} must be an object", None
            
            if 'text' not in item:
                return False, f"Item {idx} missing 'text' field", None
            
            if not isinstance(item['text'], str) or len(item['text'].strip()) == 0:
                return False, f"Item {idx} text must be non-empty string", None
        
        return True, "", items
    
    except Exception as e:
        return False, f"Validation error: {str(e)}", None


@batch_bp.route('/batch-process', methods=['POST'])
def batch_process():
    """
    Batch process items with 100ms delay per item
    
    Request:
    {
        "items": [
            {"text": "First item"},
            {"text": "Second item"},
            ...
        ]
    }
    
    Response:
    {
        "status": "success",
        "total_items": 2,
        "processed": 2,
        "results": [
            {"id": 0, "text": "First item", "processed": true, "timestamp": "..."},
            {"id": 1, "text": "Second item", "processed": true, "timestamp": "..."}
        ],
        "total_time": 0.24,
        "timestamp": "..."
    }
    """
    try:
        data = request.get_json()
        
        is_valid, error_msg, items = validate_batch_input(data)
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": error_msg
            }), 400
        
        # Process batch
        start_time = time.time()
        results = batch_processor.process_batch(items)
        total_time = time.time() - start_time
        
        return jsonify({
            "status": "success",
            "total_items": len(items),
            "processed": len(results),
            "results": results,
            "total_time": round(total_time, 3),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@batch_bp.route('/batch-process/status', methods=['GET'])
def batch_status():
    """Get batch processor status and statistics"""
    try:
        status = batch_processor.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

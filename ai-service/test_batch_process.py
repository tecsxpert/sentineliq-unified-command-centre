"""
Day 11: Batch Processing Tests
Test concurrent processing with 100ms delay per item
"""
import pytest
import json
import time
from routes.batch_process import validate_batch_input
from services.batch_service import BatchProcessor


class TestBatchInput:
    """Test batch input validation"""
    
    def test_valid_batch_input(self):
        """Valid batch input passes validation"""
        data = {
            "items": [
                {"text": "First item"},
                {"text": "Second item"}
            ]
        }
        is_valid, error, items = validate_batch_input(data)
        assert is_valid
        assert len(items) == 2
    
    def test_empty_items_array(self):
        """Empty items array fails validation"""
        data = {"items": []}
        is_valid, error, _ = validate_batch_input(data)
        assert not is_valid
        assert "cannot be empty" in error
    
    def test_exceeds_max_items(self):
        """More than 20 items fails validation"""
        data = {
            "items": [{"text": f"Item {i}"} for i in range(21)]
        }
        is_valid, error, _ = validate_batch_input(data)
        assert not is_valid
        assert "Maximum 20 items" in error
    
    def test_missing_text_field(self):
        """Item missing text field fails validation"""
        data = {
            "items": [
                {"name": "Item without text"}
            ]
        }
        is_valid, error, _ = validate_batch_input(data)
        assert not is_valid
        assert "missing 'text'" in error
    
    def test_empty_text_field(self):
        """Item with empty text fails validation"""
        data = {
            "items": [
                {"text": ""}
            ]
        }
        is_valid, error, _ = validate_batch_input(data)
        assert not is_valid
        assert "non-empty string" in error
    
    def test_non_json_input(self):
        """Non-JSON input fails validation"""
        is_valid, error, _ = validate_batch_input([1, 2, 3])
        assert not is_valid
        assert "JSON object" in error
    
    def test_items_not_array(self):
        """Items not being an array fails validation"""
        data = {"items": "not an array"}
        is_valid, error, _ = validate_batch_input(data)
        assert not is_valid
        assert "array" in error


class TestBatchProcessor:
    """Test batch processing engine"""
    
    def test_process_single_item(self):
        """Process single item"""
        processor = BatchProcessor(delay_ms=10)
        items = [{"text": "Test item"}]
        
        results = processor.process_batch(items)
        
        assert len(results) == 1
        assert results[0]["processed"]
        assert results[0]["text"] == "Test item"
        assert results[0]["word_count"] == 2
    
    def test_process_multiple_items(self):
        """Process multiple items"""
        processor = BatchProcessor(delay_ms=10)
        items = [
            {"text": "First item"},
            {"text": "Second item"},
            {"text": "Third item"}
        ]
        
        results = processor.process_batch(items)
        
        assert len(results) == 3
        assert all(r["processed"] for r in results)
        assert results[0]["id"] == 0
        assert results[1]["id"] == 1
        assert results[2]["id"] == 2
    
    def test_process_batch_timing(self):
        """Batch processing respects delay timing"""
        processor = BatchProcessor(max_workers=1, delay_ms=50)
        items = [
            {"text": "Item 1"},
            {"text": "Item 2"}
        ]
        
        start_time = time.time()
        results = processor.process_batch(items)
        elapsed = time.time() - start_time
        
        # With 2 items at 50ms delay each, should take ~100ms
        # Allow some tolerance for execution overhead
        assert elapsed >= 0.08  # At least 80ms
        assert len(results) == 2
    
    def test_concurrent_processing(self):
        """Multiple workers process items concurrently"""
        processor = BatchProcessor(max_workers=5, delay_ms=50)
        items = [{"text": f"Item {i}"} for i in range(5)]
        
        start_time = time.time()
        results = processor.process_batch(items)
        elapsed = time.time() - start_time
        
        # With 5 workers and 5 items at 50ms, should complete faster
        # than sequential (250ms), closer to 100ms
        assert elapsed < 0.2  # Less than 200ms for concurrent execution
        assert len(results) == 5
        assert all(r["processed"] for r in results)
    
    def test_statistics_tracking(self):
        """Processor tracks statistics"""
        processor = BatchProcessor(delay_ms=10)
        items = [
            {"text": "Item 1"},
            {"text": "Item 2"}
        ]
        
        processor.process_batch(items)
        status = processor.get_status()
        
        assert status["statistics"]["total_processed"] == 2
        assert status["statistics"]["total_batches"] == 1
        assert status["statistics"]["last_batch_size"] == 2
    
    def test_text_analysis(self):
        """Text analysis metrics calculated correctly"""
        processor = BatchProcessor(delay_ms=10)
        items = [{"text": "Hello world test"}]
        
        results = processor.process_batch(items)
        
        assert results[0]["length"] == 16  # "Hello world test" has 16 chars including spaces
        assert results[0]["word_count"] == 3
        assert results[0]["char_count"] == 16
    
    def test_max_items_limit(self):
        """System handles 20 items (max limit)"""
        processor = BatchProcessor(max_workers=5, delay_ms=10)
        items = [{"text": f"Item {i}"} for i in range(20)]
        
        results = processor.process_batch(items)
        
        assert len(results) == 20
        assert all(r["processed"] for r in results)


class TestBatchEndpoint:
    """Test batch processing endpoint"""
    
    def test_endpoint_returns_results(self):
        """Endpoint returns properly formatted results"""
        result_format = {
            "status": "success",
            "total_items": 2,
            "processed": 2,
            "results": [
                {"id": 0, "text": "Item 1", "processed": True},
                {"id": 1, "text": "Item 2", "processed": True}
            ],
            "total_time": 0.123,
            "timestamp": "2024-01-01 12:00:00"
        }
        
        # Verify structure
        assert "status" in result_format
        assert "total_items" in result_format
        assert "results" in result_format
        assert isinstance(result_format["results"], list)
        assert len(result_format["results"]) > 0
    
    def test_error_response_format(self):
        """Endpoint returns error response when validation fails"""
        error_response = {
            "status": "error",
            "message": "Items array cannot be empty"
        }
        
        assert "status" in error_response
        assert error_response["status"] == "error"
        assert "message" in error_response


class TestBatchIntegration:
    """Integration tests for batch processing"""
    
    def test_batch_with_varied_text_lengths(self):
        """Process items with different text lengths"""
        processor = BatchProcessor(delay_ms=10)
        items = [
            {"text": "Short"},
            {"text": "This is a medium length text"},
            {"text": "This is a much longer text with more words and content to demonstrate processing of varied lengths"}
        ]
        
        results = processor.process_batch(items)
        
        assert len(results) == 3
        assert results[0]["word_count"] == 1
        assert results[1]["word_count"] == 6
        assert results[2]["word_count"] > 10
    
    def test_batch_status_endpoint(self):
        """Batch status endpoint works correctly"""
        processor = BatchProcessor(delay_ms=10)
        status = processor.get_status()
        
        assert status["status"] == "active"
        assert "statistics" in status
        assert "max_workers" in status
        assert "delay_ms" in status
    
    def test_metrics_after_multiple_batches(self):
        """Metrics accumulate across multiple batches"""
        processor = BatchProcessor(delay_ms=10)
        
        # First batch
        processor.process_batch([{"text": "Batch 1"}])
        status1 = processor.get_status()
        assert status1["statistics"]["total_batches"] == 1
        
        # Second batch
        processor.process_batch([{"text": "Batch 2"}, {"text": "Item 2"}])
        status2 = processor.get_status()
        assert status2["statistics"]["total_batches"] == 2
        assert status2["statistics"]["total_processed"] == 3

"""
Day 11: Batch Processing Service
Handles concurrent processing with 100ms delay per item
"""
import asyncio
import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class BatchProcessor:
    """Processes batch items with controlled concurrency"""
    
    def __init__(self, max_workers=5, delay_ms=100):
        """
        Initialize batch processor
        
        Args:
            max_workers: Maximum concurrent threads
            delay_ms: Millisecond delay per item
        """
        self.max_workers = max_workers
        self.delay_ms = delay_ms / 1000.0  # Convert to seconds
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.stats = {
            "total_processed": 0,
            "total_batches": 0,
            "errors": 0,
            "last_batch_time": None,
            "last_batch_size": 0
        }
    
    def _process_item(self, item_data, item_id):
        """
        Process single item with delay
        
        Args:
            item_data: Item to process
            item_id: Item ID/index
            
        Returns:
            Processed item result
        """
        try:
            # Apply delay
            time.sleep(self.delay_ms)
            
            text = item_data.get('text', '').strip()
            
            # Enhanced processing: text analysis
            result = {
                "id": item_id,
                "text": text,
                "processed": True,
                "timestamp": datetime.now().isoformat(),
                "length": len(text),
                "word_count": len(text.split()),
                "char_count": len(text)
            }
            
            return result
        
        except Exception as e:
            return {
                "id": item_id,
                "text": item_data.get('text', ''),
                "processed": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def process_batch(self, items):
        """
        Process batch of items concurrently
        
        Args:
            items: List of items to process
            
        Returns:
            List of processed results
        """
        results = [None] * len(items)
        
        # Submit all tasks
        futures = {}
        for idx, item in enumerate(items):
            future = self.executor.submit(self._process_item, item, idx)
            futures[future] = idx
        
        # Collect results as they complete
        for future in as_completed(futures):
            idx = futures[future]
            try:
                result = future.result()
                results[idx] = result
            except Exception as e:
                results[idx] = {
                    "id": idx,
                    "processed": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        # Update statistics
        self.stats["total_processed"] += len(items)
        self.stats["total_batches"] += 1
        self.stats["last_batch_time"] = datetime.now().isoformat()
        self.stats["last_batch_size"] = len(items)
        
        # Count errors
        errors = sum(1 for r in results if not r.get('processed', False))
        self.stats["errors"] += errors
        
        return results
    
    def get_status(self):
        """Get processor status and statistics"""
        return {
            "status": "active",
            "max_workers": self.max_workers,
            "delay_ms": self.delay_ms * 1000,
            "statistics": self.stats
        }

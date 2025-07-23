"""
Progress tracking utilities for CallRail data extractor.
"""
from typing import Dict, Optional, Any
from tqdm import tqdm
from utils.logger import logger


class ProgressTracker:
    """Manages progress bars for data extraction."""
    
    def __init__(self):
        self.progress_bars: Dict[str, tqdm] = {}
        self.main_progress: Optional[tqdm] = None
    
    def create_main_progress(self, total_endpoints: int, description: str = "Overall Progress"):
        """Create the main progress bar for overall extraction."""
        self.main_progress = tqdm(
            total=total_endpoints,
            desc=description,
            position=0,
            leave=True,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
        )
        return self.main_progress
    
    def create_endpoint_progress(self, endpoint_name: str, total_records: int) -> tqdm:
        """Create a progress bar for a specific endpoint."""
        position = len(self.progress_bars) + 1
        progress_bar = tqdm(
            total=total_records,
            desc=f"Extracting {endpoint_name}",
            position=position,
            leave=False,
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
        )
        self.progress_bars[endpoint_name] = progress_bar
        return progress_bar
    
    def update_endpoint_progress(self, endpoint_name: str, increment: int = 1):
        """Update progress for a specific endpoint."""
        if endpoint_name in self.progress_bars:
            self.progress_bars[endpoint_name].update(increment)
    
    def update_main_progress(self, increment: int = 1):
        """Update the main progress bar."""
        if self.main_progress:
            self.main_progress.update(increment)
    
    def set_endpoint_description(self, endpoint_name: str, description: str):
        """Set a custom description for an endpoint progress bar."""
        if endpoint_name in self.progress_bars:
            self.progress_bars[endpoint_name].set_description(description)
    
    def finish_endpoint(self, endpoint_name: str, success: bool = True):
        """Finish and close an endpoint progress bar."""
        if endpoint_name in self.progress_bars:
            progress_bar = self.progress_bars[endpoint_name]
            if success:
                progress_bar.set_description(f"✓ {endpoint_name} completed")
            else:
                progress_bar.set_description(f"✗ {endpoint_name} failed")
            progress_bar.close()
            del self.progress_bars[endpoint_name]
    
    def finish_all(self):
        """Close all progress bars."""
        # Close endpoint progress bars
        for endpoint_name in list(self.progress_bars.keys()):
            self.finish_endpoint(endpoint_name)
        
        # Close main progress bar
        if self.main_progress:
            self.main_progress.close()
            self.main_progress = None
    
    def log_progress_summary(self, endpoint_name: str, records_processed: int, 
                           total_time: float, errors: int = 0):
        """Log a summary of progress for an endpoint."""
        rate = records_processed / total_time if total_time > 0 else 0
        logger.info(
            f"Endpoint '{endpoint_name}' completed: "
            f"{records_processed} records in {total_time:.2f}s "
            f"({rate:.2f} records/sec, {errors} errors)"
        )
    
    def get_endpoint_progress(self, endpoint_name: str) -> Optional[Dict[str, Any]]:
        """Get current progress information for an endpoint."""
        if endpoint_name not in self.progress_bars:
            return None
        
        progress_bar = self.progress_bars[endpoint_name]
        return {
            'current': progress_bar.n,
            'total': progress_bar.total,
            'percentage': (progress_bar.n / progress_bar.total * 100) if progress_bar.total > 0 else 0,
            'rate': progress_bar.format_dict.get('rate', 0),
            'elapsed': progress_bar.format_dict.get('elapsed', 0),
            'remaining': progress_bar.format_dict.get('remaining', 0)
        }


class BatchProgressTracker:
    """Tracks progress for batch processing within an endpoint."""
    
    def __init__(self, endpoint_name: str, total_records: int, batch_size: int):
        self.endpoint_name = endpoint_name
        self.total_records = total_records
        self.batch_size = batch_size
        self.processed_records = 0
        self.current_batch = 0
        self.total_batches = (total_records + batch_size - 1) // batch_size
        
        self.progress_bar = tqdm(
            total=total_records,
            desc=f"Processing {endpoint_name}",
            unit="records",
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} records [{elapsed}<{remaining}, {rate_fmt}]'
        )
    
    def start_batch(self, batch_number: int, batch_size: int):
        """Start processing a new batch."""
        self.current_batch = batch_number
        self.progress_bar.set_description(
            f"Processing {self.endpoint_name} (batch {batch_number}/{self.total_batches})"
        )
    
    def update_batch_progress(self, records_processed: int):
        """Update progress within the current batch."""
        increment = records_processed - self.processed_records
        if increment > 0:
            self.progress_bar.update(increment)
            self.processed_records = records_processed
    
    def finish_batch(self, records_in_batch: int):
        """Finish the current batch."""
        self.update_batch_progress(self.processed_records + records_in_batch)
    
    def finish(self):
        """Finish the batch progress tracker."""
        self.progress_bar.close()
    
    def get_progress_info(self) -> Dict[str, Any]:
        """Get current progress information."""
        return {
            'endpoint': self.endpoint_name,
            'current_batch': self.current_batch,
            'total_batches': self.total_batches,
            'processed_records': self.processed_records,
            'total_records': self.total_records,
            'percentage': (self.processed_records / self.total_records * 100) if self.total_records > 0 else 0
        }


# Global progress tracker instance
progress_tracker = ProgressTracker()

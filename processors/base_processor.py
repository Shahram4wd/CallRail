"""
Base processor class for CallRail API endpoints.
"""
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Generator
from callrail_api.client import CallRailClient
from config.endpoints import endpoint_registry, EndpointConfig
from config.settings import settings
from utils.logger import logger
from utils.retry_handler import with_retry, handle_rate_limit
from utils.progress_tracker import BatchProgressTracker
from utils.csv_writer import csv_writer
from models.extended_models import create_model_instance


class BaseProcessor(ABC):
    """Base class for all endpoint processors."""
    
    def __init__(self, client: CallRailClient, endpoint_name: str):
        self.client = client
        self.endpoint_name = endpoint_name
        self.endpoint_config = endpoint_registry.get_endpoint(endpoint_name)
        
        if not self.endpoint_config:
            raise ValueError(f"Unknown endpoint: {endpoint_name}")
        
        self.batch_size = settings.batch.default_batch_size
        self.max_records = settings.api.max_records_per_endpoint
        self.progress_tracker: Optional[BatchProgressTracker] = None
        
        logger.info(f"Initialized processor for endpoint: {endpoint_name}")
    
    @abstractmethod
    def get_account_id(self) -> str:
        """Get the account ID for API calls."""
        pass
    
    def get_company_id(self) -> Optional[str]:
        """Get the first company ID for API calls that require it."""
        try:
            # Try to get the first company from the companies endpoint
            from processors.generic_processor import CompaniesProcessor
            companies_processor = CompaniesProcessor(self.client, self.get_account_id())
            
            # Fetch just one company
            companies = companies_processor.fetch_batch(0, 1)
            if companies and len(companies) > 0:
                return companies[0].get('id')
        except Exception as e:
            logger.warning(f"Could not get company_id: {str(e)}")
        
        return None
    
    def process_endpoint(self, limit: Optional[int] = None, 
                        batch_size: Optional[int] = None) -> Dict[str, Any]:
        """Process the entire endpoint and save to CSV."""
        start_time = time.time()
        
        # Use provided parameters or defaults
        actual_limit = limit or self.max_records
        actual_batch_size = batch_size or self.batch_size
        
        logger.info(f"Starting processing for {self.endpoint_name} "
                   f"(limit: {actual_limit}, batch_size: {actual_batch_size})")
        
        try:
            # Initialize progress tracker
            self.progress_tracker = BatchProgressTracker(
                self.endpoint_name, actual_limit, actual_batch_size
            )
            
            # Collect all records
            all_records = []
            error_count = 0
            
            for batch_records, batch_errors in self.process_in_batches(
                actual_limit, actual_batch_size
            ):
                all_records.extend(batch_records)
                error_count += batch_errors
                
                # Update progress
                self.progress_tracker.update_batch_progress(len(all_records))
                
                # Break if we've reached the limit
                if len(all_records) >= actual_limit:
                    all_records = all_records[:actual_limit]
                    break
            
            # Write to CSV
            csv_path = ""
            if all_records:
                fieldnames = endpoint_registry.get_all_fields(self.endpoint_name)
                csv_path = csv_writer.write_records(
                    self.endpoint_name, all_records, fieldnames
                )
            
            # Finish progress tracking
            if self.progress_tracker:
                self.progress_tracker.finish()
            
            # Calculate metrics
            end_time = time.time()
            total_time = end_time - start_time
            
            result = {
                'endpoint': self.endpoint_name,
                'records_processed': len(all_records),
                'errors': error_count,
                'total_time': total_time,
                'csv_file': csv_path,
                'success': len(all_records) > 0 or error_count == 0
            }
            
            logger.info(f"Completed {self.endpoint_name}: {len(all_records)} records "
                       f"in {total_time:.2f}s with {error_count} errors")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing {self.endpoint_name}: {str(e)}")
            if self.progress_tracker:
                self.progress_tracker.finish()
            
            return {
                'endpoint': self.endpoint_name,
                'records_processed': 0,
                'errors': 1,
                'total_time': time.time() - start_time,
                'csv_file': "",
                'success': False,
                'error': str(e)
            }
    
    def process_in_batches(self, limit: int, batch_size: int) -> Generator[tuple, None, None]:
        """Process records in batches."""
        offset = 0
        batch_number = 1
        total_batches = (limit + batch_size - 1) // batch_size
        
        while offset < limit:
            current_batch_size = min(batch_size, limit - offset)
            
            logger.debug(f"Processing batch {batch_number}/{total_batches} "
                        f"for {self.endpoint_name} (offset: {offset}, size: {current_batch_size})")
            
            if self.progress_tracker:
                self.progress_tracker.start_batch(batch_number, current_batch_size)
            
            try:
                # Fetch batch of records
                batch_records = self.fetch_batch(offset, current_batch_size)
                
                # Process records (convert to models, clean data, etc.)
                processed_records = self.process_records(batch_records)
                
                yield processed_records, 0  # No errors
                
            except Exception as e:
                logger.error(f"Error processing batch {batch_number} for {self.endpoint_name}: {str(e)}")
                yield [], 1  # Empty records, 1 error
            
            offset += current_batch_size
            batch_number += 1
            
            # Small delay between batches to be respectful to the API
            time.sleep(0.1)
    
    @with_retry
    def fetch_batch(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        """Fetch a batch of records from the API."""
        params = self.build_request_params(offset, limit)
        
        try:
            if self.endpoint_config.requires_account_id:
                account_id = self.get_account_id()
                path = self.endpoint_config.path.format(account_id=account_id)
            else:
                path = self.endpoint_config.path
            
            # The client's _make_request already handles errors and returns JSON data
            data = self.client._make_request('GET', path, params=params)
            
            # Extract records from response
            records = self.extract_records_from_response(data)
            
            logger.debug(f"Fetched {len(records)} records for {self.endpoint_name} "
                        f"(offset: {offset}, limit: {limit})")
            
            return records
            
        except Exception as e:
            logger.error(f"Error fetching batch for {self.endpoint_name}: {str(e)}")
            raise
    
    def build_request_params(self, offset: int, limit: int) -> Dict[str, Any]:
        """Build request parameters for the API call."""
        params = {}
        
        # Add pagination parameters
        if self.endpoint_config.pagination_type == "offset":
            params['page'] = (offset // limit) + 1
            params['per_page'] = min(limit, self.endpoint_config.max_per_page)
        elif self.endpoint_config.pagination_type == "relative":
            if offset > 0:
                # For relative pagination, we'd need to track the last record ID
                # This is a simplified implementation
                params['page'] = (offset // limit) + 1
            params['per_page'] = min(limit, self.endpoint_config.max_per_page)
        
        # Add company_id if required
        if self.endpoint_config.requires_company_id:
            company_id = self.get_company_id()
            if company_id:
                params['company_id'] = company_id
        
        # Add field selection (skip for problematic endpoints)
        skip_fields = ['tags', 'text_messages', 'outbound_caller_ids']
        if self.endpoint_name not in skip_fields:
            all_fields = endpoint_registry.get_all_fields(self.endpoint_name)
            if all_fields:
                params['fields'] = ','.join(all_fields)
        
        return params
    
    def extract_records_from_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract records from API response."""
        # Most CallRail endpoints return data in a specific format
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Try common keys for record arrays
            for key in [self.endpoint_name, 'data', 'results', 'items']:
                if key in data and isinstance(data[key], list):
                    return data[key]
            
            # If it's a single record, wrap in list
            if 'id' in data:
                return [data]
        
        return []
    
    def process_records(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and clean records."""
        processed_records = []
        
        for record in records:
            try:
                # Create model instance (this also validates/cleans the data)
                processed_record = create_model_instance(self.endpoint_name, record)
                
                # Convert back to dict for CSV writing
                if hasattr(processed_record, '__dict__'):
                    processed_records.append(processed_record.__dict__)
                else:
                    processed_records.append(processed_record)
                    
            except Exception as e:
                logger.warning(f"Error processing record for {self.endpoint_name}: {str(e)}")
                # Include raw record if processing fails
                processed_records.append(record)
        
        return processed_records
    
    def get_endpoint_info(self) -> Dict[str, Any]:
        """Get information about the endpoint."""
        return {
            'name': self.endpoint_name,
            'path': self.endpoint_config.path,
            'requires_account_id': self.endpoint_config.requires_account_id,
            'pagination_type': self.endpoint_config.pagination_type,
            'max_per_page': self.endpoint_config.max_per_page,
            'total_fields': len(endpoint_registry.get_all_fields(self.endpoint_name)),
            'fields': endpoint_registry.get_all_fields(self.endpoint_name)
        }

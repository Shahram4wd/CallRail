"""
Calls endpoint processor for CallRail API.
"""
from typing import Dict, Any, List
from processors.base_processor import BaseProcessor
from utils.logger import logger


class CallsProcessor(BaseProcessor):
    """Processor for CallRail Calls endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "calls")
        self.account_id = account_id
    
    def get_account_id(self) -> str:
        """Get account ID for API calls."""
        return self.account_id
    
    def build_request_params(self, offset: int, limit: int) -> Dict[str, Any]:
        """Build request parameters for calls endpoint."""
        params = super().build_request_params(offset, limit)
        
        # Calls endpoint uses relative pagination for better performance
        if self.endpoint_config.pagination_type == "relative":
            # Use per_page instead of page for calls
            params = {
                'per_page': min(limit, self.endpoint_config.max_per_page)
            }
            
            # Add field selection
            all_fields = self.endpoint_config.fields + self.endpoint_config.optional_fields
            if all_fields:
                params['fields'] = ','.join(all_fields)
        
        return params
    
    def extract_records_from_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract calls from API response."""
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Check for calls key
            if 'calls' in data:
                return data['calls']
            # Check for data key (common in paginated responses)
            elif 'data' in data and isinstance(data['data'], list):
                return data['data']
            # If it's a single call
            elif 'id' in data:
                return [data]
        
        return []

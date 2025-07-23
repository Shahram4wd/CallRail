"""
Generic endpoint processor for CallRail API endpoints.
"""
from typing import Dict, Any, List
from processors.base_processor import BaseProcessor
from utils.logger import logger


class GenericProcessor(BaseProcessor):
    """Generic processor for CallRail API endpoints."""
    
    def __init__(self, client, endpoint_name: str, account_id: str):
        super().__init__(client, endpoint_name)
        self.account_id = account_id
    
    def get_account_id(self) -> str:
        """Get account ID for API calls."""
        return self.account_id
    
    def extract_records_from_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract records from API response."""
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Try endpoint-specific key first
            if self.endpoint_name in data and isinstance(data[self.endpoint_name], list):
                return data[self.endpoint_name]
            
            # Try common keys for record arrays
            for key in ['data', 'results', 'items']:
                if key in data and isinstance(data[key], list):
                    return data[key]
            
            # If it's a single record, wrap in list
            if 'id' in data:
                return [data]
        
        return []


# Specific processor classes for each endpoint
class CompaniesProcessor(GenericProcessor):
    """Processor for CallRail Companies endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "companies", account_id)


class FormSubmissionsProcessor(GenericProcessor):
    """Processor for CallRail Form Submissions endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "form_submissions", account_id)


class IntegrationsProcessor(GenericProcessor):
    """Processor for CallRail Integrations endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "integrations", account_id)


class TagsProcessor(GenericProcessor):
    """Processor for CallRail Tags endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "tags", account_id)


class TrackersProcessor(GenericProcessor):
    """Processor for CallRail Trackers endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "trackers", account_id)


class UsersProcessor(GenericProcessor):
    """Processor for CallRail Users endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "users", account_id)


class TextMessagesProcessor(GenericProcessor):
    """Processor for CallRail Text Messages endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "text_messages", account_id)


class NotificationsProcessor(GenericProcessor):
    """Processor for CallRail Notifications endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "notifications", account_id)


class OutboundCallerIdsProcessor(GenericProcessor):
    """Processor for CallRail Outbound Caller IDs endpoint."""
    
    def __init__(self, client, account_id: str):
        super().__init__(client, "outbound_caller_ids", account_id)

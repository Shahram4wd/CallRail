"""
Accounts endpoint processor for CallRail API.
"""
from typing import Dict, Any, List
from processors.base_processor import BaseProcessor
from utils.logger import logger


class AccountsProcessor(BaseProcessor):
    """Processor for CallRail Accounts endpoint."""
    
    def __init__(self, client):
        super().__init__(client, "accounts")
        self._account_id = None
    
    def get_account_id(self) -> str:
        """Get account ID. For accounts endpoint, we use the first account found."""
        if self._account_id:
            return self._account_id
        
        # For accounts endpoint, we don't need an account_id in the path
        # But we'll store the first account ID for other processors
        try:
            accounts = self.fetch_batch(0, 1)
            if accounts:
                self._account_id = accounts[0]['id']
                return self._account_id
        except Exception as e:
            logger.error(f"Error getting account ID: {str(e)}")
        
        return ""
    
    def extract_records_from_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract accounts from API response."""
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Check for accounts key
            if 'accounts' in data:
                return data['accounts']
            # If it's a single account
            elif 'id' in data:
                return [data]
        
        return []

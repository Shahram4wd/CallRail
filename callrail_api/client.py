"""
CallRail API Client

A Python client for interacting with the CallRail API v3.
"""

import os
import json
from typing import List, Optional, Dict, Any, Union
from urllib.parse import urljoin, urlencode
import requests
from dotenv import load_dotenv

from .models import (
    Account, Company, Call, Tracker, FormSubmission, 
    Conversation, TextMessage, Tag, User, PaginatedResponse
)
from .exceptions import (
    CallRailAPIException, AuthenticationError, RateLimitError,
    NotFoundError, ValidationError, ServerError
)


class CallRailClient:
    """
    CallRail API client for v3 of the CallRail API.
    
    This client provides methods to interact with CallRail's REST API,
    including authentication, rate limiting, and error handling.
    """
    
    BASE_URL = "https://api.callrail.com/v3/"
    
    def __init__(self, api_key: str = None):
        """
        Initialize the CallRail API client.
        
        Args:
            api_key: CallRail API key. If not provided, will try to load from
                    CALLRAIL_API_KEY environment variable.
        """
        if api_key is None:
            load_dotenv()
            api_key = os.getenv('CALLRAIL_API_KEY')
        
        if not api_key:
            raise ValueError(
                "API key is required. Provide it as a parameter or set "
                "CALLRAIL_API_KEY environment variable."
            )
        
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token token="{api_key}"',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the CallRail API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (relative to BASE_URL)
            params: URL parameters
            data: Request body data
            **kwargs: Additional arguments passed to requests
            
        Returns:
            Parsed JSON response
            
        Raises:
            CallRailAPIException: For various API errors
        """
        url = urljoin(self.BASE_URL, endpoint)
        
        try:
            if data:
                kwargs['json'] = data
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                **kwargs
            )
            
            # Handle different response status codes
            if response.status_code == 200:
                return response.json() if response.content else {}
            elif response.status_code == 201:
                return response.json() if response.content else {}
            elif response.status_code == 204:
                return {}
            elif response.status_code == 400:
                error_data = response.json() if response.content else {}
                raise ValidationError(
                    error_data.get('error', 'Bad Request'),
                    status_code=400,
                    response=error_data
                )
            elif response.status_code == 401:
                raise AuthenticationError(
                    "Invalid API key or authentication failed",
                    status_code=401
                )
            elif response.status_code == 403:
                error_data = response.json() if response.content else {}
                raise AuthenticationError(
                    error_data.get('error', 'Forbidden'),
                    status_code=403,
                    response=error_data
                )
            elif response.status_code == 404:
                raise NotFoundError(
                    "Resource not found",
                    status_code=404
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded",
                    status_code=429
                )
            elif response.status_code >= 500:
                raise ServerError(
                    "Server error occurred",
                    status_code=response.status_code
                )
            else:
                raise CallRailAPIException(
                    f"Unexpected status code: {response.status_code}",
                    status_code=response.status_code
                )
                
        except requests.exceptions.RequestException as e:
            raise CallRailAPIException(f"Request failed: {str(e)}")
    
    # Account methods
    def list_accounts(self, **params) -> PaginatedResponse:
        """List all accounts accessible by the API key."""
        response = self._make_request('GET', 'a.json', params=params)
        accounts = [Account(**account) for account in response.get('accounts', [])]
        return PaginatedResponse(
            page=response.get('page', 1),
            per_page=response.get('per_page', 100),
            total_pages=response.get('total_pages', 1),
            total_records=response.get('total_records', 0),
            data=accounts
        )
    
    def get_account(self, account_id: str, **params) -> Account:
        """Get a specific account by ID."""
        response = self._make_request('GET', f'a/{account_id}.json', params=params)
        return Account(**response)
    
    # Company methods
    def list_companies(self, account_id: str, **params) -> PaginatedResponse:
        """List all companies in an account."""
        response = self._make_request('GET', f'a/{account_id}/companies.json', params=params)
        companies = [Company(**company) for company in response.get('companies', [])]
        return PaginatedResponse(
            page=response.get('page', 1),
            per_page=response.get('per_page', 100),
            total_pages=response.get('total_pages', 1),
            total_records=response.get('total_records', 0),
            data=companies
        )
    
    def get_company(self, account_id: str, company_id: str, **params) -> Company:
        """Get a specific company by ID."""
        response = self._make_request('GET', f'a/{account_id}/companies/{company_id}.json', params=params)
        return Company(**response)
    
    def create_company(self, account_id: str, company_data: Dict[str, Any]) -> Company:
        """Create a new company."""
        response = self._make_request('POST', f'a/{account_id}/companies.json', data=company_data)
        return Company(**response)
    
    def update_company(self, account_id: str, company_id: str, company_data: Dict[str, Any]) -> Company:
        """Update an existing company."""
        response = self._make_request('PUT', f'a/{account_id}/companies/{company_id}.json', data=company_data)
        return Company(**response)
    
    def delete_company(self, account_id: str, company_id: str) -> None:
        """Delete (disable) a company."""
        self._make_request('DELETE', f'a/{account_id}/companies/{company_id}.json')
    
    # Call methods
    def list_calls(self, account_id: str, **params) -> PaginatedResponse:
        """List all calls in an account."""
        response = self._make_request('GET', f'a/{account_id}/calls.json', params=params)
        calls = [Call(**call) for call in response.get('calls', [])]
        return PaginatedResponse(
            page=response.get('page', 1),
            per_page=response.get('per_page', 100),
            total_pages=response.get('total_pages', 1),
            total_records=response.get('total_records', 0),
            data=calls
        )
    
    def get_call(self, account_id: str, call_id: str, **params) -> Call:
        """Get a specific call by ID."""
        response = self._make_request('GET', f'a/{account_id}/calls/{call_id}.json', params=params)
        return Call(**response)
    
    def create_outbound_call(self, account_id: str, call_data: Dict[str, Any]) -> Call:
        """Create an outbound call."""
        response = self._make_request('POST', f'a/{account_id}/calls.json', data=call_data)
        return Call(**response)
    
    def update_call(self, account_id: str, call_id: str, call_data: Dict[str, Any]) -> Call:
        """Update a call (add notes, tags, etc.)."""
        response = self._make_request('PUT', f'a/{account_id}/calls/{call_id}.json', data=call_data)
        return Call(**response)
    
    def get_call_recording(self, account_id: str, call_id: str) -> Dict[str, str]:
        """Get the recording URL for a call."""
        return self._make_request('GET', f'a/{account_id}/calls/{call_id}/recording.json')
    
    # Tracker methods
    def list_trackers(self, account_id: str, **params) -> PaginatedResponse:
        """List all trackers in an account."""
        response = self._make_request('GET', f'a/{account_id}/trackers.json', params=params)
        trackers = [Tracker(**tracker) for tracker in response.get('trackers', [])]
        return PaginatedResponse(
            page=response.get('page', 1),
            per_page=response.get('per_page', 100),
            total_pages=response.get('total_pages', 1),
            total_records=response.get('total_records', 0),
            data=trackers
        )
    
    def get_tracker(self, account_id: str, tracker_id: str, **params) -> Tracker:
        """Get a specific tracker by ID."""
        response = self._make_request('GET', f'a/{account_id}/trackers/{tracker_id}.json', params=params)
        return Tracker(**response)
    
    def create_tracker(self, account_id: str, tracker_data: Dict[str, Any]) -> Tracker:
        """Create a new tracker."""
        response = self._make_request('POST', f'a/{account_id}/trackers.json', data=tracker_data)
        return Tracker(**response)
    
    def update_tracker(self, account_id: str, tracker_id: str, tracker_data: Dict[str, Any]) -> Tracker:
        """Update an existing tracker."""
        response = self._make_request('PUT', f'a/{account_id}/trackers/{tracker_id}.json', data=tracker_data)
        return Tracker(**response)
    
    def delete_tracker(self, account_id: str, tracker_id: str) -> None:
        """Delete (disable) a tracker."""
        self._make_request('DELETE', f'a/{account_id}/trackers/{tracker_id}.json')
    
    # Form submission methods
    def list_form_submissions(self, account_id: str, **params) -> PaginatedResponse:
        """List all form submissions in an account."""
        response = self._make_request('GET', f'a/{account_id}/form_submissions.json', params=params)
        submissions = [FormSubmission(**submission) for submission in response.get('form_submissions', [])]
        return PaginatedResponse(
            page=response.get('page', 1),
            per_page=response.get('per_page', 100),
            total_pages=response.get('total_pages', 1),
            total_records=response.get('total_records', 0),
            data=submissions
        )
    
    def create_form_submission(self, account_id: str, submission_data: Dict[str, Any]) -> FormSubmission:
        """Create a new form submission."""
        response = self._make_request('POST', f'a/{account_id}/form_submissions.json', data=submission_data)
        return FormSubmission(**response)
    
    def update_form_submission(self, account_id: str, submission_id: str, submission_data: Dict[str, Any]) -> FormSubmission:
        """Update a form submission."""
        response = self._make_request('PUT', f'a/{account_id}/form_submissions/{submission_id}.json', data=submission_data)
        return FormSubmission(**response)
    
    # Text message methods
    def list_conversations(self, account_id: str, **params) -> PaginatedResponse:
        """List all text message conversations."""
        response = self._make_request('GET', f'a/{account_id}/text-messages.json', params=params)
        conversations = [Conversation(**conv) for conv in response.get('conversations', [])]
        return PaginatedResponse(
            page=response.get('page', 1),
            per_page=response.get('per_page', 100),
            total_pages=response.get('total_pages', 1),
            total_records=response.get('total_records', 0),
            data=conversations
        )
    
    def get_conversation(self, account_id: str, conversation_id: str, **params) -> Conversation:
        """Get a specific text conversation by ID."""
        response = self._make_request('GET', f'a/{account_id}/text-messages/{conversation_id}.json', params=params)
        return Conversation(**response)
    
    def send_text_message(self, account_id: str, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send a text message."""
        return self._make_request('POST', f'a/{account_id}/text-messages.json', data=message_data)
    
    # Tag methods
    def list_tags(self, account_id: str, **params) -> PaginatedResponse:
        """List all tags in an account."""
        response = self._make_request('GET', f'a/{account_id}/tags.json', params=params)
        tags = [Tag(**tag) for tag in response.get('tags', [])]
        return PaginatedResponse(
            page=response.get('page', 1),
            per_page=response.get('per_page', 100),
            total_pages=response.get('total_pages', 1),
            total_records=response.get('total_records', 0),
            data=tags
        )
    
    def create_tag(self, account_id: str, tag_data: Dict[str, Any]) -> Tag:
        """Create a new tag."""
        response = self._make_request('POST', f'a/{account_id}/tags.json', data=tag_data)
        return Tag(**response)
    
    def update_tag(self, account_id: str, tag_id: str, tag_data: Dict[str, Any]) -> Tag:
        """Update an existing tag."""
        response = self._make_request('PUT', f'a/{account_id}/tags/{tag_id}.json', data=tag_data)
        return Tag(**response)
    
    def delete_tag(self, account_id: str, tag_id: str) -> None:
        """Delete a tag."""
        self._make_request('DELETE', f'a/{account_id}/tags/{tag_id}.json')
    
    # User methods
    def list_users(self, account_id: str, **params) -> PaginatedResponse:
        """List all users in an account."""
        response = self._make_request('GET', f'a/{account_id}/users.json', params=params)
        users = [User(**user) for user in response.get('users', [])]
        return PaginatedResponse(
            page=response.get('page', 1),
            per_page=response.get('per_page', 100),
            total_pages=response.get('total_pages', 1),
            total_records=response.get('total_records', 0),
            data=users
        )
    
    def get_user(self, account_id: str, user_id: str, **params) -> User:
        """Get a specific user by ID."""
        response = self._make_request('GET', f'a/{account_id}/users/{user_id}.json', params=params)
        return User(**response)
    
    def create_user(self, account_id: str, user_data: Dict[str, Any]) -> User:
        """Create a new user."""
        response = self._make_request('POST', f'a/{account_id}/users.json', data=user_data)
        return User(**response)
    
    def update_user(self, account_id: str, user_id: str, user_data: Dict[str, Any]) -> User:
        """Update an existing user."""
        response = self._make_request('PUT', f'a/{account_id}/users/{user_id}.json', data=user_data)
        return User(**response)
    
    def delete_user(self, account_id: str, user_id: str) -> None:
        """Delete a user."""
        self._make_request('DELETE', f'a/{account_id}/users/{user_id}.json')
    
    # Summary and reporting methods
    def get_call_summary(self, account_id: str, **params) -> Dict[str, Any]:
        """Get call data summary with grouping and filtering options."""
        return self._make_request('GET', f'a/{account_id}/calls/summary.json', params=params)
    
    def get_call_timeseries(self, account_id: str, **params) -> Dict[str, Any]:
        """Get call data summarized by time series."""
        return self._make_request('GET', f'a/{account_id}/calls/timeseries.json', params=params)
    
    def get_form_summary(self, account_id: str, **params) -> Dict[str, Any]:
        """Get form submission data summary."""
        return self._make_request('GET', f'a/{account_id}/forms/summary.json', params=params)

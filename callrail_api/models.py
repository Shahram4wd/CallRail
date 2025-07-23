"""
Data models for CallRail API responses.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union
from datetime import datetime


@dataclass
class Account:
    """Represents a CallRail account."""
    id: str
    name: str
    outbound_recording_enabled: bool
    hipaa_account: bool
    numeric_id: Optional[int] = None


@dataclass
class Company:
    """Represents a CallRail company."""
    id: str
    name: str
    status: str
    time_zone: str
    created_at: str
    disabled_at: Optional[str] = None
    dni_active: Optional[bool] = None
    script_url: Optional[str] = None
    callscribe_enabled: bool = False
    lead_scoring_enabled: bool = False
    swap_exclude_jquery: Optional[bool] = None
    swap_ppc_override: Optional[bool] = None
    swap_landing_override: Optional[str] = None
    swap_cookie_duration: int = 6
    swap_cookie_duration_unit: str = "months"
    callscore_enabled: bool = False
    keyword_spotting_enabled: bool = False
    form_capture: bool = False


@dataclass
class Call:
    """Represents a CallRail call."""
    id: str
    answered: bool
    business_phone_number: Optional[str]
    customer_city: Optional[str]
    customer_country: Optional[str]
    customer_name: Optional[str]
    customer_phone_number: str
    customer_state: Optional[str]
    direction: str
    duration: int
    recording: Optional[str]
    recording_duration: Optional[str]
    recording_player: Optional[str]
    start_time: str
    tracking_phone_number: str
    voicemail: bool
    agent_email: Optional[str] = None
    call_type: Optional[str] = None
    campaign: Optional[str] = None
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    note: Optional[str] = None
    tags: Optional[List[str]] = None
    lead_status: Optional[str] = None
    value: Optional[str] = None


@dataclass
class Tracker:
    """Represents a CallRail tracker."""
    id: str
    name: str
    type: str
    status: str
    destination_number: str
    tracking_numbers: List[str]
    whisper_message: Optional[str]
    sms_enabled: bool
    sms_supported: bool
    company: Dict[str, str]
    call_flow: Dict[str, Any]
    source: Dict[str, Any]
    created_at: str
    disabled_at: Optional[str] = None


@dataclass
class FormSubmission:
    """Represents a CallRail form submission."""
    id: str
    company_id: str
    person_id: str
    form_data: Dict[str, Any]
    form_url: str
    landing_page_url: str
    referrer: str
    referring_url: str
    submitted_at: str
    first_form: bool
    customer_phone_number: Optional[str] = None


@dataclass
class TextMessage:
    """Represents a text message in a conversation."""
    id: str
    content: str
    direction: str
    created_at: str
    type: str = "sms"
    media_urls: Optional[List[str]] = None


@dataclass
class Conversation:
    """Represents a text message conversation."""
    id: str
    company_id: str
    initial_tracker_id: str
    current_tracker_id: str
    customer_name: Optional[str]
    customer_phone_number: str
    initial_tracking_number: str
    current_tracking_number: str
    state: str
    last_message_at: str
    created_at: str
    messages: List[TextMessage]


@dataclass
class PaginatedResponse:
    """Represents a paginated API response."""
    page: int
    per_page: int
    total_pages: int
    total_records: int
    data: List[Any]


@dataclass
class Tag:
    """Represents a CallRail tag."""
    id: int
    name: str
    tag_level: str
    color: str
    background_color: str
    company_id: str
    status: str
    created_at: str


@dataclass
class User:
    """Represents a CallRail user."""
    id: str
    email: str
    first_name: str
    last_name: str
    name: str
    role: str
    created_at: str
    accepted: bool
    companies: List[Dict[str, str]]

"""
Extended models for additional CallRail API endpoints.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Integration:
    """Model for CallRail Integration."""
    id: str
    name: str
    state: str
    created_at: str
    updated_at: str
    integration_data: Optional[Dict[str, Any]] = None


@dataclass
class Tag:
    """Model for CallRail Tag."""
    id: str
    name: str
    tag_level: str
    color: str
    background_color: str
    created_at: str
    updated_at: str
    company_id: Optional[str] = None


@dataclass
class Tracker:
    """Model for CallRail Tracker."""
    id: str
    name: str
    type: str
    status: str
    source: str
    tracking_number: str
    formatted_tracking_number: str
    created_at: str
    updated_at: str
    company_id: Optional[str] = None
    landing_page_url: Optional[str] = None
    referrer: Optional[str] = None
    referrer_domain: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    utm_campaign: Optional[str] = None
    destination_number: Optional[str] = None
    formatted_destination_number: Optional[str] = None
    whisper_message: Optional[str] = None
    record_calls: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    swap_exclude_jquery_selector: Optional[str] = None
    swap_ppc_override: Optional[bool] = None
    swap_landing_override: Optional[bool] = None
    swap_cookie_duration: Optional[int] = None


@dataclass
class User:
    """Model for CallRail User."""
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    created_at: str
    updated_at: str
    avatar_url: Optional[str] = None
    is_account_admin: Optional[bool] = None


@dataclass
class TextMessage:
    """Model for CallRail Text Message."""
    id: str
    company_id: str
    direction: str
    content: str
    customer_phone_number: str
    business_phone_number: str
    created_at: str
    updated_at: str
    customer_name: Optional[str] = None
    formatted_customer_phone_number: Optional[str] = None
    formatted_business_phone_number: Optional[str] = None
    conversation_id: Optional[str] = None
    lead_status: Optional[str] = None
    value: Optional[str] = None
    note: Optional[str] = None
    note_updated_at: Optional[str] = None
    tags: Optional[List[str]] = None


@dataclass
class FormSubmission:
    """Model for CallRail Form Submission."""
    id: str
    company_id: str
    person_id: Optional[str]
    submitter_id: Optional[str]
    content: Dict[str, Any]
    referrer: Optional[str]
    referring_url: Optional[str]
    landing_page_url: Optional[str]
    last_requested_url: Optional[str]
    created_at: str
    updated_at: str
    formatted_submitter_phone_number: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    utm_campaign: Optional[str] = None
    utma: Optional[str] = None
    utmb: Optional[str] = None
    utmc: Optional[str] = None
    utmv: Optional[str] = None
    utmz: Optional[str] = None
    ga: Optional[str] = None
    search_keywords: Optional[str] = None
    ip_address: Optional[str] = None
    tags: Optional[List[str]] = None
    value: Optional[str] = None
    lead_status: Optional[str] = None
    note: Optional[str] = None
    note_updated_at: Optional[str] = None


@dataclass
class Notification:
    """Model for CallRail Notification."""
    id: str
    type: str
    target: str
    webhook_url: str
    created_at: str
    updated_at: str
    company_id: Optional[str] = None
    enabled: Optional[bool] = None
    oauth_application_id: Optional[str] = None


@dataclass
class OutboundCallerId:
    """Model for CallRail Outbound Caller ID."""
    id: str
    phone_number: str
    formatted_phone_number: str
    name: str
    created_at: str
    updated_at: str
    company_id: Optional[str] = None


@dataclass
class Account:
    """Extended model for CallRail Account."""
    id: str
    name: str
    status: str
    created_at: str
    updated_at: str
    outbound_recording_enabled: Optional[bool] = None
    hipaa_account: Optional[bool] = None
    script_url: Optional[str] = None


@dataclass
class Company:
    """Extended model for CallRail Company."""
    id: str
    name: str
    status: str
    time_zone: str
    created_at: str
    updated_at: str
    script_url: Optional[str] = None
    callscore_enabled: Optional[bool] = None
    keyword_spotting_enabled: Optional[bool] = None
    call_recording_enabled: Optional[bool] = None
    conversation_intelligence_enabled: Optional[bool] = None


@dataclass
class ExtendedCall:
    """Extended model for CallRail Call with all optional fields."""
    id: str
    answered: bool
    business_phone_number: str
    customer_city: Optional[str]
    customer_country: Optional[str]
    customer_name: Optional[str]
    customer_phone_number: str
    customer_state: Optional[str]
    direction: str
    duration: int
    created_at: str
    start_time: str
    tracking_phone_number: str
    source: str
    source_name: str
    
    # Optional fields
    recording: Optional[str] = None
    recording_duration: Optional[int] = None
    voicemail: Optional[bool] = None
    note: Optional[str] = None
    lead_status: Optional[str] = None
    value: Optional[str] = None
    formatted_customer_location: Optional[str] = None
    formatted_business_location: Optional[str] = None
    formatted_customer_name_or_phone_number: Optional[str] = None
    company_id: Optional[str] = None
    device_type: Optional[str] = None
    first_call: Optional[bool] = None
    prior_calls: Optional[int] = None
    total_calls: Optional[int] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    utm_campaign: Optional[str] = None
    utma: Optional[str] = None
    utmb: Optional[str] = None
    utmc: Optional[str] = None
    utmv: Optional[str] = None
    utmz: Optional[str] = None
    ga: Optional[str] = None
    referrer: Optional[str] = None
    referring_url: Optional[str] = None
    landing_page_url: Optional[str] = None
    last_requested_url: Optional[str] = None
    ip_address: Optional[str] = None
    search_keywords: Optional[str] = None
    web_session_id: Optional[str] = None
    tags: Optional[List[str]] = None
    agent_email: Optional[str] = None
    call_type: Optional[str] = None
    company_name: Optional[str] = None
    company_time_zone: Optional[str] = None
    formatted_call_type: Optional[str] = None
    formatted_duration: Optional[str] = None
    formatted_tracking_phone_number: Optional[str] = None
    formatted_tracking_source: Optional[str] = None
    formatted_value: Optional[str] = None
    good_lead_call_id: Optional[str] = None
    good_lead_call_time: Optional[str] = None
    note_updated_at: Optional[str] = None
    tracker_id: Optional[str] = None
    transcription: Optional[str] = None
    keywords_spotted: Optional[List[str]] = None
    call_highlights: Optional[List[Dict[str, Any]]] = None


# Model mapping for endpoint processors
MODEL_MAPPING = {
    'accounts': Account,
    'calls': ExtendedCall,
    'companies': Company,
    'form_submissions': FormSubmission,
    'integrations': Integration,
    'tags': Tag,
    'trackers': Tracker,
    'users': User,
    'text_messages': TextMessage,
    'notifications': Notification,
    'outbound_caller_ids': OutboundCallerId
}


def get_model_for_endpoint(endpoint_name: str):
    """Get the appropriate model class for an endpoint."""
    return MODEL_MAPPING.get(endpoint_name)


def create_model_instance(endpoint_name: str, data: Dict[str, Any]):
    """Create a model instance from API response data."""
    model_class = get_model_for_endpoint(endpoint_name)
    if not model_class:
        return data  # Return raw data if no model found
    
    try:
        # Filter data to only include fields that exist in the model
        model_fields = {field.name for field in model_class.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in model_fields}
        return model_class(**filtered_data)
    except Exception:
        # If model creation fails, return raw data
        return data

"""
CallRail API endpoints configuration.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class EndpointConfig:
    """Configuration for a specific endpoint."""
    name: str
    path: str
    fields: List[str]
    optional_fields: List[str]
    supports_pagination: bool = True
    pagination_type: str = "offset"  # "offset" or "relative"
    max_per_page: int = 250
    requires_account_id: bool = True
    requires_company_id: bool = False


class EndpointRegistry:
    """Registry of all CallRail API endpoints."""
    
    def __init__(self):
        self.endpoints = {
            "accounts": EndpointConfig(
                name="accounts",
                path="/v3/a.json",
                fields=[
                    "id", "name", "created_at"
                ],
                optional_fields=[
                    "numeric_id", "inbound_recording_enabled", "outbound_recording_enabled", 
                    "hipaa_account", "features", "outbound_recording_on_by_default", 
                    "masked_id", "outbound_greeting_enabled", "agency_in_trial", 
                    "has_zuora_account", "brand_status", "approaching_cold_outbound_limit", 
                    "allow_cold_outbound_texting", "allow_texting", "ten_dlc_effective_date", 
                    "has_unique_subaccount"
                ],
                requires_account_id=False
            ),
            
            "calls": EndpointConfig(
                name="calls",
                path="/v3/a/{account_id}/calls.json",
                fields=[
                    "id", "answered", "business_phone_number", "customer_city",
                    "customer_country", "customer_name", "customer_phone_number",
                    "customer_state", "direction", "duration", "created_at",
                    "start_time", "tracking_phone_number", "source", "source_name"
                ],
                optional_fields=[
                    "recording", "recording_duration", "voicemail", "note",
                    "lead_status", "value", "formatted_customer_location",
                    "formatted_business_location", "formatted_customer_name_or_phone_number",
                    "company_id", "device_type", "first_call", "prior_calls",
                    "total_calls", "utm_source", "utm_medium", "utm_term",
                    "utm_content", "utm_campaign", "utma", "utmb", "utmc",
                    "utmv", "utmz", "ga", "referrer", "referring_url", "landing_page_url",
                    "last_requested_url", "ip_address", "search_keywords", "web_session_id",
                    "tags", "agent_email", "call_type", "company_name", "company_time_zone",
                    "formatted_call_type", "formatted_customer_location", "formatted_duration",
                    "formatted_tracking_phone_number", "formatted_tracking_source",
                    "formatted_value", "good_lead_call_id", "good_lead_call_time",
                    "lead_status", "note_updated_at", "source_name", "tracker_id",
                    "transcription", "keywords_spotted", "call_highlights"
                ],
                pagination_type="relative"
            ),
            
            "companies": EndpointConfig(
                name="companies",
                path="/v3/a/{account_id}/companies.json",
                fields=[
                    "id", "name", "status", "time_zone", "created_at"
                ],
                optional_fields=[
                    "disabled_at", "dni_active", "script_url", "callscore_enabled", 
                    "lead_scoring_enabled", "swap_exclude_jquery", "swap_ppc_override", 
                    "swap_landing_override", "swap_cookie_duration", "swap_cookie_duration_unit", 
                    "callscribe_enabled", "keyword_spotting_enabled", "form_capture", 
                    "verified_caller_ids", "masked_id"
                ]
            ),
            
            "form_submissions": EndpointConfig(
                name="form_submissions",
                path="/v3/a/{account_id}/form_submissions.json",
                fields=[
                    "id", "company_id", "person_id", "submitter_id", "content",
                    "referrer", "referring_url", "landing_page_url", "last_requested_url",
                    "created_at", "updated_at"
                ],
                optional_fields=[
                    "formatted_submitter_phone_number", "utm_source", "utm_medium",
                    "utm_term", "utm_content", "utm_campaign", "utma", "utmb",
                    "utmc", "utmv", "utmz", "ga", "search_keywords", "ip_address",
                    "tags", "value", "lead_status", "note", "note_updated_at"
                ]
            ),
            
            "integrations": EndpointConfig(
                name="integrations",
                path="/v3/a/{account_id}/integrations.json",
                fields=[
                    "id", "name", "state", "created_at", "updated_at"
                ],
                optional_fields=[
                    "integration_data"
                ]
            ),
            
            "tags": EndpointConfig(
                name="tags",
                path="/v3/a/{account_id}/tags.json",
                fields=[
                    "id", "name", "tag_level", "color", "background_color",
                    "created_at", "updated_at"
                ],
                optional_fields=[
                    "company_id"
                ]
            ),
            
            "trackers": EndpointConfig(
                name="trackers",
                path="/v3/a/{account_id}/trackers.json",
                fields=[
                    "id", "name", "type", "status", "source", "tracking_number",
                    "formatted_tracking_number", "created_at", "updated_at"
                ],
                optional_fields=[
                    "company_id", "landing_page_url", "referrer", "referrer_domain",
                    "utm_source", "utm_medium", "utm_term", "utm_content", "utm_campaign",
                    "destination_number", "formatted_destination_number", "whisper_message",
                    "record_calls", "sms_enabled", "swap_exclude_jquery_selector",
                    "swap_ppc_override", "swap_landing_override", "swap_cookie_duration"
                ]
            ),
            
            "users": EndpointConfig(
                name="users",
                path="/v3/a/{account_id}/users.json",
                fields=[
                    "id", "email", "first_name", "last_name", "role", "created_at", "updated_at"
                ],
                optional_fields=[
                    "avatar_url", "is_account_admin"
                ]
            ),
            
            "text_messages": EndpointConfig(
                name="text_messages",
                path="/v3/a/{account_id}/text_messages.json",
                fields=[
                    "id", "company_id", "direction", "content", "customer_phone_number",
                    "business_phone_number", "created_at", "updated_at"
                ],
                optional_fields=[
                    "customer_name", "formatted_customer_phone_number",
                    "formatted_business_phone_number", "conversation_id", "lead_status",
                    "value", "note", "note_updated_at", "tags"
                ]
            ),
            
            "notifications": EndpointConfig(
                name="notifications",
                path="/v3/a/{account_id}/notifications.json",
                fields=[
                    "id", "type", "target", "webhook_url", "created_at", "updated_at"
                ],
                optional_fields=[
                    "company_id", "enabled", "oauth_application_id"
                ]
            ),
            
            "outbound_caller_ids": EndpointConfig(
                name="outbound_caller_ids",
                path="/v3/a/{account_id}/outbound_caller_ids.json",
                fields=[
                    "id", "phone_number", "formatted_phone_number", "name",
                    "created_at", "updated_at"
                ],
                optional_fields=[
                    "company_id"
                ]
            )
        }
    
    def get_endpoint(self, name: str) -> Optional[EndpointConfig]:
        """Get endpoint configuration by name."""
        return self.endpoints.get(name)
    
    def get_all_endpoints(self) -> Dict[str, EndpointConfig]:
        """Get all endpoint configurations."""
        return self.endpoints
    
    def get_endpoint_names(self) -> List[str]:
        """Get list of all endpoint names."""
        return list(self.endpoints.keys())
    
    def get_all_fields(self, endpoint_name: str) -> List[str]:
        """Get all fields (required + optional) for an endpoint."""
        endpoint = self.get_endpoint(endpoint_name)
        if not endpoint:
            return []
        return endpoint.fields + endpoint.optional_fields


# Global endpoint registry
endpoint_registry = EndpointRegistry()

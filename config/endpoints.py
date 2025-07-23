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
                    "customer_state", "direction", "duration", "recording",
                    "recording_duration", "recording_player", "start_time", 
                    "tracking_phone_number", "voicemail"
                ],
                optional_fields=[
                    "agent_email", "call_highlights", "call_summary", "call_type",
                    "campaign", "company_id", "company_name", "company_time_zone",
                    "created_at", "custom", "device_type", "fbclid", "first_call",
                    "formatted_call_type", "formatted_customer_location", "formatted_business_phone_number",
                    "formatted_customer_name", "formatted_customer_name_or_phone_number",
                    "formatted_customer_phone_number", "formatted_duration", "formatted_tracking_phone_number",
                    "formatted_tracking_source", "formatted_value", "ga", "gclid",
                    "good_lead_call_id", "good_lead_call_time", "keypad_entries", "keywords",
                    "keywords_spotted", "landing_page_url", "last_requested_url", "lead_status",
                    "medium", "milestones", "msclkid", "note", "person_id", "prior_calls",
                    "referrer_domain", "referring_url", "sentiment", "session_uuid",
                    "source", "source_name", "speaker_percent", "tags", "detail_tags",
                    "timeline_url", "total_calls", "tracker_id", "transcription",
                    "utm_campaign", "utm_content", "utm_medium", "utm_source", "utm_term",
                    "utma", "utmb", "utmc", "utmv", "utmz", "value", "voice_assist_message",
                    "waveforms", "zip_code", "blocked_number"
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
                    "id", "company_id", "person_id", "form_data", "form_url",
                    "landing_page_url", "referrer", "referring_url", "submitted_at",
                    "first_form", "customer_phone_number", "customer_name", "customer_email"
                ],
                optional_fields=[
                    "formatted_customer_phone_number", "formatted_customer_name",
                    "source", "keywords", "campaign", "medium", "lead_status",
                    "note", "tags", "detail_tags", "milestones", "value",
                    "utm_source", "utm_medium", "utm_campaign", "form_name",
                    "company_name", "person_email", "timeline_url", "blocked_number"
                ]
            ),
            
            "integrations": EndpointConfig(
                name="integrations",
                path="/v3/a/{account_id}/integrations.json",
                fields=[
                    "id", "config", "state", "type"
                ],
                optional_fields=[
                    "signing_key"
                ],
                requires_company_id=True
            ),
            
            "tags": EndpointConfig(
                name="tags",
                path="/v3/a/{account_id}/tags.json",
                fields=[
                    "id", "name", "tag_level", "color", "background_color", 
                    "company_id", "status", "disabled", "created_at", 
                    "hex_color", "hex_background_color"
                ],
                optional_fields=[]
            ),
            
            "trackers": EndpointConfig(
                name="trackers",
                path="/v3/a/{account_id}/trackers.json",
                fields=[
                    "id", "name", "type", "status", "destination_number", "created_at"
                ],
                optional_fields=[
                    "tracking_numbers", "whisper_message", "sms_supported", "sms_enabled", 
                    "company", "source", "call_flow", "disabled_at", "call_alerts", 
                    "sms_alerts", "swap_targets", "campaign_name", "message_flow"
                ]
            ),
            
            "users": EndpointConfig(
                name="users",
                path="/v3/a/{account_id}/users.json",
                fields=[
                    "id", "email", "first_name", "last_name", "role", "created_at"
                ],
                optional_fields=[
                    "name", "companies"
                ]
            ),
            
            "text_messages": EndpointConfig(
                name="text_messages",
                path="/v3/a/{account_id}/text-messages.json",
                fields=[
                    "id", "company_id", "initial_tracker_id", "current_tracker_id",
                    "customer_name", "customer_phone_number", "initial_tracking_number",
                    "current_tracking_number", "last_message_at", "state"
                ],
                optional_fields=[
                    "company_time_zone", "formatted_customer_phone_number",
                    "formatted_initial_tracking_number", "formatted_current_tracking_number",
                    "formatted_customer_name", "recent_messages", "lead_status", "source"
                ]
            ),
            
            "notifications": EndpointConfig(
                name="notifications",
                path="/v3/a/{account_id}/notifications.json",
                fields=[
                    "id", "config", "name", "company_id"
                ],
                optional_fields=[
                    "agent_id", "agent_name", "alert_type", "call_enabled", "company_name", 
                    "short_name", "send_desktop", "send_email", "send_push", "sms_enabled", 
                    "tags", "tracker_id", "tracker_name", "user_id", "email"
                ]
            ),
            
            "outbound_caller_ids": EndpointConfig(
                name="outbound_caller_ids",
                path="/v3/a/{account_id}/caller_ids.json",
                fields=[
                    "id", "phone_number", "name", "verified", "created_at"
                ],
                optional_fields=[
                    "company_id", "formatted_phone_number", "validation_code"
                ],
                requires_company_id=True
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

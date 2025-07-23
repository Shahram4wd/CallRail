# API Reference

## Overview

This document provides comprehensive reference information for all CallRail API v3 endpoints supported by the CallRail API Data Extractor, including field specifications, data types, and usage examples.

## Table of Contents

1. [Authentication](#authentication)
2. [Rate Limits](#rate-limits)
3. [Pagination](#pagination)
4. [Endpoint Reference](#endpoint-reference)
5. [Response Formats](#response-formats)
6. [Error Handling](#error-handling)
7. [Field Definitions](#field-definitions)

## Authentication

### API Key Authentication

All requests to the CallRail API require authentication using an API key.

**Header Format:**
```
Authorization: Token token=YOUR_API_KEY
```

**Example:**
```python
headers = {
    'Authorization': 'Token token=abc123def456',
    'Content-Type': 'application/json'
}
```

### Getting Your API Key

1. Log into your CallRail account
2. Navigate to **Settings** → **API**
3. Create a new API key or copy an existing one
4. Store securely and never expose in code or logs

## Rate Limits

### Limits

- **120 requests per minute** per API key
- **10 requests per second** burst limit
- Rate limit headers included in responses

### Rate Limit Headers

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 119
X-RateLimit-Reset: 1642694400
```

### Handling Rate Limits

The system automatically handles rate limits with exponential backoff:

```python
if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    time.sleep(retry_after)
```

## Pagination

### Pagination Types

**Offset-based pagination** (most endpoints):
```
GET /v3/a/{account_id}/calls.json?per_page=100&offset=0
```

**Relative pagination** (some endpoints):
```
GET /v3/a/{account_id}/calls.json?per_page=100&page=1
```

### Pagination Parameters

| Parameter | Type | Description | Default | Max |
|-----------|------|-------------|---------|-----|
| `per_page` | integer | Records per page | 100 | 250 |
| `offset` | integer | Number of records to skip | 0 | - |
| `page` | integer | Page number (1-based) | 1 | - |

## Endpoint Reference

### 1. Accounts

**Purpose**: Retrieve account information

**Endpoint**: `GET /v3/a.json`

**Authentication**: Required

**Pagination**: No

**Parameters**: None

**Response Structure**:
```json
{
  "accounts": [
    {
      "id": "ACC123456789",
      "name": "My Business",
      "created_at": "2023-01-01T00:00:00Z",
      "numeric_id": 123456789,
      "inbound_recording_enabled": true,
      "outbound_recording_enabled": false
    }
  ]
}
```

**Example Usage**:
```bash
curl -H "Authorization: Token token=YOUR_API_KEY" \
     https://api.callrail.com/v3/a.json
```

---

### 2. Calls

**Purpose**: Retrieve call records with detailed metadata

**Endpoint**: `GET /v3/a/{account_id}/calls.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Parameters**:
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `per_page` | integer | Records per page | 100 |
| `offset` | integer | Records to skip | 0 |
| `start_date` | string | Start date (YYYY-MM-DD) | 30 days ago |
| `end_date` | string | End date (YYYY-MM-DD) | Today |
| `fields` | string | Comma-separated field list | All fields |

**Response Structure**:
```json
{
  "calls": [
    {
      "id": "CAL123456789",
      "answered": true,
      "business_phone_number": "+15551234567",
      "customer_name": "John Doe",
      "customer_phone_number": "+15559876543",
      "direction": "inbound",
      "duration": 180,
      "start_time": "2023-07-23T10:05:13Z",
      "recording": "https://app.callrail.com/calls/123456789/recording",
      "tracking_phone_number": "+15551234567",
      "source": "google_organic",
      "keywords": "plumbing services",
      "landing_page": "https://example.com/plumbing",
      "referrer": "https://google.com"
    }
  ],
  "total_records": 500,
  "page": 1,
  "per_page": 100
}
```

**Available Fields**:
- `id` - Unique call identifier
- `answered` - Whether call was answered
- `business_phone_number` - Business phone number called
- `customer_city` - Customer's city
- `customer_country` - Customer's country
- `customer_name` - Customer's name (if available)
- `customer_phone_number` - Customer's phone number
- `customer_state` - Customer's state/province
- `direction` - Call direction (inbound/outbound)
- `duration` - Call duration in seconds
- `recording` - URL to call recording (if available)
- `start_time` - Call start timestamp
- `tracking_phone_number` - Tracking number used
- `source` - Traffic source
- `keywords` - Search keywords (if available)
- `landing_page` - Landing page URL
- `referrer` - Referrer URL

---

### 3. Companies

**Purpose**: Retrieve company information within accounts

**Endpoint**: `GET /v3/a/{account_id}/companies.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Response Structure**:
```json
{
  "companies": [
    {
      "id": "COM123456789",
      "name": "Main Company",
      "status": "active",
      "created_at": "2023-01-01T00:00:00Z",
      "time_zone": "America/New_York",
      "swap_exclude_jquery": false,
      "swap_ppc_override": false,
      "swap_landing_override": false,
      "swap_cookie_duration": 90
    }
  ]
}
```

---

### 4. Form Submissions

**Purpose**: Retrieve web form submission data

**Endpoint**: `GET /v3/a/{account_id}/form_submissions.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `company_id` | string | Filter by company ID |
| `start_date` | string | Start date filter |
| `end_date` | string | End date filter |

**Response Structure**:
```json
{
  "form_submissions": [
    {
      "id": "FRM123456789",
      "company_id": "COM123456789",
      "person_id": "PER123456789",
      "created_at": "2023-07-23T10:05:13Z",
      "form_url": "https://example.com/contact",
      "form_data": {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Interested in your services"
      },
      "referrer": "https://google.com",
      "landing_page": "https://example.com/landing"
    }
  ]
}
```

---

### 5. Integrations

**Purpose**: Retrieve third-party integration configurations

**Endpoint**: `GET /v3/a/{account_id}/companies/{company_id}/integrations.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Required Parameters**:
- `company_id` - Company identifier

**Response Structure**:
```json
{
  "integrations": [
    {
      "id": "INT123456789",
      "name": "Google Analytics",
      "integration_type": "google_analytics",
      "enabled": true,
      "created_at": "2023-01-01T00:00:00Z",
      "configuration": {
        "tracking_id": "UA-123456789-1",
        "enhanced_ecommerce": false
      }
    }
  ]
}
```

---

### 6. Tags

**Purpose**: Retrieve call and form tags for categorization

**Endpoint**: `GET /v3/a/{account_id}/tags.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Response Structure**:
```json
{
  "tags": [
    {
      "id": "TAG123456789",
      "name": "Lead - Hot",
      "color": "#ff0000",
      "tag_level": "call",
      "status": "active",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

**Available Fields**:
- `id` - Unique tag identifier
- `name` - Tag display name
- `color` - Hex color code for display
- `tag_level` - Where tag can be applied (call, account, etc.)
- `status` - Tag status (active/inactive)
- `created_at` - Tag creation timestamp

---

### 7. Trackers

**Purpose**: Retrieve phone number tracking configurations

**Endpoint**: `GET /v3/a/{account_id}/companies/{company_id}/trackers.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Required Parameters**:
- `company_id` - Company identifier

**Response Structure**:
```json
{
  "trackers": [
    {
      "id": "TRK123456789",
      "name": "Main Website Tracker",
      "type": "number_pool",
      "status": "active",
      "tracking_number": "+15551234567",
      "destination_number": "+15559876543",
      "source": "website",
      "created_at": "2023-01-01T00:00:00Z",
      "whisper_message": "Call from website"
    }
  ]
}
```

**Available Fields**:
- `id` - Unique tracker identifier  
- `name` - Tracker display name
- `type` - Tracker type (source_tracker, number_pool, etc.)
- `status` - Tracker status (active/paused/disabled)
- `tracking_number` - The tracking phone number
- `destination_number` - Where calls are forwarded
- `source` - Traffic source being tracked
- `whisper_message` - Message played to call recipient

---

### 8. Users

**Purpose**: Retrieve account user information and permissions

**Endpoint**: `GET /v3/a/{account_id}/users.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Response Structure**:
```json
{
  "users": [
    {
      "id": "USR123456789",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "admin",
      "status": "active",
      "created_at": "2023-01-01T00:00:00Z",
      "last_login": "2023-07-23T09:00:00Z"
    }
  ]
}
```

**Available Fields**:
- `id` - Unique user identifier
- `email` - User's email address
- `first_name` - User's first name
- `last_name` - User's last name
- `role` - User role (admin, user, read_only)
- `status` - User status (active/inactive)
- `created_at` - User creation timestamp
- `last_login` - Last login timestamp

---

### 9. Text Messages

**Purpose**: Retrieve SMS conversation data

**Endpoint**: `GET /v3/a/{account_id}/text-messages.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `start_date` | string | Start date filter |
| `end_date` | string | End date filter |
| `direction` | string | Message direction (inbound/outbound) |

**Response Structure**:
```json
{
  "text_messages": [
    {
      "id": "TXT123456789",
      "conversation_id": "CNV123456789",
      "direction": "inbound",
      "message": "Hello, I'm interested in your services",
      "from_number": "+15559876543",
      "to_number": "+15551234567",
      "created_at": "2023-07-23T10:05:13Z",
      "status": "delivered"
    }
  ]
}
```

---

### 10. Notifications

**Purpose**: Retrieve webhook notification configurations

**Endpoint**: `GET /v3/a/{account_id}/companies/{company_id}/notifications.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Required Parameters**:
- `company_id` - Company identifier

**Response Structure**:
```json
{
  "notifications": [
    {
      "id": "NOT123456789",
      "name": "New Call Webhook",
      "webhook_url": "https://example.com/webhook",
      "events": ["call.created", "call.completed"],
      "status": "active",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

---

### 11. Outbound Caller IDs

**Purpose**: Retrieve outbound caller ID configurations

**Endpoint**: `GET /v3/a/{account_id}/companies/{company_id}/caller_ids.json`

**Authentication**: Required

**Pagination**: Yes (offset-based)

**Required Parameters**:
- `company_id` - Company identifier

**Response Structure**:
```json
{
  "caller_ids": [
    {
      "id": "CID123456789",
      "phone_number": "+15551234567",
      "name": "Main Business Line",
      "status": "verified",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

## Response Formats

### Standard Response Structure

All API responses follow a consistent structure:

```json
{
  "data_key": [...],           // Main data array
  "total_records": 500,        // Total available records
  "page": 1,                   // Current page (if paginated)
  "per_page": 100,            // Records per page
  "total_pages": 5            // Total pages available
}
```

### Data Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text value | `"Hello World"` |
| `integer` | Whole number | `123` |
| `boolean` | True/false value | `true` |
| `datetime` | ISO 8601 timestamp | `"2023-07-23T10:05:13Z"` |
| `object` | Nested JSON object | `{"key": "value"}` |
| `array` | List of values | `["item1", "item2"]` |
| `null` | Empty/missing value | `null` |

### Timestamp Format

All timestamps use ISO 8601 format in UTC:
```
2023-07-23T10:05:13Z
```

**Parsing in Python**:
```python
from datetime import datetime
timestamp = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
```

## Error Handling

### HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Invalid or missing API key |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Temporary service issue |

### Error Response Format

```json
{
  "error": {
    "message": "Invalid API key provided",
    "code": "authentication_failed",
    "details": {
      "field": "api_key",
      "reason": "The provided API key is invalid or expired"
    }
  }
}
```

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `authentication_failed` | Invalid API key | Check API key validity |
| `rate_limit_exceeded` | Too many requests | Wait and retry with backoff |
| `invalid_parameters` | Invalid request parameters | Validate parameter values |
| `resource_not_found` | Requested resource doesn't exist | Check resource ID |
| `insufficient_permissions` | Access denied | Check API key permissions |

## Field Definitions

### Common Field Types

#### ID Fields
- **Format**: String with prefix (e.g., `ACC123456789`)
- **Pattern**: `[A-Z]{3}[0-9a-f]+`
- **Examples**: `ACC123456789`, `CAL987654321`, `COM555666777`

#### Phone Numbers
- **Format**: E.164 international format
- **Pattern**: `+1NNNNNNNNNN` (US/Canada)
- **Examples**: `+15551234567`, `+15559876543`

#### Timestamps
- **Format**: ISO 8601 UTC
- **Pattern**: `YYYY-MM-DDTHH:MM:SSZ`
- **Examples**: `2023-07-23T10:05:13Z`

#### URLs
- **Format**: Full HTTP/HTTPS URLs
- **Examples**: `https://example.com/page`, `https://app.callrail.com/recording/123`

### Field Validation Rules

#### Required Fields
Fields marked as required must be present in all responses:
- `id` - Always present for all records
- `created_at` - Creation timestamp for all records

#### Optional Fields
Optional fields may be `null` or missing:
- Customer information (may be unavailable)
- Recording URLs (only if recording enabled)
- Tracking data (depends on configuration)

#### Field Constraints

**String Fields**:
- Maximum length varies by field
- UTF-8 encoding
- May contain HTML entities

**Numeric Fields**:
- Integer values for counts and IDs
- Float values for durations and prices
- Non-negative for durations and counts

**Boolean Fields**:
- Always `true` or `false`
- Never `null` for boolean fields

### Data Consistency

#### Referential Integrity
- `account_id` references valid account
- `company_id` references company within account
- `tracking_phone_number` references active tracker

#### Data Freshness
- Real-time data for active calls
- Near real-time (1-5 minutes) for completed calls
- Batch updates for historical data corrections

#### Data Completeness
- Core fields always populated
- Extended fields may be missing based on:
  - Account configuration
  - Feature availability
  - Data source limitations

## Usage Examples

### Python Client Example

```python
import requests
from datetime import datetime, timedelta

class CallRailAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.callrail.com'
        self.headers = {
            'Authorization': f'Token token={api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_calls(self, account_id, start_date=None, limit=100):
        """Get recent calls for an account."""
        
        # Default to last 30 days
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        
        params = {
            'per_page': limit,
            'start_date': start_date.strftime('%Y-%m-%d')
        }
        
        url = f'{self.base_url}/v3/a/{account_id}/calls.json'
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()

# Usage
client = CallRailAPI('your_api_key')
calls = client.get_calls('ACC123456789', limit=50)
print(f"Retrieved {len(calls['calls'])} calls")
```

### cURL Examples

**Get account information**:
```bash
curl -H "Authorization: Token token=YOUR_API_KEY" \
     https://api.callrail.com/v3/a.json
```

**Get recent calls with pagination**:
```bash
curl -H "Authorization: Token token=YOUR_API_KEY" \
     "https://api.callrail.com/v3/a/ACC123456789/calls.json?per_page=50&offset=0"
```

**Get company users**:
```bash
curl -H "Authorization: Token token=YOUR_API_KEY" \
     https://api.callrail.com/v3/a/ACC123456789/users.json
```

---

*This API reference provides comprehensive documentation for integrating with the CallRail API v3. For the most current information, always refer to the official [CallRail API documentation](https://apidocs.callrail.com/).*

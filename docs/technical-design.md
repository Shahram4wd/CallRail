# Technical Design Document (TDD)

## Document Information

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Date** | July 23, 2025 |
| **Status** | Production Ready |
| **Authors** | CallRail API Team |
| **Reviewers** | System Architecture Team |

## 1. Executive Summary

The CallRail API Data Extractor is a Python-based system designed to provide comprehensive data extraction capabilities from all CallRail API v3 endpoints. The system emphasizes reliability, extensibility, and maintainability while providing robust error handling and progress tracking.

### 1.1 Key Requirements
- Extract data from all 11 CallRail API v3 endpoints
- Support batch processing with configurable limits
- Provide real-time progress tracking
- Export data to structured CSV format
- Handle API rate limits and errors gracefully
- Support both individual and bulk endpoint processing

### 1.2 Success Criteria
- ✅ 100% endpoint coverage (11/11 endpoints)
- ✅ Zero data loss during extraction
- ✅ Automatic error recovery and retry
- ✅ Sub-second response time for system initialization
- ✅ Memory-efficient processing of large datasets

## 2. System Design

### 2.1 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Runtime** | Python | 3.13.5 | Core application runtime |
| **HTTP Client** | requests | ≥2.28.0 | API communication |
| **CLI Framework** | Click | Latest | Command-line interface |
| **Progress UI** | tqdm | Latest | Progress indicators |
| **Data Processing** | pandas | Latest | CSV operations |
| **Configuration** | python-dotenv | ≥0.19.0 | Environment management |
| **Logging** | Python logging | Built-in | System logging |

### 2.2 Core Architecture

#### 2.2.1 MasterDownloader Class

```python
class MasterDownloader:
    """Main orchestrator for data extraction operations."""
    
    def __init__(self, api_key: str):
        self.client = CallRailClient(api_key)
        self.account_id = None
        self.results = {}
        self.processor_classes = {
            # Processor mapping for all endpoints
        }
```

**Key Responsibilities:**
- Processor lifecycle management
- Progress coordination
- Error aggregation and reporting
- Results summarization

#### 2.2.2 BaseProcessor Class Hierarchy

```python
class BaseProcessor:
    """Abstract base class for all endpoint processors."""
    
    def __init__(self, client: CallRailClient):
        self.client = client
        self.endpoint_config = None
        self.logger = logger
    
    def process(self, limit: int, batch_size: int) -> ProcessingResult:
        """Template method for processing workflow."""
        # Common processing logic
```

**Design Patterns:**
- **Template Method**: Common workflow with endpoint-specific customization
- **Factory**: Dynamic processor creation
- **Strategy**: Different pagination approaches

### 2.3 Data Flow Architecture

#### 2.3.1 Request Flow

```
CLI Command → MasterDownloader → Processor → CallRailClient → CallRail API
     ↓              ↓               ↓             ↓              ↓
Progress UI ← Results Summary ← Processing ← HTTP Response ← JSON Data
```

#### 2.3.2 Error Flow

```
API Error → CallRailClient → Processor → MasterDownloader → User
    ↓             ↓            ↓             ↓               ↓
Retry Logic → Log Entry → Error Handling → Summary → CLI Output
```

## 3. Detailed Component Design

### 3.1 CallRailClient

**File**: `callrail_api/client.py`

```python
class CallRailClient:
    """HTTP client for CallRail API communication."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.callrail.com"
        self.session = requests.Session()
        self._setup_session()
    
    def get(self, endpoint: str, params: dict) -> dict:
        """Execute GET request with retry logic."""
        # Implementation with exponential backoff
```

**Key Features:**
- Session-based connection pooling
- Automatic retry with exponential backoff (max 3 attempts)
- Rate limit detection and handling
- Comprehensive error logging
- Response validation and parsing

**Error Handling:**
```python
try:
    response = self.session.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"API request failed: {e}")
    if attempt < max_retries:
        time.sleep(2 ** attempt)  # Exponential backoff
        continue
    raise
```

### 3.2 Configuration System

**File**: `config/endpoints.py`

```python
@dataclass
class EndpointConfig:
    """Configuration for API endpoints."""
    name: str
    path: str
    fields: List[str]
    optional_fields: List[str]
    supports_pagination: bool = True
    pagination_type: str = "offset"
    max_per_page: int = 250
    requires_account_id: bool = True
    requires_company_id: bool = False
```

**Configuration Registry:**
- Centralized endpoint definitions
- Field validation specifications
- Pagination configuration
- Parameter requirements

### 3.3 Processing Pipeline

#### 3.3.1 Data Processing Flow

```python
def process(self, limit: int, batch_size: int) -> ProcessingResult:
    """Main processing pipeline."""
    
    # 1. Initialize processing
    self._setup_processing(limit, batch_size)
    
    # 2. Execute batch processing
    for batch_num in range(total_batches):
        batch_data = self._process_batch(batch_num)
        self._write_batch_to_csv(batch_data)
        self._update_progress()
    
    # 3. Finalize processing
    return self._finalize_processing()
```

#### 3.3.2 Batch Processing Logic

```python
def _process_batch(self, batch_num: int) -> List[dict]:
    """Process a single batch of records."""
    
    # Calculate pagination parameters
    offset = batch_num * self.batch_size
    params = self._build_request_params(offset)
    
    # Execute API request
    response = self.client.get(self.endpoint_config.path, params)
    
    # Process and validate data
    records = self._extract_records(response)
    filtered_records = self._filter_fields(records)
    
    return filtered_records
```

### 3.4 Progress Tracking System

**File**: `utils/progress_tracker.py`

```python
class ProgressTracker:
    """Manages progress tracking across the application."""
    
    def __init__(self):
        self.main_progress = None
        self.batch_progress = None
    
    def create_main_progress(self, total: int, description: str):
        """Create main progress bar for endpoint processing."""
        self.main_progress = tqdm(
            total=total,
            desc=description,
            unit="it",
            position=0
        )
    
    def create_batch_progress(self, total: int, description: str):
        """Create batch progress bar for record processing."""
        self.batch_progress = tqdm(
            total=total,
            desc=description,
            unit="records",
            position=1
        )
```

## 4. API Integration Design

### 4.1 Endpoint Mapping

| Endpoint | Path | Method | Auth | Pagination |
|----------|------|--------|------|------------|
| accounts | `/v3/a.json` | GET | API Key | No |
| calls | `/v3/a/{account_id}/calls.json` | GET | API Key | Yes |
| companies | `/v3/a/{account_id}/companies.json` | GET | API Key | Yes |
| form_submissions | `/v3/a/{account_id}/form_submissions.json` | GET | API Key | Yes |
| integrations | `/v3/a/{account_id}/companies/{company_id}/integrations.json` | GET | API Key | Yes |
| tags | `/v3/a/{account_id}/tags.json` | GET | API Key | Yes |
| trackers | `/v3/a/{account_id}/companies/{company_id}/trackers.json` | GET | API Key | Yes |
| users | `/v3/a/{account_id}/users.json` | GET | API Key | Yes |
| text_messages | `/v3/a/{account_id}/text-messages.json` | GET | API Key | Yes |
| notifications | `/v3/a/{account_id}/companies/{company_id}/notifications.json` | GET | API Key | Yes |
| outbound_caller_ids | `/v3/a/{account_id}/companies/{company_id}/caller_ids.json` | GET | API Key | Yes |

### 4.2 Authentication

```python
headers = {
    'Authorization': f'Token token={self.api_key}',
    'Content-Type': 'application/json',
    'User-Agent': 'CallRail-Data-Extractor/1.0.0'
}
```

### 4.3 Rate Limiting

**CallRail API Limits:**
- 120 requests per minute per API key
- Burst limit: 10 requests per second

**Implementation:**
```python
def _handle_rate_limit(self, response):
    """Handle rate limit responses."""
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 60))
        logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        return True
    return False
```

## 5. Data Processing Design

### 5.1 Field Validation

```python
def _filter_fields(self, records: List[dict]) -> List[dict]:
    """Filter records to include only configured fields."""
    
    if self.endpoint_config.name in FIELD_FILTER_SKIP_LIST:
        return records  # Skip filtering for problematic endpoints
    
    allowed_fields = (
        self.endpoint_config.fields + 
        self.endpoint_config.optional_fields
    )
    
    filtered_records = []
    for record in records:
        filtered_record = {
            field: record.get(field, '')
            for field in allowed_fields
            if field in record
        }
        filtered_records.append(filtered_record)
    
    return filtered_records
```

### 5.2 CSV Export

```python
def _write_to_csv(self, records: List[dict], filename: str):
    """Write records to CSV file."""
    
    if not records:
        logger.info(f"No records to write for {filename}")
        return
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Write CSV with proper encoding
    filepath = f'data/{filename}'
    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False, encoding='utf-8')
    
    logger.info(f"Successfully wrote {len(records)} records to {filepath}")
```

## 6. Error Handling Design

### 6.1 Error Classification

| Error Type | HTTP Status | Handling Strategy |
|------------|-------------|-------------------|
| **Authentication** | 401 | Fail fast with clear message |
| **Authorization** | 403 | Log and skip endpoint |
| **Not Found** | 404 | Log and continue (empty result) |
| **Rate Limited** | 429 | Retry with exponential backoff |
| **Server Error** | 5xx | Retry with exponential backoff |
| **Network** | Timeout | Retry with exponential backoff |

### 6.2 Retry Logic

```python
def _execute_with_retry(self, func, *args, **kwargs):
    """Execute function with retry logic."""
    
    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries + 1):
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.RequestException, 
                requests.exceptions.Timeout) as e:
            
            if attempt == max_retries:
                logger.error(f"Max retries exceeded: {e}")
                raise
            
            delay = base_delay * (2 ** attempt)  # Exponential backoff
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
            time.sleep(delay)
```

## 7. Performance Considerations

### 7.1 Memory Management

**Strategy**: Streaming processing to avoid loading large datasets into memory.

```python
def _process_streaming(self, limit: int, batch_size: int):
    """Process data in streams to manage memory usage."""
    
    processed_count = 0
    current_offset = 0
    
    while processed_count < limit:
        # Process small batches
        batch_limit = min(batch_size, limit - processed_count)
        batch_data = self._fetch_batch(current_offset, batch_limit)
        
        if not batch_data:
            break
        
        # Write immediately to CSV (don't accumulate in memory)
        self._append_to_csv(batch_data)
        
        processed_count += len(batch_data)
        current_offset += batch_limit
```

### 7.2 Concurrency Considerations

**Current State**: Sequential processing for simplicity and API rate limit compliance.

**Future Enhancement**: Parallel processing with rate limit coordination.

```python
# Future implementation concept
async def _process_endpoints_parallel(self, endpoints: List[str]):
    """Process multiple endpoints concurrently."""
    
    semaphore = asyncio.Semaphore(5)  # Limit concurrent requests
    
    async def process_endpoint(endpoint_name):
        async with semaphore:
            processor = self._create_processor(endpoint_name)
            return await processor.process_async()
    
    tasks = [process_endpoint(ep) for ep in endpoints]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results
```

## 8. Testing Strategy

### 8.1 Unit Testing

**Coverage Areas:**
- API client request/response handling
- Processor data transformation logic
- Configuration validation
- Error handling scenarios

**Test Structure:**
```python
class TestCallRailClient:
    def test_successful_request(self):
        # Test successful API request
        pass
    
    def test_retry_on_timeout(self):
        # Test retry logic for timeouts
        pass
    
    def test_rate_limit_handling(self):
        # Test rate limit response handling
        pass
```

### 8.2 Integration Testing

**System Test**: `test_system.py`
```python
def test_full_system_integration():
    """Test complete system with real API calls."""
    
    downloader = MasterDownloader(api_key=test_api_key)
    
    # Test single endpoint
    result = downloader.download_endpoints(['accounts'], limit=1)
    assert result['total_records'] > 0
    assert result['total_errors'] == 0
    
    # Test multiple endpoints
    result = downloader.download_endpoints(
        ['accounts', 'calls'], 
        limit=10
    )
    assert result['successful_endpoints'] == 2
```

## 9. Deployment Architecture

### 9.1 Environment Requirements

| Requirement | Specification |
|-------------|---------------|
| **Python Version** | 3.8+ (tested with 3.13.5) |
| **Memory** | 512MB minimum, 2GB recommended |
| **Storage** | 1GB free space for data and logs |
| **Network** | HTTPS access to api.callrail.com |
| **OS** | Windows, macOS, Linux |

### 9.2 Configuration Management

**Environment Variables:**
```bash
CALLRAIL_API_KEY=your_api_key_here
LOG_LEVEL=INFO
DATA_DIR=./data
BATCH_SIZE=100
MAX_RETRIES=3
```

**Configuration Files:**
- `.env`: Environment-specific configuration
- `config/settings.py`: Application settings
- `config/endpoints.py`: API endpoint definitions

## 10. Monitoring and Logging

### 10.1 Logging Strategy

**Log Levels:**
- **DEBUG**: Detailed diagnostic information
- **INFO**: General operational messages
- **WARNING**: Warning conditions (retries, rate limits)
- **ERROR**: Error conditions that don't stop execution
- **CRITICAL**: Error conditions that stop execution

**Log Format:**
```
2025-07-23 10:05:13,047 - callrail_extractor - INFO - Initialized MasterDownloader
```

### 10.2 Metrics Collection

**Key Metrics:**
- Total processing time
- Records per endpoint
- Error rates
- API response times
- Memory usage

**Summary Report:**
```
Total time: 10.17 seconds
Total endpoints: 11
Successful endpoints: 11
Failed endpoints: 0
Total records downloaded: 288
Total errors: 0
```

## 11. Security Considerations

### 11.1 API Key Management

**Storage**: Environment variables only
**Access**: Never logged or exposed in error messages
**Rotation**: Support for key rotation without code changes

### 11.2 Data Security

**Local Storage**: CSV files with appropriate file permissions
**Network**: All API communications over HTTPS
**Logging**: Sensitive data excluded from log files

## 12. Future Enhancements

### 12.1 Planned Features

1. **Parallel Processing**: Concurrent endpoint processing with rate limit coordination
2. **Data Validation**: Enhanced data quality checks and validation
3. **Export Formats**: Support for JSON, XML, and database exports
4. **Incremental Updates**: Delta processing for large datasets
5. **Web Interface**: Optional web-based management interface
6. **Scheduling**: Cron-like scheduling for automated extractions

### 12.2 Scalability Roadmap

1. **Phase 1**: Current implementation (Sequential processing)
2. **Phase 2**: Parallel endpoint processing
3. **Phase 3**: Distributed processing with message queues
4. **Phase 4**: Microservice architecture with API gateway

---

*This Technical Design Document provides the detailed technical foundation for implementing, maintaining, and extending the CallRail API Data Extractor system.*

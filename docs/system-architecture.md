# System Architecture

## Overview

The CallRail API Data Extractor is designed as a modular, scalable system for automated data extraction from CallRail's API v3. The architecture follows separation of concerns principles with distinct layers for API communication, data processing, configuration management, and output generation.

## High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Layer    │    │  Control Layer  │    │  Output Layer   │
│                 │    │                 │    │                 │
│ • CLI Interface │───▶│ Master          │───▶│ • CSV Files     │
│ • Commands      │    │ Downloader      │    │ • Log Files     │
│ • Parameters    │    │                 │    │ • Progress UI   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Processing Layer│
                       │                 │
                       │ • Processors    │
                       │ • Base Classes  │
                       │ • Validators    │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   API Layer     │
                       │                 │
                       │ • CallRail      │
                       │   Client        │
                       │ • HTTP Handling │
                       │ • Rate Limiting │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Config Layer   │
                       │                 │
                       │ • Endpoints     │
                       │ • Settings      │
                       │ • Field Maps    │
                       └─────────────────┘
```

## Core Components

### 1. User Interface Layer

**Component**: Command Line Interface (CLI)
- **File**: `master_downloader.py`
- **Purpose**: Provides user interaction and command parsing
- **Key Features**:
  - Click-based CLI with intuitive commands
  - Parameter validation and help documentation
  - Support for single endpoint or bulk downloads
  - Configurable limits and batch sizes

### 2. Control Layer

**Component**: MasterDownloader
- **File**: `master_downloader.py`
- **Purpose**: Orchestrates the entire data extraction process
- **Responsibilities**:
  - Manages processor lifecycle
  - Coordinates progress tracking
  - Handles error aggregation
  - Provides summary reporting

### 3. Processing Layer

**Components**: Endpoint Processors
- **Files**: `processors/` directory
- **Purpose**: Handles endpoint-specific data processing logic
- **Architecture**:
  ```
  BaseProcessor (Abstract)
  ├── AccountsProcessor
  ├── CallsProcessor
  └── GenericProcessor
      ├── CompaniesProcessor
      ├── FormSubmissionsProcessor
      ├── IntegrationsProcessor
      ├── TagsProcessor
      ├── TrackersProcessor
      ├── UsersProcessor
      ├── TextMessagesProcessor
      ├── NotificationsProcessor
      └── OutboundCallerIdsProcessor
  ```

### 4. API Communication Layer

**Component**: CallRailClient
- **File**: `callrail_api/client.py`
- **Purpose**: Handles all HTTP communication with CallRail API
- **Features**:
  - RESTful API client with session management
  - Automatic retry with exponential backoff
  - Rate limit handling and respect
  - Request/response logging
  - Error handling and transformation

### 5. Configuration Layer

**Components**: Configuration Management
- **Files**: `config/` directory
- **Purpose**: Centralizes all system configuration
- **Components**:
  - `endpoints.py`: API endpoint definitions
  - `settings.py`: System-wide settings
  - Field mappings and validation rules

### 6. Utility Layer

**Components**: Support Services
- **Files**: `utils/` directory
- **Purpose**: Provides cross-cutting concerns
- **Services**:
  - Logging with structured output
  - Progress tracking with visual indicators
  - File operations and CSV generation
  - Data validation and transformation

## Data Flow

### 1. Initialization Phase
```
User Command → CLI Parser → MasterDownloader → Account ID Retrieval
```

### 2. Processing Phase
```
For each endpoint:
  Configuration Lookup → Processor Creation → API Requests → Data Processing → CSV Output
```

### 3. Completion Phase
```
Result Aggregation → Summary Generation → Progress Completion → Log Finalization
```

## Design Patterns

### 1. Factory Pattern
- **Location**: MasterDownloader processor mapping
- **Purpose**: Dynamic processor creation based on endpoint names
- **Benefits**: Extensibility, loose coupling

### 2. Template Method Pattern
- **Location**: BaseProcessor class hierarchy
- **Purpose**: Common processing workflow with endpoint-specific customization
- **Benefits**: Code reuse, consistent behavior

### 3. Strategy Pattern
- **Location**: Pagination handling in processors
- **Purpose**: Different pagination strategies for different endpoints
- **Benefits**: Flexibility, maintainability

### 4. Observer Pattern
- **Location**: Progress tracking system
- **Purpose**: Real-time progress updates across components
- **Benefits**: Decoupling, real-time feedback

## Scalability Considerations

### Horizontal Scaling
- **Processor Independence**: Each processor can run independently
- **Batch Processing**: Configurable batch sizes for memory management
- **Concurrent Processing**: Future enhancement for parallel endpoint processing

### Vertical Scaling
- **Memory Management**: Streaming data processing to handle large datasets
- **Rate Limiting**: Built-in respect for API constraints
- **Error Recovery**: Robust retry mechanisms for transient failures

## Security Architecture

### API Security
- **API Key Management**: Environment variable storage
- **HTTPS Communication**: All API calls use secure connections
- **Rate Limiting**: Prevents API abuse

### Data Security
- **Local Storage**: CSV files stored locally with appropriate permissions
- **Logging**: Sensitive data excluded from logs
- **Environment Isolation**: Configuration separated from code

## Extensibility Points

### Adding New Endpoints
1. Create endpoint configuration in `config/endpoints.py`
2. Implement processor class (inherit from BaseProcessor or GenericProcessor)
3. Register processor in MasterDownloader mapping
4. Add CLI command support if needed

### Custom Data Processing
1. Override processing methods in custom processor
2. Implement custom field validation
3. Add endpoint-specific error handling

### Output Formats
1. Extend base processor with new output methods
2. Add format selection to CLI
3. Implement format-specific validation

## Quality Attributes

### Reliability
- **Error Handling**: Comprehensive exception handling at all layers
- **Retry Logic**: Exponential backoff for transient failures
- **Data Validation**: Field validation and data integrity checks

### Maintainability
- **Modular Design**: Clear separation of concerns
- **Documentation**: Comprehensive inline documentation
- **Logging**: Detailed operation logging for debugging

### Performance
- **Batch Processing**: Efficient data processing in configurable batches
- **Progress Tracking**: Non-blocking progress updates
- **Memory Management**: Streaming processing for large datasets

### Usability
- **CLI Interface**: Intuitive command-line interface
- **Progress Feedback**: Real-time progress indicators
- **Error Messages**: Clear, actionable error messages

---

*This document provides the architectural foundation for understanding and extending the CallRail API Data Extractor system.*

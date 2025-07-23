# CallRail API Data Extractor

A comprehensive Python system for downloading data from all CallRail API endpoints and saving them to CSV files. This system provides modular, batch processing with retry mechanisms, progress tracking, and proper logging.

## Features

- **Complete API Coverage**: Supports all major CallRail API v3 endpoints
- **Modular Architecture**: Separate processors for each endpoint
- **Batch Processing**: Efficient handling of large datasets
- **Retry Mechanism**: Automatic retry with exponential backoff
- **Progress Tracking**: Real-time progress bars for downloads
- **Comprehensive Logging**: Detailed logs with configurable levels
- **CSV Export**: Clean CSV files with all available fields
- **Rate Limit Handling**: Respects API rate limits
- **Error Handling**: Robust error handling and reporting

## Supported Endpoints

- **accounts** - Account information
- **calls** - Call records with detailed metadata
- **companies** - Company data within accounts
- **form_submissions** - Web form submissions
- **integrations** - Third-party integrations
- **tags** - Call and form tags
- **trackers** - Phone number trackers
- **users** - Account users
- **text_messages** - SMS conversations
- **notifications** - Webhook notifications
- **outbound_caller_ids** - Outbound caller ID numbers

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd CallRail
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your CallRail API key
   CALLRAIL_API_KEY=your_api_key_here
   ```

## Quick Start

### Download All Endpoints
```bash
python master_downloader.py --all --limit 100
```

### Download Specific Endpoints
```bash
python master_downloader.py --endpoints accounts,calls,companies --limit 50
```

### List Available Endpoints
```bash
python master_downloader.py --list-endpoints
```

### Get Endpoint Information
```bash
python master_downloader.py --endpoint-info calls
```

## Usage Examples

### Basic Usage
```bash
# Download the last 100 records from all endpoints
python master_downloader.py --all --limit 100

# Download specific endpoints with custom batch size
python master_downloader.py --endpoints calls,form_submissions --limit 500 --batch-size 50

# Download with maximum records (default: 100 per endpoint)
python master_downloader.py --endpoints accounts,users
```

### Advanced Usage
```bash
# Set custom environment variables
export CALLRAIL_MAX_RECORDS=1000
export CALLRAIL_BATCH_SIZE=200
export CALLRAIL_LOG_LEVEL=DEBUG

python master_downloader.py --all
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CALLRAIL_API_KEY` | Your CallRail API key | Required |
| `CALLRAIL_MAX_RECORDS` | Max records per endpoint | 100 |
| `CALLRAIL_BATCH_SIZE` | Batch size for processing | 100 |
| `CALLRAIL_MAX_RETRIES` | Max retry attempts | 3 |
| `CALLRAIL_LOG_LEVEL` | Logging level | INFO |
| `CALLRAIL_DATA_DIR` | Output directory | data |

### Configuration Files

- **`config/settings.py`** - Main configuration settings
- **`config/endpoints.py`** - Endpoint definitions and field mappings
- **`.env`** - Environment variables (create from `.env.example`)

## Output

### CSV Files
- Files are saved in the `data/` directory
- Each endpoint creates a separate CSV file (e.g., `accounts.csv`, `calls.csv`)
- Files include all available fields for each endpoint
- Headers are automatically included

### Logs
- Logs are written to `logs/callrail_extractor.log`
- Log file is overwritten on each run (configurable)
- Console output shows progress and summary information

## System Architecture

### Core Components

1. **Master Downloader** (`master_downloader.py`)
   - Main orchestrator for all downloads
   - Handles command-line interface
   - Manages progress tracking and reporting

2. **Processors** (`processors/`)
   - `base_processor.py` - Abstract base class
   - `accounts_processor.py` - Accounts endpoint
   - `calls_processor.py` - Calls endpoint
   - `generic_processor.py` - Other endpoints

3. **Utilities** (`utils/`)
   - `logger.py` - Logging configuration
   - `retry_handler.py` - Retry mechanism
   - `progress_tracker.py` - Progress bars
   - `csv_writer.py` - CSV file generation

4. **Configuration** (`config/`)
   - `settings.py` - Application settings
   - `endpoints.py` - API endpoint definitions

5. **Models** (`models/`)
   - `extended_models.py` - Data models for validation

### Data Flow

1. **Initialization**: Load configuration and authenticate with API
2. **Account Discovery**: Fetch account ID for endpoints that require it
3. **Batch Processing**: Download data in configurable batch sizes
4. **Data Processing**: Clean and validate records using models
5. **CSV Export**: Write processed data to CSV files
6. **Progress Tracking**: Real-time progress bars and logging
7. **Error Handling**: Retry failed requests with exponential backoff

## Testing

### Run System Test
```bash
python test_system.py
```

### Test Specific Functionality
```bash
# Test the existing client
python test_client.py

# Test with specific endpoints
python master_downloader.py --endpoints accounts --limit 5
```

## Error Handling

The system includes comprehensive error handling:

- **API Errors**: Automatic retry with exponential backoff
- **Rate Limiting**: Respects API rate limits with appropriate delays
- **Network Issues**: Retry mechanism for transient network problems
- **Data Validation**: Graceful handling of malformed data
- **File I/O**: Proper error handling for file operations

## Logging

Logs include:
- API request/response details
- Processing progress and timing
- Error messages with full stack traces
- Summary statistics for each run

Log levels:
- `DEBUG`: Detailed API and processing information
- `INFO`: General progress and summary information
- `WARNING`: Non-fatal issues and data problems
- `ERROR`: Errors that prevent processing

## Performance

### Optimization Features
- Batch processing to minimize API calls
- Configurable batch sizes for memory management
- Progress tracking for long-running operations
- Efficient CSV writing with streaming
- Connection pooling for API requests

### Typical Performance
- **Accounts**: ~1-5 records, <1 second
- **Calls**: ~100-1000 records, 10-60 seconds
- **Companies**: ~10-50 records, 2-10 seconds
- **Other endpoints**: Varies by data volume

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```
   Error: Invalid API key or authentication failed
   Solution: Check your CALLRAIL_API_KEY environment variable
   ```

2. **Rate Limiting**
   ```
   Error: Rate limit exceeded
   Solution: The system automatically handles this with retries
   ```

3. **No Data Returned**
   ```
   Warning: No account data returned
   Solution: Check if your API key has access to the account
   ```

4. **Unicode Encoding Issues**
   ```
   Error: 'charmap' codec can't encode character
   Solution: System has been updated to handle Unicode properly
   ```

### Debug Mode
```bash
export CALLRAIL_LOG_LEVEL=DEBUG
python master_downloader.py --endpoints accounts --limit 5
```

## API Documentation

For detailed information about CallRail API endpoints and fields, refer to:
- [CallRail API Documentation](https://apidocs.callrail.com/#api)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for detailed error information
3. Consult the CallRail API documentation
4. Open an issue in the repository

## Version History

- **v1.0.0** - Initial release with full endpoint support
  - Complete API coverage for CallRail v3
  - Modular processor architecture
  - Batch processing with retry mechanisms
  - Progress tracking and comprehensive logging
  - CSV export with all available fields

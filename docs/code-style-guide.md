# Code Style Guide

## Overview

This document establishes coding standards and best practices for the CallRail API Data Extractor project to ensure consistency, maintainability, and readability across the codebase.

## Table of Contents

1. [General Principles](#general-principles)
2. [Python Style Guidelines](#python-style-guidelines)
3. [Code Organization](#code-organization)
4. [Naming Conventions](#naming-conventions)
5. [Documentation Standards](#documentation-standards)
6. [Error Handling](#error-handling)
7. [Testing Standards](#testing-standards)
8. [Code Formatting Tools](#code-formatting-tools)

## General Principles

### 1. Readability First
- Code should be self-documenting
- Prefer explicit over implicit
- Use meaningful names for variables, functions, and classes
- Keep functions and classes focused on a single responsibility

### 2. Consistency
- Follow established patterns throughout the codebase
- Use consistent naming conventions
- Maintain consistent code structure and organization

### 3. Maintainability
- Write code that's easy to modify and extend
- Use proper abstraction and encapsulation
- Minimize dependencies and coupling

### 4. Robustness
- Handle errors gracefully
- Validate inputs and outputs
- Use appropriate logging and monitoring

## Python Style Guidelines

This project follows [PEP 8](https://pep8.org/) with some project-specific additions and clarifications.

### Import Organization

```python
"""
Import order:
1. Standard library imports
2. Related third-party imports
3. Local/project imports
"""

# Standard library
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party
import requests
import click
from tqdm import tqdm

# Local imports
from callrail_api.client import CallRailClient
from config.endpoints import endpoint_registry
from utils.logger import logger
```

### Line Length and Formatting

```python
# Maximum line length: 88 characters (Black default)
# Use parentheses for line continuation

# Good
result = self.client.get(
    endpoint_path,
    params={
        'per_page': batch_size,
        'offset': offset,
        'fields': ','.join(fields)
    }
)

# Avoid using backslashes for line continuation
# Bad
result = self.client.get(endpoint_path, \
                        params={'per_page': batch_size})
```

### String Formatting

```python
# Prefer f-strings for string formatting
name = "CallRail"
version = "1.0.0"

# Good
message = f"Starting {name} version {version}"

# Acceptable for compatibility
message = "Starting {} version {}".format(name, version)

# Avoid % formatting (unless required for logging)
# Bad
message = "Starting %s version %s" % (name, version)
```

### Type Hints

```python
"""Use type hints for all public functions and methods."""

from typing import Dict, List, Optional, Union, Any

def process_endpoint(
    self,
    endpoint_name: str,
    limit: Optional[int] = None,
    batch_size: int = 100
) -> Dict[str, Any]:
    """Process a single endpoint with type hints."""
    pass

# For complex types, use type aliases
ProcessingResult = Dict[str, Union[int, str, List[Dict[str, Any]]]]

def get_results(self) -> ProcessingResult:
    """Return processing results."""
    pass
```

### Exception Handling

```python
"""Exception handling best practices."""

# Specific exception handling
try:
    response = self.client.get(endpoint)
    data = response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"API request failed: {e}")
    raise
except ValueError as e:
    logger.error(f"Invalid JSON response: {e}")
    raise

# Use context managers for resource management
with open(file_path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Don't catch and ignore exceptions
# Bad
try:
    risky_operation()
except Exception:
    pass  # Never do this
```

## Code Organization

### Project Structure

```
callrail_extractor/
├── callrail_api/          # Core API client
│   ├── __init__.py
│   ├── client.py          # Main API client
│   ├── exceptions.py      # Custom exceptions
│   └── models.py          # Data models
├── config/                # Configuration
│   ├── __init__.py
│   ├── endpoints.py       # Endpoint definitions
│   └── settings.py        # Application settings
├── processors/            # Data processors
│   ├── __init__.py
│   ├── base_processor.py  # Base processor class
│   ├── accounts_processor.py
│   ├── calls_processor.py
│   └── generic_processor.py
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── logger.py          # Logging configuration
│   ├── progress_tracker.py # Progress tracking
│   └── csv_writer.py      # CSV utilities
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_client.py
│   ├── test_processors.py
│   └── fixtures/
└── master_downloader.py   # Main application
```

### Module Organization

```python
"""
Standard module structure:
1. Module docstring
2. Imports
3. Constants
4. Exception classes
5. Helper functions
6. Main classes
7. Module-level code (if any)
"""

"""
CallRail API client module.

This module provides the main interface for interacting with the CallRail API.
"""

import os
import time
from typing import Dict, Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
BASE_URL = 'https://api.callrail.com'

# Exceptions
class CallRailAPIError(Exception):
    """Base exception for CallRail API errors."""
    pass

# Helper functions
def _build_headers(api_key: str) -> Dict[str, str]:
    """Build request headers."""
    return {
        'Authorization': f'Token token={api_key}',
        'Content-Type': 'application/json'
    }

# Main classes
class CallRailClient:
    """Client for CallRail API interactions."""
    
    def __init__(self, api_key: str):
        """Initialize the client."""
        pass
```

## Naming Conventions

### Variables and Functions

```python
# Use snake_case for variables and functions
user_count = 10
batch_size = 100

def get_account_id():
    """Get the account ID."""
    pass

def process_batch_data(data_batch):
    """Process a batch of data."""
    pass

# Use descriptive names
# Good
total_records_processed = 0
api_response_timeout = 30

# Bad
n = 0
t = 30
```

### Classes

```python
# Use PascalCase for class names
class CallRailClient:
    """Client for CallRail API."""
    pass

class BaseProcessor:
    """Base class for data processors."""
    pass

class EndpointConfig:
    """Configuration for API endpoints."""
    pass
```

### Constants

```python
# Use UPPER_CASE for constants
API_BASE_URL = 'https://api.callrail.com'
DEFAULT_BATCH_SIZE = 100
MAX_RETRY_ATTEMPTS = 3

# Group related constants
class HTTPStatus:
    """HTTP status codes."""
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    RATE_LIMITED = 429
```

### File and Directory Names

```python
# Use snake_case for file names
# Good
base_processor.py
accounts_processor.py
progress_tracker.py

# Bad
BaseProcessor.py
accountsProcessor.py
progressTracker.py

# Use descriptive directory names
processors/     # Not proc/
configuration/  # Not config/ (unless very common)
utilities/      # Not utils/ (unless very common)
```

## Documentation Standards

### Module Docstrings

```python
"""
CallRail API Data Extractor - Main Application Module.

This module provides the main entry point for the CallRail API data extraction
system. It includes the MasterDownloader class which orchestrates the entire
data extraction process across all supported endpoints.

Example:
    Basic usage of the downloader:

    >>> from master_downloader import MasterDownloader
    >>> downloader = MasterDownloader(api_key='your_key')
    >>> results = downloader.download_all_endpoints(limit=100)

Attributes:
    logger: Module-level logger instance
    
Classes:
    MasterDownloader: Main orchestrator for data extraction

Functions:
    main: CLI entry point
"""
```

### Class Docstrings

```python
class CallRailClient:
    """
    HTTP client for CallRail API interactions.
    
    This class provides a high-level interface for making requests to the
    CallRail API v3. It handles authentication, rate limiting, retries,
    and error handling automatically.
    
    Attributes:
        api_key (str): The CallRail API key for authentication
        base_url (str): Base URL for the CallRail API
        session (requests.Session): HTTP session for connection pooling
        
    Example:
        Basic client usage:
        
        >>> client = CallRailClient('your_api_key')
        >>> response = client.get('/v3/a.json')
        >>> accounts = response['accounts']
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the CallRail API client.
        
        Args:
            api_key: Valid CallRail API key for authentication
            
        Raises:
            ValueError: If api_key is empty or None
            CallRailAPIError: If initial connection fails
        """
        pass
```

### Function Docstrings

```python
def process_endpoint(
    self,
    endpoint_name: str,
    limit: Optional[int] = None,
    batch_size: int = 100
) -> Dict[str, Any]:
    """
    Process data from a specific CallRail API endpoint.
    
    This method handles the complete processing workflow for a single
    endpoint, including pagination, data transformation, and CSV output.
    
    Args:
        endpoint_name: Name of the endpoint to process (e.g., 'calls', 'accounts')
        limit: Maximum number of records to process. If None, processes all
            available records.
        batch_size: Number of records to process in each API request.
            Must be between 1 and 250.
    
    Returns:
        Dictionary containing processing results with the following keys:
        - 'total_records': Total number of records processed
        - 'processing_time': Time taken to process in seconds
        - 'output_file': Path to the generated CSV file
        - 'errors': List of any errors encountered
    
    Raises:
        ValueError: If endpoint_name is not supported or batch_size is invalid
        CallRailAPIError: If API requests fail after all retries
        IOError: If CSV file cannot be written
        
    Example:
        >>> processor = DataProcessor(client)
        >>> result = processor.process_endpoint('calls', limit=100)
        >>> print(f"Processed {result['total_records']} records")
    """
    pass
```

### Inline Comments

```python
def _build_request_params(self, offset: int, limit: int) -> Dict[str, Any]:
    """Build parameters for API request."""
    params = {
        'per_page': min(limit, self.batch_size),  # Respect API limits
        'offset': offset
    }
    
    # Add company_id for endpoints that require it
    if self.endpoint_config.requires_company_id:
        company_id = self.get_company_id()
        if company_id:
            params['company_id'] = company_id
    
    # Include only specified fields to reduce response size
    if self.endpoint_config.fields:
        params['fields'] = ','.join(self.endpoint_config.fields)
    
    return params
```

## Error Handling

### Custom Exceptions

```python
"""Define project-specific exceptions."""

class CallRailExtractorError(Exception):
    """Base exception for CallRail Extractor."""
    pass

class APIError(CallRailExtractorError):
    """API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class ConfigurationError(CallRailExtractorError):
    """Configuration-related errors."""
    pass

class ProcessingError(CallRailExtractorError):
    """Data processing errors."""
    
    def __init__(self, message: str, endpoint: Optional[str] = None):
        super().__init__(message)
        self.endpoint = endpoint
```

### Error Handling Patterns

```python
"""Error handling best practices."""

def process_data(self, data: List[Dict]) -> List[Dict]:
    """Process data with proper error handling."""
    
    processed_data = []
    errors = []
    
    for i, record in enumerate(data):
        try:
            # Process individual record
            processed_record = self._process_record(record)
            processed_data.append(processed_record)
            
        except (ValueError, KeyError) as e:
            # Log error but continue processing
            error_msg = f"Error processing record {i}: {e}"
            logger.warning(error_msg)
            errors.append(error_msg)
            continue
            
        except Exception as e:
            # Unexpected error - log and re-raise
            logger.error(f"Unexpected error processing record {i}: {e}")
            raise ProcessingError(f"Processing failed at record {i}") from e
    
    # Log summary
    if errors:
        logger.warning(f"Processing completed with {len(errors)} errors")
    
    return processed_data

def _process_record(self, record: Dict) -> Dict:
    """Process a single record with validation."""
    
    # Validate required fields
    required_fields = ['id', 'created_at']
    for field in required_fields:
        if field not in record:
            raise ValueError(f"Missing required field: {field}")
    
    # Process the record
    processed = {
        'id': str(record['id']),
        'created_at': self._parse_datetime(record['created_at']),
        # ... other processing
    }
    
    return processed
```

### Logging Standards

```python
"""Logging best practices."""

import logging

# Configure logger at module level
logger = logging.getLogger(__name__)

class DataProcessor:
    """Example class with proper logging."""
    
    def __init__(self, client):
        self.client = client
        # Don't create new logger instances in classes
        self.logger = logger
    
    def process_endpoint(self, endpoint_name: str) -> Dict:
        """Process endpoint with comprehensive logging."""
        
        # Info level for normal operations
        self.logger.info(f"Starting processing for endpoint: {endpoint_name}")
        
        start_time = time.time()
        
        try:
            # Debug level for detailed information
            self.logger.debug(f"Endpoint config: {self.endpoint_config}")
            
            results = self._do_processing()
            
            # Info level for completion
            processing_time = time.time() - start_time
            self.logger.info(
                f"Completed {endpoint_name}: {results['count']} records "
                f"in {processing_time:.2f}s"
            )
            
            return results
            
        except Exception as e:
            # Error level for exceptions
            self.logger.error(
                f"Failed processing {endpoint_name}: {e}",
                exc_info=True  # Include traceback
            )
            raise
    
    def _handle_api_response(self, response):
        """Handle API response with appropriate logging."""
        
        if response.status_code == 429:
            # Warning for rate limits
            retry_after = response.headers.get('Retry-After', 60)
            self.logger.warning(f"Rate limited, waiting {retry_after}s")
            
        elif response.status_code >= 400:
            # Error for HTTP errors
            self.logger.error(
                f"API error {response.status_code}: {response.text}"
            )
            
        else:
            # Debug for successful responses
            self.logger.debug(f"API response: {response.status_code}")
```

## Testing Standards

### Test Organization

```python
"""Test organization and structure."""

import pytest
from unittest.mock import Mock, patch
from callrail_api.client import CallRailClient

class TestCallRailClient:
    """Test suite for CallRailClient."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.api_key = 'test_api_key'
        self.client = CallRailClient(self.api_key)
    
    def test_initialization(self):
        """Test client initialization."""
        assert self.client.api_key == self.api_key
        assert self.client.base_url == 'https://api.callrail.com'
    
    @patch('requests.Session.get')
    def test_successful_request(self, mock_get):
        """Test successful API request."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_get.return_value = mock_response
        
        # Act
        result = self.client.get('/test/endpoint')
        
        # Assert
        assert result == {'data': 'test'}
        mock_get.assert_called_once()
    
    @patch('requests.Session.get')
    def test_request_timeout(self, mock_get):
        """Test request timeout handling."""
        # Arrange
        mock_get.side_effect = requests.exceptions.Timeout()
        
        # Act & Assert
        with pytest.raises(APIError):
            self.client.get('/test/endpoint')
    
    @pytest.mark.parametrize("status_code,expected_exception", [
        (401, APIError),
        (404, APIError),
        (500, APIError)
    ])
    def test_error_status_codes(self, status_code, expected_exception):
        """Test handling of various HTTP error codes."""
        with patch('requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = status_code
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
            mock_get.return_value = mock_response
            
            with pytest.raises(expected_exception):
                self.client.get('/test/endpoint')
```

### Test Naming

```python
"""Test naming conventions."""

class TestDataProcessor:
    """Tests for DataProcessor class."""
    
    # Test method naming: test_[method]_[scenario]_[expected_result]
    def test_process_endpoint_with_valid_data_returns_success(self):
        """Test processing valid endpoint data returns success."""
        pass
    
    def test_process_endpoint_with_invalid_api_key_raises_auth_error(self):
        """Test processing with invalid API key raises authentication error."""
        pass
    
    def test_process_endpoint_with_empty_response_returns_zero_records(self):
        """Test processing empty API response returns zero records."""
        pass
    
    # Integration test naming
    def test_integration_full_endpoint_processing_workflow(self):
        """Integration test for complete endpoint processing workflow."""
        pass
```

## Code Formatting Tools

### Black Configuration

Create `.black` or add to `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

### Flake8 Configuration

Create `.flake8`:

```ini
[flake8]
max-line-length = 88
extend-ignore = 
    # E203: whitespace before ':'
    E203,
    # W503: line break before binary operator
    W503
exclude = 
    .git,
    __pycache__,
    venv,
    .venv,
    dist,
    build,
    *.egg-info
per-file-ignores =
    # Allow unused imports in __init__.py files
    __init__.py:F401
    # Allow long lines in configuration files
    config/*.py:E501
```

### MyPy Configuration

Create `mypy.ini` or add to `pyproject.toml`:

```ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True

[mypy-tests.*]
disallow_untyped_defs = False

[mypy-requests.*]
ignore_missing_imports = True

[mypy-tqdm.*]
ignore_missing_imports = True
```

### Pre-commit Configuration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### IDE Configuration

#### VS Code Settings (`.vscode/settings.json`)

```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.lintOnSave": true,
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "python.defaultInterpreterPath": "./venv/bin/python"
}
```

### Code Quality Scripts

#### Format Script (`scripts/format.sh`)

```bash
#!/bin/bash
# Code formatting script

echo "Running code formatting..."

# Format with Black
echo "Formatting with Black..."
black .

# Sort imports with isort
echo "Sorting imports with isort..."
isort .

# Lint with flake8
echo "Linting with flake8..."
flake8 .

# Type check with mypy
echo "Type checking with mypy..."
mypy .

echo "Code formatting complete!"
```

#### Quality Check Script (`scripts/quality-check.sh`)

```bash
#!/bin/bash
# Code quality check script

set -e

echo "Running code quality checks..."

# Check formatting
echo "Checking code formatting..."
black --check .

# Check import sorting
echo "Checking import sorting..."
isort --check-only .

# Lint code
echo "Linting code..."
flake8 .

# Type checking
echo "Type checking..."
mypy .

# Run tests
echo "Running tests..."
pytest tests/ -v --cov=. --cov-report=term-missing

echo "All quality checks passed!"
```

### Makefile for Development

```makefile
# Makefile for CallRail API Extractor

.PHONY: help install format lint test clean

help:
	@echo "Available commands:"
	@echo "  install    Install dependencies"
	@echo "  format     Format code with black and isort"
	@echo "  lint       Run linting checks"
	@echo "  test       Run test suite"
	@echo "  clean      Clean build artifacts"

install:
	pip install -r requirements-dev.txt
	pre-commit install

format:
	black .
	isort .

lint:
	flake8 .
	mypy .

test:
	pytest tests/ -v --cov=. --cov-report=term-missing

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build dist .coverage .pytest_cache .mypy_cache
```

---

*This code style guide ensures consistent, maintainable, and high-quality code across the CallRail API Data Extractor project. All contributors should follow these guidelines to maintain code quality and readability.*

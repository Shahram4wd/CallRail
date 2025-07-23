# Environment Documentation

## Overview

This document provides comprehensive information about setting up and managing environments for the CallRail API Data Extractor, including development, testing, staging, and production environments.

## Table of Contents

1. [Environment Types](#environment-types)
2. [Python Environment Setup](#python-environment-setup)
3. [Virtual Environment Management](#virtual-environment-management)
4. [Environment Variables](#environment-variables)
5. [Configuration Management](#configuration-management)
6. [Dependency Management](#dependency-management)
7. [Environment Validation](#environment-validation)

## Environment Types

### Development Environment

**Purpose**: Local development and testing
**Location**: Developer workstations
**Data**: Sample/test data
**API**: Development API keys with limited access

**Characteristics:**
- Debug logging enabled
- Smaller batch sizes for faster testing
- Automatic code reloading
- Comprehensive error reporting

### Testing Environment

**Purpose**: Automated testing and CI/CD
**Location**: CI/CD servers (GitHub Actions, Jenkins, etc.)
**Data**: Mock data and test fixtures
**API**: Test API keys or mock services

**Characteristics:**
- Automated test execution
- Code coverage reporting
- Performance benchmarking
- Integration testing

### Staging Environment

**Purpose**: Production-like testing before deployment
**Location**: Staging servers
**Data**: Sanitized production data copy
**API**: Staging API keys

**Characteristics:**
- Production-like configuration
- Full feature testing
- Performance validation
- User acceptance testing

### Production Environment

**Purpose**: Live system serving real users
**Location**: Production servers
**Data**: Live CallRail data
**API**: Production API keys

**Characteristics:**
- Optimized performance settings
- Error monitoring and alerting
- Backup and recovery systems
- Security hardening

## Python Environment Setup

### Python Version Management

#### Using pyenv (Recommended for Development)

**Install pyenv:**

```bash
# macOS with Homebrew
brew install pyenv

# Linux
curl https://pyenv.run | bash

# Add to shell profile
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

**Install and use Python version:**

```bash
# List available versions
pyenv install --list | grep 3.11

# Install Python 3.11
pyenv install 3.11.7

# Set global version
pyenv global 3.11.7

# Set local version for project
cd /path/to/CallRail
pyenv local 3.11.7

# Verify version
python --version
```

#### Direct Python Installation

**Windows:**
1. Download from [python.org](https://python.org)
2. Run installer with "Add Python to PATH" checked
3. Verify installation: `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Verify installation
python3.11 --version
```

**Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3.11 python3.11-venv python3.11-pip

# Verify installation
python3.11 --version
```

### System Dependencies

#### Development Dependencies

**Windows:**
- Git for Windows
- Windows Terminal (recommended)
- Visual Studio Code or similar editor

**macOS:**
```bash
# Install Xcode command line tools
xcode-select --install

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install git curl wget
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3.11-dev
```

## Virtual Environment Management

### Creating Virtual Environments

#### Standard venv (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Verify activation
which python
pip --version
```

#### virtualenv Alternative

```bash
# Install virtualenv
pip install virtualenv

# Create virtual environment
virtualenv venv --python=python3.11

# Activate (same as venv)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

#### conda Environment

```bash
# Create conda environment
conda create -n callrail python=3.11

# Activate environment
conda activate callrail

# Install pip packages
pip install -r requirements.txt

# Deactivate
conda deactivate
```

### Environment Management Scripts

#### Setup Script (`setup-env.sh`)

```bash
#!/bin/bash
# Environment setup script for CallRail API Extractor

set -e

echo "Setting up CallRail API Extractor environment..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher required. Found: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p data logs

# Copy environment template
if [ ! -f .env ]; then
    echo "Creating environment file..."
    cp .env.example .env
    echo "Please edit .env with your CallRail API key"
fi

echo "Environment setup complete!"
echo "To activate: source venv/bin/activate"
echo "To test: python master_downloader.py --help"
```

#### Windows Setup Script (`setup-env.ps1`)

```powershell
# CallRail API Extractor Environment Setup Script
Write-Host "Setting up CallRail API Extractor environment..." -ForegroundColor Green

# Check Python version
$pythonVersion = python --version 2>&1
if ($pythonVersion -notmatch "Python 3\.([8-9]|\d{2})") {
    Write-Error "Python 3.8 or higher required. Found: $pythonVersion"
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "data", "logs"

# Copy environment template
if (!(Test-Path ".env")) {
    Write-Host "Creating environment file..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "Please edit .env with your CallRail API key" -ForegroundColor Red
}

Write-Host "Environment setup complete!" -ForegroundColor Green
Write-Host "To activate: venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "To test: python master_downloader.py --help" -ForegroundColor Cyan
```

### Environment Activation Scripts

#### Bash Activation (`activate-env.sh`)

```bash
#!/bin/bash
# Quick environment activation script

# Change to project directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
    echo "Python: $(which python)"
    echo "Current directory: $(pwd)"
else
    echo "Virtual environment not found. Run setup-env.sh first."
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "Environment variables loaded"
else
    echo "Warning: .env file not found"
fi

# Start new shell with environment
exec "$SHELL"
```

#### PowerShell Activation (`Activate-Env.ps1`)

```powershell
# Quick environment activation script for Windows

# Change to project directory
Set-Location $PSScriptRoot

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "Virtual environment activated" -ForegroundColor Green
    Write-Host "Python: $(Get-Command python | Select-Object -ExpandProperty Source)" -ForegroundColor Cyan
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Cyan
} else {
    Write-Error "Virtual environment not found. Run setup-env.ps1 first."
    exit 1
}

# Load environment variables
if (Test-Path ".env") {
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^([^#][^=]+)=(.*)$") {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
    Write-Host "Environment variables loaded" -ForegroundColor Green
} else {
    Write-Warning ".env file not found"
}
```

## Environment Variables

### Required Variables

| Variable | Description | Example | Default |
|----------|-------------|---------|---------|
| `CALLRAIL_API_KEY` | CallRail API authentication key | `abc123...` | None (required) |

### Optional Configuration Variables

| Variable | Description | Development | Production |
|----------|-------------|-------------|------------|
| `LOG_LEVEL` | Logging verbosity | `DEBUG` | `INFO` |
| `DATA_DIR` | Output directory for CSV files | `./data` | `/var/lib/callrail/data` |
| `BATCH_SIZE` | Records per API request | `10` | `100` |
| `MAX_RETRIES` | Maximum retry attempts | `3` | `5` |
| `REQUEST_TIMEOUT` | API request timeout (seconds) | `60` | `30` |
| `RATE_LIMIT_DELAY` | Delay between requests (seconds) | `2` | `1` |

### Environment-Specific Configuration

#### Development Environment (`.env.development`)

```env
# Development Configuration
CALLRAIL_API_KEY=your_dev_api_key_here

# Debug settings
LOG_LEVEL=DEBUG
LOG_FORMAT=detailed

# Small batches for fast testing
BATCH_SIZE=10
DEFAULT_LIMIT=5
REQUEST_TIMEOUT=60

# Development paths
DATA_DIR=./dev-data
LOG_DIR=./dev-logs

# Feature flags
ENABLE_PROGRESS_BARS=true
ENABLE_CSV_VALIDATION=true
SKIP_FIELD_FILTERING=true
```

#### Testing Environment (`.env.testing`)

```env
# Testing Configuration
CALLRAIL_API_KEY=mock_api_key_for_testing

# Test settings
LOG_LEVEL=WARNING
BATCH_SIZE=5
DEFAULT_LIMIT=3
REQUEST_TIMEOUT=10

# Test paths
DATA_DIR=./test-data
LOG_DIR=./test-logs

# Test-specific flags
MOCK_API_RESPONSES=true
VALIDATE_OUTPUT=true
CLEANUP_AFTER_TEST=true
```

#### Production Environment (`.env.production`)

```env
# Production Configuration
CALLRAIL_API_KEY=${CALLRAIL_API_KEY}  # From secure storage

# Performance settings
LOG_LEVEL=INFO
BATCH_SIZE=100
DEFAULT_LIMIT=1000
REQUEST_TIMEOUT=30
RATE_LIMIT_DELAY=1

# Production paths
DATA_DIR=/var/lib/callrail/data
LOG_DIR=/var/log/callrail

# Production optimizations
ENABLE_PROGRESS_BARS=false
COMPRESS_LOGS=true
ROTATE_LOGS=true
```

### Environment Variable Loading

#### Python dotenv Loading

```python
# config/environment.py
import os
from pathlib import Path
from dotenv import load_dotenv

def load_environment(env_name=None):
    """Load environment-specific configuration."""
    
    # Determine environment
    env_name = env_name or os.getenv('ENV', 'development')
    
    # Load base environment
    base_env = Path('.env')
    if base_env.exists():
        load_dotenv(base_env)
    
    # Load environment-specific overrides
    env_file = Path(f'.env.{env_name}')
    if env_file.exists():
        load_dotenv(env_file, override=True)
    
    # Validate required variables
    required_vars = ['CALLRAIL_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {missing_vars}")
    
    return env_name

# Usage in application
from config.environment import load_environment

env_name = load_environment()
print(f"Loaded {env_name} environment")
```

#### Shell Environment Loading

```bash
# load-env.sh
#!/bin/bash

ENV_NAME=${1:-development}
ENV_FILE=".env.${ENV_NAME}"

if [ -f ".env" ]; then
    echo "Loading base environment..."
    export $(cat .env | grep -v '^#' | xargs)
fi

if [ -f "$ENV_FILE" ]; then
    echo "Loading $ENV_NAME environment..."
    export $(cat "$ENV_FILE" | grep -v '^#' | xargs)
else
    echo "Warning: $ENV_FILE not found"
fi

echo "Environment: $ENV_NAME"
echo "API Key configured: $([ -n "$CALLRAIL_API_KEY" ] && echo "Yes" || echo "No")"
```

## Configuration Management

### Configuration Files Structure

```
config/
├── __init__.py
├── base.py              # Base configuration
├── development.py       # Development overrides
├── testing.py          # Testing configuration
├── production.py       # Production configuration
└── environments.py     # Environment loading logic
```

#### Base Configuration (`config/base.py`)

```python
"""Base configuration for all environments."""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = Path(os.getenv('DATA_DIR', BASE_DIR / 'data'))
LOG_DIR = Path(os.getenv('LOG_DIR', BASE_DIR / 'logs'))

# API Configuration
API_BASE_URL = 'https://api.callrail.com'
API_VERSION = 'v3'
API_KEY = os.getenv('CALLRAIL_API_KEY')

# Processing defaults
DEFAULT_BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))
DEFAULT_LIMIT = int(os.getenv('DEFAULT_LIMIT', 100))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Feature flags
ENABLE_PROGRESS_BARS = os.getenv('ENABLE_PROGRESS_BARS', 'true').lower() == 'true'
VALIDATE_CSV_OUTPUT = os.getenv('VALIDATE_CSV_OUTPUT', 'false').lower() == 'true'
```

#### Development Configuration (`config/development.py`)

```python
"""Development environment configuration."""
from .base import *

# Override for development
LOG_LEVEL = 'DEBUG'
DEFAULT_BATCH_SIZE = 10
DEFAULT_LIMIT = 5
REQUEST_TIMEOUT = 60

# Development features
ENABLE_PROGRESS_BARS = True
VALIDATE_CSV_OUTPUT = True
DETAILED_ERROR_MESSAGES = True

# Development paths
DATA_DIR = BASE_DIR / 'dev-data'
LOG_DIR = BASE_DIR / 'dev-logs'
```

#### Production Configuration (`config/production.py`)

```python
"""Production environment configuration."""
from .base import *

# Production optimizations
DEFAULT_BATCH_SIZE = 100
DEFAULT_LIMIT = 1000
REQUEST_TIMEOUT = 30
MAX_RETRIES = 5

# Production features
ENABLE_PROGRESS_BARS = False
COMPRESS_LOGS = True
ROTATE_LOGS = True

# Production paths
DATA_DIR = Path('/var/lib/callrail/data')
LOG_DIR = Path('/var/log/callrail')
```

### Dynamic Configuration Loading

```python
# config/__init__.py
"""Configuration module with environment-aware loading."""
import os
import importlib

def get_config():
    """Load configuration based on environment."""
    env = os.getenv('ENV', 'development')
    
    try:
        config_module = importlib.import_module(f'config.{env}')
        return config_module
    except ImportError:
        # Fallback to base configuration
        from . import base
        return base

# Usage
from config import get_config
config = get_config()

print(f"API Key configured: {bool(config.API_KEY)}")
print(f"Data directory: {config.DATA_DIR}")
print(f"Log level: {config.LOG_LEVEL}")
```

## Dependency Management

### Requirements Files

#### Base Requirements (`requirements.txt`)

```txt
# Core dependencies
requests>=2.28.0
click>=8.0.0
tqdm>=4.64.0
python-dotenv>=0.19.0
dataclasses-json>=0.5.7
typing-extensions>=4.0.0

# CSV processing
pandas>=1.5.0

# Date/time handling
python-dateutil>=2.8.0
```

#### Development Requirements (`requirements-dev.txt`)

```txt
# Include base requirements
-r requirements.txt

# Development tools
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=1.0.0
pre-commit>=3.0.0

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.0.0

# Debugging
ipython>=8.0.0
ipdb>=0.13.0
```

#### Testing Requirements (`requirements-test.txt`)

```txt
# Include base requirements
-r requirements.txt

# Testing framework
pytest>=7.0.0
pytest-mock>=3.10.0
pytest-asyncio>=0.21.0
responses>=0.23.0

# Coverage reporting
coverage>=7.0.0
pytest-cov>=4.0.0

# Performance testing
pytest-benchmark>=4.0.0
```

### Dependency Installation Scripts

#### Install Script (`install-deps.sh`)

```bash
#!/bin/bash
# Dependency installation script

set -e

# Determine environment
ENV=${1:-development}

echo "Installing dependencies for $ENV environment..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found"
    exit 1
fi

# Upgrade pip
pip install --upgrade pip

# Install based on environment
case $ENV in
    "development")
        pip install -r requirements-dev.txt
        ;;
    "testing")
        pip install -r requirements-test.txt
        ;;
    "production")
        pip install -r requirements.txt
        ;;
    *)
        echo "Unknown environment: $ENV"
        echo "Usage: $0 [development|testing|production]"
        exit 1
        ;;
esac

# Verify installation
echo "Verifying installation..."
python -c "
import requests, click, tqdm, dotenv
print('✓ All core packages installed successfully')
"

# Create freeze file
pip freeze > requirements-frozen.txt
echo "✓ Created requirements-frozen.txt"

echo "Dependencies installed successfully for $ENV environment"
```

### Version Pinning Strategy

#### Development Strategy
- Use minimum version requirements (`>=`) for flexibility
- Pin specific versions only when necessary for compatibility
- Regular updates to latest stable versions

#### Production Strategy
- Pin exact versions for reproducibility
- Use `pip freeze` to capture exact environment
- Controlled updates with thorough testing

```bash
# Create production requirements with exact versions
pip freeze > requirements-production.txt

# Install exact versions in production
pip install -r requirements-production.txt
```

## Environment Validation

### Validation Script (`validate-env.py`)

```python
#!/usr/bin/env python3
"""Environment validation script for CallRail API Extractor."""

import os
import sys
import importlib
from pathlib import Path
from typing import List, Tuple

class EnvironmentValidator:
    """Validates environment configuration and dependencies."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_python_version(self) -> bool:
        """Validate Python version."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.errors.append(f"Python 3.8+ required, found {version.major}.{version.minor}")
            return False
        return True
    
    def validate_dependencies(self) -> bool:
        """Validate required dependencies."""
        required_packages = [
            'requests', 'click', 'tqdm', 'dotenv', 
            'dataclasses_json', 'typing_extensions'
        ]
        
        missing = []
        for package in required_packages:
            try:
                importlib.import_module(package.replace('-', '_'))
            except ImportError:
                missing.append(package)
        
        if missing:
            self.errors.append(f"Missing packages: {', '.join(missing)}")
            return False
        return True
    
    def validate_environment_variables(self) -> bool:
        """Validate environment variables."""
        required_vars = ['CALLRAIL_API_KEY']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            self.errors.append(f"Missing environment variables: {', '.join(missing_vars)}")
            return False
        
        # Validate API key format
        api_key = os.getenv('CALLRAIL_API_KEY', '')
        if len(api_key) < 10:
            self.warnings.append("API key appears to be too short")
        
        return True
    
    def validate_directories(self) -> bool:
        """Validate required directories."""
        required_dirs = ['data', 'logs']
        
        for dir_name in required_dirs:
            path = Path(dir_name)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                except OSError as e:
                    self.errors.append(f"Cannot create directory {dir_name}: {e}")
                    return False
            
            # Check write permissions
            if not os.access(path, os.W_OK):
                self.errors.append(f"No write permission for directory {dir_name}")
                return False
        
        return True
    
    def validate_configuration(self) -> bool:
        """Validate configuration files."""
        config_files = ['.env']
        
        for config_file in config_files:
            if not Path(config_file).exists():
                self.warnings.append(f"Configuration file {config_file} not found")
        
        return True
    
    def run_all_validations(self) -> bool:
        """Run all validations."""
        validations = [
            ("Python Version", self.validate_python_version),
            ("Dependencies", self.validate_dependencies),
            ("Environment Variables", self.validate_environment_variables),
            ("Directories", self.validate_directories),
            ("Configuration", self.validate_configuration),
        ]
        
        all_passed = True
        for name, validation_func in validations:
            try:
                passed = validation_func()
                status = "✓ PASS" if passed else "✗ FAIL"
                print(f"{name:<25} {status}")
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"{name:<25} ✗ ERROR: {e}")
                all_passed = False
        
        return all_passed
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 50)
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  ✗ {error}")
        
        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if not self.errors and not self.warnings:
            print("✓ All validations passed - Environment is ready!")
        elif not self.errors:
            print("✓ Environment is ready (with warnings)")
        else:
            print("✗ Environment validation failed")
        
        print("=" * 50)

def main():
    """Main validation function."""
    print("CallRail API Extractor - Environment Validation")
    print("=" * 50)
    
    validator = EnvironmentValidator()
    success = validator.run_all_validations()
    validator.print_summary()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

### Automated Environment Testing

#### Environment Test Suite (`test_environment.py`)

```python
"""Environment-specific test suite."""
import os
import pytest
from pathlib import Path

class TestEnvironment:
    """Test environment configuration."""
    
    def test_api_key_configured(self):
        """Test that API key is configured."""
        api_key = os.getenv('CALLRAIL_API_KEY')
        assert api_key is not None, "CALLRAIL_API_KEY not configured"
        assert len(api_key) > 10, "API key appears invalid"
    
    def test_directories_exist(self):
        """Test that required directories exist."""
        required_dirs = ['data', 'logs']
        for dir_name in required_dirs:
            path = Path(dir_name)
            assert path.exists(), f"Directory {dir_name} does not exist"
            assert path.is_dir(), f"{dir_name} is not a directory"
    
    def test_write_permissions(self):
        """Test write permissions for data directories."""
        test_dirs = ['data', 'logs']
        for dir_name in test_dirs:
            path = Path(dir_name)
            assert os.access(path, os.W_OK), f"No write permission for {dir_name}"
    
    def test_configuration_values(self):
        """Test configuration value types and ranges."""
        batch_size = int(os.getenv('BATCH_SIZE', 100))
        assert 1 <= batch_size <= 250, f"Invalid batch size: {batch_size}"
        
        max_retries = int(os.getenv('MAX_RETRIES', 3))
        assert 1 <= max_retries <= 10, f"Invalid max retries: {max_retries}"
        
        timeout = int(os.getenv('REQUEST_TIMEOUT', 30))
        assert 5 <= timeout <= 300, f"Invalid timeout: {timeout}"

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Environment Health Monitoring

#### Health Check Service (`health_monitor.py`)

```python
"""Environment health monitoring service."""
import os
import time
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EnvironmentHealthMonitor:
    """Monitor environment health metrics."""
    
    def __init__(self):
        self.checks = {
            'disk_space': self.check_disk_space,
            'memory_usage': self.check_memory_usage,
            'api_connectivity': self.check_api_connectivity,
            'log_file_size': self.check_log_file_size,
        }
    
    def check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space."""
        data_dir = Path(os.getenv('DATA_DIR', './data'))
        
        try:
            stat = os.statvfs(data_dir)
            free_bytes = stat.f_frsize * stat.f_bavail
            free_gb = free_bytes / (1024**3)
            
            status = 'healthy' if free_gb > 1 else 'warning' if free_gb > 0.1 else 'critical'
            
            return {
                'status': status,
                'free_space_gb': round(free_gb, 2),
                'message': f"Free disk space: {free_gb:.2f} GB"
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error checking disk space: {e}"
            }
    
    def check_memory_usage(self) -> Dict[str, Any]:
        """Check memory usage."""
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            usage_percent = memory.percent
            status = 'healthy' if usage_percent < 80 else 'warning' if usage_percent < 95 else 'critical'
            
            return {
                'status': status,
                'usage_percent': usage_percent,
                'message': f"Memory usage: {usage_percent}%"
            }
        except ImportError:
            return {
                'status': 'unknown',
                'message': "psutil not available for memory monitoring"
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error checking memory: {e}"
            }
    
    def check_api_connectivity(self) -> Dict[str, Any]:
        """Check API connectivity."""
        try:
            import requests
            response = requests.get('https://api.callrail.com', timeout=10)
            
            status = 'healthy' if response.status_code < 500 else 'warning'
            
            return {
                'status': status,
                'response_code': response.status_code,
                'message': f"API response: {response.status_code}"
            }
        except Exception as e:
            return {
                'status': 'critical',
                'message': f"API connectivity error: {e}"
            }
    
    def check_log_file_size(self) -> Dict[str, Any]:
        """Check log file sizes."""
        log_dir = Path(os.getenv('LOG_DIR', './logs'))
        
        try:
            total_size = sum(f.stat().st_size for f in log_dir.glob('*.log'))
            size_mb = total_size / (1024**2)
            
            status = 'healthy' if size_mb < 100 else 'warning' if size_mb < 500 else 'critical'
            
            return {
                'status': status,
                'size_mb': round(size_mb, 2),
                'message': f"Log files size: {size_mb:.2f} MB"
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error checking log files: {e}"
            }
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {}
        overall_status = 'healthy'
        
        for check_name, check_func in self.checks.items():
            try:
                result = check_func()
                results[check_name] = result
                
                # Update overall status
                if result['status'] == 'critical':
                    overall_status = 'critical'
                elif result['status'] in ['warning', 'error'] and overall_status == 'healthy':
                    overall_status = 'warning'
                    
            except Exception as e:
                results[check_name] = {
                    'status': 'error',
                    'message': f"Health check failed: {e}"
                }
                if overall_status == 'healthy':
                    overall_status = 'warning'
        
        results['overall'] = {
            'status': overall_status,
            'timestamp': time.time(),
            'message': f"Overall system status: {overall_status}"
        }
        
        return results

# CLI interface for health monitoring
if __name__ == "__main__":
    monitor = EnvironmentHealthMonitor()
    results = monitor.run_health_check()
    
    print("Environment Health Check Results:")
    print("=" * 40)
    
    for check_name, result in results.items():
        status_icon = {
            'healthy': '✓',
            'warning': '⚠',
            'critical': '✗',
            'error': '✗',
            'unknown': '?'
        }.get(result['status'], '?')
        
        print(f"{status_icon} {check_name}: {result['message']}")
    
    # Exit with appropriate code
    overall_status = results['overall']['status']
    exit_code = 0 if overall_status == 'healthy' else 1 if overall_status == 'warning' else 2
    exit(exit_code)
```

---

*This environment documentation provides comprehensive guidance for setting up, managing, and monitoring environments for the CallRail API Data Extractor across all deployment scenarios.*

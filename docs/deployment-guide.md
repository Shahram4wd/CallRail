# Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the CallRail API Data Extractor in various environments, from development setups to production systems.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Environment](#development-environment)
3. [Production Environment](#production-environment)
4. [Docker Deployment](#docker-deployment)
5. [Automated Deployment](#automated-deployment)
6. [Environment Configuration](#environment-configuration)
7. [Troubleshooting Deployment](#troubleshooting-deployment)

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Operating System** | Windows 10, macOS 10.14, Ubuntu 18.04 | Latest versions |
| **Python** | 3.8+ | 3.11+ |
| **Memory** | 512 MB | 2 GB |
| **Storage** | 1 GB free space | 5 GB |
| **Network** | Internet access to api.callrail.com | Stable broadband |

### Required Software

- **Python**: Download from [python.org](https://python.org)
- **Git**: Download from [git-scm.com](https://git-scm.com)
- **Text Editor**: VS Code, Notepad++, or similar

### CallRail Account Requirements

- Active CallRail account
- API access enabled
- Valid API key with appropriate permissions

## Development Environment

### Quick Setup (5 minutes)

```bash
# 1. Clone repository
git clone <repository-url>
cd CallRail

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env with your API key

# 6. Test installation
python master_downloader.py accounts --limit 1
```

### Detailed Development Setup

#### Step 1: Environment Preparation

**Windows:**
```powershell
# Check Python version
python --version  # Should be 3.8+

# Create project directory
mkdir C:\Projects\CallRail
cd C:\Projects\CallRail

# Clone repository
git clone <repository-url> .
```

**macOS/Linux:**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Create project directory
mkdir ~/Projects/CallRail
cd ~/Projects/CallRail

# Clone repository
git clone <repository-url> .
```

#### Step 2: Virtual Environment Setup

**Why Use Virtual Environment?**
- Isolates dependencies from system Python
- Prevents version conflicts
- Enables clean uninstallation

**Setup Commands:**
```bash
# Create virtual environment
python -m venv venv

# Activate (choose your platform)
# Windows Command Prompt:
venv\Scripts\activate.bat
# Windows PowerShell:
venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

#### Step 3: Dependency Installation

```bash
# Install production dependencies
pip install -r requirements.txt

# Verify installation
pip list

# Check critical packages
python -c "import requests, click, tqdm; print('All packages installed successfully')"
```

#### Step 4: Configuration

**Create Environment File:**
```bash
# Copy template
cp .env.example .env

# Edit with your information
# Windows:
notepad .env
# macOS:
open -e .env
# Linux:
nano .env
```

**Environment File Content:**
```env
# Required Configuration
CALLRAIL_API_KEY=your_api_key_here

# Optional Configuration
LOG_LEVEL=INFO
DATA_DIR=./data
BATCH_SIZE=100
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

#### Step 5: Verification

```bash
# Test API connection
python master_downloader.py accounts --limit 1

# Run comprehensive test
python test_system.py

# Check log output
type logs\callrail_extractor.log  # Windows
cat logs/callrail_extractor.log   # macOS/Linux
```

## Production Environment

### Production Checklist

- [ ] Dedicated server or VM
- [ ] Python 3.8+ installed
- [ ] Secure API key storage
- [ ] Automated backup system
- [ ] Log rotation configured
- [ ] Monitoring setup
- [ ] Error alerting configured

### Server Setup

#### Ubuntu/Debian Server

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git -y

# 3. Create application user
sudo useradd -m -s /bin/bash callrail
sudo su - callrail

# 4. Clone and setup application
git clone <repository-url> callrail-extractor
cd callrail-extractor

# 5. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Configure environment
cp .env.example .env
nano .env  # Add your API key

# 8. Test installation
python master_downloader.py accounts --limit 1
```

#### CentOS/RHEL Server

```bash
# 1. Update system
sudo yum update -y

# 2. Install Python and dependencies
sudo yum install python3 python3-pip git -y

# 3. Create application user
sudo useradd -m callrail
sudo su - callrail

# 4. Follow same steps as Ubuntu from step 4
```

#### Windows Server

```powershell
# 1. Install Python from python.org
# 2. Install Git from git-scm.com

# 3. Create application directory
New-Item -ItemType Directory -Path "C:\Applications\CallRail"
Set-Location "C:\Applications\CallRail"

# 4. Clone repository
git clone <repository-url> .

# 5. Create virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# 6. Install dependencies
pip install -r requirements.txt

# 7. Configure environment
Copy-Item .env.example .env
notepad .env  # Add your API key

# 8. Test installation
python master_downloader.py accounts --limit 1
```

### Production Configuration

#### Secure API Key Storage

**Linux/macOS:**
```bash
# Create secure environment file
sudo mkdir -p /etc/callrail
sudo touch /etc/callrail/config
sudo chmod 600 /etc/callrail/config
sudo chown callrail:callrail /etc/callrail/config

# Add to config file
echo "CALLRAIL_API_KEY=your_api_key_here" | sudo tee /etc/callrail/config

# Source in application
export $(cat /etc/callrail/config | xargs)
```

**Windows:**
```powershell
# Use Windows credential manager or secure registry
# Set environment variable at system level
[Environment]::SetEnvironmentVariable("CALLRAIL_API_KEY", "your_api_key_here", "Machine")
```

#### Log Rotation

**Linux logrotate configuration:**
```bash
# Create logrotate config
sudo tee /etc/logrotate.d/callrail << EOF
/home/callrail/callrail-extractor/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 callrail callrail
}
EOF
```

## Docker Deployment

### Dockerfile

Create `Dockerfile` in the project root:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 callrail && \
    chown -R callrail:callrail /app
USER callrail

# Create necessary directories
RUN mkdir -p data logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "master_downloader.py", "--help"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  callrail-extractor:
    build: .
    container_name: callrail-extractor
    environment:
      - CALLRAIL_API_KEY=${CALLRAIL_API_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
    restart: unless-stopped
    
  # Optional: Add cron service for scheduled runs
  callrail-scheduler:
    build: .
    container_name: callrail-scheduler
    environment:
      - CALLRAIL_API_KEY=${CALLRAIL_API_KEY}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./crontab:/etc/cron.d/callrail-cron:ro
    command: cron -f
    restart: unless-stopped
```

### Docker Deployment Steps

```bash
# 1. Build image
docker build -t callrail-extractor .

# 2. Create environment file
echo "CALLRAIL_API_KEY=your_api_key_here" > .env

# 3. Run with docker-compose
docker-compose up -d

# 4. Test deployment
docker-compose exec callrail-extractor python master_downloader.py accounts --limit 1

# 5. View logs
docker-compose logs -f callrail-extractor
```

## Automated Deployment

### Linux Cron Jobs

```bash
# Edit crontab
crontab -e

# Add scheduled runs
# Daily at 2 AM
0 2 * * * /home/callrail/callrail-extractor/venv/bin/python /home/callrail/callrail-extractor/master_downloader.py --all --limit 1000 >> /home/callrail/callrail-extractor/logs/cron.log 2>&1

# Weekly full export on Sundays at 1 AM
0 1 * * 0 /home/callrail/callrail-extractor/venv/bin/python /home/callrail/callrail-extractor/master_downloader.py --all --limit 10000 >> /home/callrail/callrail-extractor/logs/weekly.log 2>&1
```

### Windows Task Scheduler

```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "C:\Applications\CallRail\venv\Scripts\python.exe" -Argument "C:\Applications\CallRail\master_downloader.py --all --limit 1000" -WorkingDirectory "C:\Applications\CallRail"

$trigger = New-ScheduledTaskTrigger -Daily -At "2:00AM"

$principal = New-ScheduledTaskPrincipal -UserId "NT AUTHORITY\SYSTEM" -LogonType ServiceAccount

Register-ScheduledTask -TaskName "CallRail Data Extract" -Action $action -Trigger $trigger -Principal $principal -Description "Daily CallRail data extraction"
```

### Deployment Scripts

**Linux deployment script** (`deploy.sh`):

```bash
#!/bin/bash
set -e

echo "Starting CallRail API Extractor deployment..."

# Configuration
APP_DIR="/home/callrail/callrail-extractor"
BACKUP_DIR="/home/callrail/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup
echo "Creating backup..."
mkdir -p $BACKUP_DIR
cp -r $APP_DIR $BACKUP_DIR/callrail-extractor_$TIMESTAMP

# Update application
echo "Updating application..."
cd $APP_DIR
git pull origin main

# Update dependencies
echo "Updating dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Run tests
echo "Running tests..."
python test_system.py

# Restart services if using systemd
if systemctl is-active --quiet callrail-extractor; then
    echo "Restarting service..."
    sudo systemctl restart callrail-extractor
fi

echo "Deployment completed successfully!"
```

**Windows deployment script** (`deploy.ps1`):

```powershell
# CallRail API Extractor Deployment Script
Write-Host "Starting CallRail API Extractor deployment..." -ForegroundColor Green

# Configuration
$AppDir = "C:\Applications\CallRail"
$BackupDir = "C:\Backups\CallRail"
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Create backup
Write-Host "Creating backup..." -ForegroundColor Yellow
if (!(Test-Path $BackupDir)) { New-Item -ItemType Directory -Path $BackupDir }
Copy-Item -Path $AppDir -Destination "$BackupDir\callrail-extractor_$Timestamp" -Recurse

# Update application
Write-Host "Updating application..." -ForegroundColor Yellow
Set-Location $AppDir
git pull origin main

# Update dependencies
Write-Host "Updating dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
pip install -r requirements.txt

# Run tests
Write-Host "Running tests..." -ForegroundColor Yellow
python test_system.py

Write-Host "Deployment completed successfully!" -ForegroundColor Green
```

## Environment Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CALLRAIL_API_KEY` | Yes | None | Your CallRail API key |
| `LOG_LEVEL` | No | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `DATA_DIR` | No | ./data | Directory for CSV output files |
| `BATCH_SIZE` | No | 100 | Records per API request |
| `MAX_RETRIES` | No | 3 | Maximum retry attempts |
| `REQUEST_TIMEOUT` | No | 30 | Request timeout in seconds |
| `RATE_LIMIT_DELAY` | No | 1 | Delay between requests in seconds |

### Configuration Files

#### Settings Configuration (`config/settings.py`)

```python
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = Path(os.getenv('DATA_DIR', BASE_DIR / 'data'))
LOG_DIR = BASE_DIR / 'logs'

# API Configuration
API_BASE_URL = 'https://api.callrail.com'
API_VERSION = 'v3'
API_KEY = os.getenv('CALLRAIL_API_KEY')

# Processing Configuration
DEFAULT_BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))
DEFAULT_LIMIT = int(os.getenv('DEFAULT_LIMIT', 100))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

### Multi-Environment Configuration

#### Development Environment (`.env.development`)

```env
CALLRAIL_API_KEY=your_dev_api_key
LOG_LEVEL=DEBUG
BATCH_SIZE=10
DEFAULT_LIMIT=5
REQUEST_TIMEOUT=60
```

#### Production Environment (`.env.production`)

```env
CALLRAIL_API_KEY=your_prod_api_key
LOG_LEVEL=INFO
BATCH_SIZE=100
DEFAULT_LIMIT=1000
REQUEST_TIMEOUT=30
RATE_LIMIT_DELAY=1
```

#### Loading Environment-Specific Config

```bash
# Load development config
export ENV=development
python -c "from dotenv import load_dotenv; load_dotenv('.env.development')"

# Load production config
export ENV=production
python -c "from dotenv import load_dotenv; load_dotenv('.env.production')"
```

## Troubleshooting Deployment

### Common Deployment Issues

#### 1. Python Version Conflicts

**Problem:** Multiple Python versions causing conflicts

**Solution:**
```bash
# Check Python version
python --version
python3 --version

# Use specific Python version
python3.11 -m venv venv
```

#### 2. Permission Issues

**Problem:** Permission denied errors

**Solution:**
```bash
# Fix file permissions
chmod +x master_downloader.py
chown -R callrail:callrail /path/to/app

# Fix directory permissions
chmod 755 data logs
```

#### 3. Network Connectivity

**Problem:** Cannot connect to CallRail API

**Solution:**
```bash
# Test connectivity
curl -I https://api.callrail.com
ping api.callrail.com

# Check firewall rules
sudo ufw status
sudo iptables -L
```

#### 4. Missing Dependencies

**Problem:** ImportError for required packages

**Solution:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check for conflicts
pip check
```

### Health Check Script

Create `health_check.py`:

```python
#!/usr/bin/env python3
"""Health check script for CallRail API Extractor."""

import os
import sys
import requests
from pathlib import Path

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        return False, f"Python {version.major}.{version.minor} (requires 3.8+)"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"

def check_dependencies():
    """Check required dependencies."""
    required = ['requests', 'click', 'tqdm', 'python-dotenv']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        return False, f"Missing packages: {', '.join(missing)}"
    return True, "All dependencies installed"

def check_api_key():
    """Check API key configuration."""
    api_key = os.getenv('CALLRAIL_API_KEY')
    if not api_key:
        return False, "CALLRAIL_API_KEY not set"
    return True, "API key configured"

def check_api_connectivity():
    """Check API connectivity."""
    try:
        response = requests.get('https://api.callrail.com', timeout=10)
        return True, f"API accessible (status: {response.status_code})"
    except requests.RequestException as e:
        return False, f"API connection failed: {e}"

def check_directories():
    """Check required directories."""
    dirs = ['data', 'logs']
    for dir_name in dirs:
        path = Path(dir_name)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                return False, f"Cannot create {dir_name}: {e}"
    return True, "All directories accessible"

def main():
    """Run all health checks."""
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("API Key", check_api_key),
        ("API Connectivity", check_api_connectivity),
        ("Directories", check_directories),
    ]
    
    print("CallRail API Extractor Health Check")
    print("=" * 50)
    
    all_passed = True
    for name, check_func in checks:
        try:
            passed, message = check_func()
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{name:<20} {status:<8} {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"{name:<20} ✗ ERROR   {e}")
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("✓ All checks passed - System ready")
        sys.exit(0)
    else:
        print("✗ Some checks failed - See errors above")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Run the health check:

```bash
python health_check.py
```

### Monitoring Setup

#### Log Monitoring

```bash
# Monitor logs in real-time
tail -f logs/callrail_extractor.log

# Monitor with log rotation
logrotate -f /etc/logrotate.d/callrail
```

#### System Monitoring

```bash
# Create monitoring script
cat > /usr/local/bin/callrail-monitor.sh << 'EOF'
#!/bin/bash
LOG_FILE="/home/callrail/callrail-extractor/logs/callrail_extractor.log"
ERROR_COUNT=$(grep -c "ERROR" "$LOG_FILE" | tail -1)

if [ "$ERROR_COUNT" -gt 10 ]; then
    echo "High error count detected: $ERROR_COUNT errors" | mail -s "CallRail Extractor Alert" admin@company.com
fi
EOF

chmod +x /usr/local/bin/callrail-monitor.sh

# Add to cron
echo "*/15 * * * * /usr/local/bin/callrail-monitor.sh" | crontab -
```

---

*This deployment guide provides comprehensive instructions for setting up the CallRail API Data Extractor in various environments with proper security, monitoring, and automation.*

# Troubleshooting Guide

## Overview

This guide provides solutions to common issues encountered when using the CallRail API Data Extractor. Issues are organized by category with step-by-step solutions and prevention strategies.

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Installation Issues](#installation-issues)
3. [Configuration Problems](#configuration-problems)
4. [API Connection Issues](#api-connection-issues)
5. [Data Processing Errors](#data-processing-errors)
6. [Performance Issues](#performance-issues)
7. [Output Problems](#output-problems)
8. [Environment Issues](#environment-issues)
9. [Advanced Troubleshooting](#advanced-troubleshooting)

## Quick Diagnostics

### Health Check Command

Run this first to identify common issues:

```bash
python -c "
import sys, os, requests
print(f'Python: {sys.version}')
print(f'API Key Set: {bool(os.getenv(\"CALLRAIL_API_KEY\"))}')
try:
    import click, tqdm, dotenv
    print('Dependencies: OK')
except ImportError as e:
    print(f'Dependencies: MISSING - {e}')
try:
    r = requests.get('https://api.callrail.com', timeout=5)
    print(f'API Connectivity: OK ({r.status_code})')
except Exception as e:
    print(f'API Connectivity: FAILED - {e}')
"
```

### Log Analysis

Check the most recent log entries:

```bash
# Windows
type logs\callrail_extractor.log | findstr "ERROR"

# macOS/Linux  
tail -n 50 logs/callrail_extractor.log | grep ERROR
```

### Quick Test

Test with minimal data:

```bash
python master_downloader.py accounts --limit 1
```

## Installation Issues

### Issue: "Python command not found"

**Symptoms:**
```
'python' is not recognized as an internal or external command
python: command not found
```

**Solution:**

**Windows:**
1. Download Python from [python.org](https://python.org)
2. During installation, check "Add Python to PATH"
3. Restart command prompt
4. Test: `python --version`

**macOS:**
```bash
# Install via Homebrew
brew install python

# Or use python3 instead
python3 --version
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Use python3 command
python3 --version
```

### Issue: "No module named 'requests'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'requests'
ImportError: No module named 'click'
```

**Solution:**

1. **Ensure virtual environment is activated:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   pip list | grep requests
   ```

### Issue: "Permission denied" during installation

**Symptoms:**
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solution:**

1. **Use virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```

2. **Or install for user only:**
   ```bash
   pip install --user -r requirements.txt
   ```

### Issue: "SSL Certificate verify failed"

**Symptoms:**
```
SSL: CERTIFICATE_VERIFY_FAILED
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

**Solution:**

1. **Update certificates:**
   ```bash
   # macOS
   /Applications/Python\ 3.x/Install\ Certificates.command
   
   # Windows - update Windows
   # Linux - update ca-certificates
   sudo apt update && sudo apt install ca-certificates
   ```

2. **Temporary bypass (not recommended for production):**
   ```bash
   pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
   ```

## Configuration Problems

### Issue: "CALLRAIL_API_KEY not set"

**Symptoms:**
```
ERROR - Environment variable CALLRAIL_API_KEY is required
KeyError: 'CALLRAIL_API_KEY'
```

**Solution:**

1. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file:**
   ```env
   CALLRAIL_API_KEY=your_actual_api_key_here
   ```

3. **Verify API key format:**
   - Should be a long string of letters and numbers
   - No spaces or special characters
   - Obtained from CallRail Settings → API

### Issue: "Invalid API key"

**Symptoms:**
```
ERROR - API request failed: 401 Client Error: Unauthorized
Authentication failed: Invalid API key provided
```

**Solution:**

1. **Verify API key in CallRail:**
   - Log into CallRail account
   - Go to Settings → API
   - Check if key is active and not expired

2. **Check .env file:**
   ```bash
   # Show API key (be careful - don't share output)
   cat .env | grep CALLRAIL_API_KEY
   ```

3. **Test API key manually:**
   ```bash
   curl -H "Authorization: Token token=YOUR_API_KEY" https://api.callrail.com/v3/a.json
   ```

### Issue: "Configuration file not found"

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: '.env'
```

**Solution:**

1. **Create from template:**
   ```bash
   cp .env.example .env
   ```

2. **Or create manually:**
   ```bash
   echo "CALLRAIL_API_KEY=your_key_here" > .env
   ```

## API Connection Issues

### Issue: "Connection timeout"

**Symptoms:**
```
requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='api.callrail.com', port=443)
requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='api.callrail.com', port=443)
```

**Solution:**

1. **Check internet connection:**
   ```bash
   ping api.callrail.com
   ```

2. **Test with longer timeout:**
   ```bash
   REQUEST_TIMEOUT=60 python master_downloader.py accounts --limit 1
   ```

3. **Check firewall/proxy settings:**
   - Ensure HTTPS (port 443) is allowed
   - Configure proxy if needed:
     ```bash
     export https_proxy=http://proxy.company.com:8080
     ```

### Issue: "Rate limit exceeded"

**Symptoms:**
```
WARNING - Rate limited. Waiting 60 seconds...
ERROR - API request failed: 429 Client Error: Too Many Requests
```

**Solution:**

1. **Wait for automatic retry:**
   - System handles rate limits automatically
   - Uses exponential backoff

2. **Reduce batch size:**
   ```bash
   python master_downloader.py --all --batch-size 25 --limit 100
   ```

3. **Increase delay between requests:**
   ```bash
   RATE_LIMIT_DELAY=2 python master_downloader.py --all --limit 100
   ```

### Issue: "DNS resolution failed"

**Symptoms:**
```
requests.exceptions.ConnectionError: [Errno -2] Name or service not known
gaierror: [Errno -2] Name or service not known
```

**Solution:**

1. **Check DNS settings:**
   ```bash
   nslookup api.callrail.com
   ```

2. **Try different DNS servers:**
   ```bash
   # Temporarily use Google DNS
   echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
   ```

3. **Check system time:**
   ```bash
   date
   # Ensure system time is correct for SSL certificates
   ```

## Data Processing Errors

### Issue: "No records found" for endpoints

**Symptoms:**
```
INFO - Completed text_messages: 0 records in 0.94s with 0 errors
INFO - Completed form_submissions: 0 records in 0.28s with 0 errors
```

**This is often normal:**
- `text_messages`: Only if SMS is enabled
- `form_submissions`: Only if web forms are used  
- `notifications`: Only if webhooks are configured
- `outbound_caller_ids`: Only if outbound calling is set up

**Verify with CallRail dashboard** to confirm if data should exist.

### Issue: "Field validation errors"

**Symptoms:**
```
ERROR - API request failed: 400 Client Error: Bad Request
field values not allowed: invalid_field_name
```

**Solution:**

1. **System automatically handles this** by updating field definitions
2. **Check logs for field updates:**
   ```bash
   grep "field values not allowed" logs/callrail_extractor.log
   ```

3. **Manual fix if needed:**
   Edit `config/endpoints.py` to remove problematic fields

### Issue: "Company ID required"

**Symptoms:**
```
ERROR - API request failed: 400 Client Error: Bad Request
company_id parameter is required
```

**Solution:**

System automatically handles this, but if manual fix needed:

```python
# In processors/base_processor.py
def get_company_id(self) -> Optional[str]:
    """Get company ID for endpoints that require it."""
    try:
        companies_processor = CompaniesProcessor(self.client)
        companies = companies_processor.get_companies()
        if companies:
            return companies[0]['id']
    except Exception as e:
        logger.warning(f"Could not get company ID: {e}")
    return None
```

### Issue: "JSON decode error"

**Symptoms:**
```
ValueError: Expecting value: line 1 column 1 (char 0)
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

**Solution:**

1. **Check API response:**
   ```python
   # Enable debug logging
   LOG_LEVEL=DEBUG python master_downloader.py accounts --limit 1
   ```

2. **API might be returning HTML error page:**
   - Check for maintenance notices
   - Verify API endpoint URLs

3. **Check rate limiting:**
   - May be receiving HTML rate limit page instead of JSON

## Performance Issues

### Issue: "System running slowly"

**Symptoms:**
- Very slow progress bars
- Long processing times
- High memory usage

**Solution:**

1. **Reduce batch size:**
   ```bash
   python master_downloader.py --all --batch-size 25 --limit 100
   ```

2. **Check system resources:**
   ```bash
   # Windows
   taskmgr
   
   # macOS/Linux
   top
   htop
   ```

3. **Process endpoints individually:**
   ```bash
   python master_downloader.py calls --limit 100
   python master_downloader.py trackers --limit 100
   ```

### Issue: "Memory usage too high"

**Symptoms:**
```
MemoryError: Unable to allocate array
System running out of memory
```

**Solution:**

1. **Use smaller batch sizes:**
   ```bash
   python master_downloader.py --all --batch-size 10 --limit 100
   ```

2. **Process endpoints separately:**
   ```bash
   for endpoint in accounts calls companies; do
     python master_downloader.py $endpoint --limit 1000
   done
   ```

3. **Monitor memory usage:**
   ```python
   import psutil
   print(f"Memory usage: {psutil.virtual_memory().percent}%")
   ```

## Output Problems

### Issue: "Permission denied writing CSV files"

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'data/calls.csv'
IOError: [Errno 13] Permission denied: 'data/calls.csv'
```

**Solution:**

1. **Check directory permissions:**
   ```bash
   # Windows
   icacls data
   
   # macOS/Linux
   ls -la data/
   chmod 755 data/
   ```

2. **Check if files are open elsewhere:**
   - Close Excel or other programs using CSV files
   - Check for file locks

3. **Use different output directory:**
   ```bash
   DATA_DIR=./output python master_downloader.py --all --limit 100
   ```

### Issue: "CSV files are empty or corrupted"

**Symptoms:**
- CSV files exist but have no data
- Files contain partial data
- Excel can't open files

**Solution:**

1. **Check processing logs:**
   ```bash
   grep "Successfully wrote" logs/callrail_extractor.log
   ```

2. **Verify file encoding:**
   ```bash
   file data/calls.csv
   head -n 5 data/calls.csv
   ```

3. **Re-run with debug logging:**
   ```bash
   LOG_LEVEL=DEBUG python master_downloader.py calls --limit 10
   ```

### Issue: "Missing expected fields in CSV"

**Symptoms:**
- CSV has fewer columns than expected
- Important fields are missing

**Solution:**

1. **Check field filtering:**
   - System automatically filters fields based on API responses
   - Some fields may not be available for your account

2. **Disable field filtering for testing:**
   ```python
   # In processors/base_processor.py
   FIELD_FILTER_SKIP_LIST = ['all_endpoints']  # Skip filtering for all
   ```

3. **Check API response manually:**
   ```bash
   curl -H "Authorization: Token token=YOUR_API_KEY" \
        "https://api.callrail.com/v3/a/YOUR_ACCOUNT_ID/calls.json?per_page=1"
   ```

## Environment Issues

### Issue: "Virtual environment not working"

**Symptoms:**
```
ModuleNotFoundError even after pip install
Wrong Python version being used
```

**Solution:**

1. **Check if environment is activated:**
   ```bash
   # Should show (venv) in prompt
   which python  # Should point to venv/bin/python
   ```

2. **Recreate virtual environment:**
   ```bash
   rm -rf venv
   python -m venv venv
   
   # Activate
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   
   # Reinstall
   pip install -r requirements.txt
   ```

3. **Use absolute path:**
   ```bash
   # Windows
   C:\path\to\project\venv\Scripts\python.exe master_downloader.py --help
   
   # macOS/Linux
   /path/to/project/venv/bin/python master_downloader.py --help
   ```

### Issue: "Wrong Python version"

**Symptoms:**
```
Python 2.7 being used instead of Python 3
SyntaxError: invalid syntax (f-strings)
```

**Solution:**

1. **Use python3 explicitly:**
   ```bash
   python3 -m venv venv
   python3 master_downloader.py --help
   ```

2. **Check Python version:**
   ```bash
   python --version
   python3 --version
   which python
   ```

3. **Update PATH or use pyenv:**
   ```bash
   # Install pyenv and set Python version
   pyenv install 3.11.7
   pyenv local 3.11.7
   ```

## Advanced Troubleshooting

### Enable Debug Logging

```bash
LOG_LEVEL=DEBUG python master_downloader.py accounts --limit 1
```

This shows:
- Detailed API requests and responses
- Processing steps
- Error details
- Timing information

### Network Debugging

1. **Test API connectivity:**
   ```bash
   curl -v -H "Authorization: Token token=YOUR_API_KEY" \
        https://api.callrail.com/v3/a.json
   ```

2. **Check network path:**
   ```bash
   traceroute api.callrail.com
   ```

3. **Monitor network traffic:**
   ```bash
   # macOS/Linux
   sudo netstat -i
   
   # Windows
   netstat -e
   ```

### System Resource Monitoring

```python
# Create monitoring script: monitor.py
import psutil
import time

def monitor_resources():
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        print(f"CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%")
        time.sleep(5)

if __name__ == "__main__":
    monitor_resources()
```

### Database of Common Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "SSL: CERTIFICATE_VERIFY_FAILED" | SSL certificate issues | Update certificates, check system time |
| "Connection timeout" | Network/firewall issues | Check connectivity, increase timeout |
| "Rate limit exceeded" | Too many API requests | Wait, reduce batch size |
| "Invalid API key" | Wrong/expired API key | Verify key in CallRail account |
| "Permission denied" | File/directory permissions | Check permissions, close files |
| "ModuleNotFoundError" | Missing dependencies | Activate venv, install requirements |
| "JSON decode error" | Invalid API response | Check API status, enable debug logging |
| "Memory error" | Insufficient RAM | Reduce batch size, process separately |

### Creating Support Logs

When requesting support, include:

1. **System information:**
   ```bash
   python --version
   pip list
   uname -a  # Linux/macOS
   ver       # Windows
   ```

2. **Error logs:**
   ```bash
   tail -n 100 logs/callrail_extractor.log
   ```

3. **Configuration (sanitized):**
   ```bash
   cat .env | sed 's/CALLRAIL_API_KEY=.*/CALLRAIL_API_KEY=[REDACTED]/'
   ```

4. **Test results:**
   ```bash
   LOG_LEVEL=DEBUG python master_downloader.py accounts --limit 1 > debug.log 2>&1
   ```

### Recovery Procedures

#### Complete Reset

```bash
# 1. Backup existing data
cp -r data data_backup_$(date +%Y%m%d)

# 2. Clean environment
rm -rf venv
rm -rf __pycache__
rm -rf logs/*.log

# 3. Fresh setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 4. Test basic functionality
python master_downloader.py accounts --limit 1
```

#### Partial Recovery

```bash
# 1. Clear problematic data
rm -rf data/*.csv

# 2. Reset logs
> logs/callrail_extractor.log

# 3. Test specific endpoint
python master_downloader.py accounts --limit 1

# 4. Gradually add endpoints
python master_downloader.py accounts calls --limit 10
```

### Performance Optimization

1. **Optimal batch sizes by endpoint:**
   - `calls`: 50-100 records
   - `trackers`: 100-250 records  
   - `tags`: 100-250 records
   - `users`: 50-100 records

2. **Memory optimization:**
   ```bash
   BATCH_SIZE=25 python master_downloader.py --all --limit 1000
   ```

3. **Network optimization:**
   ```bash
   REQUEST_TIMEOUT=45 RATE_LIMIT_DELAY=0.5 python master_downloader.py --all
   ```

---

*This troubleshooting guide covers the most common issues encountered with the CallRail API Data Extractor. For issues not covered here, check the system logs and consider creating a support request with relevant log information.*

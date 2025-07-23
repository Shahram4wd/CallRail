# User Manual

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Basic Usage](#basic-usage)
5. [Advanced Usage](#advanced-usage)
6. [Understanding Output](#understanding-output)
7. [Troubleshooting](#troubleshooting)
8. [Examples](#examples)

## Getting Started

The CallRail API Data Extractor is a command-line tool that downloads data from your CallRail account and saves it to CSV files. This tool supports all CallRail API endpoints and provides real-time progress tracking.

### What You'll Need

- A CallRail account with API access
- Your CallRail API key
- Python 3.8 or higher installed on your system
- Basic familiarity with command-line interfaces

### What the Tool Does

- **Extracts data** from all 11 CallRail API endpoints
- **Saves data** to CSV files in the `data/` folder
- **Shows progress** with real-time progress bars
- **Handles errors** automatically with retry logic
- **Provides summaries** of all operations

## Installation

### Step 1: Download the System

```bash
# Clone the repository
git clone <repository-url>
cd CallRail
```

### Step 2: Set Up Python Environment

**Windows:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python master_downloader.py --help
```

You should see the help menu with available commands.

## Configuration

### Step 1: Get Your API Key

1. Log into your CallRail account
2. Go to **Settings** → **API**
3. Create a new API key or copy your existing key
4. Keep this key secure - you'll need it for configuration

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit the `.env` file with your information:

```env
# Required: Your CallRail API key
CALLRAIL_API_KEY=your_api_key_here

# Optional: Customize these settings
LOG_LEVEL=INFO
DATA_DIR=./data
BATCH_SIZE=100
MAX_RETRIES=3
```

### Step 3: Test Configuration

```bash
python master_downloader.py accounts --limit 1
```

If configured correctly, this will download your account information.

## Basic Usage

### Command Structure

```bash
python master_downloader.py [ENDPOINT] [OPTIONS]
```

### Download All Data

To download data from all endpoints (recommended for first-time users):

```bash
python master_downloader.py --all --limit 100
```

This command:
- Downloads from all 11 endpoints
- Limits each endpoint to 100 records
- Shows progress bars for each operation
- Creates CSV files in the `data/` folder

### Download Specific Endpoints

To download from specific endpoints:

```bash
# Download calls only
python master_downloader.py calls --limit 50

# Download calls and companies
python master_downloader.py calls companies --limit 50
```

### Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--limit` | Maximum records per endpoint | `--limit 100` |
| `--batch-size` | Records per API request | `--batch-size 50` |
| `--all` | Download from all endpoints | `--all` |
| `--help` | Show help information | `--help` |

## Advanced Usage

### Large Data Extractions

For large datasets, use smaller batch sizes to manage memory:

```bash
python master_downloader.py --all --limit 1000 --batch-size 50
```

### Specific Use Cases

**Daily Call Reports:**
```bash
python master_downloader.py calls --limit 500
```

**User Management:**
```bash
python master_downloader.py users companies --limit 100
```

**Complete Data Export:**
```bash
python master_downloader.py --all --limit 10000
```

### Environment Variables Override

You can override settings with environment variables:

```bash
# Use different API key for this run
CALLRAIL_API_KEY=different_key python master_downloader.py accounts

# Change log level
LOG_LEVEL=DEBUG python master_downloader.py calls --limit 10
```

## Understanding Output

### Progress Display

While running, you'll see two progress bars:

```
Downloading 11 endpoints:  45%|███████████████████▌       | 5/11 [00:06<00:05,  1.04it/s]
Processing calls (batch 1/2): 100%|███████████████| 100/100 records [00:04<00:00, 20.13records/s]
```

- **Top bar**: Overall progress across all endpoints
- **Bottom bar**: Current endpoint processing progress

### CSV Output Files

The tool creates CSV files in the `data/` folder:

```
data/
├── accounts.csv          # Account information
├── calls.csv            # Call records
├── companies.csv        # Company data
├── form_submissions.csv # Web form submissions
├── integrations.csv     # Third-party integrations
├── tags.csv            # Call and form tags
├── trackers.csv        # Phone number trackers
├── users.csv           # Account users
├── text_messages.csv   # SMS messages (if available)
├── notifications.csv   # Webhooks (if available)
└── outbound_caller_ids.csv # Caller IDs (if available)
```

### Summary Report

At the end of each run, you'll see a summary:

```
============================================================
DOWNLOAD SUMMARY
============================================================
Total time: 10.17 seconds
Total endpoints: 11
Successful endpoints: 11
Failed endpoints: 0
Total records downloaded: 288
Total errors: 0

SUCCESS accounts: 1 records (0.40s)
  -> data\accounts.csv
SUCCESS calls: 100 records (4.97s)
  -> data\calls.csv
...
```

### Log Files

Detailed logs are saved to `logs/callrail_extractor.log`:

```
2025-07-23 10:05:13,047 - callrail_extractor - INFO - Initialized MasterDownloader
2025-07-23 10:05:13,048 - callrail_extractor - INFO - Fetching account information...
2025-07-23 10:05:13,493 - callrail_extractor - INFO - Using account ID: ACC2e66c0fd...
```

## Troubleshooting

### Common Issues

#### "Invalid API key" Error

```
ERROR - Authentication failed: Invalid API key
```

**Solution:**
1. Check your API key in the `.env` file
2. Ensure there are no extra spaces or characters
3. Verify the key is active in your CallRail account

#### "No records found" for Some Endpoints

```
INFO - Completed text_messages: 0 records in 0.94s with 0 errors
```

**This is normal** - some endpoints may have no data:
- `text_messages`: Only if SMS is enabled
- `form_submissions`: Only if web forms are used
- `notifications`: Only if webhooks are configured

#### Rate Limiting

```
WARNING - Rate limited. Waiting 60 seconds...
```

**The system handles this automatically** by waiting and retrying. No action needed.

#### Network Timeouts

```
ERROR - Request timeout after 30 seconds
```

**Solutions:**
1. Check your internet connection
2. Try again - the system has built-in retry logic
3. Use smaller batch sizes: `--batch-size 25`

### Getting Help

1. **Check the log file**: `logs/callrail_extractor.log`
2. **Run with debug logging**: `LOG_LEVEL=DEBUG python master_downloader.py ...`
3. **Try a simple test**: `python master_downloader.py accounts --limit 1`
4. **Check your API key**: Log into CallRail and verify it's active

## Examples

### Example 1: First-Time Setup

```bash
# 1. Set up environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Configure API key
echo "CALLRAIL_API_KEY=your_key_here" > .env

# 3. Test connection
python master_downloader.py accounts --limit 1

# 4. Download sample data
python master_downloader.py --all --limit 10
```

### Example 2: Daily Call Report

```bash
# Download recent calls for daily reporting
python master_downloader.py calls --limit 200
```

The `calls.csv` file will contain:
- Call duration, direction, phone numbers
- Customer information and location
- Recording links and call outcomes
- Timestamps and tracking information

### Example 3: User Management Export

```bash
# Export users and company structure
python master_downloader.py users companies --limit 100
```

This creates:
- `users.csv`: All account users with roles and permissions
- `companies.csv`: Company structure and settings

### Example 4: Complete Data Export

```bash
# Full export for data migration or backup
python master_downloader.py --all --limit 5000 --batch-size 50
```

This downloads all available data from your CallRail account.

### Example 5: Marketing Campaign Analysis

```bash
# Download campaign-related data
python master_downloader.py calls trackers tags --limit 1000
```

This provides:
- `calls.csv`: Call details and outcomes
- `trackers.csv`: Phone number tracking configuration
- `tags.csv`: Call categorization and tagging

## Best Practices

### 1. Start Small

For first-time use, start with small limits:

```bash
python master_downloader.py --all --limit 10
```

### 2. Regular Backups

Set up regular data exports:

```bash
# Weekly backup script
python master_downloader.py --all --limit 1000
```

### 3. Monitor Logs

Check `logs/callrail_extractor.log` for any issues or warnings.

### 4. API Rate Limits

The system respects CallRail's rate limits automatically, but for large exports:
- Use smaller batch sizes (`--batch-size 25`)
- Allow extra time for completion
- Run during off-peak hours

### 5. Data Validation

After export, verify your CSV files:
- Check record counts match expectations
- Verify critical fields are populated
- Compare with CallRail dashboard counts

## Command Reference

### Main Commands

```bash
# Download all endpoints
python master_downloader.py --all [OPTIONS]

# Download specific endpoints
python master_downloader.py ENDPOINT1 ENDPOINT2 [OPTIONS]

# Show help
python master_downloader.py --help
```

### Available Endpoints

- `accounts` - Account information
- `calls` - Call records
- `companies` - Company data
- `form_submissions` - Web form submissions
- `integrations` - Third-party integrations
- `tags` - Call and form tags
- `trackers` - Phone number trackers
- `users` - Account users
- `text_messages` - SMS messages
- `notifications` - Webhook notifications
- `outbound_caller_ids` - Outbound caller IDs

### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--limit` | `-l` | Maximum records per endpoint | 100 |
| `--batch-size` | `-b` | Records per API request | 100 |
| `--all` | `-a` | Process all endpoints | False |
| `--help` | `-h` | Show help message | - |

---

*This user manual provides comprehensive guidance for using the CallRail API Data Extractor effectively and safely.*

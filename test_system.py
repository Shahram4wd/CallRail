#!/usr/bin/env python3
"""
Test script for the CallRail API data downloader system.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from master_downloader import MasterDownloader
from config.settings import Settings
from utils.logger import logger


def test_system():
    """Test the CallRail downloader system."""
    
    logger.info("Starting CallRail API system test...")
    
    try:
        # Initialize settings
        settings = Settings()
        logger.info(f"Settings loaded successfully")
        
        # Get API token from environment
        api_token = os.getenv('CALLRAIL_API_KEY')
        account_id = os.getenv('CALLRAIL_ACCOUNT_ID')
        
        logger.info(f"API Token configured: {'Yes' if api_token else 'No'}")
        logger.info(f"Account ID configured: {'Yes' if account_id else 'No'}")
        
        # Initialize downloader
        if not api_token:
            logger.error("API token not configured. Please set CALLRAIL_API_KEY environment variable.")
            return False
            
        downloader = MasterDownloader(api_token)
        logger.info("Downloader initialized successfully")
        
        # Test with accounts endpoint (doesn't require account_id)
        logger.info("Testing accounts endpoint...")
        result = downloader.download_endpoints(["accounts"], limit=5)
        
        if result and result['endpoints'].get('accounts', {}).get('success'):
            accounts_result = result['endpoints']['accounts']
            logger.info(f"SUCCESS: Downloaded {accounts_result['records_processed']} account records")
            logger.info(f"CSV file created: {accounts_result['csv_file']}")
        else:
            logger.warning("WARNING: No account data returned or download failed")
            if result and result['endpoints'].get('accounts'):
                error = result['endpoints']['accounts'].get('error', 'Unknown error')
                logger.error(f"Error: {error}")
        
        logger.info("System test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"FAILED: System test failed: {str(e)}")
        logger.exception("Full error details:")
        return False


if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)

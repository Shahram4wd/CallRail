"""
Master downloader for CallRail API data extraction.
"""
import os
import sys
import time
import click
from typing import List, Dict, Any, Optional
from callrail_api.client import CallRailClient
from config.endpoints import endpoint_registry
from config.settings import settings
from utils.logger import logger
from utils.progress_tracker import progress_tracker
from processors.accounts_processor import AccountsProcessor
from processors.calls_processor import CallsProcessor
from processors.generic_processor import (
    CompaniesProcessor, FormSubmissionsProcessor, IntegrationsProcessor,
    TagsProcessor, TrackersProcessor, UsersProcessor, TextMessagesProcessor,
    NotificationsProcessor, OutboundCallerIdsProcessor
)


class MasterDownloader:
    """Master controller for CallRail data extraction."""
    
    def __init__(self, api_key: str):
        self.client = CallRailClient(api_key)
        self.account_id = None
        self.results = {}
        
        # Processor mapping
        self.processor_classes = {
            'accounts': AccountsProcessor,
            'calls': CallsProcessor,
            'companies': CompaniesProcessor,
            'form_submissions': FormSubmissionsProcessor,
            'integrations': IntegrationsProcessor,
            'tags': TagsProcessor,
            'trackers': TrackersProcessor,
            'users': UsersProcessor,
            'text_messages': TextMessagesProcessor,
            'notifications': NotificationsProcessor,
            'outbound_caller_ids': OutboundCallerIdsProcessor
        }
        
        logger.info("Initialized MasterDownloader")
    
    def get_account_id(self) -> str:
        """Get the account ID for API calls."""
        if self.account_id:
            return self.account_id
        
        try:
            logger.info("Fetching account information...")
            accounts_processor = AccountsProcessor(self.client)
            self.account_id = accounts_processor.get_account_id()
            
            if not self.account_id:
                raise ValueError("No account ID found")
            
            logger.info(f"Using account ID: {self.account_id}")
            return self.account_id
            
        except Exception as e:
            logger.error(f"Error getting account ID: {str(e)}")
            raise
    
    def download_all_endpoints(self, limit: Optional[int] = None, 
                             batch_size: Optional[int] = None) -> Dict[str, Any]:
        """Download data from all available endpoints."""
        endpoints = endpoint_registry.get_endpoint_names()
        return self.download_endpoints(endpoints, limit, batch_size)
    
    def download_endpoints(self, endpoint_names: List[str], 
                          limit: Optional[int] = None,
                          batch_size: Optional[int] = None) -> Dict[str, Any]:
        """Download data from specified endpoints."""
        start_time = time.time()
        
        # Validate endpoints
        available_endpoints = endpoint_registry.get_endpoint_names()
        invalid_endpoints = [ep for ep in endpoint_names if ep not in available_endpoints]
        if invalid_endpoints:
            raise ValueError(f"Invalid endpoints: {invalid_endpoints}. "
                           f"Available: {available_endpoints}")
        
        # Get account ID
        account_id = self.get_account_id()
        
        # Initialize progress tracking
        progress_tracker.create_main_progress(
            len(endpoint_names), 
            f"Downloading {len(endpoint_names)} endpoints"
        )
        
        logger.info(f"Starting download for {len(endpoint_names)} endpoints: {endpoint_names}")
        
        results = {
            'start_time': start_time,
            'endpoints': {},
            'summary': {
                'total_endpoints': len(endpoint_names),
                'successful_endpoints': 0,
                'failed_endpoints': 0,
                'total_records': 0,
                'total_errors': 0
            }
        }
        
        # Process each endpoint
        for endpoint_name in endpoint_names:
            try:
                logger.info(f"Processing endpoint: {endpoint_name}")
                
                # Create processor
                processor = self.create_processor(endpoint_name, account_id)
                
                # Process endpoint
                endpoint_result = processor.process_endpoint(limit, batch_size)
                
                # Store results
                results['endpoints'][endpoint_name] = endpoint_result
                
                # Update summary
                if endpoint_result['success']:
                    results['summary']['successful_endpoints'] += 1
                else:
                    results['summary']['failed_endpoints'] += 1
                
                results['summary']['total_records'] += endpoint_result['records_processed']
                results['summary']['total_errors'] += endpoint_result['errors']
                
                # Update main progress
                progress_tracker.update_main_progress()
                
                logger.info(f"Completed {endpoint_name}: "
                           f"{endpoint_result['records_processed']} records, "
                           f"{endpoint_result['errors']} errors")
                
            except Exception as e:
                logger.error(f"Error processing endpoint {endpoint_name}: {str(e)}")
                
                results['endpoints'][endpoint_name] = {
                    'endpoint': endpoint_name,
                    'records_processed': 0,
                    'errors': 1,
                    'total_time': 0,
                    'csv_file': "",
                    'success': False,
                    'error': str(e)
                }
                
                results['summary']['failed_endpoints'] += 1
                results['summary']['total_errors'] += 1
                
                # Update main progress
                progress_tracker.update_main_progress()
        
        # Finalize results
        results['end_time'] = time.time()
        results['total_time'] = results['end_time'] - results['start_time']
        
        # Close progress bars
        progress_tracker.finish_all()
        
        # Log summary
        self.log_summary(results)
        
        return results
    
    def create_processor(self, endpoint_name: str, account_id: str):
        """Create a processor for the specified endpoint."""
        processor_class = self.processor_classes.get(endpoint_name)
        
        if not processor_class:
            raise ValueError(f"No processor available for endpoint: {endpoint_name}")
        
        # Special handling for accounts processor (doesn't need account_id)
        if endpoint_name == 'accounts':
            return processor_class(self.client)
        else:
            return processor_class(self.client, account_id)
    
    def log_summary(self, results: Dict[str, Any]):
        """Log a summary of the download results."""
        summary = results['summary']
        
        logger.info("=" * 60)
        logger.info("DOWNLOAD SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total time: {results['total_time']:.2f} seconds")
        logger.info(f"Total endpoints: {summary['total_endpoints']}")
        logger.info(f"Successful endpoints: {summary['successful_endpoints']}")
        logger.info(f"Failed endpoints: {summary['failed_endpoints']}")
        logger.info(f"Total records downloaded: {summary['total_records']}")
        logger.info(f"Total errors: {summary['total_errors']}")
        logger.info("")
        
        # Log individual endpoint results
        for endpoint_name, result in results['endpoints'].items():
            status = "SUCCESS" if result['success'] else "FAILED"
            logger.info(f"{status} {endpoint_name}: {result['records_processed']} records "
                       f"({result['total_time']:.2f}s)")
            if result['csv_file']:
                logger.info(f"  -> {result['csv_file']}")
        
        logger.info("=" * 60)
    
    def get_available_endpoints(self) -> List[str]:
        """Get list of available endpoints."""
        return endpoint_registry.get_endpoint_names()
    
    def get_endpoint_info(self, endpoint_name: str) -> Dict[str, Any]:
        """Get information about a specific endpoint."""
        endpoint_config = endpoint_registry.get_endpoint(endpoint_name)
        if not endpoint_config:
            return {}
        
        return {
            'name': endpoint_name,
            'path': endpoint_config.path,
            'requires_account_id': endpoint_config.requires_account_id,
            'pagination_type': endpoint_config.pagination_type,
            'max_per_page': endpoint_config.max_per_page,
            'total_fields': len(endpoint_registry.get_all_fields(endpoint_name)),
            'fields': endpoint_registry.get_all_fields(endpoint_name)
        }


@click.command()
@click.option('--api-key', envvar='CALLRAIL_API_KEY', required=True,
              help='CallRail API key (can be set via CALLRAIL_API_KEY env var)')
@click.option('--endpoints', '-e', help='Comma-separated list of endpoints to download')
@click.option('--all', 'download_all', is_flag=True, 
              help='Download all available endpoints')
@click.option('--limit', '-l', type=int, default=100,
              help='Maximum number of records per endpoint (default: 100)')
@click.option('--batch-size', '-b', type=int, 
              help='Batch size for processing (default: from config)')
@click.option('--list-endpoints', is_flag=True,
              help='List all available endpoints and exit')
@click.option('--endpoint-info', help='Show information about a specific endpoint')
def main(api_key: str, endpoints: str, download_all: bool, limit: int, 
         batch_size: int, list_endpoints: bool, endpoint_info: str):
    """
    CallRail API Data Extractor
    
    Download data from CallRail API endpoints and save to CSV files.
    
    Examples:
        # Download all endpoints
        python master_downloader.py --all
        
        # Download specific endpoints
        python master_downloader.py --endpoints calls,companies,users
        
        # Download with custom limits
        python master_downloader.py --endpoints calls --limit 500 --batch-size 50
        
        # List available endpoints
        python master_downloader.py --list-endpoints
    """
    try:
        downloader = MasterDownloader(api_key)
        
        if list_endpoints:
            available_endpoints = downloader.get_available_endpoints()
            click.echo("Available endpoints:")
            for endpoint in available_endpoints:
                click.echo(f"  - {endpoint}")
            return
        
        if endpoint_info:
            info = downloader.get_endpoint_info(endpoint_info)
            if info:
                click.echo(f"Endpoint: {info['name']}")
                click.echo(f"Path: {info['path']}")
                click.echo(f"Requires Account ID: {info['requires_account_id']}")
                click.echo(f"Pagination Type: {info['pagination_type']}")
                click.echo(f"Max Per Page: {info['max_per_page']}")
                click.echo(f"Total Fields: {info['total_fields']}")
                click.echo("Fields:")
                for field in info['fields']:
                    click.echo(f"  - {field}")
            else:
                click.echo(f"Endpoint '{endpoint_info}' not found")
            return
        
        if download_all:
            results = downloader.download_all_endpoints(limit, batch_size)
        elif endpoints:
            endpoint_list = [ep.strip() for ep in endpoints.split(',')]
            results = downloader.download_endpoints(endpoint_list, limit, batch_size)
        else:
            click.echo("Please specify --all or --endpoints. Use --help for more information.")
            return
        
        # Exit with appropriate code
        if results['summary']['failed_endpoints'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

"""
Configuration settings for CallRail data extractor.
"""
import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class RetryConfig:
    """Configuration for retry mechanism."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True


@dataclass
class BatchConfig:
    """Configuration for batch processing."""
    default_batch_size: int = 100
    max_batch_size: int = 1000
    min_batch_size: int = 10


@dataclass
class LoggingConfig:
    """Configuration for logging."""
    log_file: str = "logs/callrail_extractor.log"
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    overwrite_on_run: bool = True


@dataclass
class APIConfig:
    """Configuration for API settings."""
    base_url: str = "https://api.callrail.com/v3"
    rate_limit_per_hour: int = 1000
    rate_limit_per_day: int = 10000
    timeout: int = 30
    max_records_per_endpoint: int = 100


@dataclass
class OutputConfig:
    """Configuration for output settings."""
    data_directory: str = "data"
    csv_encoding: str = "utf-8"
    csv_delimiter: str = ","
    include_headers: bool = True


class Settings:
    """Main settings class."""
    
    def __init__(self):
        self.retry = RetryConfig()
        self.batch = BatchConfig()
        self.logging = LoggingConfig()
        self.api = APIConfig()
        self.output = OutputConfig()
        
        # Load environment variables
        self._load_from_env()
    
    def _load_from_env(self):
        """Load settings from environment variables."""
        # API settings
        if os.getenv("CALLRAIL_API_TIMEOUT"):
            self.api.timeout = int(os.getenv("CALLRAIL_API_TIMEOUT"))
        
        if os.getenv("CALLRAIL_MAX_RECORDS"):
            self.api.max_records_per_endpoint = int(os.getenv("CALLRAIL_MAX_RECORDS"))
        
        # Batch settings
        if os.getenv("CALLRAIL_BATCH_SIZE"):
            self.batch.default_batch_size = int(os.getenv("CALLRAIL_BATCH_SIZE"))
        
        # Retry settings
        if os.getenv("CALLRAIL_MAX_RETRIES"):
            self.retry.max_attempts = int(os.getenv("CALLRAIL_MAX_RETRIES"))
        
        # Logging settings
        if os.getenv("CALLRAIL_LOG_LEVEL"):
            self.logging.log_level = os.getenv("CALLRAIL_LOG_LEVEL")
        
        # Output settings
        if os.getenv("CALLRAIL_DATA_DIR"):
            self.output.data_directory = os.getenv("CALLRAIL_DATA_DIR")


# Global settings instance
settings = Settings()

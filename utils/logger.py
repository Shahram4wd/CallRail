"""
Logging utilities for CallRail data extractor.
"""
import logging
import os
from typing import Optional
from config.settings import settings


class CallRailLogger:
    """Custom logger for CallRail data extractor."""
    
    def __init__(self, name: str = "callrail_extractor"):
        self.name = name
        self.logger = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Set up the logger with file and console handlers."""
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(getattr(logging, settings.logging.log_level.upper()))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(settings.logging.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler
        file_mode = 'w' if settings.logging.overwrite_on_run else 'a'
        file_handler = logging.FileHandler(settings.logging.log_file, mode=file_mode)
        file_handler.setLevel(getattr(logging, settings.logging.log_level.upper()))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(settings.logging.log_format)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback."""
        self.logger.exception(message, **kwargs)


# Global logger instance
logger = CallRailLogger()

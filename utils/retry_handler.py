"""
Retry mechanism utilities for CallRail data extractor.
"""
import time
import random
import logging
from typing import Callable, Any, Optional, Type, Union
from functools import wraps
from tenacity import (
    retry, stop_after_attempt, wait_exponential, 
    retry_if_exception_type, before_sleep_log
)
import requests
from callrail_api.exceptions import (
    CallRailAPIException, RateLimitError, ServerError, 
    AuthenticationError, NotFoundError
)
from config.settings import settings
from utils.logger import logger


class RetryHandler:
    """Handles retry logic for API calls."""
    
    def __init__(self):
        self.config = settings.retry
    
    def should_retry(self, exception: Exception) -> bool:
        """Determine if an exception should trigger a retry."""
        # Don't retry authentication errors or not found errors
        if isinstance(exception, (AuthenticationError, NotFoundError)):
            return False
        
        # Retry on rate limit errors, server errors, and connection errors
        if isinstance(exception, (RateLimitError, ServerError)):
            return True
        
        # Retry on specific HTTP status codes
        if isinstance(exception, requests.exceptions.RequestException):
            if hasattr(exception, 'response') and exception.response:
                status_code = exception.response.status_code
                # Retry on 5xx errors and 429 (rate limit)
                if status_code >= 500 or status_code == 429:
                    return True
        
        # Retry on connection errors
        if isinstance(exception, (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError
        )):
            return True
        
        return False
    
    def get_retry_decorator(self):
        """Get a tenacity retry decorator with configured settings."""
        return retry(
            stop=stop_after_attempt(self.config.max_attempts),
            wait=wait_exponential(
                multiplier=self.config.base_delay,
                max=self.config.max_delay,
                exp_base=self.config.exponential_base
            ),
            retry=retry_if_exception_type((
                RateLimitError,
                ServerError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError
            )),
            before_sleep=before_sleep_log(logger.logger, logging.WARNING),
            reraise=True
        )
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with retry logic."""
        decorator = self.get_retry_decorator()
        wrapped_func = decorator(func)
        return wrapped_func(*args, **kwargs)


def with_retry(func: Callable) -> Callable:
    """Decorator to add retry logic to a function."""
    retry_handler = RetryHandler()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        return retry_handler.execute_with_retry(func, *args, **kwargs)
    
    return wrapper


def handle_rate_limit(response: requests.Response) -> None:
    """Handle rate limit responses by waiting appropriately."""
    if response.status_code == 429:
        # Check for Retry-After header
        retry_after = response.headers.get('Retry-After')
        if retry_after:
            try:
                wait_time = int(retry_after)
                logger.warning(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                return
            except ValueError:
                pass
        
        # Default wait time for rate limits
        wait_time = 60  # 1 minute default
        logger.warning(f"Rate limit hit. Waiting {wait_time} seconds...")
        time.sleep(wait_time)
        
        raise RateLimitError(
            "API rate limit exceeded",
            status_code=429,
            response=response.json() if response.content else None
        )


def exponential_backoff(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """Calculate exponential backoff delay."""
    delay = min(base_delay * (2 ** attempt), max_delay)
    
    # Add jitter to avoid thundering herd
    if settings.retry.jitter:
        delay *= (0.5 + random.random() * 0.5)
    
    return delay


# Global retry handler instance
retry_handler = RetryHandler()

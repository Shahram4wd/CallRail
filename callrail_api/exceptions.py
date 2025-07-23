"""
Base exception classes for CallRail API client.
"""


class CallRailAPIException(Exception):
    """Base exception for CallRail API errors."""
    
    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthenticationError(CallRailAPIException):
    """Raised when API authentication fails."""
    pass


class RateLimitError(CallRailAPIException):
    """Raised when API rate limit is exceeded."""
    pass


class NotFoundError(CallRailAPIException):
    """Raised when a resource is not found."""
    pass


class ValidationError(CallRailAPIException):
    """Raised when request validation fails."""
    pass


class ServerError(CallRailAPIException):
    """Raised when the server encounters an error."""
    pass

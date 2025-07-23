"""
CallRail API Client

A Python client for the CallRail API v3.
"""

__version__ = "1.0.0"

from .client import CallRailClient
from .models import *

__all__ = ["CallRailClient"]

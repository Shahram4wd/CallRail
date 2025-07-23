"""
Test script to verify the CallRail API client works correctly.

This script tests the basic functionality of the client without making
actual API calls (for quick verification).
"""

import sys
import os

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")
    
    try:
        from callrail_api import CallRailClient
        print("✓ CallRailClient imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import CallRailClient: {e}")
        return False
    
    try:
        from callrail_api.models import Account, Company, Call, Tracker
        print("✓ Models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import models: {e}")
        return False
    
    try:
        from callrail_api.exceptions import CallRailAPIException, AuthenticationError
        print("✓ Exceptions imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import exceptions: {e}")
        return False
    
    return True


def test_client_initialization():
    """Test client initialization."""
    print("\nTesting client initialization...")
    
    try:
        from callrail_api import CallRailClient
        
        # Test with explicit API key
        client = CallRailClient(api_key="test_key")
        print("✓ Client initialized with explicit API key")
        
        # Verify headers are set correctly
        expected_auth = 'Token token="test_key"'
        if client.session.headers.get('Authorization') == expected_auth:
            print("✓ Authorization header set correctly")
        else:
            print("❌ Authorization header not set correctly")
            return False
            
        # Verify other headers
        if client.session.headers.get('Content-Type') == 'application/json':
            print("✓ Content-Type header set correctly")
        else:
            print("❌ Content-Type header not set correctly")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False


def test_model_creation():
    """Test that models can be created correctly."""
    print("\nTesting model creation...")
    
    try:
        from callrail_api.models import Account, Company, Call
        
        # Test Account model
        account_data = {
            'id': 'ACC123',
            'name': 'Test Account',
            'outbound_recording_enabled': True,
            'hipaa_account': False
        }
        account = Account(**account_data)
        print(f"✓ Account model created: {account.name}")
        
        # Test Company model
        company_data = {
            'id': 'COM123',
            'name': 'Test Company',
            'status': 'active',
            'time_zone': 'America/New_York',
            'created_at': '2023-01-01T00:00:00Z'
        }
        company = Company(**company_data)
        print(f"✓ Company model created: {company.name}")
        
        # Test Call model
        call_data = {
            'id': 'CAL123',
            'answered': True,
            'business_phone_number': '+15551234567',
            'customer_city': 'New York',
            'customer_country': 'US',
            'customer_name': 'John Doe',
            'customer_phone_number': '+15559876543',
            'customer_state': 'NY',
            'direction': 'inbound',
            'duration': 120,
            'recording': None,
            'recording_duration': None,
            'recording_player': None,
            'start_time': '2023-01-01T12:00:00Z',
            'tracking_phone_number': '+15551234567',
            'voicemail': False
        }
        call = Call(**call_data)
        print(f"✓ Call model created: {call.customer_name} -> {call.tracking_phone_number}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False


def test_exceptions():
    """Test that custom exceptions work correctly."""
    print("\nTesting exceptions...")
    
    try:
        from callrail_api.exceptions import (
            CallRailAPIException, AuthenticationError, RateLimitError
        )
        
        # Test base exception
        try:
            raise CallRailAPIException("Test error", status_code=400)
        except CallRailAPIException as e:
            if e.status_code == 400:
                print("✓ CallRailAPIException works correctly")
            else:
                print("❌ CallRailAPIException status code not set correctly")
                return False
        
        # Test authentication error
        try:
            raise AuthenticationError("Auth failed", status_code=401)
        except AuthenticationError as e:
            if e.status_code == 401:
                print("✓ AuthenticationError works correctly")
            else:
                print("❌ AuthenticationError status code not set correctly")
                return False
        
        # Test rate limit error
        try:
            raise RateLimitError("Rate limit exceeded", status_code=429)
        except RateLimitError as e:
            if e.status_code == 429:
                print("✓ RateLimitError works correctly")
            else:
                print("❌ RateLimitError status code not set correctly")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Exception testing failed: {e}")
        return False


def main():
    """Run all tests."""
    print("CallRail API Client - Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_client_initialization,
        test_model_creation,
        test_exceptions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The CallRail API client is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

"""
Example usage of the CallRail API client.

This file demonstrates how to use the CallRail API client to interact
with various CallRail API endpoints.
"""

import os
from callrail_api import CallRailClient
from callrail_api.exceptions import CallRailAPIException


def main():
    """Main example function demonstrating CallRail API usage."""
    
    # Initialize the client (API key will be loaded from .env file)
    try:
        client = CallRailClient()
        print("✓ CallRail API client initialized successfully")
    except ValueError as e:
        print(f"❌ Error initializing client: {e}")
        return
    
    try:
        # 1. List all accounts
        print("\n--- Listing Accounts ---")
        accounts_response = client.list_accounts()
        print(f"Found {accounts_response.total_records} accounts")
        
        if accounts_response.data:
            first_account = accounts_response.data[0]
            print(f"First account: {first_account.name} (ID: {first_account.id})")
            account_id = first_account.id
            
            # 2. List companies in the first account
            print(f"\n--- Listing Companies in Account {account_id} ---")
            companies_response = client.list_companies(account_id)
            print(f"Found {companies_response.total_records} companies")
            
            if companies_response.data:
                first_company = companies_response.data[0]
                print(f"First company: {first_company.name} (ID: {first_company.id})")
                
                # 3. List calls (recent calls by default)
                print(f"\n--- Listing Recent Calls ---")
                calls_response = client.list_calls(account_id, per_page=5)
                print(f"Found {calls_response.total_records} total calls (showing first 5)")
                
                for call in calls_response.data:
                    status = "Answered" if call.answered else "Missed"
                    duration = f"{call.duration}s" if call.duration else "N/A"
                    print(f"  - {call.customer_phone_number} → {call.tracking_phone_number}")
                    print(f"    Status: {status}, Duration: {duration}, Time: {call.start_time}")
                
                # 4. List trackers
                print(f"\n--- Listing Trackers ---")
                trackers_response = client.list_trackers(account_id)
                print(f"Found {trackers_response.total_records} trackers")
                
                for tracker in trackers_response.data:
                    numbers = ", ".join(tracker.tracking_numbers)
                    print(f"  - {tracker.name} ({tracker.type}): {numbers}")
                
                # 5. List tags
                print(f"\n--- Listing Tags ---")
                tags_response = client.list_tags(account_id)
                print(f"Found {tags_response.total_records} tags")
                
                for tag in tags_response.data:
                    print(f"  - {tag.name} ({tag.color})")
                
                # 6. Get call summary for recent period
                print(f"\n--- Call Summary (Recent) ---")
                summary = client.get_call_summary(account_id, date_range="recent")
                if 'total_results' in summary:
                    total_calls = summary['total_results'].get('total_calls', 0)
                    print(f"Total calls in recent period: {total_calls}")
                
        else:
            print("No accounts found")
            
    except CallRailAPIException as e:
        print(f"❌ CallRail API Error: {e}")
        if hasattr(e, 'status_code'):
            print(f"   Status Code: {e.status_code}")
        if hasattr(e, 'response') and e.response:
            print(f"   Response: {e.response}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def example_create_tag():
    """Example of creating a new tag."""
    client = CallRailClient()
    
    try:
        # Get the first account and company
        accounts = client.list_accounts()
        if not accounts.data:
            print("No accounts available")
            return
            
        account_id = accounts.data[0].id
        companies = client.list_companies(account_id)
        if not companies.data:
            print("No companies available")
            return
            
        company_id = companies.data[0].id
        
        # Create a new tag
        tag_data = {
            "name": "API Example Tag",
            "company_id": company_id,
            "color": "blue1"
        }
        
        new_tag = client.create_tag(account_id, tag_data)
        print(f"✓ Created tag: {new_tag.name} (ID: {new_tag.id})")
        
    except CallRailAPIException as e:
        print(f"❌ Error creating tag: {e}")


def example_update_call():
    """Example of updating a call with notes and tags."""
    client = CallRailClient()
    
    try:
        # Get the first account
        accounts = client.list_accounts()
        if not accounts.data:
            print("No accounts available")
            return
            
        account_id = accounts.data[0].id
        
        # Get recent calls
        calls = client.list_calls(account_id, per_page=1)
        if not calls.data:
            print("No calls available")
            return
            
        call = calls.data[0]
        call_id = call.id
        
        # Update the call with a note
        update_data = {
            "note": "Updated via API example",
            "tags": ["Important"],
            "append_tags": True
        }
        
        updated_call = client.update_call(account_id, call_id, update_data)
        print(f"✓ Updated call {call_id} with note: {updated_call.note}")
        
    except CallRailAPIException as e:
        print(f"❌ Error updating call: {e}")


if __name__ == "__main__":
    print("CallRail API Client Example")
    print("=" * 40)
    main()
    
    print("\n" + "=" * 40)
    print("Additional Examples:")
    print("Uncomment the lines below to try other examples")
    
    # Uncomment to try these examples:
    # example_create_tag()
    # example_update_call()

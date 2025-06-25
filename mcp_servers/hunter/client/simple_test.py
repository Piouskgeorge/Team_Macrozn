#!/usr/bin/env python3
"""
Simple Hunter.io API Test

This script directly tests the Hunter.io API to show it's working correctly.
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

def test_domain_search():
    """Test domain search directly"""
    print("🔍 Testing Domain Search")
    print("=" * 40)
    
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": "microsoft.com",
        "api_key": HUNTER_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            emails = data.get('data', {}).get('emails', [])
            print(f"✅ SUCCESS! Found {len(emails)} emails")
            
            if emails:
                print("Sample emails:")
                for email in emails[:5]:
                    print(f"  - {email.get('value', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print()

def test_email_finder():
    """Test email finder directly"""
    print("📧 Testing Email Finder")
    print("=" * 40)
    
    url = "https://api.hunter.io/v2/email-finder"
    params = {
        "full_name": "Bill Gates",
        "domain": "microsoft.com",
        "api_key": HUNTER_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            email = data.get('data', {}).get('email')
            score = data.get('data', {}).get('score')
            
            if email:
                print(f"✅ SUCCESS! Found email: {email}")
                print(f"   Confidence score: {score}")
            else:
                print("⚠️  No email found")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print()

def test_email_verifier():
    """Test email verifier directly"""
    print("✅ Testing Email Verifier")
    print("=" * 40)
    
    test_email = "bill.gates@microsoft.com"
    url = "https://api.hunter.io/v2/email-verifier"
    params = {
        "email": test_email,
        "api_key": HUNTER_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('data', {}).get('status')
            score = data.get('data', {}).get('score')
            
            print(f"✅ SUCCESS! Email: {test_email}")
            print(f"   Status: {status}")
            print(f"   Score: {score}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print()

def test_account_info():
    """Test account info directly"""
    print("👤 Testing Account Info")
    print("=" * 40)
    
    url = "https://api.hunter.io/v2/account"
    params = {
        "api_key": HUNTER_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            account = data.get('data', {})
            
            print(f"✅ SUCCESS! Account Info:")
            print(f"   Name: {account.get('first_name', '')} {account.get('last_name', '')}")
            print(f"   Email: {account.get('email', 'N/A')}")
            print(f"   Plan: {account.get('plan_name', 'N/A')}")
            
            # Show usage
            calls = account.get('calls', {})
            searches = calls.get('searches', {})
            if searches:
                used = searches.get('used', 0)
                available = searches.get('available', 0)
                print(f"   Searches: {used}/{available}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print()

def test_email_count():
    """Test email count directly"""
    print("📊 Testing Email Count")
    print("=" * 40)
    
    url = "https://api.hunter.io/v2/email-count"
    params = {
        "domain": "microsoft.com",
        "api_key": HUNTER_API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('data', {}).get('total')
            
            print(f"✅ SUCCESS! Total emails: {total}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print()

def main():
    """Main test function"""
    print("🚀 Simple Hunter.io API Test")
    print("=" * 50)
    
    if not HUNTER_API_KEY:
        print("❌ HUNTER_API_KEY not found in environment variables")
        return
    
    print(f"✅ API Key found: {HUNTER_API_KEY[:10]}...")
    print()
    
    # Run tests
    test_domain_search()
    test_email_finder()
    test_email_verifier()
    test_account_info()
    test_email_count()
    
    print("🎉 All direct API tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main() 
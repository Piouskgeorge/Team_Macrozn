#!/usr/bin/env python3
"""
Test script for Hunter.io MCP Server Tools

This script tests all available Hunter.io tools with various scenarios
to ensure they're working correctly.
"""

import requests
import json
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configuration
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
MCP_SERVER_URL = "http://localhost:8888"

def test_domain_search():
    """Test the domain search tool"""
    print("🔍 Testing Domain Search Tool")
    print("=" * 50)
    
    test_domains = [
        "microsoft.com",
        "google.com", 
        "github.com"
    ]
    
    for domain in test_domains:
        print(f"\nTesting domain: {domain}")
        try:
            response = requests.post(
                f"{MCP_SERVER_URL}/tools/hunter_domain_search",
                json={"domain": domain},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: Found {len(result.get('data', {}).get('emails', []))} emails")
                if result.get('data', {}).get('emails'):
                    print(f"   Sample emails: {[email['value'] for email in result['data']['emails'][:3]]}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        time.sleep(1)  # Rate limiting

def test_email_finder():
    """Test the email finder tool"""
    print("\n\n📧 Testing Email Finder Tool")
    print("=" * 50)
    
    test_cases = [
        {"full_name": "Bill Gates", "domain": "microsoft.com"},
        {"full_name": "Sundar Pichai", "domain": "google.com"},
        {"full_name": "Satya Nadella", "domain": "microsoft.com"}
    ]
    
    for case in test_cases:
        print(f"\nTesting: {case['full_name']} at {case['domain']}")
        try:
            response = requests.post(
                f"{MCP_SERVER_URL}/tools/hunter_email_finder",
                json=case,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('data', {}).get('email'):
                    print(f"✅ Found email: {result['data']['email']}")
                    print(f"   Score: {result['data'].get('score', 'N/A')}")
                else:
                    print("⚠️  No email found")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        time.sleep(1)  # Rate limiting

def test_email_verifier():
    """Test the email verifier tool"""
    print("\n\n✅ Testing Email Verifier Tool")
    print("=" * 50)
    
    test_emails = [
        "bill.gates@microsoft.com",
        "sundar@google.com",
        "test@nonexistentdomain12345.com",
        "invalid-email-format"
    ]
    
    for email in test_emails:
        print(f"\nTesting email: {email}")
        try:
            response = requests.post(
                f"{MCP_SERVER_URL}/tools/hunter_email_verifier",
                json={"email": email},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('data', {}).get('status'):
                    status = result['data']['status']
                    print(f"✅ Status: {status}")
                    if status == 'valid':
                        print(f"   Score: {result['data'].get('score', 'N/A')}")
                        print(f"   Disposable: {result['data'].get('disposable', 'N/A')}")
                else:
                    print("⚠️  No verification data")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        time.sleep(1)  # Rate limiting

def test_lead_finder():
    """Test the lead finder tool"""
    print("\n\n👥 Testing Lead Finder Tool")
    print("=" * 50)
    
    test_cases = [
        {"domain": "microsoft.com"},
        {"domain": "google.com", "department": "engineering"},
        {"domain": "github.com", "seniority": "senior"}
    ]
    
    for case in test_cases:
        print(f"\nTesting: {case}")
        try:
            response = requests.post(
                f"{MCP_SERVER_URL}/tools/hunter_lead_finder",
                json=case,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('data', {}).get('leads'):
                    leads = result['data']['leads']
                    print(f"✅ Found {len(leads)} leads")
                    if leads:
                        print(f"   Sample lead: {leads[0].get('email', 'N/A')} - {leads[0].get('first_name', '')} {leads[0].get('last_name', '')}")
                else:
                    print("⚠️  No leads found")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        time.sleep(1)  # Rate limiting

def test_email_count():
    """Test the email count tool"""
    print("\n\n📊 Testing Email Count Tool")
    print("=" * 50)
    
    test_domains = [
        "microsoft.com",
        "google.com",
        "github.com"
    ]
    
    for domain in test_domains:
        print(f"\nTesting domain: {domain}")
        try:
            response = requests.post(
                f"{MCP_SERVER_URL}/tools/hunter_email_count",
                json={"domain": domain},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('data', {}).get('total'):
                    total = result['data']['total']
                    print(f"✅ Total emails: {total}")
                else:
                    print("⚠️  No count data")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        time.sleep(1)  # Rate limiting

def test_account_info():
    """Test the account info tool"""
    print("\n\n👤 Testing Account Info Tool")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/tools/hunter_account_info",
            json={},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('data'):
                data = result['data']
                print(f"✅ Account: {data.get('first_name', '')} {data.get('last_name', '')}")
                print(f"   Email: {data.get('email', 'N/A')}")
                print(f"   Plan: {data.get('plan_name', 'N/A')}")
                print(f"   Searches left: {data.get('calls', {}).get('searches', {}).get('used', 0)}/{data.get('calls', {}).get('searches', {}).get('available', 0)}")
            else:
                print("⚠️  No account data")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_email_sources():
    """Test the email sources tool"""
    print("\n\n🔍 Testing Email Sources Tool")
    print("=" * 50)
    
    test_emails = [
        "bill.gates@microsoft.com",
        "sundar@google.com"
    ]
    
    for email in test_emails:
        print(f"\nTesting email: {email}")
        try:
            response = requests.post(
                f"{MCP_SERVER_URL}/tools/hunter_email_sources",
                json={"email": email},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('data', {}).get('sources'):
                    sources = result['data']['sources']
                    print(f"✅ Found {len(sources)} sources")
                    if sources:
                        print(f"   Sample source: {sources[0].get('domain', 'N/A')} - {sources[0].get('uri', 'N/A')}")
                else:
                    print("⚠️  No sources found")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        time.sleep(1)  # Rate limiting

def test_direct_hunter_api():
    """Test direct Hunter.io API calls for comparison"""
    print("\n\n🔧 Testing Direct Hunter.io API")
    print("=" * 50)
    
    if not HUNTER_API_KEY:
        print("❌ HUNTER_API_KEY not found in environment variables")
        return
    
    # Test domain search
    print("\nTesting direct domain search...")
    try:
        response = requests.get(
            "https://api.hunter.io/v2/domain-search",
            params={
                "domain": "microsoft.com",
                "api_key": HUNTER_API_KEY
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Direct API: Found {len(data.get('data', {}).get('emails', []))} emails")
        else:
            print(f"❌ Direct API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Direct API Exception: {str(e)}")

def check_server_status():
    """Check if the MCP server is running"""
    print("🔍 Checking MCP Server Status")
    print("=" * 50)
    
    try:
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ MCP Server is running")
            return True
        else:
            print(f"⚠️  MCP Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ MCP Server is not running")
        print("   Please start the server with: python server.py")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Hunter.io MCP Server Test Suite")
    print("=" * 60)
    
    # Check if server is running
    if not check_server_status():
        return
    
    # Check API key
    if not HUNTER_API_KEY:
        print("❌ HUNTER_API_KEY not found in environment variables")
        print("   Please set up your .env file with your Hunter.io API key")
        return
    
    print(f"✅ Hunter.io API Key found: {HUNTER_API_KEY[:10]}...")
    
    # Run tests
    test_direct_hunter_api()
    test_domain_search()
    test_email_finder()
    test_email_verifier()
    test_lead_finder()
    test_email_count()
    test_account_info()
    test_email_sources()
    
    print("\n\n🎉 Test suite completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Setup script for Hunter.io MCP Server

This script helps set up the Hunter.io MCP server by:
1. Installing dependencies
2. Creating .env file from template
3. Validating configuration
"""

import os
import subprocess
import sys
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    print("\n🔧 Setting up environment file...")
    
    env_template = Path("env_template.txt")
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env file creation")
            return True
    
    if not env_template.exists():
        print("❌ env_template.txt not found")
        return False
    
    try:
        # Copy template to .env
        with open(env_template, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created from template")
        print("📝 Please edit .env file with your actual API keys:")
        print("   - HUNTER_API_KEY: Get from https://hunter.io/api-keys")
        print("   - Azure OpenAI credentials (if using Azure)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def validate_configuration():
    """Validate the configuration"""
    print("\n🔍 Validating configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    hunter_key = os.getenv("HUNTER_API_KEY")
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    api_key = os.getenv("API_KEY")
    model = os.getenv("MODEL")
    
    if not hunter_key or hunter_key == "your_hunter_api_key_here":
        print("❌ HUNTER_API_KEY not configured")
        return False
    
    if not azure_endpoint or azure_endpoint == "your_azure_endpoint_here":
        print("❌ AZURE_ENDPOINT not configured")
        return False
    
    if not api_key or api_key == "your_azure_api_key_here":
        print("❌ API_KEY not configured")
        return False
    
    if not model or model == "your_azure_model_name_here":
        print("❌ MODEL not configured")
        return False
    
    print("✅ Configuration validated")
    return True

def test_hunter_api():
    """Test Hunter.io API connection"""
    print("\n🧪 Testing Hunter.io API connection...")
    
    from dotenv import load_dotenv
    import requests
    
    load_dotenv()
    hunter_key = os.getenv("HUNTER_API_KEY")
    
    if not hunter_key or hunter_key == "your_hunter_api_key_here":
        print("❌ HUNTER_API_KEY not configured")
        return False
    
    try:
        response = requests.get(
            "https://api.hunter.io/v2/account",
            params={"api_key": hunter_key},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                account = data['data']
                print(f"✅ API connection successful")
                print(f"   Account: {account.get('first_name', '')} {account.get('last_name', '')}")
                print(f"   Plan: {account.get('plan_name', 'N/A')}")
                return True
            else:
                print("❌ Invalid API response")
                return False
        elif response.status_code == 401:
            print("❌ Invalid API key")
            return False
        else:
            print(f"❌ API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Hunter.io MCP Server Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("server.py").exists():
        print("❌ Please run this script from the hunter directory")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Validate configuration
    if not validate_configuration():
        print("\n📝 Please configure your .env file and run setup again")
        return
    
    # Test API connection
    if not test_hunter_api():
        print("\n❌ Hunter.io API test failed")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the server: python server.py")
    print("2. Run tests: python test_hunter_tools.py")
    print("3. The server will be available at http://localhost:8888")

if __name__ == "__main__":
    main() 
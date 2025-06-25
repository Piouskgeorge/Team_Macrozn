#!/usr/bin/env python3
"""
Startup script for the Apify Conversational Interface
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
from dotenv import load_dotenv
load_dotenv()
      
# Set environment variables for Azure OpenAI
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://opeanai-eastus.openai.azure.com/")
os.environ.setdefault("AZURE_OPENAI_API_KEY", "")
os.environ.setdefault("AZURE_OPENAI_MODEL", "gpt4o")

# Check if APIFY_API_KEY is set
if not os.getenv("APIFY_API_KEY"):
    print("⚠️  Warning: APIFY_API_KEY not set. Some features may be limited.")
    print("   Set it with: export APIFY_API_KEY='your_apify_api_key_here'")
    print()

async def main():
    """Main entry point"""
    try:
        print("🚀 Starting Apify Conversational Interface...")
        print("Trying simple version first (recommended for Windows)...")
        
        # Try the simple version first
        try:
            from simple_conversation import SimpleApifyConversationalInterface
            
            async with SimpleApifyConversationalInterface() as interface:
                await interface.interactive_chat()
                
        except ImportError as e:
            print(f"Simple version failed: {e}")
            print("Trying full version...")
            
            # Fall back to the full version
            from conversational_interface import ApifyConversationalInterface
            
            async with ApifyConversationalInterface() as interface:
                await interface.interactive_chat()
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required dependencies:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting interface: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 
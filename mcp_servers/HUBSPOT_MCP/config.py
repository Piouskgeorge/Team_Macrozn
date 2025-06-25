import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for HubSpot MCP"""
    
    # Azure OpenAI Configuration
    AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
    AZURE_API_KEY = os.getenv('AZURE_API_KEY')
    AZURE_MODEL = os.getenv('AZURE_MODEL')
    
    # HubSpot Configuration
    HUBSPOT_ACCESS_TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')
    
    # API Configuration
    HUBSPOT_API_BASE_URL = "https://api.hubapi.com"
    AZURE_API_VERSION = "2024-02-15-preview"
    
    # Default limits
    DEFAULT_CONTACT_LIMIT = 5
    DEFAULT_DEAL_LIMIT = 5
    DEFAULT_CART_LIMIT = 5
    
    # Custom Object Configuration
    CART_OBJECT_TYPE = "carts"
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        required_vars = [
            'AZURE_ENDPOINT', 'AZURE_API_KEY', 'AZURE_MODEL', 'HUBSPOT_ACCESS_TOKEN'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True 
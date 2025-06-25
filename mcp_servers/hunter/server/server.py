from fastapi import FastAPI, HTTPException
from mcp.server.fastmcp import FastMCP
import os
import requests
from dotenv import load_dotenv
from typing import Optional

# Load .env variables
load_dotenv()

# Environment variables
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

# Validate required environment variables
if not HUNTER_API_KEY:
    raise ValueError("HUNTER_API_KEY environment variable is required")
if not AZURE_ENDPOINT:
    raise ValueError("AZURE_ENDPOINT environment variable is required")
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")
if not MODEL:
    raise ValueError("MODEL environment variable is required")

# Initialize FastMCP server
mcp = FastMCP("Hunter MCP", openai_endpoint=AZURE_ENDPOINT, openai_api_key=API_KEY, openai_model=MODEL)

# Create FastAPI app and mount MCP
app = FastAPI(title="Hunter.io MCP Server", version="1.0.0")

# Add health endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Hunter.io MCP Server"}

# Mount the MCP app
app.mount("/", mcp.streamable_http_app)

# === TOOL: Domain Search ===
@mcp.tool(name="hunter_domain_search", description="Find emails and domain info using Hunter.io")
def domain_search(domain: str) -> dict:
    """
    Search domain using Hunter.io to find email addresses and domain information.
    
    Args:
        domain: The domain to search (e.g., "example.com")
    
    Returns:
        Dictionary containing domain search results from Hunter.io
    """
    try:
        url = f"https://api.hunter.io/v2/domain-search"
        params = {
            "domain": domain,
            "api_key": HUNTER_API_KEY
        }
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your HUNTER_API_KEY."}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"API request failed with status {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# === TOOL: Email Finder ===
@mcp.tool(name="hunter_email_finder", description="Find a professional email using full name and domain")
def email_finder(full_name: str, domain: str) -> dict:
    """
    Find email address using Hunter.io based on full name and domain.
    
    Args:
        full_name: The full name of the person (e.g., "John Doe")
        domain: The domain to search (e.g., "example.com")
    
    Returns:
        Dictionary containing email finder results from Hunter.io
    """
    try:
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "full_name": full_name,
            "domain": domain,
            "api_key": HUNTER_API_KEY
        }
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your HUNTER_API_KEY."}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"API request failed with status {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# === TOOL: Email Verifier ===
@mcp.tool(name="hunter_email_verifier", description="Verify if an email address is valid and deliverable")
def email_verifier(email: str) -> dict:
    """
    Verify email address using Hunter.io to check if it's valid and deliverable.
    
    Args:
        email: The email address to verify (e.g., "john@example.com")
    
    Returns:
        Dictionary containing email verification results from Hunter.io
    """
    try:
        url = "https://api.hunter.io/v2/email-verifier"
        params = {
            "email": email,
            "api_key": HUNTER_API_KEY
        }
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your HUNTER_API_KEY."}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"API request failed with status {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# === TOOL: Lead Finder ===
@mcp.tool(name="hunter_lead_finder", description="Find leads based on company domain and other criteria")
def lead_finder(domain: str, first_name: Optional[str] = None, last_name: Optional[str] = None, 
                seniority: Optional[str] = None, department: Optional[str] = None) -> dict:
    """
    Find leads using Hunter.io based on various criteria.
    
    Args:
        domain: The company domain (e.g., "example.com")
        first_name: First name filter (optional)
        last_name: Last name filter (optional)
        seniority: Seniority level filter (optional, e.g., "senior", "junior", "executive")
        department: Department filter (optional, e.g., "engineering", "sales", "marketing")
    
    Returns:
        Dictionary containing lead finder results from Hunter.io
    """
    try:
        url = "https://api.hunter.io/v2/lead-finder"
        params = {
            "domain": domain,
            "api_key": HUNTER_API_KEY
        }
        
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if seniority:
            params["seniority"] = seniority
        if department:
            params["department"] = department
            
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your HUNTER_API_KEY."}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"API request failed with status {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# === TOOL: Email Count ===
@mcp.tool(name="hunter_email_count", description="Get the number of email addresses for a domain")
def email_count(domain: str) -> dict:
    """
    Get the number of email addresses available for a domain.
    
    Args:
        domain: The domain to check (e.g., "example.com")
    
    Returns:
        Dictionary containing email count results from Hunter.io
    """
    try:
        url = "https://api.hunter.io/v2/email-count"
        params = {
            "domain": domain,
            "api_key": HUNTER_API_KEY
        }
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your HUNTER_API_KEY."}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"API request failed with status {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# === TOOL: Account Information ===
@mcp.tool(name="hunter_account_info", description="Get information about your Hunter.io account")
def account_info() -> dict:
    """
    Get information about your Hunter.io account including usage and limits.
    
    Returns:
        Dictionary containing account information from Hunter.io
    """
    try:
        url = "https://api.hunter.io/v2/account"
        params = {
            "api_key": HUNTER_API_KEY
        }
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your HUNTER_API_KEY."}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"API request failed with status {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# === TOOL: Email Sources ===
@mcp.tool(name="hunter_email_sources", description="Find sources where an email address was found")
def email_sources(email: str) -> dict:
    """
    Find sources where an email address was found on the web.
    
    Args:
        email: The email address to search for sources (e.g., "john@example.com")
    
    Returns:
        Dictionary containing email sources results from Hunter.io
    """
    try:
        url = "https://api.hunter.io/v2/email-sources"
        params = {
            "email": email,
            "api_key": HUNTER_API_KEY
        }
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key. Please check your HUNTER_API_KEY."}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            return {"error": f"API request failed with status {response.status_code}: {response.text}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app on port 8888
    uvicorn.run(app, host="0.0.0.0", port=8888)

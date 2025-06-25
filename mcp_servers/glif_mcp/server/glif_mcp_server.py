import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode
from dotenv import load_dotenv
import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("glif-mcp")

# Constants
GLIF_API_BASE = "https://glif.app/api"
GLIF_SIMPLE_API = "https://simple-api.glif.app"

# Define a minimal NotificationOptions class to fix the AttributeError
class NotificationOptions:
    tools_changed = False  # Set to False as a default; adjust if needed

class GlifMCPServer:
    """MCP Server for Glif.app API integration"""
    
    def __init__(self):
        self.server = Server("glif-mcp")
        self.api_token = os.environ.get("GLIF_API_TOKEN")
        self.http_client = None
        
        # Register tools
        self._register_tools()
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.http_client = httpx.AsyncClient(timeout=30.0)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.http_client:
            await self.http_client.aclose()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authorization"""
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers
    
    def _register_tools(self):
        """Register all available tools"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="get_glif",
                    description="Fetch a specific glif by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "glif_id": {
                                "type": "string",
                                "description": "The ID of the glif to fetch"
                            },
                            "include_graph": {
                                "type": "boolean",
                                "description": "Include full glif-graph JSON data",
                                "default": False
                            }
                        },
                        "required": ["glif_id"]
                    }
                ),
                Tool(
                    name="list_glifs",
                    description="List glifs with optional filters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "featured": {
                                "type": "boolean",
                                "description": "Get featured glifs only"
                            },
                            "username": {
                                "type": "string",
                                "description": "Filter by username"
                            },
                            "user_id": {
                                "type": "string",
                                "description": "Filter by user ID"
                            },
                            "page": {
                                "type": "integer",
                                "description": "Page number for pagination",
                                "default": 1
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of results per page (max 100)",
                                "default": 20
                            },
                            "include_graph": {
                                "type": "boolean",
                                "description": "Include full glif-graph JSON data",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="run_glif",
                    description="Execute a glif using the Simple API",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "glif_id": {
                                "type": "string",
                                "description": "The ID of the glif to run"
                            },
                            "inputs": {
                                "type": ["array", "object"],
                                "description": "Inputs for the glif (array for positional, object for named)"
                            },
                            "visibility": {
                                "type": "string",
                                "enum": ["PUBLIC", "PRIVATE"],
                                "description": "Visibility of the run",
                                "default": "PRIVATE"
                            },
                            "strict": {
                                "type": "boolean",
                                "description": "Enable strict mode (fail if insufficient inputs)",
                                "default": False
                            }
                        },
                        "required": ["glif_id"]
                    }
                ),
                Tool(
                    name="get_run",
                    description="Fetch details of a specific run",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "run_id": {
                                "type": "string",
                                "description": "The ID of the run to fetch"
                            }
                        },
                        "required": ["run_id"]
                    }
                ),
                Tool(
                    name="list_runs",
                    description="List runs with optional filters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "glif_id": {
                                "type": "string",
                                "description": "Filter by glif ID"
                            },
                            "username": {
                                "type": "string",
                                "description": "Filter by username"
                            },
                            "user_id": {
                                "type": "string",
                                "description": "Filter by user ID"
                            },
                            "page": {
                                "type": "integer",
                                "description": "Page number for pagination",
                                "default": 1
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of results per page (max 100)",
                                "default": 20
                            }
                        }
                    }
                ),
                Tool(
                    name="get_user_info",
                    description="Get information about a user",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Username to look up"
                            },
                            "user_id": {
                                "type": "string",
                                "description": "User ID to look up"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_me",
                    description="Get information about the authenticated user",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="list_spheres",
                    description="List all public spheres (collections)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "slug": {
                                "type": "string",
                                "description": "Get glifs from a specific sphere by slug"
                            },
                            "sphere_id": {
                                "type": "string",
                                "description": "Get glifs from a specific sphere by ID"
                            },
                            "include_graph": {
                                "type": "boolean",
                                "description": "Include full glif-graph JSON data",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="create_glif",
                    description="Create a new glif (requires API token)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the glif"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the glif"
                            },
                            "graph": {
                                "type": "object",
                                "description": "The glif graph structure with nodes",
                                "properties": {
                                    "nodes": {
                                        "type": "array",
                                        "description": "Array of nodes in the glif graph",
                                        "items": {
                                            "type": "object"
                                        }
                                    }
                                },
                                "required": ["nodes"]
                            },
                            "published_at": {
                                "type": "string",
                                "description": "ISO date string to publish the glif"
                            }
                        },
                        "required": ["name", "description", "graph"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls"""
            try:
                if name == "get_glif":
                    return await self._get_glif(arguments)
                elif name == "list_glifs":
                    return await self._list_glifs(arguments)
                elif name == "run_glif":
                    return await self._run_glif(arguments)
                elif name == "get_run":
                    return await self._get_run(arguments)
                elif name == "list_runs":
                    return await self._list_runs(arguments)
                elif name == "get_user_info":
                    return await self._get_user_info(arguments)
                elif name == "get_me":
                    return await self._get_me(arguments)
                elif name == "list_spheres":
                    return await self._list_spheres(arguments)
                elif name == "create_glif":
                    return await self._create_glif(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _get_glif(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get a specific glif"""
        glif_id = args["glif_id"]
        include_graph = args.get("include_graph", False)
        
        params = {"id": glif_id}
        if include_graph:
            params["includes"] = "spells.data"
        
        url = f"{GLIF_API_BASE}/glifs?" + urlencode(params)
        
        response = await self.http_client.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
    
    async def _list_glifs(self, args: Dict[str, Any]) -> List[TextContent]:
        """List glifs with filters"""
        params = {}
        
        if args.get("featured"):
            params["featured"] = "1"
        if args.get("username"):
            params["username"] = args["username"]
        if args.get("user_id"):
            params["userId"] = args["user_id"]
        if args.get("page", 1) > 1:
            params["page"] = args["page"]
        if args.get("limit", 20) != 20:
            params["limit"] = args["limit"]
        if args.get("include_graph"):
            params["includes"] = "spells.data"
        
        url = f"{GLIF_API_BASE}/glifs"
        if params:
            url += "?" + urlencode(params)
        
        response = await self.http_client.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
    
    async def _run_glif(self, args: Dict[str, Any]) -> List[TextContent]:
        """Run a glif using the Simple API"""
        if not self.api_token:
            return [TextContent(type="text", text="Error: API token required for running glifs")]
        
        glif_id = args["glif_id"]
        inputs = args.get("inputs", [])
        visibility = args.get("visibility", "PRIVATE")
        strict = args.get("strict", False)
        
        payload = {
            "id": glif_id,
            "inputs": inputs,
            "visibility": visibility
        }
        
        url = GLIF_SIMPLE_API
        if strict:
            url += "?strict=1"
        
        response = await self.http_client.post(
            url,
            json=payload,
            headers=self._get_headers()
        )
        response.raise_for_status()
        
        data = response.json()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
    
    async def _get_run(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get a specific run"""
        run_id = args["run_id"]
        
        url = f"{GLIF_API_BASE}/runs?id={run_id}"
        
        response = await self.http_client.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
    
    async def _list_runs(self, args: Dict[str, Any]) -> List[TextContent]:
        """List runs with filters"""
        params = {}
        
        if args.get("glif_id"):
            params["glifId"] = args["glif_id"]
        if args.get("username"):
            params["username"] = args["username"]
        if args.get("user_id"):
            params["userId"] = args["user_id"]
        if args.get("page", 1) > 1:
            params["page"] = args["page"]
        if args.get("limit", 20) != 20:
            params["limit"] = args["limit"]
        
        url = f"{GLIF_API_BASE}/runs"
        if params:
            url += "?" + urlencode(params)
        
        response = await self.http_client.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
    
    async def _get_user_info(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get user information"""
        params = {}
        
        if args.get("username"):
            params["username"] = args["username"]
        elif args.get("user_id"):
            params["id"] = args["user_id"]
        else:
            return [TextContent(type="text", text="Error: Either username or user_id required")]
        
        url = f"{GLIF_API_BASE}/user?" + urlencode(params)
        
        try:
            response = await self.http_client.get(url, headers=self._get_headers())
            response.raise_for_status()
            
            # Check if response has content
            if not response.content:
                return [TextContent(type="text", text="No user found with the provided information")]
            
            # Try to parse JSON
            try:
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]
            except json.JSONDecodeError:
                # If it's not JSON, return the raw text
                text_content = response.text.strip()
                if text_content:
                    return [TextContent(type="text", text=f"Raw response: {text_content}")]
                else:
                    return [TextContent(type="text", text="No user found with the provided information")]
                    
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return [TextContent(type="text", text="User not found")]
            else:
                return [TextContent(type="text", text=f"HTTP error: {e.response.status_code} - {e.response.text}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error fetching user info: {str(e)}")]
    
    async def _get_me(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get authenticated user information"""
        if not self.api_token:
            return [TextContent(type="text", text="Error: API token required")]
        
        url = f"{GLIF_API_BASE}/me"
        
        response = await self.http_client.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
    
    async def _list_spheres(self, args: Dict[str, Any]) -> List[TextContent]:
        """List spheres (collections)"""
        params = {}
        
        if args.get("slug"):
            params["slug"] = args["slug"]
        elif args.get("sphere_id"):
            params["id"] = args["sphere_id"]
        
        if args.get("include_graph"):
            params["includes"] = "spells.data"
        
        url = f"{GLIF_API_BASE}/spheres"
        if params:
            url += "?" + urlencode(params)
        
        response = await self.http_client.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
    
    async def _create_glif(self, args: Dict[str, Any]) -> List[TextContent]:
        """Create a new glif"""
        if not self.api_token:
            return [TextContent(type="text", text="Error: API token required for creating glifs")]
        
        # Validate graph.nodes
        if "graph" not in args or not isinstance(args["graph"], dict):
            return [TextContent(type="text", text="Error: graph must be an object")]
        if "nodes" not in args["graph"] or not isinstance(args["graph"]["nodes"], list):
            return [TextContent(type="text", text="Error: graph.nodes must be an array")]
        
        payload = {
            "name": args["name"],
            "description": args["description"],
            "graph": args["graph"]
        }
        
        if args.get("published_at"):
            payload["publishedAt"] = args["published_at"]
        
        url = f"{GLIF_API_BASE}/glifs"
        
        response = await self.http_client.post(
            url,
            json=payload,
            headers=self._get_headers()
        )
        response.raise_for_status()
        
        data = response.json()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]

async def main():
    """Main entry point"""
    # Check for API token
    api_token = os.getenv("GLIF_API_TOKEN")
    if not api_token:
        logger.warning("GLIF_API_TOKEN not found. Some features will be limited.")
    
    async with GlifMCPServer() as server:
        # Create notification_options to fix AttributeError
        notification_options = NotificationOptions()
        logger.info(f"Notification options: {notification_options.tools_changed}")
        
        # Run the server
        async with stdio_server() as (read_stream, write_stream):
            await server.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="glif-mcp",
                    server_version="1.0.0",
                    capabilities=server.server.get_capabilities(
                        notification_options=notification_options,
                        experimental_capabilities=None,
                    ),
                ),
            )

if __name__ == "__main__":
    asyncio.run(main())
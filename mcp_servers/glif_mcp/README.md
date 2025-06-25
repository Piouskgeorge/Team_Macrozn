# Glif.app MCP Server

A comprehensive Model Context Protocol (MCP) server that provides seamless integration with [Glif.app](https://glif.app), enabling AI models to interact with Glif workflows, users, and resources through natural language.

## Overview

This MCP server provides tools for:
- **Glif Management**: Create, fetch, and list glifs (workflows)
- **Execution**: Run glifs with various input types and configurations
- **User Management**: Get user information and profiles
- **Run Tracking**: Monitor and retrieve execution results
- **Sphere Management**: Access public collections and spheres
- **Conversational Interface**: Natural language interaction with Azure OpenAI

## Features

### 🤖 Conversational AI Integration
- **Azure OpenAI Powered**: Seamless integration with GPT-4 and other Azure OpenAI models
- **Natural Language Processing**: Convert user queries into appropriate tool calls
- **Context Awareness**: Maintain conversation history for better interactions
- **Automatic Tool Selection**: AI automatically chooses the right tools based on user intent

### 🔧 Glif.app API Tools
- **Glif Operations**: Create, fetch, and list glifs with full metadata
- **Execution Engine**: Run glifs with positional or named inputs
- **User Management**: Get detailed user profiles and information
- **Run Tracking**: Monitor execution status and retrieve results
- **Sphere Access**: Browse public collections and spheres

### 🛠️ Multiple Interface Options
- **Simple Interface**: Direct tool calling without subprocess management
- **Full Interface**: Complete conversational experience with subprocess handling
- **Client Library**: Programmatic access to all MCP tools
- **Testing Suite**: Comprehensive test scripts for all functionality

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Azure OpenAI Account** with API access
3. **Glif.app Account** (optional, for full functionality)

### Setup

1. **Clone or navigate to the directory**:
   ```bash
   cd glifmcp/glif_mcp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   # Required for Azure OpenAI
   export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
   export AZURE_OPENAI_API_KEY="your-azure-api-key"
   export AZURE_OPENAI_MODEL="gpt4o"  # or your preferred model
   
   # Optional: Glif.app API token for full functionality
   export GLIF_API_TOKEN="your_glif_api_token_here"
   ```

4. **Start the conversational interface**:
   ```bash
   python start_conversation.py
   ```

## Usage

### Starting the System

The system automatically tries the best interface for your environment:

```bash
python start_conversation.py
```

This will:
1. Try the simple interface first (recommended for Windows)
2. Fall back to the full interface if needed
3. Provide helpful error messages if dependencies are missing

### Available Tools

#### 1. `get_glif`
Fetch a specific glif by ID with optional graph data.

**Parameters:**
- `glif_id` (string, required): The ID of the glif to fetch
- `include_graph` (boolean, optional): Include full glif-graph JSON data

**Example:**
```json
{
  "name": "get_glif",
  "arguments": {
    "glif_id": "abc123",
    "include_graph": true
  }
}
```

#### 2. `list_glifs`
List glifs with various filtering options.

**Parameters:**
- `featured` (boolean, optional): Get featured glifs only
- `username` (string, optional): Filter by username
- `user_id` (string, optional): Filter by user ID
- `page` (integer, optional): Page number for pagination
- `limit` (integer, optional): Number of results per page (max 100)
- `include_graph` (boolean, optional): Include full glif-graph JSON data

**Example:**
```json
{
  "name": "list_glifs",
  "arguments": {
    "featured": true,
    "limit": 10,
    "include_graph": false
  }
}
```

#### 3. `run_glif`
Execute a glif using the Simple API.

**Parameters:**
- `glif_id` (string, required): The ID of the glif to run
- `inputs` (array/object, optional): Inputs for the glif
- `visibility` (string, optional): "PUBLIC" or "PRIVATE"
- `strict` (boolean, optional): Enable strict mode

**Example:**
```json
{
  "name": "run_glif",
  "arguments": {
    "glif_id": "xyz789",
    "inputs": ["hello", "world"],
    "visibility": "PRIVATE",
    "strict": false
  }
}
```

#### 4. `get_run`
Fetch details of a specific run.

**Parameters:**
- `run_id` (string, required): The ID of the run to fetch

**Example:**
```json
{
  "name": "get_run",
  "arguments": {
    "run_id": "run_abc123"
  }
}
```

#### 5. `list_runs`
List runs with optional filters.

**Parameters:**
- `glif_id` (string, optional): Filter by glif ID
- `username` (string, optional): Filter by username
- `user_id` (string, optional): Filter by user ID
- `page` (integer, optional): Page number for pagination
- `limit` (integer, optional): Number of results per page

**Example:**
```json
{
  "name": "list_runs",
  "arguments": {
    "glif_id": "xyz789",
    "limit": 20
  }
}
```

#### 6. `get_user_info`
Get information about a specific user.

**Parameters:**
- `username` (string, required): The username to look up

**Example:**
```json
{
  "name": "get_user_info",
  "arguments": {
    "username": "john_doe"
  }
}
```

#### 7. `get_me`
Get information about the authenticated user (requires API token).

**Example:**
```json
{
  "name": "get_me",
  "arguments": {}
}
```

#### 8. `list_spheres`
List all public spheres (collections).

**Example:**
```json
{
  "name": "list_spheres",
  "arguments": {}
}
```

#### 9. `create_glif`
Create a new glif (requires API token).

**Parameters:**
- `name` (string, required): Name of the glif
- `description` (string, optional): Description of the glif
- `graph` (object, required): Glif graph definition
- `visibility` (string, optional): "PUBLIC" or "PRIVATE"

**Example:**
```json
{
  "name": "create_glif",
  "arguments": {
    "name": "My New Glif",
    "description": "A test glif",
    "graph": {...},
    "visibility": "PRIVATE"
  }
}
```

## Architecture

### Core Components

1. **`glif_mcp_server.py`**: Main MCP server with all Glif.app API tools
2. **`start_conversation.py`**: Smart startup script that chooses the best interface
3. **`simple_conversation.py`**: Direct tool calling interface (recommended)
4. **`conversational_interface.py`**: Full conversational interface with subprocess management
5. **`glif_mcp_client.py`**: Client library for programmatic access

### Interface Options

#### Simple Interface (Recommended)
- **File**: `simple_conversation.py`
- **Pros**: Faster, more reliable, better Windows compatibility
- **Use Case**: Direct tool calling without subprocess overhead

#### Full Interface
- **File**: `conversational_interface.py`
- **Pros**: Complete conversational experience
- **Use Case**: When you need full subprocess management

### Data Flow

```
User Input → Azure OpenAI → Tool Selection → MCP Server → Glif.app API → Response
```

1. User sends a natural language query
2. Azure OpenAI analyzes the query and determines required tools
3. MCP server calls the appropriate Glif.app API endpoints
4. Results are processed and returned in a conversational format

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Yes | - |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes | - |
| `AZURE_OPENAI_MODEL` | Model name to use | No | `gpt4o` |
| `GLIF_API_TOKEN` | Glif.app API token | No | - |

### API Endpoints

The server connects to:
- **Glif API**: `https://glif.app/api`
- **Simple API**: `https://simple-api.glif.app`

## Examples

### Natural Language Queries

**User:** "Show me some featured glifs"
- AI calls: `list_glifs` with `featured: true`

**User:** "Get information about glif with ID abc123"
- AI calls: `get_glif` with `glif_id: "abc123"`

**User:** "Run the glif with ID xyz789 with inputs ['hello', 'world']"
- AI calls: `run_glif` with the specified parameters

**User:** "Who is user john_doe?"
- AI calls: `get_user_info` with `username: "john_doe"`

**User:** "What's my profile information?"
- AI calls: `get_me` (requires API token)

### Programmatic Usage

```python
from glif_mcp_client import GlifMCPClient

async with GlifMCPClient() as client:
    # List featured glifs
    glifs = await client.list_glifs(featured=True, limit=5)
    
    # Run a glif
    result = await client.run_glif(
        glif_id="xyz789",
        inputs=["hello", "world"]
    )
    
    # Get user info
    user = await client.get_user_info(username="john_doe")
```

## Testing

The system includes comprehensive test scripts:

- **`test_conversation.py`**: Test the conversational interface
- **`test_glif_run.py`**: Test glif execution functionality
- **`test_user_lookup.py`**: Test user information retrieval
- **`test_user_profile.py`**: Test authenticated user profile access

Run tests with:
```bash
python test_conversation.py
python test_glif_run.py
python test_user_lookup.py
python test_user_profile.py
```

## Error Handling

The system includes robust error handling:

- **API Errors**: Graceful handling of Glif.app API errors
- **Authentication**: Clear messages for missing API tokens
- **Network Issues**: Connection error recovery
- **Invalid Inputs**: Input validation and helpful error messages
- **Rate Limiting**: Automatic handling of API rate limits

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Azure OpenAI Configuration**
   - Verify `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY`
   - Check model availability in your Azure deployment

3. **Glif.app API Issues**
   - Verify `GLIF_API_TOKEN` is set correctly
   - Check API token permissions

4. **Windows Path Issues**
   - The system automatically tries the simple interface first
   - If issues persist, check Python path configuration

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

- **API Key Protection**: Never expose API keys in logs or responses
- **Token Management**: Use environment variables for sensitive data
- **Input Validation**: All inputs are validated before API calls
- **Error Sanitization**: Error messages don't expose sensitive information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- **Glif.app Documentation**: [docs.glif.app](https://docs.glif.app)
- **Glif.app Website**: [glif.app](https://glif.app)
- **Azure OpenAI**: [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- **MCP Protocol**: [Model Context Protocol](https://modelcontextprotocol.io/)

## Related Projects

- [Glif.app](https://glif.app): Visual AI workflow builder
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service): Azure OpenAI Service
- [MCP](https://modelcontextprotocol.io/): Model Context Protocol
- [httpx](https://www.python-httpx.org/): Modern HTTP client for Python 
# Hunter.io MCP Server

This is a Model Context Protocol (MCP) server that integrates with Hunter.io API to provide comprehensive email finding and verification capabilities through Azure OpenAI.

## Features

- **Domain Search**: Find all email addresses associated with a domain
- **Email Finder**: Find a professional email address using full name and domain
- **Email Verifier**: Verify if an email address is valid and deliverable
- **Lead Finder**: Find leads based on company domain and various criteria
- **Email Count**: Get the number of email addresses available for a domain
- **Account Information**: Get information about your Hunter.io account and usage
- **Email Sources**: Find sources where an email address was found on the web

## Quick Start

### 1. Automated Setup

Run the setup script to automatically install dependencies and configure the environment:

```bash
python setup.py
```

The setup script will:
- Install all required dependencies
- Create a `.env` file from the template
- Validate your configuration
- Test the Hunter.io API connection

### 2. Manual Setup

If you prefer manual setup:

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Copy the `env_template.txt` file to `.env` and fill in your API keys:

```bash
cp env_template.txt .env
```

Edit the `.env` file with your actual API keys:

```env
# Hunter.io API Key (get from https://hunter.io/api-keys)
HUNTER_API_KEY=your_hunter_api_key_here

# Azure OpenAI Configuration
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
API_KEY=your_azure_api_key_here
MODEL=your_model_deployment_name
```

### 3. Get Your API Keys

- **Hunter.io API Key**: Sign up at [Hunter.io](https://hunter.io) and get your API key from the dashboard
- **Azure OpenAI**: Set up Azure OpenAI service and get your endpoint, API key, and model deployment name

## Running the Server

### Option 1: Direct Python execution
```bash
python server.py
```

### Option 2: Using uvicorn
```bash
uvicorn server:app --host 0.0.0.0 --port 8888
```

The server will start on `http://localhost:8888`

## Testing

Run the comprehensive test suite to verify all tools are working:

```bash
python test_hunter_tools.py
```

The test suite will:
- Check if the server is running
- Test all Hunter.io tools with various scenarios
- Compare results with direct API calls
- Display detailed results and any errors

## Available Tools

### 1. Domain Search
Find all email addresses associated with a domain.

**Tool Name**: `hunter_domain_search`

**Parameters**:
- `domain` (string): The domain to search (e.g., "example.com")

**Example Usage**:
```
Search for all emails at microsoft.com
```

### 2. Email Finder
Find a professional email address using full name and domain.

**Tool Name**: `hunter_email_finder`

**Parameters**:
- `full_name` (string): The full name of the person (e.g., "John Doe")
- `domain` (string): The domain to search (e.g., "example.com")

**Example Usage**:
```
Find the email for John Smith at microsoft.com
```

### 3. Email Verifier
Verify if an email address is valid and deliverable.

**Tool Name**: `hunter_email_verifier`

**Parameters**:
- `email` (string): The email address to verify (e.g., "john@example.com")

**Example Usage**:
```
Verify if john.doe@microsoft.com is a valid email
```

### 4. Lead Finder
Find leads based on company domain and various criteria.

**Tool Name**: `hunter_lead_finder`

**Parameters**:
- `domain` (string): The company domain (e.g., "example.com")
- `first_name` (string, optional): First name filter
- `last_name` (string, optional): Last name filter
- `seniority` (string, optional): Seniority level (e.g., "senior", "junior", "executive")
- `department` (string, optional): Department (e.g., "engineering", "sales", "marketing")

**Example Usage**:
```
Find engineering leads at microsoft.com
Find senior executives at google.com
```

### 5. Email Count
Get the number of email addresses available for a domain.

**Tool Name**: `hunter_email_count`

**Parameters**:
- `domain` (string): The domain to check (e.g., "example.com")

**Example Usage**:
```
Get email count for microsoft.com
```

### 6. Account Information
Get information about your Hunter.io account and usage.

**Tool Name**: `hunter_account_info`

**Parameters**: None

**Example Usage**:
```
Get my Hunter.io account information
```

### 7. Email Sources
Find sources where an email address was found on the web.

**Tool Name**: `hunter_email_sources`

**Parameters**:
- `email` (string): The email address to search for sources (e.g., "john@example.com")

**Example Usage**:
```
Find sources for bill.gates@microsoft.com
```

## Integration with MCP Clients

This server can be used with any MCP-compatible client. The server exposes the Hunter.io API functionality through a standardized interface that can be consumed by AI assistants and other applications.

## Error Handling

The server includes comprehensive error handling for:
- Invalid API keys
- Rate limiting
- Network errors
- Invalid requests

All errors are returned in a structured format with descriptive messages.

## Rate Limits

Hunter.io has rate limits based on your plan:
- Free: 25 searches per month
- Paid plans: Higher limits

The server will return appropriate error messages when rate limits are exceeded.

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- The server validates all required environment variables on startup

## Troubleshooting

### Common Issues

1. **Server not starting**: Check that all environment variables are set correctly
2. **API errors**: Verify your Hunter.io API key is valid and has sufficient credits
3. **Rate limiting**: Wait before making additional requests or upgrade your Hunter.io plan
4. **Network errors**: Check your internet connection and firewall settings

### Debug Mode

To enable debug logging, set the `DEBUG` environment variable:

```env
DEBUG=true
```

## Contributing

Feel free to submit issues and enhancement requests! 
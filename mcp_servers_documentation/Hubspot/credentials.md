# HubSpot MCP Server Credentials

## Overview
This document provides instructions on structuring the credentials needed to connect the HubSpot MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "HUBSPOT": {
    "access_token": "pat-na2-090aa37b-a868-47ff-a223-0af893d7f26f"
  },
  "AZURE_OPENAI": {
    "endpoint": "https://your-endpoint.openai.azure.com/",
    "api_key": "your-azure-api-key",
    "model": "gpt-4o"
  }
}
```

- `access_token`: Your HubSpot private app access token (required)
- `endpoint`, `api_key`, `model`: Your Azure OpenAI deployment details (required)

## Environment Variables
- `HUBSPOT_ACCESS_TOKEN`
- `AZURE_ENDPOINT`
- `AZURE_API_KEY`
- `AZURE_MODEL` 

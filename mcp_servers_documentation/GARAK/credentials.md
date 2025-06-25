# Garak MCP Server Credentials

## Overview
This document provides instructions on structuring the credentials needed to connect the Garak MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "AZURE_OPENAI": {
    "endpoint": "https://your-endpoint.openai.azure.com/",
    "api_key": "your-azure-api-key",
    "model_name": "gpt4o",
    "api_version": "2024-06-01"
  }
}
```

- `endpoint`, `api_key`, `model_name`, `api_version`: Your Azure OpenAI deployment details (required)

## Environment Variables
- `AZURE_ENDPOINT`
- `AZURE_API_KEY`
- `AZURE_MODEL_NAME`
- `AZURE_API_VERSION`

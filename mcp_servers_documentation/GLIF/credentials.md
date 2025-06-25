# Glif MCP Server Credentials

## Overview
This document provides instructions on structuring the credentials needed to connect the Glif MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "GLIF": {
    "api_token":"glif_1494c103cb6c6cf58fb7a7bf9e6e899fe27c6cd162b528442501eed9c49af929"
  },
  "AZURE_OPENAI": {
    "endpoint": "https://your-endpoint.openai.azure.com/",
    "api_key": "your-azure-api-key",
    "model": "gpt4o"
  }
}
```

- `api_token`: Your Glif.app API token (optional, for full functionality)
- `endpoint`, `api_key`, `model`: Your Azure OpenAI deployment details (required)

## Environment Variables
- `GLIF_API_TOKEN`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_MODEL` 
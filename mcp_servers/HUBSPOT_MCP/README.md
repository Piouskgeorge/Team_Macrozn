# HubSpot MCP Server (Python)

## Overview

The HubSpot MCP Server is a modular backend component that integrates HubSpot CRM with the MCP platform. It provides endpoints and business logic for managing HubSpot contacts, deals, and carts, and can be extended to support more features.

## Directory Structure

```
servers/HUBSPOT_MCP/
├── config.py                # Server configuration (API keys, endpoints, etc.)
├── main.py                  # Entry point for the server
├── handlers/
│   ├── __init__.py
│   └── tool_handler.py      # Handles incoming tool/API requests
├── services/
│   ├── __init__.py
│   ├── azure_openai.py      # Azure OpenAI integration
│   ├── hubspot_carts.py     # HubSpot carts business logic
│   ├── hubspot_contacts.py  # HubSpot contacts business logic
│   └── hubspot_deals.py     # HubSpot deals business logic
├── utils/
│   ├── __init__.py
│   └── cart_manager.py      # Utility functions for cart management
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignore rules for this server
├── LICENSE                  # License file
└── README.md                # This documentation
```

## How It Works

- **Configuration**: The server loads API keys and settings from environment variables or `.env` files.
- **Request Handling**: Incoming requests are routed to handlers in the `handlers/` directory.
- **Business Logic**: Handlers call service modules in `services/` to interact with HubSpot APIs and perform operations.
- **Utilities**: Helper functions in `utils/` support the main logic.
- **Security**: Secrets and API keys are stored in `.env` files and are not committed to version control.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Create a `.env` file in this directory with your HubSpot and Azure OpenAI credentials.

3. **Run the server:**
   ```bash
   python -m servers.HUBSPOT_MCP.main
   ```

## Key Files

- `main.py`: Starts the server and handles the main loop.
- `config.py`: Loads and validates configuration.
- `handlers/tool_handler.py`: Main entry point for processing tool/API calls.
- `services/`: Contains all business logic for interacting with HubSpot and Azure OpenAI.

## Adding New Features

- Add new business logic in the `services/` directory.
- Add new request handlers in the `handlers/` directory.
- Update `main.py` and `config.py` as needed.

## Security

- **Never commit secrets or API keys.** Always use `.env` files and add them to `.gitignore`.

## License

This project is licensed under the MIT License.

MCP Servers Collection
A comprehensive collection of Model Context Protocol (MCP) servers designed for seamless integration between AI assistants and various external services and APIs. This repository contains Python-based MCP servers for multiple platforms, enabling natural language interaction with standardized interfaces.
🚀 Overview
The MCP Servers Collection facilitates interaction between AI models and external services through a unified protocol. Each server is implemented in Python and supports natural language commands for streamlined automation and data processing.
Included Servers

Apify: Web scraping and automation platform
Garak: LLM vulnerability scanning and safety evaluation
Glif.app: Workflow automation and execution platform
HubSpot: CRM and marketing automation platform

📋 Table of Contents

Features
Available Servers
Quick Start
Server Details
Usage Examples
Common Setup
Troubleshooting
Contributing
License
Additional Resources

✨ Features

Standardized Interface: Consistent API for AI model interactions across services
Natural Language Processing: Leverage Azure OpenAI for intuitive command handling
Modular Architecture: Easily extensible for new services and platforms
Comprehensive Documentation: Detailed guides and examples for each server
Error Handling: Robust error management and recovery mechanisms
Community-Driven: Open for contributions to add new servers or enhance existing ones

🔌 Available Servers



Server
Description
Status
Language



Apify
Web scraping, Instagram scraping, and automation tools
✅ Active
Python


Garak
LLM vulnerability scanning and safety evaluation
✅ Active
Python


Glif.app
Workflow automation and execution platform
✅ Active
Python


HubSpot
CRM, contacts, deals, and marketing automation
✅ Active
Python


🚀 Quick Start
Prerequisites

Python 3.8+
pip package manager
Azure OpenAI Account (required for most servers)
Service-specific API keys (refer to individual server documentation)

Installation Steps

Clone the repository:
git clone https://github.com/Piouskgeorge/Team_Macrozn.git
cd mcp-servers-collection


Navigate to the server directory:
cd mcp_servers/[server_name]


Install dependencies:
pip install -r requirements.txt


Configure environment variables:
# Common variables (check individual READMEs for specifics)
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_MODEL="gpt4o"


Start the server:
python server.py
# or
python main.py



📖 Server Details
🔧 Apify MCP Server
Purpose: Integrates with Apify for web scraping, Instagram data extraction, and automation.
Key Features:

Instagram profile and post scraping
Web scraping with Cheerio and Web Scraper actors
Dataset and key-value store management
Actor and task execution
Enhanced logging and error handling

Tools Available:

run_actor: Execute Apify actors
run_task: Execute Apify tasks
get_datasets: Retrieve datasets
get_key_value_stores: Manage key-value stores
list_available_actors: Browse available actors

Setup:
cd apify
pip install -r requirements.txt
export APIFY_API_KEY="your_apify_api_key_here"
python start_conversation.py

🛡️ Garak MCP Server
Purpose: Facilitates LLM vulnerability scanning and safety evaluation using the Garak framework.
Key Features:

AI research assistant with safety checks
Comprehensive vulnerability assessments
Support for multiple probes (e.g., prompt injection, jailbreaks)
Azure OpenAI integration
Conversation history management

Tools Available:

ask_research_agent: Query the AI research assistant
run_safety_evaluation: Perform Garak safety evaluations
get_agent_history: Retrieve conversation history
reset_agent: Clear conversation history
update_agent_role: Modify agent role/system prompt

Setup:
cd garak_mcp
pip install -r requirements.txt
pip install garak
export AZURE_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_API_KEY="your-api-key"
export AZURE_MODEL_NAME="gpt4o"
python server.py

🔄 Glif.app MCP Server
Purpose: Enables workflow automation and execution through Glif.app.
Key Features:

Workflow creation and management
Execution with diverse input types
User management and profile access
Run tracking and result monitoring
Sphere and collection browsing

Tools Available:

get_glif: Fetch specific glif by ID
list_glifs: List glifs with filtering options
run_glif: Execute glif workflows
get_run: Retrieve run details
list_runs: List runs with filters
get_user_info: Access user information

Setup:
cd glif_mcp
pip install -r requirements.txt
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_MODEL="gpt4o"
export GLIF_API_TOKEN="your_glif_api_token_here"
python start_conversation.py

📊 HubSpot MCP Server
Purpose: Integrates with HubSpot for CRM, contacts, deals, and marketing automation.
Key Features:

Contact creation and management
Deal tracking and updates
Cart management for e-commerce
Azure OpenAI-powered natural language processing
Modular design for extensibility

Tools Available:

Contact creation and management
Deal tracking and updates
Cart operations
User information retrieval

Setup:
cd HUBSPOT_MCP
pip install -r requirements.txt
# Create .env file with HubSpot and Azure OpenAI credentials
python -m servers.HUBSPOT_MCP.main

💡 Usage Examples
Apify - Instagram Scraping
# Scrape Instagram profile
"Scrape the Instagram profile of 'nike'"

# Get posts with hashtag
"Get posts with hashtag 'travel', limit to 5"

# Web scraping
"Scrape the first paragraph from https://example.com"

Garak - Safety Evaluation
# Ask research question
"What are the latest developments in AI safety?"

# Run safety evaluation
"Run Garak safety evaluation on GPT-4 with prompt injection probes"

# Update agent role
"Update the agent to be a cybersecurity expert"

Glif.app - Workflow Management
# List featured glifs
"Show me featured glifs"

# Run a glif
"Run glif abc123 with inputs ['hello', 'world']"

# Get user information
"Get information about user 'john_doe'"

HubSpot - CRM Operations
# Create contact
"Create a new contact for John Doe with email john@example.com"

# Update deal
"Update deal status to 'Closed Won'"

# Get contact information
"Get contact details for john@example.com"

🔧 Common Setup
Environment Variables
Most servers require these environment variables:
# Azure OpenAI (required for most servers)
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_MODEL="gpt4o"

# Service-specific API keys
export APIFY_API_KEY="your_apify_api_key_here"
export GLIF_API_TOKEN="your_glif_api_token_here"
export HUBSPOT_API_KEY="your_hubspot_api_key_here"

Directory Structure
Each server follows a consistent structure:
[server_name]/
├── server/              # Server implementation
├── client/              # Client implementation
├── requirements.txt     # Python dependencies
├── README.md           # Detailed documentation
└── [config files]      # Configuration files

🛠️ Troubleshooting
Common Issues

Import Errors:
pip install -r requirements.txt


API Key Issues:

Verify environment variables are correctly set
Check API key permissions and quotas
Ensure API keys are not expired


Azure OpenAI Connection:

Confirm endpoint URL accuracy
Verify API key permissions
Ensure model name is available in your deployment


Service-specific Issues:

Consult individual server README files
Review service API documentation
Verify account permissions and quotas



Getting Help

Check individual server README files for detailed guidance
Explore the mcp_servers_documentation/ directory for comprehensive guides
Use provided Postman collections in postman_api_collections/ for API testing

🤝 Contributing
We welcome contributions to enhance existing servers or add new ones!
Adding New Servers

Create a new directory in mcp_servers/

Follow the standard structure:
[new_server]/
├── server/
├── client/
├── requirements.txt
├── README.md
└── [config files]


Update this main README with server details

Add documentation to mcp_servers_documentation/

Create a Postman collection in postman_api_collections/


Development Guidelines

Adhere to Python PEP 8 style guidelines
Implement comprehensive error handling
Provide clear, concise documentation
Include example usage and testing scripts
Maintain consistent code formatting

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
📚 Additional Resources

Main Project README: Overview of the project
MCP Servers Documentation: Detailed server guides
Postman Collections: API testing collections
Model Context Protocol: Official MCP documentation
Issue Tracker: Report bugs or suggest features

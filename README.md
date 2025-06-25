# 🚀 MCP Servers Collection

A comprehensive collection of **Model Context Protocol (MCP)** servers designed to seamlessly integrate AI assistants with external services and APIs. This repository contains Python-based MCP servers for various platforms, enabling **natural language interaction** with standardized interfaces.

---

## 📋 Table of Contents

- [✨ Features](#-features)  
- [🔌 Available Servers](#-available-servers)  
- [🚀 Quick Start](#-quick-start)  
- [📖 Server Details](#-server-details)  
- [💡 Usage Examples](#-usage-examples)  
- [🔧 Common Setup](#-common-setup)  
- [🛠️ Troubleshooting](#️-troubleshooting)  
- [🤝 Contributing](#-contributing)  
- [📜 License](#-license)  
- [📚 Additional Resources](#-additional-resources)  

---

## ✨ Features

- **Standardized Interface** – Consistent API format across all services  
- **Natural Language Support** – Azure OpenAI-powered command processing  
- **Modular Architecture** – Add new services with minimal changes  
- **Comprehensive Docs** – Step-by-step instructions and examples  
- **Robust Error Handling** – Recovery from common runtime issues  
- **Community-Driven** – Open to contributions and server extensions  

---

## 🔌 Available Servers

| Server     | Description                                   | Status | Language |
|------------|-----------------------------------------------|--------|----------|
| Apify      | Web scraping and Instagram automation         | ✅ Active | Python   |
| Garak      | LLM vulnerability scanning and safety eval.   | ✅ Active | Python   |
| Glif.app   | Workflow automation and execution             | ✅ Active | Python   |
| HubSpot    | CRM, deals, contacts, marketing automation    | ✅ Active | Python   |

---

## 🚀 Quick Start

### 🔧 Prerequisites

- Python 3.8+  
- `pip` package manager  
- Azure OpenAI Account  
- Service-specific API keys  

### 📦 Installation Steps

\`\`\`bash
# Clone the repository
git clone https://github.com/Piouskgeorge/Team_Macrozn.git
cd mcp-servers-collection

# Navigate to desired server directory
cd mcp_servers/[server_name]

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_MODEL="gpt4o"

# Start the server
python server.py
# or
python main.py
\`\`\`

---

## 📖 Server Details

### 🔧 Apify MCP Server

- **Purpose**: Web & Instagram scraping, automation  
- **Key Tools**:  
  - \`run_actor\`, \`run_task\`  
  - \`get_datasets\`, \`get_key_value_stores\`  
  - \`list_available_actors\`  

\`\`\`bash
cd apify
pip install -r requirements.txt
export APIFY_API_KEY="your_apify_api_key_here"
python start_conversation.py
\`\`\`

---

### 🛡️ Garak MCP Server

- **Purpose**: LLM safety evaluations and vulnerability scanning  
- **Key Tools**:  
  - \`ask_research_agent\`, \`run_safety_evaluation\`  
  - \`get_agent_history\`, \`reset_agent\`, \`update_agent_role\`  

\`\`\`bash
cd garak_mcp
pip install -r requirements.txt
pip install garak
export AZURE_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_API_KEY="your-api-key"
export AZURE_MODEL_NAME="gpt4o"
python server.py
\`\`\`

---

### 🔄 Glif.app MCP Server

- **Purpose**: Workflow automation through Glif.app  
- **Key Tools**:  
  - \`get_glif\`, \`list_glifs\`, \`run_glif\`  
  - \`get_run\`, \`list_runs\`, \`get_user_info\`  

\`\`\`bash
cd glif_mcp
pip install -r requirements.txt
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_MODEL="gpt4o"
export GLIF_API_TOKEN="your_glif_api_token_here"
python start_conversation.py
\`\`\`

---

### 📊 HubSpot MCP Server

- **Purpose**: CRM operations like contacts, deals, and cart management  
- **Key Tools**:  
  - \`create_contact\`, \`update_deal\`, \`cart_operations\`  

\`\`\`bash
cd HUBSPOT_MCP
pip install -r requirements.txt
# Add environment variables in a \`.env\` file
python -m servers.HUBSPOT_MCP.main
\`\`\`

---

## 💡 Usage Examples

### 🕸️ Apify

- "Scrape the Instagram profile of 'nike'"  
- "Get posts with hashtag 'travel', limit to 5"  
- "Scrape the first paragraph from https://example.com"  

### 🧪 Garak

- "What are the latest developments in AI safety?"  
- "Run Garak safety evaluation on GPT-4 with prompt injection probes"  
- "Update the agent to be a cybersecurity expert"  

### ⚙️ Glif.app

- "Show me featured glifs"  
- "Run glif abc123 with inputs ['hello', 'world']"  
- "Get information about user 'john_doe'"  

### 📇 HubSpot

- "Create a new contact for John Doe with email john@example.com"  
- "Update deal status to 'Closed Won'"  
- "Get contact details for john@example.com"  

---

## 🔧 Common Setup

### 🌍 Environment Variables

\`\`\`bash
# Azure OpenAI (Required for all)
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_MODEL="gpt4o"

# Service-specific
export APIFY_API_KEY="your_apify_api_key_here"
export GLIF_API_TOKEN="your_glif_api_token_here"
export HUBSPOT_API_KEY="your_hubspot_api_key_here"
\`\`\`

### 🗂 Directory Structure

\`\`\`
[server_name]/
├── server/              # Server logic
├── client/              # Client logic (optional)
├── requirements.txt     # Dependencies
├── README.md            # Server-specific docs
└── [config files]       # Configuration
\`\`\`

---

## 🛠️ Troubleshooting

### Common Issues & Fixes

- **Import Errors**  
  \`pip install -r requirements.txt\`

- **API Key Errors**  
  - Ensure all API keys are set and valid  
  - Check key quotas and scopes  

- **Azure OpenAI Errors**  
  - Verify endpoint and model deployment  
  - Check permissions  

- **Server-Specific Issues**  
  - See individual README files  
  - Refer to official API docs  

---

## 🤝 Contributing

We welcome your contributions!

### Add a New Server

1. Create a new folder in \`mcp_servers/\`:
   \`\`\`
   mcp_servers/
   └── your_new_server/
       ├── server/
       ├── client/
       ├── requirements.txt
       ├── README.md
       └── config/
   \`\`\`

2. Update the main README and add:
   - Documentation in \`mcp_servers_documentation/\`  
   - Postman collection in \`postman_api_collections/\`  

### Dev Guidelines

- Follow PEP 8  
- Use meaningful error messages  
- Add usage examples  
- Keep consistent structure  

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for more details.

---

## 📚 Additional Resources

- **Main Project README** – Overview of the repository  
- **MCP Servers Documentation** – Detailed per-server docs  
- **Postman Collections** – Ready-made API test scripts  
- **Model Context Protocol Docs** – Official specifications  

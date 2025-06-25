import requests
import re
import json
from ..config import Config

class AzureOpenAIService:
    """Service class for Azure OpenAI operations"""
    
    def __init__(self):
        self.endpoint = Config.AZURE_ENDPOINT
        self.api_key = Config.AZURE_API_KEY
        self.model = Config.AZURE_MODEL
        self.api_version = Config.AZURE_API_VERSION
    
    def ask_gpt_tool_selection(self, user_input, history):
        """
        Ask GPT to decide which tool to use and with what parameters, or to just answer as a chatbot.
        Returns a dict: {"tool": <tool_name or None>, "parameters": {...}, "answer": <optional>}
        """
        tool_prompt = (
            "You are an assistant for HubSpot MCP. "
            "You have access to these tools: "
            "1. list_contacts(limit) - List HubSpot contacts. "
            "2. create_contact(firstname, lastname, email) - Create a new contact. "
            "3. get_contact(email) - Get a contact by email. "
            "4. list_deals(limit) - List HubSpot deals/contracts. "
            "5. create_cart(name, status) - Create a new cart in HubSpot. "
            "6. list_carts(limit) - List all carts from HubSpot. "
            "If the user wants to perform one of these actions, respond ONLY in this JSON format: "
            "{\"tool\": <tool_name>, \"parameters\": {<params>} } "
            "For example: {\"tool\": \"create_cart\", \"parameters\": {\"name\": \"naveen@example.com\", \"status\": \"new\"}} "
            "If the user just wants to chat, respond with: {\"tool\": null, \"answer\": <your answer>} "
            "User: " + user_input
        )
        
        url = f"{self.endpoint}openai/deployments/{self.model}/chat/completions?api-version={self.api_version}"
        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        messages = history + [{"role": "user", "content": tool_prompt}]
        data = {
            "messages": messages,
            "max_tokens": 256
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        
        # Remove code block markers if present
        content = re.sub(r'^```[a-zA-Z]*\n|```$', '', content.strip(), flags=re.MULTILINE).strip()
        
        # Try to parse the JSON from GPT
        try:
            result = json.loads(content)
        except Exception:
            result = {"tool": None, "answer": content}
        
        return result 
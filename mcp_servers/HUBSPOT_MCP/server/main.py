import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .config import Config
from .services.azure_openai import AzureOpenAIService
from .handlers.tool_handler import ToolHandler

def main():
    """Main chatbot loop"""
    try:
        # Validate configuration
        Config.validate_config()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
        return
    
    print("Welcome to the HubSpot MCP Chatbot! Type 'exit' to quit.")
    
    # Initialize services
    openai_service = AzureOpenAIService()
    tool_handler = ToolHandler()
    
    # Initialize conversation history
    history = [{"role": "system", "content": "You are a helpful assistant for HubSpot CRM and Azure OpenAI."}]
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ("exit", "quit"): 
                print("Goodbye!")
                break
            
            # Ask GPT which tool to use
            try:
                tool_decision = openai_service.ask_gpt_tool_selection(user_input, history)
            except Exception as e:
                print(f"Error from GPT or API: {e}")
                continue
            
            tool = tool_decision.get("tool")
            
            if tool is None:
                # Just chat
                answer = tool_decision.get("answer", "Sorry, I didn't understand.")
                print("Bot:", answer)
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": answer})
                continue
            
            # Tool call
            params = tool_decision.get("parameters", {})
            result = tool_handler.handle_tool_call(tool, params)
            print(result)
            
            # Add to history
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": str(tool_decision)})
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

if __name__ == "__main__":
    main() 
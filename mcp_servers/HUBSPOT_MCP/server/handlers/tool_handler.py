from ..services.hubspot_contacts import HubSpotContactsService
from ..services.hubspot_deals import HubSpotDealsService
from ..services.hubspot_carts import HubSpotCartsService
from ..utils.cart_manager import CartManager

class ToolHandler:
    """Handler class for processing tool calls and executing actions"""
    
    def __init__(self):
        self.contacts_service = HubSpotContactsService()
        self.deals_service = HubSpotDealsService()
        self.carts_service = HubSpotCartsService()
        self.cart_manager = CartManager()
    
    def handle_tool_call(self, tool, params):
        """Handle tool calls and execute the appropriate action"""
        try:
            if tool == "list_contacts":
                return self._handle_list_contacts(params)
            elif tool == "create_contact":
                return self._handle_create_contact(params)
            elif tool == "get_contact":
                return self._handle_get_contact(params)
            elif tool == "list_deals":
                return self._handle_list_deals(params)
            elif tool == "create_cart":
                return self._handle_create_cart(params)
            elif tool == "list_carts":
                return self._handle_list_carts(params)
            else:
                return "Bot: Sorry, I don't know how to do that yet."
        except Exception as e:
            return f"Bot: Error executing tool: {e}"
    
    def _handle_list_contacts(self, params):
        """Handle listing contacts"""
        limit = params.get("limit", 5)
        if isinstance(limit, str) and limit.lower() == "all":
            limit = 100
        try:
            limit = int(limit)
        except Exception:
            limit = 5
        
        contacts = self.contacts_service.list_contacts(limit=limit)
        if not contacts:
            return "Bot: No contacts found."
        else:
            result = "Bot: Contacts:\n"
            for c in contacts:
                props = c['properties']
                result += f"- {props.get('firstname', '')} {props.get('lastname', '')} <{props.get('email', '')}>\n"
            return result
    
    def _handle_create_contact(self, params):
        """Handle creating a contact"""
        result = self.contacts_service.create_contact(
            params.get("firstname", ""),
            params.get("lastname", ""),
            params.get("email", "")
        )
        return f"Bot: Contact created with ID {result['id']}"
    
    def _handle_get_contact(self, params):
        """Handle getting a contact by email"""
        contact = self.contacts_service.get_contact_by_email(params.get("email", ""))
        if contact:
            props = contact['properties']
            return f"Bot: Contact: {props.get('firstname', '')} {props.get('lastname', '')} <{props.get('email', '')}>"
        else:
            return "Bot: Contact not found."
    
    def _handle_list_deals(self, params):
        """Handle listing deals"""
        limit = params.get("limit", 5)
        if isinstance(limit, str) and limit.lower() == "all":
            limit = 100
        try:
            limit = int(limit)
        except Exception:
            limit = 5
        
        try:
            deals = self.deals_service.list_deals(limit=limit)
            if not deals:
                return "Bot: No deals/contracts found."
            else:
                result = "Bot: Deals/Contracts:\n"
                for d in deals:
                    props = d['properties']
                    result += f"- {props.get('dealname', 'Unnamed Deal')}\n"
                return result
        except Exception as e:
            return f"Bot: Error fetching deals: {e}"
    
    def _handle_create_cart(self, params):
        """Handle creating a cart"""
        name = params.get("user_email", "") or params.get("name", "")
        status = params.get("status", "active")
        try:
            result = self.carts_service.create_cart(name, status)
            return f"Bot: Cart created with ID {result['id']} for {name}."
        except Exception:
            return "Bot: Error creating cart."
    
    def _handle_list_carts(self, params):
        """Handle listing carts from HubSpot"""
        limit = params.get("limit", 5)
        try:
            limit = int(limit)
        except Exception:
            limit = 5
        
        try:
            carts = self.carts_service.list_carts(limit=limit)
            if not carts:
                return "Bot: No carts found."
            else:
                result = "Bot: Carts:\n"
                for c in carts:
                    props = c['properties']
                    result += f"- Cart ID: {c['id']}, Name: {props.get('name', '')}, Status: {props.get('status', '')}\n"
                return result
        except Exception as e:
            return f"Bot: Error fetching carts: {e}" 
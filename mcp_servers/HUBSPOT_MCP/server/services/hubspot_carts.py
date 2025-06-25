import requests
from ..config import Config

class HubSpotCartsService:
    """Service class for HubSpot carts operations"""
    
    def __init__(self):
        self.base_url = Config.HUBSPOT_API_BASE_URL
        self.access_token = Config.HUBSPOT_ACCESS_TOKEN
        self.object_type = Config.CART_OBJECT_TYPE
    
    def create_cart(self, name, status="active"):
        """Create a new cart in HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/{self.object_type}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "properties": {
                "name": name,      # Use 'name' for the cart name or user email
                "status": status   # Use 'status' for the cart status
            }
        }
        response = requests.post(url, headers=headers, json=data)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Bot: Error creating cart: {e}\nPayload: {data}\nResponse: {response.text}")
            raise
        return response.json()
    
    def list_carts(self, limit=Config.DEFAULT_CART_LIMIT):
        """List carts from HubSpot"""
        url = f"{self.base_url}/crm/v3/objects/{self.object_type}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {"limit": limit, "sort": "-createdate"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['results'] 
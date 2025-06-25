import requests
from ..config import Config

class HubSpotDealsService:
    """Service class for HubSpot deals operations"""
    
    def __init__(self):
        self.base_url = Config.HUBSPOT_API_BASE_URL
        self.access_token = Config.HUBSPOT_ACCESS_TOKEN
    
    def list_deals(self, limit=Config.DEFAULT_DEAL_LIMIT):
        """List HubSpot deals/contracts"""
        url = f"{self.base_url}/crm/v3/objects/deals"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {"limit": limit}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['results'] 
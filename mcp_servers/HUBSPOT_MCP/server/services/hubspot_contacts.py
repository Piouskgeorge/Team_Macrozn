import requests
from ..config import Config

class HubSpotContactsService:
    """Service class for HubSpot contacts operations"""
    
    def __init__(self):
        self.base_url = Config.HUBSPOT_API_BASE_URL
        self.access_token = Config.HUBSPOT_ACCESS_TOKEN
    
    def list_contacts(self, limit=Config.DEFAULT_CONTACT_LIMIT):
        """List HubSpot contacts"""
        url = f"{self.base_url}/crm/v3/objects/contacts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        params = {"limit": limit, "sort": "-createdate"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['results']
    
    def create_contact(self, firstname, lastname, email):
        """Create a new HubSpot contact"""
        url = f"{self.base_url}/crm/v3/objects/contacts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "properties": {
                "firstname": firstname,
                "lastname": lastname,
                "email": email
            }
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_contact_by_email(self, email):
        """Get a HubSpot contact by email"""
        url = f"{self.base_url}/crm/v3/objects/contacts/search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "filterGroups": [
                {
                    "filters": [
                        {"propertyName": "email", "operator": "EQ", "value": email}
                    ]
                }
            ],
            "properties": ["firstname", "lastname", "email"]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        results = response.json().get('results', [])
        return results[0] if results else None 
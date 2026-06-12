import os
import requests

class GoogleSafeBrowsing:
    def __init__(self):
        self.api_key = os.getenv("SAFE_BROWSING_API_KEY")
        
        # Kommentera ut den här om du saknar api nyckel
        if not self.api_key:
            raise ValueError("SAFE_BROWSING_API_KEY environment variable is not set.")
            
            
        self.url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.api_key}"

    def is_url_safe(self, target_url: str) -> bool:
        """
        Queries Google Safe Browsing. 
        Returns True if safe, False if Google flags it as a threat.
        """
        payload = {
            "client": {
                "clientId": "bth-phishing-detector",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": target_url}]
            }
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if "matches" in data:
                return False
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            return True
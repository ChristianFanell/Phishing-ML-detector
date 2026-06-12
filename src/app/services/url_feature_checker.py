import urllib.parse
import re
import socket
import ssl
from datetime import datetime

class FeatureExtractor:
    def __init__(self):
        # exakt samma ordning som träningen
        self.feature_names = [
            'having_IPhaving_IP_Address', 'URLURL_Length', 'having_At_Symbol', 
            'double_slash_redirecting', 'Prefix_Suffix', 'having_Sub_Domain', 
            'HTTPS_token', 'DNSRecord', 'SSLfinal_State', 'Redirect', 'Shortining_Service'
        ]

    def extract(self, url: str) -> list:
        """Translates a URL string into a feature vector (e.g., [1, -1, 1, 1...])"""
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc
        features = {}
        # ip blir första elementet. Viktigt då vi gör en domänkontroll i pipelinen när vi kör modellen om url är ip
        features['having_IPhaving_IP_Address'] = -1 if re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", url) else 1

        features['URLURL_Length'] = -1 if len(url) >= 54 else 1
        features['having_At_Symbol'] = -1 if '@' in url else 1
        features['double_slash_redirecting'] = -1 if url.rfind('//') > 8 else 1
        features['Prefix_Suffix'] = -1 if '-' in domain else 1
        features['having_Sub_Domain'] = 1 if domain.count('.') <= 1 else (0 if domain.count('.') == 2 else -1)
        features['HTTPS_token'] = -1 if 'https' in domain and parsed.scheme != 'https' else 1
        
        shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl']
        features['Shortining_Service'] = -1 if any(s in domain for s in shorteners) else 1

        features['DNSRecord'] = self._check_dns(domain)
        features['SSLfinal_State'] = self._check_ssl(domain)
        
        # Defaultar redirect till 1 
        features['Redirect'] = 1 

        # 2D array
        return [[features[col] for col in self.feature_names]]

    def _check_dns(self, domain: str) -> int:
        try:
            socket.gethostbyname(domain)
            return 1
        except socket.error:
            return -1

    def _check_ssl(self, domain: str) -> int:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=domain):
                    return 1
        except Exception:
            return -1
        
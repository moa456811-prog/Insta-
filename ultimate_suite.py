import requests
import random
import time
from typing import Dict, Optional

class InstagramCore:
    def __init__(self, proxy: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'X-IG-App-ID': '936619743392459', 
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/',
        })
        if proxy:
            self.session.proxies = {'http': proxy, 'https': proxy}

    def recon_user(self, username: str) -> Dict:
        username = username.strip().replace('@', '')
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        
        try:
            time.sleep(random.uniform(1.0, 2.0)) 
            resp = self.session.get(url, timeout=15)
            
            if resp.status_code == 200:
                user = resp.json().get('data', {}).get('user', {})
                if not user: return {"success": False, "error": "Utilisateur introuvable"}
                
                return {
                    "success": True,
                    "username": username,
                    "full_name": user.get('full_name'),
                    "followers": user.get('edge_followed_by', {}).get('count', 0),
                    "private": user.get('is_private', False),
                    "posts": user.get('edge_owner_to_timeline_media', {}).get('count', 0)
                }
            return {"success": False, "error": f"Erreur HTTP {resp.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
#!/usr/bin/env python3
"""
Instagram Ultimate Suite v8.0 - Core Engine
"""

__version__ = "8.0.0"

import requests
import json
import random
from typing import Dict, List, Optional

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
]

class C:
    GRN, RED, CYN = "\033[92m", "\033[91m", "\033[96m"
    RESET = "\033[0m"

def cb(color: str, text: str) -> str:
    return f"{color}{text}{C.RESET}"

def recon_instagram(username: str) -> Dict:
    """OSINT Instagram rapide"""
    session = requests.Session()
    session.headers['User-Agent'] = random.choice(UA_POOL)
    
    try:
        url = f"https://www.instagram.com/{username}/?__a=1"
        resp = session.get(url, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            user = data.get('graphql', {}).get('user', {})
            
            return {
                "success": True,
                "username": username,
                "private": user.get('is_private', False),
                "followers": user.get('edge_followed_by', {}).get('count', 0),
                "posts": user.get('edge_owner_to_timeline_media', {}).get('count', 0)
            }
    except:
        pass
    
    return {"success": False, "username": username, "error": "Target not found"}

def generate_report(results: List[Dict]) -> str:
    """HTML report simple"""
    html = f"""
    <html><body>
    <h1>Instagram Recon Report</h1>
    <table border="1">
    """
    for r in results:
        status = "🔒 Private" if r.get('private') else "🌐 Public"
        html += f"<tr><td>@{r['username']}</td><td>{status}</td><td>{r.get('followers', 0)}</td></tr>"
    html += "</table></body></html>"
    return html

if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] if len(sys.argv) > 1 else ['testuser']
    results = [recon_instagram(t) for t in targets]
    
    print(cb(C.CYN, f"Recon {len(results)} targets"))
    for r in results:
        if r['success']:
            print(cb(C.GRN, f"✅ @{r['username']} | {r['followers']} followers"))
        else:
            print(cb(C.RED, f"❌ @{r['username']}"))
    
    with open("report.html", "w") as f:
        f.write(generate_report(results))
    print(cb(C.GRN, "📊 report.html généré"))

#!/usr/bin/env python3
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    version = os.getenv('VERSION', '8.1')
    return f"""
<!DOCTYPE html>
<html style="background:black;color:lime;font-family:monospace;padding:50px;">
<h1>🏴‍☠️ Instagram Pentest Dashboard v{version}</h1>
<p>✅ Dashboard opérationnel</p>
<p>Discord Bot: !osint user1 !brute target</p>
<p>Core: ultimate_suite v8.0 - OSINT ready</p>
<hr><small>Render Deploy OK</small>
</html>
    """

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
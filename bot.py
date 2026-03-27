import os
from flask import Flask
from ultimate_suite import InstagramCore 

app = Flask(__name__)
# Initialisation du moteur de scan
core = InstagramCore()

@app.route('/')
def home():
    version = os.getenv('VERSION', '8.1')
    return f"""
    <!DOCTYPE html>
    <html style="background:black;color:lime;font-family:monospace;padding:50px;">
    <h1>🏴‍☠️ Instagram Pentest Dashboard v{version}</h1>
    <p>✅ Statut : Opérationnel</p>
    <p>Utilisez /scan/NOM_UTILISATEUR pour tester.</p>
    <hr><small>Render Deploy OK</small>
    </html>
    """

@app.route('/scan/<username>')
def api_scan(username):
    # Appelle la logique de ultimate_suite.py
    results = core.recon_user(username)
    return results

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

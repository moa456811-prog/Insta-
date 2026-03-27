import os
from flask import Flask
from ultimate_suite import InstagramCore 

app = Flask(__name__)
core = InstagramCore()

@app.route('/')
def home():
    v = os.getenv('VERSION', '8.1')
    return f"""
    <body style="background:#000;color:#0f0;font-family:monospace;padding:50px;">
        <h1>🏴‍☠️ Instagram Pentest Dashboard v{v}</h1>
        <p>Statut : <span style="color:white;">Opérationnel</span></p>
        <hr>
        <p>Utilisez <b>/scan/NOM_UTILISATEUR</b> pour tester.</p>
    </body>
    """

@app.route('/scan/<username>')
def api_scan(username):
    results = core.recon_user(username)
    return results

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import os
from flask import Flask
from ultimate_suite import InstagramCore # Vérifie bien le nom du fichier !

app = Flask(__name__)
# On initialise le moteur
try:
    core = InstagramCore()
except Exception as e:
    print(f"Erreur initialisation moteur: {e}")

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
    # Appelle la fonction de ton fichier ultimate_suite.py
    results = core.recon_user(username)
    return results

if __name__ == "__main__":
    # Important pour Render si tu n'utilises pas Gunicorn
    port = int(os.environ.get("PORT", 5000))
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=port)
=======
    app.run(host='0.0.0.0', port=port)
>>>>>>> c6f6e02d1b82398f59f8eb87060de4cd83edae54

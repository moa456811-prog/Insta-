from flask import Flask, request
from ultimate_suite import InstagramCore  # On importe ton moteur amélioré

app = Flask(__name__)
core = InstagramCore() # On initialise le moteur une seule fois

@app.route('/scan/<username>')
def scan(username):
    data = core.recon_user(username) # On utilise la méthode du moteur
    return data # Retourne le résultat en JSON

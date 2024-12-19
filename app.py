from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Remplace ces valeurs par tes identifiants École Directe
USER_ID = "MXTwisT"
PASSWORD = "A0B1323D9871."

# URL API École Directe
ED_API_URL = "https://api.ecoledirecte.com/v3/login.awp"

def get_token():
    """
    Authentifie l'utilisateur sur École Directe et retourne le token.
    """
    payload = {
        "identifiant": USER_ID,
        "motdepasse": PASSWORD
    }
    response = requests.post(ED_API_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 200:
            return data["data"]["token"]
        else:
            raise Exception("Erreur d'authentification : " + data.get("message", "Inconnu"))
    else:
        raise Exception("Erreur de connexion à l'API École Directe.")

def get_homeworks(token):
    """
    Récupère les devoirs depuis École Directe.
    """
    homework_url = "https://api.ecoledirecte.com/v3/eleves/{id_eleve}/cahierdetexte.awp?verbe=get"
    headers = {"x-token": token}
    response = requests.get(homework_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 200:
            return data["data"]
        else:
            raise Exception("Erreur lors de la récupération des devoirs : " + data.get("message", "Inconnu"))
    else:
        raise Exception("Erreur de connexion pour récupérer les devoirs.")

@app.route("/devoirs", methods=["GET"])
def devoirs():
    """
    Endpoint pour récupérer et afficher les devoirs.
    """
    try:
        token = get_token()
        devoirs = get_homeworks(token)
        return jsonify(devoirs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    """
    Page d'accueil simple.
    """
    return "Bienvenue ! Utilise l'endpoint '/devoirs' pour voir tes devoirs."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

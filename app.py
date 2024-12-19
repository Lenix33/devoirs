from flask import Flask, jsonify
import requests
import os

# Crée l'application Flask
app = Flask(__name__)

USER_ID = "MXTwisT"
PASSWORD = "A0B1323D9871."
ED_API_URL = "https://api.ecoledirecte.com/v3/login.awp"
HOMEWORK_API_URL = "https://api.ecoledirecte.com/v3/eleves/{id_eleve}/cahierdetexte.awp?verbe=get"

def get_token():
    payload = {
        "identifiant": USER_ID,
        "motdepasse": PASSWORD
    }
    response = requests.post(ED_API_URL, json=payload)

    print("Réponse de l'API (Token):", response.text)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if data.get("code") == 200:
                return data["data"]["token"]
            else:
                raise Exception("Erreur d'authentification : " + data.get("message", "Inconnu"))
        except ValueError:
            raise Exception("La réponse de l'API n'est pas un JSON valide.")
    else:
        raise Exception(f"Erreur de connexion à l'API École Directe: {response.status_code}")

def get_homeworks(token):
    homework_url = HOMEWORK_API_URL.format(id_eleve="ton_id_eleve")
    headers = {"x-token": token}
    response = requests.get(homework_url, headers=headers)

    print("Réponse de l'API (Devoirs):", response.text)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if data.get("code") == 200:
                return data["data"]
            else:
                raise Exception("Erreur lors de la récupération des devoirs : " + data.get("message", "Inconnu"))
        except ValueError:
            raise Exception("La réponse de l'API n'est pas un JSON valide.")
    else:
        raise Exception(f"Erreur de connexion pour récupérer les devoirs: {response.status_code}")

# Définir la route pour obtenir les devoirs
@app.route("/devoirs", methods=["GET"])
def devoirs():
    try:
        token = get_token()
        devoirs = get_homeworks(token)
        return jsonify(devoirs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)


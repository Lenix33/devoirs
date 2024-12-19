import requests
import json

# Paramètres pour la connexion à l'API d'École Directe
USER_ID = "MXTwisT"
PASSWORD = "A0B1323D9871."
ED_API_URL = "https://api.ecoledirecte.com/v3/login.awp"  # Remplace par l'URL correcte

# Fonction pour obtenir un token de session
def get_token():
    payload = {
        "identifiant": USER_ID,
        "motdepasse": PASSWORD
    }

    # Envoi de la requête POST pour obtenir le token
    response = requests.post(ED_API_URL, json=payload)

    # Affiche la réponse brute pour débogage
    print("Réponse brute de l'API (Token):", response.text)

    try:
        # Tentative de parsing du JSON
        data = response.json()
    except ValueError:
        raise Exception("La réponse de l'API n'est pas un JSON valide.")

    # Vérification de la réussite de l'authentification
    if response.status_code == 200:
        if data.get("code") == 200:
            return data["data"]["token"]
        else:
            raise Exception("Erreur d'authentification : " + data.get("message", "Inconnu"))
    else:
        raise Exception(f"Erreur de connexion à l'API École Directe: {response.status_code}")

# Fonction pour récupérer les devoirs depuis le cahier de texte
def get_homework():
    # Obtenir le token d'authentification
    token = get_token()

    # URL pour récupérer les devoirs
    homeworks_url = "https://api.ecoledirecte.com/v3/eleves/cahierDeTextes.awp"
    params = {
        "token": token
    }

    # Envoi de la requête pour obtenir les devoirs
    response = requests.get(homeworks_url, params=params)

    # Affiche la réponse brute pour débogage
    print("Réponse brute de l'API (Devoirs):", response.text)

    try:
        # Tentative de parsing du JSON
        data = response.json()
    except ValueError:
        raise Exception("La réponse de l'API n'est pas un JSON valide.")

    # Vérification de la réussite de la récupération des devoirs
    if response.status_code == 200:
        if data.get("code") == 200:
            devoirs = data.get("data", {}).get("devoirs", [])
            if devoirs:
                return devoirs
            else:
                raise Exception("Aucun devoir trouvé.")
        else:
            raise Exception("Erreur lors de la récupération des devoirs : " + data.get("message", "Inconnu"))
    else:
        raise Exception(f"Erreur de connexion à l'API École Directe: {response.status_code}")

# Fonction principale
if __name__ == "__main__":
    try:
        devoirs = get_homework()
        print("Devoirs récupérés :", devoirs)
    except Exception as e:
        print("Erreur:", e)

import json
import requests
from datetime import datetime

# 🔧 Configuration
GITHUB_REPO = "ton-utilisateur/muscu-automation"  # 🔹 Remplace avec ton repo
GITHUB_TOKEN = "TON_GITHUB_TOKEN"  # 🔹 Stocke-le dans GitHub Secrets !
GITHUB_FILE_PATH = "data/utilisateur.json"  # 🔹 Fichier JSON stocké dans le repo
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/m2pnfh9sj251v8rkj3g1vyl3mjys58ih"  # 🔹 Ton Webhook Make

# 🔄 Simulation des données utilisateur
def get_user_data():
    return {
       
        "nom": "John Doe",
         sexe": "Homme" ou "Femme"
        "objectif": "Prise de masse",
        "frequence_entrainement": "4 fois/semaine",
        "pas_quotidiens": 8000,
        "morphologie": {
            "bras": "Longs",
            "jambes": "Courtes",
            "torse": "Moyen",
            "epaules": "Larges"
        },
        "exercices_selectionnes": ["Développé incliné", "Rowing barre"],
        "programme": "Jour 1: Pecs/Dos, Jour 2: Jambes",
        "nutrition": "3000 kcal/jour"
    }

# 🔄 Mise à jour des données sur GitHub
def update_github_data(user_data):
    github_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
    json_data = json.dumps(user_data, indent=4)
    
    # Vérifier si le fichier existe déjà
    response = requests.get(github_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json().get("sha", "")

    # Préparer la requête
    payload = {
        "message": f"Maj données utilisateur {datetime.now()}",
        "content": json_data.encode("utf-8").decode("latin1"),
        "branch": "main",
    }
    
    if sha:
        payload["sha"] = sha  # Ajout du SHA si le fichier existe déjà

    # Envoi sur GitHub
    github_response = requests.put(github_url, headers={"Authorization": f"token {GITHUB_TOKEN}"}, json=payload)

    if github_response.status_code in [200, 201]:
        print("✅ Données mises à jour sur GitHub")
        return True
    else:
        print("❌ Erreur GitHub :", github_response.json())
        return False

# 🔄 Envoi des données à Make
def send_data_to_make(user_data):
    response = requests.post(MAKE_WEBHOOK_URL, json=user_data)
    
    if response.status_code == 200:
        print("✅ Données envoyées à Make")
    else:
        print("❌ Erreur Make :", response.json())

# 🔄 Automatisation
if __name__ == "__main__":
    print("\n🔄 Récupération des données utilisateur...")
    user_data = get_user_data()

    print("📡 Mise à jour GitHub...")
    if update_github_data(user_data):
        print("📡 Envoi à Make...")
        send_data_to_make(user_data)

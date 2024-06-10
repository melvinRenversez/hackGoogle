import os
import time
import sqlite3
import pandas as pd

def get_chrome_history():
    # Définir le chemin vers le fichier History de Chrome (modifiez selon votre OS)
    if os.name == 'nt':  # Windows
        history_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History'
    elif os.name == 'posix':  # macOS
        history_path = os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/Default/History'
    else:  # Linux (à adapter si nécessaire)
        history_path = os.path.expanduser('~') + '/.config/google-chrome/Default/History'

    # Connexion à la base de données SQLite
    try:
        con = sqlite3.connect(history_path)
        cursor = con.cursor()

        # Exécuter la requête SQL pour récupérer l'historique
        cursor.execute("SELECT urls.url, urls.title, urls.visit_count, urls.last_visit_time FROM urls")

        # Récupérer les résultats dans un DataFrame pandas
        columns = ['url', 'title', 'visit_count', 'last_visit_time']
        history_items = cursor.fetchall()
        history_df = pd.DataFrame(history_items, columns=columns)

        # Convertir le format de la colonne 'last_visit_time'
        history_df['last_visit_time'] = pd.to_datetime(history_df['last_visit_time'], unit='us', origin='1601-01-01')

        # Fermer la connexion
        con.close()

        return history_df
    except sqlite3.OperationalError as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

def is_database_locked():
    # Chemin vers le fichier History de Chrome (modifiez selon votre OS)
    if os.name == 'nt':  # Windows
        history_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History'
    elif os.name == 'posix':  # macOS
        history_path = os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/Default/History'
    else:  # Linux (à adapter si nécessaire)
        history_path = os.path.expanduser('~') + '/.config/google-chrome/Default/History'

    # Vérifie si le fichier de la base de données est verrouillé
    try:
        con = sqlite3.connect(history_path)
        con.close()
        return False  # La base de données n'est pas verrouillée
    except sqlite3.OperationalError as e:
        return True  # La base de données est verrouillée

def run_script():
    print("La base de données n'est plus verrouillée, le script peut être lancé !")
    history_df = get_chrome_history()
    if history_df is not None:
        print(history_df.head())  # Affiche les premières lignes de l'historique
    else:
        print("Impossible de récupérer l'historique.")

# Vérifie en permanence si la base de données est verrouillée
while is_database_locked():
    print("La base de données est verrouillée. Attente avant de réessayer...")
    time.sleep(5)  # Attend 5 secondes avant de réessayer

# Une fois que la base de données n'est plus verrouillée, exécute le script
run_script()
print("Le script a été exécuté avec succès !")

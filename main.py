import os
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

# Exemple d'utilisation
if __name__ == "__main__":
    history_df = get_chrome_history()
    print(history_df.head(10))  # Affiche les 10 premières entrées de l'historique

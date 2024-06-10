import sqlite3
import os
import shutil

nombre_de_requet  =int(input('nombre_de_requet : '))

# Chemin vers le fichier History de Google Chrome
history_path = "C:\\Users\\melvi\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"

# Copier le fichier History pour éviter les problèmes d'accès
temp_history_path = "temp_history"
shutil.copyfile(history_path, temp_history_path)

# Connexion à la base de données SQLite
conn = sqlite3.connect(temp_history_path)
cursor = conn.cursor()

# Requête pour sélectionner les URL visitées
query = f"SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT {nombre_de_requet};"
cursor.execute(query)

# Affichage des résultats
i = 0
with open("history.txt", "w", encoding="utf-8") as txt:
    for row in cursor.fetchall():
        i += 1
        txt.write(f"Requete : {i}\n")
        url = row[0]
        title = row[1]
        visit_count = row[2]
        last_visit_time = row[3]
        txt.write(f"URL: {url}\nTitre: {title}\nNombre de visites: {visit_count}\nDerniere visite: {last_visit_time}\n\n")
        
        # Affichage dans la console
        print(f"Requete : {i}")
        print(f"URL: {url}\nTitre: {title}\nNombre de visites: {visit_count}\nDernière visite: {last_visit_time}\n")



# Fermeture de la connexion à la base de données
conn.close()

# Supprimer le fichier temporaire
os.remove(temp_history_path)

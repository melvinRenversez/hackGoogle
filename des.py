import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_password(encrypted_password, key, iv):
    # Déchiffrement des données
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_password = decryptor.update(encrypted_password) + decryptor.finalize()

        # Suppression du padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    password = unpadder.update(padded_password) + unpadder.finalize()

    return password.decode('utf-8')

def read_encrypted_passwords_from_file(filename):
    passwords = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 5):  # Utilisation de 5 car chaque ensemble de données est séparé par une ligne vide
            try:
                origin_url = lines[i].strip().split(': ')[1]
                username = lines[i+1].strip().split(': ')[1]
                encrypted_password = bytes.fromhex(lines[i+2].strip().split(': ')[1])
                iv = bytes.fromhex(lines[i+3].strip().split(': ')[1])  # Ajout de l'IV
                passwords.append((origin_url, username, encrypted_password, iv))  # Ajout de l'IV à la liste
            except: 
                pass
    return passwords


# Clé secrète connue uniquement de votre appareil
secret_key = b'v10]\x8b\x07h\xb2&\xb5\xf6_\x0c\xacJ\xac\xbeu\xe4F!\x8c5L2!pr\xca\xf5\x9c\xed\xaf\x8f\xe95\x1aT\xa1'

# Lire les mots de passe cryptés à partir du fichier

encrypted_passwords = read_encrypted_passwords_from_file("encrypted_passwords.txt")

print("i")

# Tenter de déchiffrer les mots de passe
for origin_url, username, encrypted_password, iv in encrypted_passwords:
    print("r")
    password = decrypt_password(encrypted_password, secret_key, iv)
    if password:
        print(f'URL: {origin_url}\nUsername: {username}\nPassword: {password}\n')
    else:
        print(f'Failed to decrypt password for URL: {origin_url}\n')

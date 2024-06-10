import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.backends import default_backend

def encrypt_password(password, key):
    try:
        # Ajout du padding au mot de passe
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_password = padder.update(password.encode('utf-8')) + padder.finalize()

        # Génération d'un IV aléatoire de la bonne taille pour AES-CBC
        iv = os.urandom(16)
        print("IV:", iv.hex())

        # Chiffrement des données
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_password) + encryptor.finalize()

        # Renvoyer le IV et le texte chiffré
        return iv, ciphertext
    except Exception as e:
        print(e)
        return None, None

# Génération d'une clé AES de 256 bits (32 octets)
secret_key = b'v10\xfd;$\x91\x15\x17\x03|\xdd\xfeZ\x9d\xb4\xffX\xa3\x99\xcd/l3\x8aH\xda\xa2F=\x18'
print("secret_key", secret_key)

# Mot de passe à chiffrer
password_to_encrypt = "melvin.1"

# Chiffrement du mot de passe
iv, encrypted_password = encrypt_password(password_to_encrypt, secret_key)

if iv is not None and encrypted_password is not None:
    print("IV:", iv.hex())
    print("Mot de passe chiffré:", encrypted_password.hex())

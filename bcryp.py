import hashlib
import bcrypt
import scrypt
from argon2 import PasswordHasher

password = b"Azerty"  # Convertir en bytes

# Liste des algorithmes de hachage à utiliser
hash_algorithms = [
    hashlib.pbkdf2_hmac,  # PBKDF2
    PasswordHasher().hash,  # Argon2
    scrypt.hash,           # scrypt
    bcrypt.hashpw,         # bcrypt
    hashlib.sha256         # SHA-256
]

# Données supplémentaires pour certains algorithmes
salt_pbkdf2 = b'sel_pbkdf2'
salt_scrypt = b'sel_scrypt_long_enough'
rounds_bcrypt = 12

for i, hash_func in enumerate(hash_algorithms, start=1):
    if hash_func == hashlib.pbkdf2_hmac:
        # Utiliser PBKDF2 avec un sel et un nombre d'itérations
        hashed_password = hash_func('sha256', password, salt_pbkdf2, 100000)
        print(f"Mot de passe haché avec PBKDF2 (méthode {i}): {hashed_password}")

    elif hash_func == PasswordHasher().hash:
        # Utiliser Argon2 avec un coût de travail personnalisé
        hashed_password = hash_func(password)
        print(f"Mot de passe haché avec Argon2 (méthode {i}): {hashed_password}")

    elif hash_func == scrypt.hash:
        # Utiliser scrypt avec un sel et un coût de travail personnalisé
        hashed_password = hash_func(password, salt_scrypt, N=2**14, r=8, p=1, buflen=64)
        print(f"Mot de passe haché avec scrypt (méthode {i}): {hashed_password}")

    elif hash_func == bcrypt.hashpw:
        # Utiliser bcrypt avec un sel et un coût de travail personnalisé
        salt_bcrypt = bcrypt.gensalt(rounds=rounds_bcrypt)
        hashed_password = hash_func(password, salt_bcrypt)
        print(f"Mot de passe haché avec bcrypt (méthode {i}): {hashed_password}")

    elif hash_func == hashlib.sha256:
        # Utiliser SHA-256
        hashed_password = hash_func(password).hexdigest()
        print(f"Mot de passe haché avec SHA-256 (méthode {i}): {hashed_password}")

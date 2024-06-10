import hashlib

password = "Melvin.1"
encoded_string = "763130b7c07c40df172c2c34f47ba86813baba790b99d0a631998eca54dd0c31f9930165d1"

# Convertir la chaîne hexadécimale en bytes
encoded_bytes = bytes.fromhex(encoded_string)

# Convertir le mot de passe en bytes
password_bytes = password.encode('utf-8')

# Liste des algorithmes de hachage à utiliser
hash_algorithms = [
    hashlib.md5(),
    hashlib.sha1(),
    hashlib.sha224(),
    hashlib.sha256(),
    hashlib.sha384(),
    hashlib.sha512(),
    hashlib.blake2b(),
    hashlib.blake2s(),
    hashlib.sha3_224(),
    hashlib.sha3_256(),
    hashlib.sha3_384(),
    hashlib.sha3_512()
]

for algorithm in hash_algorithms:
    algorithm.update(password_bytes)
    hashed_password = algorithm.hexdigest()
    print(hashed_password)
    print(" ")
    if hashed_password == encoded_string:
        print(f"Mot de passe haché avec {algorithm.name} correspond à la chaîne encodée fournie.")

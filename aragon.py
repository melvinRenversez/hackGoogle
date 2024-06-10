from argon2 import PasswordHasher

password = b"Azerty"  # Convertir en bytes

password_hasher = PasswordHasher()
hashed_password_argon2 = password_hasher.hash(password)

# Extraire la valeur hachée du résultat de la méthode argon2.PasswordHasher().hash
hashed_password_argon2_value = hashed_password_argon2.split("$")[-1]

print(f"Mot de passe haché avec Argon2 (méthode 2): {hashed_password_argon2_value}")

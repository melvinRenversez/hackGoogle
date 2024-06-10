import hashlib
import bcrypt
import scrypt
from argon2 import PasswordHasher
import hmac

string = "Hello World"

# Liste des algorithmes de hachage
algorithms = ["sha1", "md5", "md4", "sha256", "sha384", "sha512", "ripemd128", "ripemd160", "ripemd256",
              "ripemd320", "whirlpool", "tiger128,3", "tiger160,3", "tiger192,3", "tiger128,4", "tiger160,4",
              "tiger192,4", "snefru", "gost", "adler32", "crc32", "crc32b", "haval128,3", "haval160,3", "haval192,3",
              "haval224,3", "haval256,3", "haval128,4", "haval160,4", "haval192,4", "haval224,4", "haval256,4",
              "haval128,5", "haval160,5", "haval192,5", "haval224,5", "haval256,5"]

# Essayer toutes les méthodes de hachage
for algorithm in algorithms:
    if algorithm == "bcrypt":
        hashed_string = bcrypt.hashpw(string.encode(), bcrypt.gensalt())
    elif algorithm == "scrypt":
        hashed_string = scrypt.hash(string, salt=scrypt.gensalt())
    elif algorithm == "argon2":
        password_hasher = PasswordHasher()
        hashed_string = password_hasher.hash(string)
    elif algorithm == "hmac":
        hashed_string = hmac.new(string.encode(), digestmod=hashlib.sha256).hexdigest()
    else:
        hashed_string = hashlib.new(algorithm, string.encode()).hexdigest()
    print(f"{algorithm}: {hashed_string}")

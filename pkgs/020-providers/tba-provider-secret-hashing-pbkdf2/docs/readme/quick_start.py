from tba_provider_secret_hashing_pbkdf2 import Pbkdf2SecretHasher

hasher = Pbkdf2SecretHasher()
record = hasher.hash_secret("example password for documentation")
assert hasher.verify_secret("example password for documentation", record).verified

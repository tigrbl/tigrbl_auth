from tba_provider_secret_hashing_pbkdf2 import Pbkdf2SecretHasher

legacy = Pbkdf2SecretHasher(rounds=310_000)
current = Pbkdf2SecretHasher(rounds=600_000)
password = "example password for documentation"
record = legacy.hash_secret(password)

verified = current.verify_secret(password, record)
assert verified.verified and verified.needs_rehash

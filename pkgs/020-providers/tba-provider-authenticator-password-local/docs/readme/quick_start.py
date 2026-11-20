from tba_provider_authenticator_password_local import PasswordLocalAuthenticator
from tba_provider_secret_hashing_bcrypt import BcryptSecretHasher

verifier = BcryptSecretHasher()
stored = verifier.hash_secret("example-password")
authenticator = PasswordLocalAuthenticator(secret_verifier=verifier)
assert authenticator.verify_secret("example-password", stored)
assert not authenticator.verify_secret("incorrect-password", stored)

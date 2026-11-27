"""DNSSEC key adapters for cryptography-backed algorithms."""

from cryptography.hazmat.primitives import serialization

from .base import GenericPrivateKey, GenericPublicKey


def _check_key_type(key, expected):
    from ..dnssec import AlgorithmKeyMismatch

    if expected is None:
        raise TypeError("DNSSEC key type must be specified")
    if not isinstance(key, expected):
        raise AlgorithmKeyMismatch("key does not match its DNSSEC algorithm")


class CryptographyPublicKey(GenericPublicKey):
    key_cls = None

    def __init__(self, key):
        _check_key_type(key, self.key_cls)
        self.key = key

    @classmethod
    def from_pem(cls, public_pem):
        return cls(key=serialization.load_pem_public_key(public_pem))

    def to_pem(self):
        return self.key.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
        )


class CryptographyPrivateKey(GenericPrivateKey):
    key_cls = None

    def __init__(self, key):
        _check_key_type(key, self.key_cls)
        self.key = key

    def public_key(self):
        return self.public_cls(key=self.key.public_key())

    @classmethod
    def from_pem(cls, private_pem, password=None):
        return cls(key=serialization.load_pem_private_key(private_pem, password))

    def to_pem(self, password=None):
        encryption = (
            serialization.BestAvailableEncryption(password)
            if password
            else serialization.NoEncryption()
        )
        return self.key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, encryption
        )

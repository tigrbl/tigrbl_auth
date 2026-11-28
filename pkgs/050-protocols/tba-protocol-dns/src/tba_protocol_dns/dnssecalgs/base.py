"""Public interfaces for DNSSEC key formats and signature algorithms."""

from abc import ABC, abstractmethod

from tba_codec_dns.rdtypes.ANY.DNSKEY import DNSKEY
from tba_codec_dns.wire import RecordClass, RecordType


class GenericPublicKey(ABC):
    algorithm: int

    @abstractmethod
    def __init__(self, key):
        """Accept a public key in the implementation's native representation."""

    @classmethod
    @abstractmethod
    def from_dnskey(cls, key):
        """Construct a public key from DNSKEY RDATA."""

    @abstractmethod
    def encode_key_bytes(self):
        """Encode the DNSKEY public key field."""

    @abstractmethod
    def verify(self, signature, data):
        """Verify a DNSSEC signature or raise an invalid-signature exception."""

    def to_dnskey(self, flags=256, protocol=3):
        if not 0 <= flags <= 65535 or not 0 <= protocol <= 255:
            raise ValueError("DNSKEY flags or protocol outside its wire range")
        return DNSKEY(
            RecordClass.IN,
            RecordType.DNSKEY,
            int(flags),
            int(protocol),
            int(self.algorithm),
            self.encode_key_bytes(),
        )

    @classmethod
    def _ensure_algorithm_key_combination(cls, key):
        from ..dnssec import AlgorithmKeyMismatch

        if key.algorithm != cls.algorithm:
            raise AlgorithmKeyMismatch("DNSKEY does not match its DNSSEC algorithm")

    @classmethod
    @abstractmethod
    def from_pem(cls, public_pem):
        """Read a PEM SubjectPublicKeyInfo public key."""

    @abstractmethod
    def to_pem(self):
        """Write a PEM SubjectPublicKeyInfo public key."""


class GenericPrivateKey(ABC):
    public_cls: type[GenericPublicKey]

    @abstractmethod
    def __init__(self, key):
        """Accept a private key in the implementation's native representation."""

    @abstractmethod
    def sign(self, data, verify=False, deterministic=True):
        """Sign canonical DNSSEC data."""

    @abstractmethod
    def public_key(self):
        """Return the associated DNSSEC public key."""

    @classmethod
    @abstractmethod
    def from_pem(cls, private_pem, password=None):
        """Read a PEM PKCS#8 private key."""

    @abstractmethod
    def to_pem(self, password=None):
        """Write a PEM PKCS#8 private key."""

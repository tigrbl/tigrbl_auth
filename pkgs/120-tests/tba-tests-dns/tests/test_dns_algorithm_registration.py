"""Exercise registered DNSSEC key formats through public signing operations."""

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from tba_codec_dns.rrset import from_text as rrset_from_text
from tba_primitives_dns_name.name import from_text
from tba_protocol_dns import dnssec
from tba_protocol_dns.dnssecalgs import algorithms, register_algorithm_cls
from tba_protocol_dns.dnssecalgs.cryptography import (
    CryptographyPrivateKey,
    CryptographyPublicKey,
)
from tba_protocol_dns.dnssecalgs.eddsa import PrivateED25519


@pytest.mark.parametrize("algorithm", [253, 254])
def test_private_dnssec_algorithm_registration(algorithm, monkeypatch):
    name = from_text("ed25519.example.")
    oid = b"\x2b\x06\x01\x04\x01"
    prefix = name if algorithm == 253 else bytes((len(oid),)) + oid
    encoded = name.to_wire() if algorithm == 253 else prefix

    class PublicKey(CryptographyPublicKey):
        key_cls = Ed25519PublicKey

        @classmethod
        def from_dnskey(cls, key):
            assert key.key.startswith(encoded)
            return cls(Ed25519PublicKey.from_public_bytes(key.key[len(encoded) :]))

        def encode_key_bytes(self):
            return encoded + self.key.public_bytes_raw()

        def verify(self, signature, data):
            self.key.verify(signature, data)

    PublicKey.algorithm = algorithm

    class PrivateKey(CryptographyPrivateKey):
        key_cls = Ed25519PrivateKey
        public_cls = PublicKey

        def sign(self, data, verify=False, deterministic=True):
            signature = self.key.sign(data)
            if verify:
                self.public_key().verify(signature, data)
            return signature

    monkeypatch.setitem(algorithms, (algorithm, prefix), PrivateED25519)
    register_algorithm_cls(
        algorithm, PrivateKey, **({"name": name} if algorithm == 253 else {"oid": oid})
    )
    key = Ed25519PrivateKey.generate()
    dnskey = dnssec.make_dnskey(PublicKey(key.public_key()), algorithm)
    assert dnssec.make_cdnskey(PublicKey(key.public_key()), algorithm).key == dnskey.key
    assert dnssec.get_algorithm_cls(algorithm, prefix) is PrivateKey
    assert dnssec.get_algorithm_cls_from_dnskey(dnskey) is PrivateKey

    signer = from_text("example.")
    rrset = rrset_from_text("www.example.", 300, "IN", "A", "192.0.2.1")
    signature = dnssec.sign(
        rrset, key, signer, dnskey, inception=100, expiration=200, verify=True
    )
    key_record = dnskey.record(signer.labels[:-1], 300)
    dnssec.validate_rrsig(rrset, signature, [key_record], now=150)
    with pytest.raises(dnssec.ValidationError):
        dnssec.validate_rrsig(
            rrset_from_text("www.example.", 300, "IN", "A", "192.0.2.2"),
            signature,
            [key_record],
            now=150,
        )


def test_builtin_registration_and_pem_round_trip():
    assert dnssec.get_algorithm_cls("ED25519") is PrivateED25519
    private = PrivateED25519.generate()
    reopened = PrivateED25519.from_pem(private.to_pem(b"fixture"), b"fixture")
    public = reopened.public_key()
    dnskey = public.to_dnskey()
    assert dnssec.get_algorithm_cls_from_dnskey(dnskey) is PrivateED25519
    public.from_dnskey(dnskey).verify(reopened.sign(b"test", verify=True), b"test")
    with pytest.raises(TypeError):
        register_algorithm_cls("ED25519", object)
    with pytest.raises(ValueError):
        register_algorithm_cls("PRIVATEDNS", PrivateED25519)

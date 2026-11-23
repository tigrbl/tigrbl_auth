"""DNSSEC EdDSA key implementations."""

from cryptography.hazmat.primitives.asymmetric import ed448, ed25519

from ._native import implementations

for _number, _name, _public, _private in (
    (15, "ED25519", ed25519.Ed25519PublicKey, ed25519.Ed25519PrivateKey),
    (16, "ED448", ed448.Ed448PublicKey, ed448.Ed448PrivateKey),
):
    globals().update(
        implementations(
            __name__, {_number: _name}, _public, _private, _private.generate
        )
    )

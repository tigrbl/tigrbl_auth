import json
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from tigrbl_jose_cryptography_provider import (
    JweCryptographyProvider,
    JwsCryptographyProvider,
)
from tigrbl_protected_envelope_capability import ProtectedEnvelopeCapability
from tigrbl_security_protocol_jws import JWSProfile, JwsProtocol
from tigrbl_security_protocol_jwe import JWEProfile, JweProtocol
from tigrbl_auth_protocol_jwt import JwtProfile, JwtProtocol


def keys():
    private = ed25519.Ed25519PrivateKey.generate()
    return private.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ), private.public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
    )


def test_jws_jwe_and_jwt_protocols_delegate_to_capabilities() -> None:
    private, public = keys()
    jws_profile = JWSProfile("signed", frozenset({"EdDSA"}), frozenset({"alg", "kid"}))
    signed = JwsProtocol(
        ProtectedEnvelopeCapability(
            JwsCryptographyProvider({"k": private}),
            JwsCryptographyProvider({"k": public}),
        ),
        jws_profile,
    ).sign(
        json.dumps({"iss": "i", "sub": "s", "aud": "a", "exp": 20, "iat": 1}).encode(),
        key_reference="k",
        headers={"alg": "EdDSA", "kid": "k", "typ": "JWT"},
    )
    jwt = JwtProtocol(
        ProtectedEnvelopeCapability(
            JwsCryptographyProvider({"k": private}),
            JwsCryptographyProvider({"k": public}),
        ),
        JwtProfile(
            "id",
            frozenset({"JWT"}),
            frozenset({"iss", "sub", "aud", "exp", "iat"}),
            frozenset({"EdDSA"}),
        ),
    )
    assert jwt.verify(signed, issuer="i", audience="a", now=10)[0]["sub"] == "s"
    provider = JweCryptographyProvider({"e": b"0" * 32})
    cap = ProtectedEnvelopeCapability(provider, provider)
    protocol = JweProtocol(
        cap,
        JWEProfile("encrypted", frozenset({"dir"}), frozenset({"alg", "enc", "kid"})),
    )
    envelope = protocol.encrypt(
        b"secret",
        key_reference="e",
        headers={"alg": "dir", "enc": "A256GCM", "kid": "e"},
    )
    assert protocol.decrypt(envelope).payload == b"secret"

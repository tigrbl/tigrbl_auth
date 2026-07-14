from __future__ import annotations

from types import SimpleNamespace

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from tigrbl_auth.standards.oauth2.dpop import issue_nonce, jwk_from_public_key, jwk_thumbprint, make_proof, verify_proof
from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import validate_certificate_binding


def _ed25519_keyref() -> SimpleNamespace:
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return SimpleNamespace(material=private_pem, public=public_pem)


class _ReplayOps:
    def __init__(self) -> None:
        self.keys: set[tuple[str, str, str, str, str | None]] = set()

    def check(self, claims, *, ttl_s: int = 300) -> bool:
        key = (claims.jkt, claims.jti, claims.htm, claims.htu, claims.ath)
        replayed = key in self.keys
        self.keys.add(key)
        return replayed


class _NonceOps:
    def __init__(self) -> None:
        self.values: set[str] = set()

    def issue(self, *, ttl_s: int = 300) -> str:
        nonce = f"nonce-{len(self.values) + 1}"
        self.values.add(nonce)
        return nonce

    def consume(self, nonce: str, *, now=None) -> bool:
        if nonce not in self.values:
            return False
        self.values.remove(nonce)
        return True


@pytest.mark.security
def test_sender_constraint_replay_and_binding_fail_closed() -> None:
    keyref = _ed25519_keyref()
    jkt = jwk_thumbprint(jwk_from_public_key(keyref.public))
    replay = _ReplayOps()
    nonce_ops = _NonceOps()
    nonce = issue_nonce(issuer=nonce_ops.issue)
    access_token = "capability-token"
    proof = make_proof(keyref, "POST", "https://rs.example.com/resource", access_token=access_token, nonce=nonce)

    assert (
        verify_proof(
            proof,
            "POST",
            "https://rs.example.com/resource",
            jkt=jkt,
            access_token=access_token,
            expected_nonce=nonce,
            replay_checker=replay.check,
            nonce_consumer=nonce_ops.consume,
        )
        == jkt
    )
    with pytest.raises(ValueError):
        verify_proof(
            proof,
            "POST",
            "https://rs.example.com/resource",
            jkt=jkt,
            access_token=access_token,
            replay_checker=replay.check,
        )
    with pytest.raises(Exception):
        validate_certificate_binding({"cnf": {"x5t#S256": "thumb-a"}}, "thumb-b", enabled=True)

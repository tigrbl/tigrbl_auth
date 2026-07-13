from __future__ import annotations

from types import SimpleNamespace

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from tigrbl_auth.standards.oauth2.dpop import clear_runtime_state, configure_state_providers, issue_nonce, jwk_from_public_key, jwk_thumbprint, make_proof, verify_proof
from tigrbl_replay_memory_provider import MemoryReplayCheckProvider, MemorySingleUseNonceProvider
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


@pytest.mark.security
def test_sender_constraint_replay_and_binding_fail_closed() -> None:
    configure_state_providers(
        replay=MemoryReplayCheckProvider(), nonce=MemorySingleUseNonceProvider()
    )
    clear_runtime_state()
    keyref = _ed25519_keyref()
    jkt = jwk_thumbprint(jwk_from_public_key(keyref.public))
    nonce = issue_nonce()
    access_token = "capability-token"
    proof = make_proof(keyref, "POST", "https://rs.example.com/resource", access_token=access_token, nonce=nonce)

    assert verify_proof(proof, "POST", "https://rs.example.com/resource", jkt=jkt, access_token=access_token, expected_nonce=nonce) == jkt
    with pytest.raises(ValueError):
        verify_proof(proof, "POST", "https://rs.example.com/resource", jkt=jkt, access_token=access_token)
    with pytest.raises(Exception):
        validate_certificate_binding({"cnf": {"x5t#S256": "thumb-a"}}, "thumb-b", enabled=True)

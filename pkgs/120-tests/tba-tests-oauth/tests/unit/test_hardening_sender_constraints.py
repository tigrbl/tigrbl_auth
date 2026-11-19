from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from cryptography.x509.oid import NameOID

from tba_auth.cli.artifacts import deployment_from_options
from tba_auth.config.settings import settings
from tba_auth.standards.oauth2.dpop import (
    issue_nonce,
    jwk_from_public_key,
    jwk_thumbprint,
    make_proof,
    verify_proof,
)
from tba_protocol_oauth.standards.mutual_tls_client_authentication import (
    authenticate_mtls_client,
    presented_certificate_thumbprint,
    thumbprint_from_cert_pem,
    validate_request_certificate_binding,
)
from tba_protocol_oauth.standards.oauth_security_bcp import (
    OAuthPolicyViolation,
    validate_sender_constraint,
)


def _generate_cert_pem() -> bytes:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "capability.example")])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc) - timedelta(minutes=1))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=1))
        .sign(key, hashes.SHA256())
    )
    return cert.public_bytes(serialization.Encoding.PEM)


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


def test_mtls_registration_auth_and_request_binding_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "enable_rfc8705", True)
    cert_pem = _generate_cert_pem()
    thumbprint = thumbprint_from_cert_pem(cert_pem)
    request = SimpleNamespace(headers={"X-Client-Cert": cert_pem.decode("utf-8")}, scope={})

    assert presented_certificate_thumbprint(request) == thumbprint

    registration_metadata = {
        "token_endpoint_auth_method": "tls_client_auth",
        "tls_client_certificate_thumbprint": thumbprint,
    }
    authn = authenticate_mtls_client(registration_metadata, thumbprint)
    assert authn.auth_method == "tls_client_auth"
    assert authn.confirmation_claim == {"x5t#S256": thumbprint}

    payload = {"cnf": {"x5t#S256": thumbprint}}
    assert validate_request_certificate_binding(payload, request) == thumbprint


def test_dpop_fallback_round_trip_nonce_ath_and_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "enable_rfc9449", True)
    keyref = _ed25519_keyref()
    jkt = jwk_thumbprint(jwk_from_public_key(keyref.public))
    replay = _ReplayOps()
    nonce_ops = _NonceOps()
    nonce = issue_nonce(issuer=nonce_ops.issue)
    access_token = "capability-access-token"
    proof = make_proof(keyref, "POST", "https://rs.example.com/resource", access_token=access_token, nonce=nonce)

    assert verify_proof(
        proof,
        "POST",
        "https://rs.example.com/resource",
        jkt=jkt,
        access_token=access_token,
        expected_nonce=nonce,
        replay_checker=replay.check,
        nonce_consumer=nonce_ops.consume,
    ) == jkt

    with pytest.raises(ValueError):
        verify_proof(
            proof,
            "POST",
            "https://rs.example.com/resource",
            jkt=jkt,
            access_token=access_token,
            replay_checker=replay.check,
        )


def test_dpop_rejects_ath_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "enable_rfc9449", True)
    keyref = _ed25519_keyref()
    proof = make_proof(keyref, "GET", "https://rs.example.com/userinfo", access_token="token-a")
    with pytest.raises(ValueError):
        verify_proof(
            proof,
            "GET",
            "https://rs.example.com/userinfo",
            access_token="token-b",
            replay_checker=_ReplayOps().check,
        )


def test_hardening_sender_constraint_policy_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "enable_rfc9449", True)
    monkeypatch.setattr(settings, "enable_rfc8705", True)
    deployment = deployment_from_options(profile="hardening")
    request = SimpleNamespace(headers={}, scope={}, method="POST", url="https://issuer.example/token")
    with pytest.raises(OAuthPolicyViolation) as exc_info:
        validate_sender_constraint(request, deployment)
    assert exc_info.value.error == "invalid_request"

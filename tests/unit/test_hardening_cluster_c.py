from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from cryptography.x509.oid import NameOID

from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.config.settings import settings
from tigrbl_auth.standards.oauth2.dpop import (
    clear_runtime_state,
    configure_state_providers,
    issue_nonce,
    jwk_from_public_key,
    jwk_thumbprint,
    make_proof,
    verify_proof,
)
from tigrbl_replay_memory_provider import MemoryReplayCheckProvider, MemorySingleUseNonceProvider
from tigrbl_auth_protocol_oauth.standards.mutual_tls_client_authentication import (
    authenticate_mtls_client,
    presented_certificate_thumbprint,
    thumbprint_from_cert_pem,
    validate_request_certificate_binding,
)
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    OAuthPolicyViolation,
    runtime_security_profile,
    validate_sender_constraint,
)
from tigrbl_auth_protocol_oidc.standards import backchannel_logout, frontchannel_logout
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import build_openid_config


def _generate_cert_pem() -> bytes:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "capability.example")])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(UTC) - timedelta(minutes=1))
        .not_valid_after(datetime.now(UTC) + timedelta(days=1))
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
    configure_state_providers(
        replay=MemoryReplayCheckProvider(), nonce=MemorySingleUseNonceProvider()
    )
    clear_runtime_state()
    keyref = _ed25519_keyref()
    jkt = jwk_thumbprint(jwk_from_public_key(keyref.public))
    nonce = issue_nonce()
    access_token = "capability-access-token"
    proof = make_proof(keyref, "POST", "https://rs.example.com/resource", access_token=access_token, nonce=nonce)

    assert verify_proof(
        proof,
        "POST",
        "https://rs.example.com/resource",
        jkt=jkt,
        access_token=access_token,
        expected_nonce=nonce,
    ) == jkt

    with pytest.raises(ValueError):
        verify_proof(
            proof,
            "POST",
            "https://rs.example.com/resource",
            jkt=jkt,
            access_token=access_token,
        )


def test_dpop_rejects_ath_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "enable_rfc9449", True)
    configure_state_providers(
        replay=MemoryReplayCheckProvider(), nonce=MemorySingleUseNonceProvider()
    )
    clear_runtime_state()
    keyref = _ed25519_keyref()
    proof = make_proof(keyref, "GET", "https://rs.example.com/userinfo", access_token="token-a")
    with pytest.raises(ValueError):
        verify_proof(proof, "GET", "https://rs.example.com/userinfo", access_token="token-b")


def test_hardening_sender_constraint_policy_is_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "enable_rfc9449", True)
    monkeypatch.setattr(settings, "enable_rfc8705", True)
    deployment = deployment_from_options(profile="hardening")
    request = SimpleNamespace(headers={}, scope={}, method="POST", url="https://issuer.example/token")
    with pytest.raises(OAuthPolicyViolation) as exc_info:
        validate_sender_constraint(request, deployment)
    assert exc_info.value.error == "invalid_request"


@pytest.mark.asyncio
async def test_frontchannel_descriptor_and_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    client_id = uuid4()

    class _Registration:
        registration_metadata = {
            "frontchannel_logout_uri": "https://rp.example/frontchannel-logout",
            "frontchannel_logout_session_required": True,
            "frontchannel_retry_window_seconds": 45,
        }

    class _Persistence:
        async def get_client_registration_async(self, resolved_client_id):
            assert resolved_client_id == client_id
            return _Registration()

    monkeypatch.setattr(frontchannel_logout, "_persistence", lambda: _Persistence())
    descriptor = await frontchannel_logout.build_frontchannel_descriptor(
        client_id=client_id,
        sid="sid-123",
        iss="https://issuer.example",
        logout_id=uuid4(),
    )
    assert descriptor is not None
    assert descriptor["delivery"]["status"] == "pending"
    assert descriptor["delivery"]["replay_protected"] is True
    assert descriptor["delivery"]["retry_window_seconds"] == 45
    assert "sid=sid-123" in str(descriptor["redirect_uri"])
    validated = frontchannel_logout.validate_frontchannel_request(
        params={"iss": "https://issuer.example", "sid": "sid-123", "logout_id": descriptor["logout_id"]},
        expected_sid="sid-123",
        expected_iss="https://issuer.example",
        expected_logout_id=descriptor["logout_id"],
    )
    assert validated["logout_id"] == descriptor["logout_id"]


@pytest.mark.asyncio
async def test_backchannel_logout_token_fallback_and_replay(monkeypatch: pytest.MonkeyPatch) -> None:
    client_id = uuid4()
    logout_id = uuid4()
    seen_jti: set[str] = set()

    class _Registration:
        registration_metadata = {
            "backchannel_logout_uri": "https://rp.example/backchannel-logout",
            "backchannel_logout_session_required": True,
        }

    class _Persistence:
        async def get_client_registration_async(self, resolved_client_id):
            assert resolved_client_id == client_id
            return _Registration()

        async def register_backchannel_replay_async(
            self,
            *,
            jti: str,
            issuer: str,
            client_id: str,
            expires_at,
            now,
        ):
            assert issuer == "https://issuer.example"
            assert client_id
            assert expires_at > now
            if jti in seen_jti:
                raise ValueError("replayed logout token")
            seen_jti.add(jti)

    def _missing_jwt_coder_cls():
        raise RuntimeError("no runtime JWT coder in dependency-light checkpoint")

    monkeypatch.setattr(backchannel_logout, "_persistence", lambda: _Persistence())
    monkeypatch.setattr(backchannel_logout, "_jwt_coder_cls", _missing_jwt_coder_cls)
    descriptor = await backchannel_logout.build_backchannel_descriptor(
        client_id=client_id,
        sid="sid-123",
        sub="user-123",
        iss="https://issuer.example",
        logout_id=logout_id,
    )
    assert descriptor is not None
    assert descriptor["delivery"]["status"] == "pending"
    assert descriptor["delivery"]["replay_protected"] is True
    claims = await backchannel_logout.validate_backchannel_logout_token(
        str(descriptor["logout_token"]),
        client_id=client_id,
        issuer="https://issuer.example",
    )
    assert claims["events"]
    assert claims["sid"] == "sid-123"
    with pytest.raises(ValueError):
        await backchannel_logout.validate_backchannel_logout_token(
            str(descriptor["logout_token"]),
            client_id=client_id,
            issuer="https://issuer.example",
        )


def test_hardening_discovery_and_contract_are_truthful_for_sender_constraints_and_logout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "enable_rfc8705", True)
    monkeypatch.setattr(settings, "enable_rfc9449", True)
    monkeypatch.setattr(settings, "enable_rfc9700", True)
    monkeypatch.setattr(settings, "enable_oidc_frontchannel_logout", True)
    monkeypatch.setattr(settings, "enable_oidc_backchannel_logout", True)
    deployment = deployment_from_options(profile="hardening")
    policy = runtime_security_profile(deployment)
    metadata = build_openid_config(deployment)
    openapi = build_openapi_contract(deployment, version="0.0.0-capability")

    assert policy.sender_constraint_required is True
    assert metadata["dpop_signing_alg_values_supported"] == ["EdDSA"]
    assert metadata["tls_client_certificate_bound_access_tokens"] is True
    assert metadata["frontchannel_logout_supported"] is True
    assert metadata["backchannel_logout_supported"] is True
    runtime_meta = openapi["paths"]["/token"]["post"]["x-runtime-profile"]
    assert runtime_meta["query_bearer_disabled"] is True
    assert runtime_meta["form_bearer_disabled"] is True
    logout_schema = openapi["components"]["schemas"]["LogoutResponse"]["properties"]
    assert "frontchannel_delivery" in logout_schema
    assert "backchannel_delivery" in logout_schema
UTC = timezone.utc

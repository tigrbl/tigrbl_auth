from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from urllib.parse import urlencode
from uuid import uuid4

import pytest

from tigrbl_auth.api.rest.schemas import DynamicClientRegistrationIn
from tigrbl_auth.cli.artifacts import deployment_from_options
from tigrbl_auth.config.settings import settings
import tigrbl_identity_storage_runtime.par as par_ops
from tigrbl_identity_storage.tables.client_registration import _route_op as register_ops
from tigrbl_identity_storage.tables.token_record import _route as token_ops
from tigrbl_auth_protocol_oauth.standards.oauth_security_bcp import (
    OAuthPolicyViolation,
    assert_authorization_request_allowed,
    runtime_security_profile,
)
from tigrbl_auth_protocol_oauth.standards.protected_resource_metadata import build_protected_resource_metadata
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import build_openid_config


class _Form(dict):
    def getlist(self, key: str):
        value = self.get(key)
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]


class _FakeRequest:
    def __init__(
        self,
        form_data: dict[str, object] | None = None,
        *,
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
        method: str = "POST",
        url: str = "https://issuer.example/token",
    ) -> None:
        self._form_data = _Form(form_data or {})
        self.headers = headers or {}
        self.body = body or b""
        self.method = method
        self.url = url
        self.scope = {"scheme": "https"}

    async def form(self):
        return self._form_data


class _FakeDB:
    def __init__(self, *scalars):
        self._scalars = list(scalars)
        self.added: list[object] = []
        self.commits = 0

    async def scalar(self, _stmt):
        if not self._scalars:
            return None
        return self._scalars.pop(0)

    def add(self, row):
        self.added.append(row)

    async def commit(self):
        self.commits += 1

    async def refresh(self, _row):
        return None


def _patch_token_handler_records(
    monkeypatch: pytest.MonkeyPatch,
    *,
    client: object,
    registration: object | None = None,
    auth_code: object | None = None,
    user: object | None = None,
) -> None:
    async def _read_handler_record(model, db, ident):
        if model is token_ops.Client:
            return client
        if model is token_ops.AuthCode:
            return auth_code
        if model is token_ops.User:
            return user
        return None

    async def _first_handler_record(model, db, filters):
        if model is token_ops.ClientRegistration:
            return registration
        return None

    async def _delete_handler_record(model, db, ident):
        return None

    monkeypatch.setattr(token_ops, "read_handler_record", _read_handler_record)
    monkeypatch.setattr(token_ops, "first_handler_record", _first_handler_record)
    monkeypatch.setattr(token_ops, "delete_handler_record", _delete_handler_record)


class _SenderConstraint:
    def __init__(self, *, mechanism: str | None = None, token_type: str = "DPoP", jkt: str | None = None, cert_thumbprint: str | None = None):
        self.mechanism = mechanism
        self.token_type = token_type
        self.jkt = jkt
        self.cert_thumbprint = cert_thumbprint
        self.confirmation_claim = {"jkt": jkt} if jkt else ({"x5t#S256": cert_thumbprint} if cert_thumbprint else None)


def _fapi_deployment():
    return deployment_from_options(
        profile="fapi2-security",
        issuer="https://issuer.example",
    )


def test_fapi_discovery_and_resource_metadata_are_profile_specific():
    deployment = _fapi_deployment()
    policy = runtime_security_profile(deployment)
    metadata = build_openid_config(deployment)
    resource_metadata = build_protected_resource_metadata(deployment)

    assert policy.fapi_mode is True
    assert metadata["token_endpoint_auth_methods_supported"] == [
        "private_key_jwt",
        "tls_client_auth",
        "self_signed_tls_client_auth",
    ]
    assert metadata["response_types_supported"] == ["code"]
    assert metadata["require_pushed_authorization_requests"] is True
    assert metadata["authorization_response_iss_parameter_supported"] is True
    assert metadata["mtls_endpoint_aliases"]["token_endpoint"] == "https://issuer.example/token"
    assert resource_metadata["fapi_profiles_supported"] == ["fapi2-security"]
    assert resource_metadata["tls_client_certificate_bound_access_tokens"] is True


def test_fapi_authorization_policy_rejects_non_minimal_front_channel_and_requires_pkce():
    deployment = _fapi_deployment()
    with pytest.raises(OAuthPolicyViolation) as excinfo:
        assert_authorization_request_allowed(
            {
                "_frontchannel_request": True,
                "client_id": "client-1",
                "request_uri": "urn:ietf:params:oauth:request_uri:test",
                "response_type": "code",
                "scope": "openid",
                "redirect_uri": "https://client.example/cb",
                "code_challenge": "challenge",
                "code_challenge_method": "S256",
            },
            deployment,
        )
    assert excinfo.value.error == "invalid_request"

    with pytest.raises(OAuthPolicyViolation) as pkce_exc:
        assert_authorization_request_allowed(
            {
                "response_type": "code",
                "request_uri": "urn:ietf:params:oauth:request_uri:test",
                "client_id": "client-1",
            },
            deployment,
        )
    assert pkce_exc.value.error == "invalid_request"


@pytest.mark.asyncio
async def test_fapi_par_requires_redirect_uri_and_client_auth(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(par_ops, "resolve_deployment", lambda _settings: _fapi_deployment())
    client = SimpleNamespace(id=uuid4(), tenant_id=uuid4())
    registration = SimpleNamespace(registration_metadata={"token_endpoint_auth_method": "private_key_jwt"})

    async def _read_record(model, db, ident):
        return client

    async def _first_record(model, db, filters):
        return registration

    monkeypatch.setattr(par_ops, "read_record", _read_record)
    monkeypatch.setattr(par_ops, "first_record", _first_record)

    missing_redirect_request = _FakeRequest(
        body=urlencode({"client_id": str(client.id), "response_type": "code", "scope": "openid"}).encode("utf-8"),
        url="https://issuer.example/par",
    )
    with pytest.raises(par_ops.HTTPException) as excinfo:
        await par_ops.pushed_authorization_request(request=missing_redirect_request, db=_FakeDB())
    assert excinfo.value.status_code == 400

    authed_request = _FakeRequest(
        body=urlencode(
            {
                "client_id": str(client.id),
                "response_type": "code",
                "scope": "openid",
                "redirect_uri": "https://client.example/cb",
            }
        ).encode("utf-8"),
        url="https://issuer.example/par",
    )
    with pytest.raises(par_ops.HTTPException) as auth_exc:
        await par_ops.pushed_authorization_request(request=authed_request, db=_FakeDB())
    assert auth_exc.value.status_code == 401


@pytest.mark.asyncio
async def test_fapi_registration_rejects_shared_secret_auth(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(register_ops, "resolve_deployment", lambda _settings: _fapi_deployment())
    tenant = SimpleNamespace(id=uuid4(), slug="public")

    async def _first_handler_record(model, db, filters):
        return tenant

    monkeypatch.setattr(register_ops, "first_handler_record", _first_handler_record)
    payload = DynamicClientRegistrationIn(
        tenant_slug="public",
        redirect_uris=["https://client.example/cb"],
        grant_types=["authorization_code", "refresh_token"],
        response_types=["code"],
        token_endpoint_auth_method="client_secret_basic",
    )

    with pytest.raises(register_ops.HTTPException) as excinfo:
        await register_ops._validated_registration_payload(db=_FakeDB(tenant), payload=payload)
    assert excinfo.value.status_code == 400


@pytest.mark.asyncio
async def test_fapi_token_request_rejects_shared_secret_auth(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(token_ops, "_require_tls", lambda request: None)
    monkeypatch.setattr(token_ops, "resolve_deployment", lambda _settings: _fapi_deployment())
    client = SimpleNamespace(id=uuid4(), tenant_id=uuid4(), verify_secret=lambda secret: True)
    registration = SimpleNamespace(registration_metadata={"token_endpoint_auth_method": "client_secret_basic"})
    _patch_token_handler_records(monkeypatch, client=client, registration=registration)
    request = _FakeRequest(
        {"grant_type": "client_credentials", "client_id": str(client.id), "client_secret": "secret"},
        url="https://issuer.example/token",
    )

    response = await token_ops.token_request(request=request, db=_FakeDB(client, registration))
    assert response.status_code == 401
    assert response.content["error"] == "invalid_client"


@pytest.mark.asyncio
async def test_fapi_private_key_jwt_uses_issuer_as_assertion_audience(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(token_ops, "_require_tls", lambda request: None)
    monkeypatch.setattr(token_ops, "resolve_deployment", lambda _settings: _fapi_deployment())
    monkeypatch.setattr(token_ops, "assert_token_request_allowed", lambda data, deployment: None)
    captured: dict[str, object] = {}

    def _authenticate(**kwargs):
        captured["audience"] = kwargs["audience"]
        return {"iss": kwargs["client_id"]}

    async def _issue_pair(db, **kwargs):
        captured["audience_claim"] = kwargs.get("audience")
        return ("access-token", "refresh-token")

    monkeypatch.setattr(token_ops, "authenticate_client_assertion", _authenticate)
    monkeypatch.setattr(token_ops, "validate_sender_constraint", lambda *args, **kwargs: _SenderConstraint(mechanism="dpop", jkt="jkt-1"))
    monkeypatch.setattr(token_ops, "issue_token_pair_records", _issue_pair)

    client = SimpleNamespace(id=uuid4(), tenant_id=uuid4())
    registration = SimpleNamespace(registration_metadata={"token_endpoint_auth_method": "private_key_jwt"})
    _patch_token_handler_records(monkeypatch, client=client, registration=registration)
    request = _FakeRequest(
        {
            "grant_type": "client_credentials",
            "client_id": str(client.id),
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": "jwt",
        },
        headers={"DPoP": "proof"},
        url="https://issuer.example/token",
    )

    response = await token_ops.token_request(request=request, db=_FakeDB(client, registration))
    assert captured["audience"] == "https://issuer.example"
    assert captured["audience_claim"] == "https://authn.example.com/resource"
    assert response["access_token"] == "access-token"
    assert response["token_type"] == "DPoP"


@pytest.mark.asyncio
async def test_fapi_authorization_code_requires_sender_key_continuity(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(token_ops, "_require_tls", lambda request: None)
    monkeypatch.setattr(token_ops, "resolve_deployment", lambda _settings: _fapi_deployment())
    monkeypatch.setattr(token_ops, "validate_sender_constraint", lambda *args, **kwargs: _SenderConstraint(mechanism="dpop", jkt="jkt-live"))
    monkeypatch.setattr(token_ops, "verify_code_challenge", lambda verifier, challenge: True)

    async def _issue_pair(db, **kwargs):
        return ("access-token", "refresh-token")

    async def _mint_id_token(**kwargs):
        return "id-token"

    monkeypatch.setattr(token_ops, "mint_id_token", _mint_id_token)
    monkeypatch.setattr(token_ops, "issue_token_pair_records", _issue_pair)
    monkeypatch.setattr(
        token_ops,
        "authenticate_client_assertion",
        lambda **kwargs: {"iss": kwargs["client_id"]},
    )

    client = SimpleNamespace(id=uuid4(), tenant_id=uuid4(), verify_secret=lambda secret: True)
    registration = SimpleNamespace(registration_metadata={"token_endpoint_auth_method": "private_key_jwt"})
    auth_code = SimpleNamespace(
        id=uuid4(),
        client_id=client.id,
        redirect_uri="https://client.example/cb",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
        code_challenge="challenge",
        user_id=uuid4(),
        tenant_id=uuid4(),
        scope="openid",
        nonce="nonce",
        session_id=None,
        claims={"_dpop_jkt": "jkt-init"},
    )
    _patch_token_handler_records(monkeypatch, client=client, registration=registration, auth_code=auth_code)
    request = _FakeRequest(
        {
            "grant_type": "authorization_code",
            "client_id": str(client.id),
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": "jwt",
            "code": str(auth_code.id),
            "redirect_uri": auth_code.redirect_uri,
            "code_verifier": "verifier",
        },
        url="https://issuer.example/token",
    )

    response = await token_ops.token_request(request=request, db=_FakeDB(client, registration, auth_code))
    assert response.status_code == 400
    assert response.content["error"] == "invalid_grant"

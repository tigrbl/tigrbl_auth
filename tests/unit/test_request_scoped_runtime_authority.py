from __future__ import annotations

import asyncio
from types import SimpleNamespace
from uuid import uuid4

from tigrbl_auth.api.rest.schemas import DynamicClientRegistrationIn
import tigrbl_identity_storage_runtime.par as par_ops
from tigrbl_identity_storage.tables.client_registration import _route_op as register_ops
import tigrbl_identity_storage_runtime.device_authorization as device_auth_ops
import tigrbl_identity_storage_runtime.logout as logout_ops
from tigrbl_auth_protocol_oidc.standards import rp_initiated_logout as rp_logout
from tigrbl_auth_protocol_oidc.standards.session_mgmt import compute_session_state, session_state_for_client


def test_session_state_hash_changes_with_effective_issuer() -> None:
    session_id = uuid4()
    tenant_state = compute_session_state(
        client_id="client-1",
        redirect_uri="https://rp.example/callback",
        session_id=session_id,
        salt="salt-a",
        issuer="https://tenant-a.example.com",
    )
    other_tenant_state = compute_session_state(
        client_id="client-1",
        redirect_uri="https://rp.example/callback",
        session_id=session_id,
        salt="salt-a",
        issuer="https://tenant-b.example.com",
    )
    assert tenant_state != other_tenant_state


def test_session_state_for_client_uses_request_scoped_deployment_issuer() -> None:
    session_row = SimpleNamespace(id=uuid4(), session_state_salt="salt-z")
    deployment = SimpleNamespace(
        issuer="https://tenant-a.example.com",
        flag_enabled=lambda name: name == "enable_oidc_session_management",
    )
    result = session_state_for_client(
        session_row,
        client_id="client-1",
        redirect_uri="https://rp.example/callback",
        deployment=deployment,
    )
    expected = compute_session_state(
        client_id="client-1",
        redirect_uri="https://rp.example/callback",
        session_id=session_row.id,
        salt="salt-z",
        issuer="https://tenant-a.example.com",
    )
    assert result == expected


def test_build_logout_plan_uses_deployment_issuer_for_fanout(monkeypatch) -> None:
    session_row = SimpleNamespace(id=uuid4(), user_id=uuid4())
    logout_row = SimpleNamespace(id=uuid4(), logout_metadata={}, frontchannel_required=True, backchannel_required=True)
    observed: dict[str, object] = {}

    class _Persistence:
        async def get_latest_logout_for_session_async(self, session_id):
            assert session_id == session_row.id
            return None

        async def terminate_session_async(self, session_id, **kwargs):
            assert session_id == session_row.id
            return logout_row

        async def update_logout_metadata_async(self, logout_id, *, metadata=None, status=None):
            assert logout_id == logout_row.id
            logout_row.logout_metadata = dict(metadata or {})
            return logout_row

    async def _frontchannel_builder(**kwargs):
        observed["front_iss"] = kwargs["iss"]
        return {"delivery": {"status": "pending", "attempts": 0, "max_retries": 3}}

    async def _backchannel_builder(**kwargs):
        observed["back_iss"] = kwargs["iss"]
        return {"delivery": {"status": "pending", "attempts": 0, "max_retries": 3}}

    monkeypatch.setattr(rp_logout, "_persistence", lambda: _Persistence())
    monkeypatch.setattr(rp_logout, "_frontchannel_builder", lambda: _frontchannel_builder)
    monkeypatch.setattr(rp_logout, "_backchannel_builder", lambda: _backchannel_builder)

    deployment = SimpleNamespace(
        issuer="https://tenant-a.example.com",
        flag_enabled=lambda name: True,
    )
    result = asyncio.run(
        rp_logout.build_logout_plan(
            session_row=session_row,
            client_id=uuid4(),
            post_logout_redirect_uri="https://rp.example/logout/callback",
            state="state-1",
            deployment=deployment,
        )
    )
    assert result is logout_row
    assert observed["front_iss"] == "https://tenant-a.example.com"
    assert observed["back_iss"] == "https://tenant-a.example.com"


def test_logout_request_uses_request_scoped_deployment_for_issuer_binding(monkeypatch) -> None:
    deployment = SimpleNamespace(
        issuer="https://tenant-a.example.com",
        flag_enabled=lambda name: name == "enable_oidc_rp_initiated_logout",
    )
    session_row = SimpleNamespace(id=uuid4(), tenant_id=uuid4(), user_id=uuid4())
    observed: dict[str, object] = {}

    async def _resolve_browser_session(request, *, deployment=None):
        observed["session_deployment_issuer"] = getattr(deployment, "issuer", None)
        return session_row

    async def _validate_logout_request(**kwargs):
        observed["validated_issuer"] = kwargs["issuer"]
        return rp_logout.LogoutRequestContext(
            client_id=uuid4(),
            post_logout_redirect_uri=None,
            id_token_hint_claims={"sid": str(session_row.id)},
        )

    async def _build_logout_plan(**kwargs):
        observed["planned_issuer"] = kwargs["deployment"].issuer
        return SimpleNamespace(
            id=uuid4(),
            frontchannel_required=False,
            backchannel_required=False,
            logout_metadata={},
        )

    async def _append_audit_event_async(**kwargs):
        observed["audit_event"] = kwargs["event_type"]

    monkeypatch.setattr(logout_ops, "deployment_from_request", lambda request, fallback_settings: deployment)
    monkeypatch.setattr(logout_ops, "resolve_browser_session", _resolve_browser_session)
    monkeypatch.setattr(logout_ops, "validate_logout_request", _validate_logout_request)
    monkeypatch.setattr(logout_ops, "build_logout_plan", _build_logout_plan)
    monkeypatch.setattr(logout_ops, "append_audit_event_async", _append_audit_event_async)
    monkeypatch.setattr(logout_ops, "clear_session_cookie", lambda response: response.headers.__setitem__("x-test-cookie-cleared", "1"))

    request = SimpleNamespace(
        app=SimpleNamespace(state=SimpleNamespace(tigrbl_auth_deployment=deployment)),
        query_params={},
        body=b"",
        cookies={},
    )
    response = asyncio.run(logout_ops.logout_request(request=request, db=None))
    assert response.status_code == 200
    assert observed["session_deployment_issuer"] == "https://tenant-a.example.com"
    assert observed["validated_issuer"] == "https://tenant-a.example.com"
    assert observed["planned_issuer"] == "https://tenant-a.example.com"
    assert observed["audit_event"] == "session.logout"
    assert response.headers["x-test-cookie-cleared"] == "1"


def test_register_client_uses_request_scoped_registration_client_uri(monkeypatch) -> None:
    tenant_id = uuid4()
    deployment = SimpleNamespace(issuer="https://tenant-a.example.com")

    class _FakeClient:
        def __init__(self, tenant_id, client_id, client_secret, redirects):
            self.tenant_id = tenant_id
            self.id = client_id
            self.client_secret_hash = f"hash:{client_secret}".encode()
            self.redirect_uris = " ".join(redirects)
            self.grant_types = ""
            self.response_types = ""

        @staticmethod
        def new(tenant_id, client_id, client_secret, redirects):
            return _FakeClient(tenant_id, client_id, client_secret, redirects)

    class _DB:
        def add(self, obj):
            return None

        async def commit(self):
            return None

        async def refresh(self, obj):
            return None

    async def _validated_registration_payload(**kwargs):
        return SimpleNamespace(id=tenant_id), {"native_application": False, "pkce_required": False}

    async def _create_handler_record(model, db, payload):
        if model is _FakeClient:
            return SimpleNamespace(**payload)
        return SimpleNamespace(
            id=uuid4(),
            registration_metadata=payload["registration_metadata"],
            registration_client_uri=payload["registration_client_uri"],
            issued_at=None,
        )

    async def _registration_response(**kwargs):
        return {"registration_client_uri": kwargs["registration"].registration_client_uri}

    monkeypatch.setattr(register_ops, "Client", _FakeClient)
    monkeypatch.setattr(register_ops, "deployment_from_request", lambda request, fallback_settings: deployment)
    monkeypatch.setattr(register_ops, "_validated_registration_payload", _validated_registration_payload)
    monkeypatch.setattr(register_ops, "create_handler_record", _create_handler_record)
    monkeypatch.setattr(register_ops, "_registration_response", _registration_response)
    monkeypatch.setattr(register_ops, "append_audit_event_record", lambda db, **kwargs: asyncio.sleep(0))
    monkeypatch.setattr(register_ops.secrets, "token_urlsafe", lambda length: "token-value")
    monkeypatch.setattr(register_ops, "runtime_security_profile", lambda deployment: SimpleNamespace(fapi_mode=False, allowed_client_auth_methods=()))

    payload = DynamicClientRegistrationIn(
        tenant_slug="tenant-a",
        redirect_uris=["https://client.example/callback"],
    )
    result = asyncio.run(
        register_ops.register_client(
            request=SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(tigrbl_auth_deployment=deployment))),
            db=_DB(),
            payload=payload,
        )
    )
    assert result["registration_client_uri"].startswith("https://tenant-a.example.com/register/")


def test_device_authorization_uses_request_scoped_verification_uri(monkeypatch) -> None:
    deployment = SimpleNamespace(
        issuer="https://tenant-a.example.com",
        flag_enabled=lambda name: True,
    )
    client = SimpleNamespace(id=uuid4(), tenant_id=uuid4())

    class _DB:
        pass

    async def _read_record(model, db, ident):
        return client

    async def _create_record(model, db, payload):
        return SimpleNamespace(id=payload.get("device_code"), **payload)

    monkeypatch.setattr(device_auth_ops, "deployment_from_request", lambda request, fallback_settings: deployment)
    monkeypatch.setattr(device_auth_ops, "generate_device_code", lambda: "device-code-1")
    monkeypatch.setattr(device_auth_ops, "generate_user_code", lambda: "USER-CODE")
    monkeypatch.setattr(device_auth_ops, "read_record", _read_record)
    monkeypatch.setattr(device_auth_ops, "create_record", _create_record)
    monkeypatch.setattr(device_auth_ops.AuditEvent, "record", lambda db, **kwargs: asyncio.sleep(0))

    request = SimpleNamespace(
        app=SimpleNamespace(state=SimpleNamespace(tigrbl_auth_deployment=deployment)),
        body=b"client_id=00000000-0000-0000-0000-000000000001&scope=openid",
    )
    result = asyncio.run(device_auth_ops.device_authorization_request(request=request, db=_DB()))
    assert result["verification_uri"] == "https://tenant-a.example.com/device"
    assert result["verification_uri_complete"] == "https://tenant-a.example.com/device?user_code=USER-CODE"


def test_normalized_par_params_uses_request_scoped_issuer_for_request_object_audience(monkeypatch) -> None:
    deployment = SimpleNamespace(issuer="https://tenant-a.example.com", flag_enabled=lambda name: True)
    observed: dict[str, object] = {}

    async def _parse_request_object(token, **kwargs):
        observed["expected_audience"] = kwargs["expected_audience"]
        return {"client_id": "client-1"}

    monkeypatch.setattr(par_ops, "parse_request_object", _parse_request_object)
    result = asyncio.run(
        par_ops._normalized_par_params(
            {"client_id": "client-1", "request": "signed-request-object"},
            deployment,
        )
    )
    assert result["client_id"] == "client-1"
    assert observed["expected_audience"] == "https://tenant-a.example.com"

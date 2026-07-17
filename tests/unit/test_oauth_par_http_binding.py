from __future__ import annotations

from types import SimpleNamespace

import pytest
from httpx import ASGITransport, AsyncClient
from tigrbl import TigrblApp

from tigrbl_auth_router_oauth_par import (
    build_pushed_authorization_router,
    request_body_data,
)
from tigrbl_auth_protocol_oauth.standards.pushed_authorization_requests import (
    RFC9126PushedAuthorizationService,
)
from tigrbl_identity_contracts.oauth import (
    PushedAuthorizationPersistenceRequest,
)
from tigrbl_pushed_authorization_capability import PushedAuthorizationCapability
import tigrbl_auth_backend_app_core.surfaces.par_surface as par_surface


@pytest.mark.asyncio
async def test_par_binding_materializes_json_and_urlencoded_bodies() -> None:
    assert await request_body_data(
        SimpleNamespace(body=b'{"client_id":"client-1","scope":"openid"}')
    ) == {"client_id": "client-1", "scope": "openid"}
    assert await request_body_data(
        SimpleNamespace(body=b"client_id=client-1&resource=api-a&resource=api-b")
    ) == {"client_id": "client-1", "resource": ["api-a", "api-b"]}


def test_par_binding_builds_post_par_carrier() -> None:
    service = RFC9126PushedAuthorizationService(
        PushedAuthorizationCapability(
            lambda request: {
                "request_uri": "urn:ietf:params:oauth:request_uri:abc",
                "expires_in": 90,
            }
        )
    )
    router = build_pushed_authorization_router(
        service_for_request=lambda request, db: service,
        normalize_request=lambda request, params: params,
        authorize_caller=lambda request, params, db: (
            PushedAuthorizationPersistenceRequest(
                client_id=str(params["client_id"]),
                tenant_id=None,
                params=params,
            )
        ),
        observe_response=None,
        get_db=lambda: object(),
    )

    route = next(
        item for item in router.routes if getattr(item, "path", None) == "/par"
    )
    assert "POST" in route.methods


@pytest.mark.asyncio
async def test_par_binding_executes_successful_http_round_trip() -> None:
    persisted = []
    observed = []

    async def persist(request):
        persisted.append(request)
        return {
            "request_uri": "urn:ietf:params:oauth:request_uri:round-trip",
            "expires_in": 90,
            "record_id": "par-1",
        }

    service = RFC9126PushedAuthorizationService(
        PushedAuthorizationCapability(persist)
    )
    router = build_pushed_authorization_router(
        service_for_request=lambda request, db: service,
        normalize_request=lambda request, params: params,
        authorize_caller=lambda request, params, db: (
            PushedAuthorizationPersistenceRequest(
                client_id=str(params["client_id"]),
                tenant_id="tenant-1",
                params=params,
            )
        ),
        observe_response=lambda request, payload: observed.append(dict(payload)),
        get_db=lambda: object(),
    )
    app = TigrblApp()
    app.include_router(router)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.post(
            "/par",
            data={"client_id": "client-1", "scope": "openid"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "request_uri": "urn:ietf:params:oauth:request_uri:round-trip",
        "expires_in": 90,
    }
    assert persisted[0].params == {"client_id": "client-1", "scope": "openid"}
    assert observed == [response.json()]


@pytest.mark.asyncio
async def test_par_runtime_does_not_persist_client_authentication_secrets(
    monkeypatch,
) -> None:
    client = SimpleNamespace(id="client-1", tenant_id="tenant-1")
    deployment = SimpleNamespace(flag_enabled=lambda name: False)
    policy = SimpleNamespace(
        par_redirect_uri_required=False,
        par_client_auth_required=False,
        request_uri_max_lifetime_seconds=90,
    )

    async def read_record(model, db, ident):
        return client

    monkeypatch.setattr(
        par_surface,
        "_resolve_request_deployment",
        lambda request: deployment,
    )
    monkeypatch.setattr(par_surface, "runtime_security_profile", lambda value: policy)
    monkeypatch.setattr(par_surface, "read_record", read_record)
    monkeypatch.setattr(par_surface, "dpop_proof_from_request", lambda request: None)
    monkeypatch.setattr(
        par_surface,
        "client_certificate_thumbprint_from_request",
        lambda request: None,
    )

    authorized = await par_surface.authorize_pushed_authorization_caller(
        SimpleNamespace(headers={}, method="POST", url="https://issuer.example/par"),
        {
            "client_id": "00000000-0000-0000-0000-000000000001",
            "scope": "openid",
            "client_assertion": "signed-secret",
            "client_assertion_type": "jwt-bearer",
            "client_secret": "secret",
        },
        object(),
    )

    assert authorized.params == {"client_id": "00000000-0000-0000-0000-000000000001", "scope": "openid"}

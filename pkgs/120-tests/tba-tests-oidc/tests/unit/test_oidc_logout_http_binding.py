from __future__ import annotations

from uuid import uuid4

import pytest
from tba_runtime_oidc_provider_logout import (
    LogoutRequest,
    LogoutRuntime,
    LogoutSession,
    LogoutStatus,
    ValidatedLogout,
)
from httpx import ASGITransport, AsyncClient
from tigrbl import TigrblApp
from tba_protocol_oidc.standards.rp_initiated_logout import (
    validate_post_logout_redirect_uri,
)
from tba_router_oidc_logout import (
    build_logout_router,
    include_logout_endpoint,
)


def _router(target):
    return build_logout_router(logout_request=target, get_db=lambda: object())


def test_http_binding_builds_get_and_post_logout_carriers() -> None:
    async def logout_request(*, request, db):
        return {"status": "logged_out"}

    route = next(
        item
        for item in _router(logout_request).routes
        if getattr(item, "path", None) == "/logout"
    )

    assert route.methods == {"GET", "POST"}


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "POST"])
async def test_http_binding_delegates_each_logout_method(method: str) -> None:
    observed = []

    async def logout_request(*, request, db):
        observed.append((request.method, db))
        return {"status": "logged_out"}

    app = TigrblApp()
    app.include_router(_router(logout_request))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.request(method, "/logout")

    assert response.status_code == 200
    assert response.json() == {"status": "logged_out"}
    assert observed[0][0] == method


def test_http_binding_mounts_logout_carrier_once() -> None:
    async def logout_request(*, request, db):
        return {"status": "logged_out"}

    router = _router(logout_request)
    app = TigrblApp()
    include_logout_endpoint(app, router)
    include_logout_endpoint(app, router)

    paths = [getattr(route, "path", None) for route in app.router.routes]
    assert paths.count("/logout") == 1


@pytest.mark.asyncio
async def test_provider_runtime_handoff_through_get_and_post() -> None:
    issuer = "https://issuer.example"
    redirect = "https://rp.example/done"
    expected = LogoutRequest(issuer, "fixture-client", "verified-hint", redirect, "s")
    session = LogoutSession(issuer, "session-1", "alice")
    other = LogoutSession("https://second.example", "session-2", "bob")
    active = {session, other}
    attempts = {}

    class AttemptStore:
        async def save(self, token, attempt):
            attempts[token] = attempt

        async def consume(self, token, *, issuer, browser_binding, now):
            attempt = attempts.get(token)
            if (
                attempt is None
                or attempt.request.issuer != issuer
                or attempt.browser_binding != browser_binding
                or attempt.expires_at <= now
            ):
                return None
            return attempts.pop(token)

    async def validate(value, current):
        assert value == expected
        return ValidatedLogout(
            value.client_id, value.post_logout_redirect_uri, current == session
        )

    async def revoke(current, validated):
        if current not in active:
            return False
        active.remove(current)
        return True

    runtime = LogoutRuntime(validate, revoke, AttemptStore())

    async def handler(*, request, db):
        if request.method == "POST":
            from urllib.parse import parse_qs

            form = parse_qs((request.body or b"").decode("utf-8"))
            received_hint = form["id_token_hint"][0]
            value = LogoutRequest(
                issuer, "fixture-client", received_hint, redirect, "s"
            )
            result = await runtime.handoff(value, browser_binding="first-party-proof")
        else:
            result = await runtime.resume(
                request.query_params["handoff"],
                issuer,
                session,
                browser_binding="first-party-proof",
            )
        return {
            "status": result.status.value,
            "handoff": result.token,
            "redirect_uri": result.redirect_uri,
        }

    app = TigrblApp()
    app.include_router(_router(handler))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=issuer,
    ) as client:
        post = await client.post("/logout", data={"id_token_hint": "verified-hint"})
        assert post.status_code == 200
        assert post.json()["status"] == LogoutStatus.HANDOFF_REQUIRED.value
        assert active == {session, other}
        handoff = post.json()["handoff"]
        completed = await client.get("/logout", params={"handoff": handoff})
        repeated = await client.get("/logout", params={"handoff": handoff})
    assert completed.status_code == 200
    assert completed.json()["status"] == LogoutStatus.COMPLETED.value
    assert completed.json()["redirect_uri"] == redirect + "?state=s"
    assert repeated.json()["status"] == LogoutStatus.REJECTED.value
    assert active == {other}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "return_uri", ["http://rp.example/callback", "https://rp.example/unregistered"]
)
async def test_http_binding_rejects_unregistered_logout_redirect(return_uri: str) -> None:
    async def logout_request(*, request, db):
        return await validate_post_logout_redirect_uri(
            client_id=uuid4(),
            post_logout_redirect_uri=return_uri,
            registration_metadata={
                "post_logout_redirect_uris": ["https://rp.example/callback"]
            },
        )

    app = TigrblApp()
    app.include_router(_router(logout_request))
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://issuer.example",
    ) as client:
        response = await client.get("/logout")

    assert response.status_code == 400
    assert "location" not in response.headers

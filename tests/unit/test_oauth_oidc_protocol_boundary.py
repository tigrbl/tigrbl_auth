from __future__ import annotations

import ast
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_auth_protocol_oauth import (  # noqa: E402
    DPoPProof,
    InMemoryOAuthRepository,
    OAuthClient,
    OAuthError,
    OAuthGrantStatus,
    OAuthProtocolService,
    sha256_thumbprint,
)
from tigrbl_auth_protocol_oidc import (  # noqa: E402
    LogoutRequest,
    OidcProviderError,
    OidcProviderRuntime,
    OidcSessionStatus,
    TenantBranding,
    new_login_request,
)


NOW = datetime(2026, 5, 23, 12, 0, tzinfo=timezone.utc)


def _oauth_service() -> OAuthProtocolService:
    repo = InMemoryOAuthRepository()
    service = OAuthProtocolService(repository=repo, now=lambda: NOW)
    service.register_client(
        OAuthClient(
            client_id="client-a",
            tenant_id="tenant-a",
            allowed_scopes=("openid", "profile", "tenant.read", "tenant.write"),
            redirect_uris=("https://rp.example.test/callback",),
            jwk_thumbprint=sha256_thumbprint("client-a-dpop-key"),
            mtls_thumbprint=sha256_thumbprint("client-a-cert"),
        )
    )
    return service


@pytest.mark.unit
def test_oauth_oidc_t0_public_surfaces_are_importable() -> None:
    service = _oauth_service()
    request = new_login_request(
        tenant_id="tenant-a",
        client_id="client-a",
        redirect_uri="https://rp.example.test/callback",
        scopes=("openid", "profile"),
    )

    assert service.repository.get_client("client-a") is not None
    assert request.scope == ("openid", "profile")


@pytest.mark.unit
def test_oauth_t1_device_flow_token_exchange_dpop_and_mtls() -> None:
    service = _oauth_service()
    grant = service.start_device_authorization(
        client_id="client-a", scopes=("openid", "tenant.read")
    )

    with pytest.raises(OAuthError) as pending:
        service.poll_device_authorization(grant.device_code)
    assert pending.value.code == "authorization_pending"

    approved = service.approve_device_authorization(
        grant.device_code, subject="user:123"
    )
    result = service.poll_device_authorization(approved.device_code)

    assert approved.status == OAuthGrantStatus.APPROVED
    assert result.subject == "user:123"
    assert result.scopes == ("openid", "tenant.read")

    exchanged = service.exchange_token(
        client_id="client-a",
        subject_token_subject="user:123",
        requested_subject="service:worker",
        audience="api://tenant-a",
        scopes=("tenant.read",),
        actor="user:123",
    )
    assert exchanged.subject == "service:worker"
    assert exchanged.actor == "user:123"

    proof = DPoPProof(
        jti="proof-1",
        htm="POST",
        htu="https://issuer.example.test/token",
        iat=int(NOW.timestamp()),
        jwk_thumbprint=sha256_thumbprint("client-a-dpop-key"),
    )
    service.validate_dpop(
        client_id="client-a",
        proof=proof,
        method="POST",
        url="https://issuer.example.test/token",
    )
    service.validate_mtls_client(
        client_id="client-a",
        certificate_thumbprint=sha256_thumbprint("client-a-cert"),
    )


@pytest.mark.unit
def test_oauth_t2_hardening_rejects_replay_bad_scope_bad_actor_and_bad_mtls() -> None:
    service = _oauth_service()
    proof = DPoPProof(
        jti="proof-1",
        htm="POST",
        htu="https://issuer.example.test/token",
        iat=int(NOW.timestamp()),
        jwk_thumbprint=sha256_thumbprint("client-a-dpop-key"),
    )
    service.validate_dpop(
        client_id="client-a",
        proof=proof,
        method="POST",
        url="https://issuer.example.test/token",
    )

    with pytest.raises(OAuthError) as replay:
        service.validate_dpop(
            client_id="client-a",
            proof=proof,
            method="POST",
            url="https://issuer.example.test/token",
        )
    with pytest.raises(OAuthError) as scope:
        service.start_device_authorization(client_id="client-a", scopes=("admin.*",))
    with pytest.raises(OAuthError) as actor:
        service.exchange_token(
            client_id="client-a",
            subject_token_subject="user:123",
            requested_subject="service:worker",
            audience="api://tenant-a",
            scopes=("tenant.read",),
            actor="user:other",
        )
    with pytest.raises(OAuthError) as mtls:
        service.validate_mtls_client(
            client_id="client-a", certificate_thumbprint="wrong"
        )

    assert replay.value.code == "use_dpop_nonce"
    assert scope.value.code == "invalid_scope"
    assert actor.value.code == "invalid_request"
    assert mtls.value.code == "invalid_client"


@pytest.mark.unit
def test_oidc_t1_hosted_login_white_label_session_and_logout() -> None:
    runtime = OidcProviderRuntime(
        allowed_redirect_uris={
            "client-a": (
                "https://rp.example.test/callback",
                "https://rp.example.test/logout",
            )
        },
        frontchannel_logout_uris={
            "client-a": ("https://rp.example.test/frontchannel-logout",)
        },
        backchannel_logout_uris={
            "client-a": ("https://rp.example.test/backchannel-logout",)
        },
        now=lambda: NOW,
    )
    request = new_login_request(
        tenant_id="tenant-a",
        client_id="client-a",
        redirect_uri="https://rp.example.test/callback",
        scopes=("openid", "profile"),
    )
    page = runtime.render_hosted_login(
        request,
        TenantBranding(
            tenant_id="tenant-a",
            display_name="<Tenant A>",
            logo_uri="/assets/tenant-a/logo.svg",
            primary_color="#005f73",
        ),
    )
    session = runtime.create_session(
        tenant_id="tenant-a",
        subject="user:123",
        client_id="client-a",
        nonce=request.nonce,
    )
    plan = runtime.build_logout_plan(
        LogoutRequest(
            tenant_id="tenant-a",
            client_id="client-a",
            session_id=session.session_id,
            post_logout_redirect_uri="https://rp.example.test/logout",
            state="logout-state",
        )
    )

    assert "&lt;Tenant A&gt;" in page.html
    assert "<Tenant A>" not in page.html
    assert runtime.sessions[session.session_id].status == OidcSessionStatus.LOGGED_OUT
    assert plan.frontchannel_notifications == (
        "https://rp.example.test/frontchannel-logout",
    )
    assert plan.backchannel_notifications == (
        "https://rp.example.test/backchannel-logout",
    )
    assert plan.redirect_uri == "https://rp.example.test/logout"


@pytest.mark.unit
def test_oidc_t2_rejects_unregistered_redirect_logo_policy_and_session_mismatch() -> (
    None
):
    runtime = OidcProviderRuntime(
        allowed_redirect_uris={"client-a": ("https://rp.example.test/callback",)},
        now=lambda: NOW,
    )
    request = new_login_request(
        tenant_id="tenant-a",
        client_id="client-a",
        redirect_uri="https://rp.example.test/callback",
        scopes=("openid",),
    )
    session = runtime.create_session(
        tenant_id="tenant-a",
        subject="user:123",
        client_id="client-a",
        nonce=request.nonce,
    )

    with pytest.raises(OidcProviderError, match="outside the tenant asset policy"):
        runtime.render_hosted_login(
            request,
            TenantBranding(
                tenant_id="tenant-a",
                display_name="Tenant A",
                logo_uri="https://cdn.example.test/logo.svg",
            ),
        )
    with pytest.raises(OidcProviderError, match="redirect URI"):
        runtime.build_logout_plan(
            LogoutRequest(
                tenant_id="tenant-a",
                client_id="client-a",
                session_id=session.session_id,
                post_logout_redirect_uri="https://evil.example.test/logout",
            )
        )
    with pytest.raises(OidcProviderError, match="does not match"):
        runtime.build_logout_plan(
            LogoutRequest(
                tenant_id="tenant-b",
                client_id="client-a",
                session_id=session.session_id,
            )
        )


@pytest.mark.unit
def test_oauth_oidc_t2_public_boundary_has_no_forbidden_imports() -> None:
    root = Path("pkgs") / "50-protocols"
    files = [
        root / "tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/__init__.py",
        root / "tigrbl-auth-protocol-oauth/src/tigrbl_auth_protocol_oauth/protocol.py",
        root / "tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/__init__.py",
        root / "tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/provider.py",
    ]
    forbidden = {
        "tigrbl_auth",
        "tigrbl_identity_admin",
        "tigrbl_authz_resource_server",
        "tigrbl_auth_protocol_rp",
        "tigrbl_identity_server",
    }

    imports: set[str] = set()
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imports.add(node.module.split(".")[0])

    assert imports.isdisjoint(forbidden)


@pytest.mark.unit
def test_protocol_and_capability_layers_do_not_define_dataclasses() -> None:
    # Capability packages orchestrate contracts and must not redefine data
    # models. Protocol packages may own revision-specific wire/configuration
    # dataclasses and version records.
    roots = (Path("pkgs") / "40-capabilities",)
    offenders: list[str] = []

    for root in roots:
        for file in root.rglob("*.py"):
            if file.name == "versions.py":
                continue
            tree = ast.parse(file.read_text(encoding="utf-8"))
            dataclass_aliases = {"dataclass"}
            dataclasses_module_aliases = {"dataclasses"}
            for node in tree.body:
                if isinstance(node, ast.ImportFrom) and node.module == "dataclasses":
                    dataclass_aliases.update(
                        alias.asname or alias.name
                        for alias in node.names
                        if alias.name == "dataclass"
                    )
                elif isinstance(node, ast.Import):
                    dataclasses_module_aliases.update(
                        alias.asname or alias.name
                        for alias in node.names
                        if alias.name == "dataclasses"
                    )
            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                for decorator in node.decorator_list:
                    target = (
                        decorator.func if isinstance(decorator, ast.Call) else decorator
                    )
                    if isinstance(target, ast.Name) and target.id in dataclass_aliases:
                        offenders.append(f"{file.as_posix()}:{node.lineno}:{node.name}")
                    elif (
                        isinstance(target, ast.Attribute)
                        and target.attr == "dataclass"
                        and isinstance(target.value, ast.Name)
                        and target.value.id in dataclasses_module_aliases
                    ):
                        offenders.append(f"{file.as_posix()}:{node.lineno}:{node.name}")

    assert offenders == []

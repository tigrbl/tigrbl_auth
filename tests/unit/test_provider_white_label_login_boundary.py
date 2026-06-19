from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_auth_protocol_oidc import (  # noqa: E402
    LoginThemeAssetPolicy,
    OidcProviderError,
    OidcProviderRuntime,
    TenantBranding,
    TenantBrandingRegistry,
    new_login_request,
    render_login_template,
)


def _runtime() -> OidcProviderRuntime:
    return OidcProviderRuntime(
        allowed_redirect_uris={
            "client-a": ("https://rp.example.test/callback",),
            "client-b": ("https://rp-b.example.test/callback",),
        }
    )


def _request(*, tenant_id: str = "tenant-a", client_id: str = "client-a", redirect_uri: str = "https://rp.example.test/callback"):
    return new_login_request(
        tenant_id=tenant_id,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=("openid", "profile"),
    )


@pytest.mark.unit
def test_provider_white_label_t0_public_surfaces_are_importable() -> None:
    policy = LoginThemeAssetPolicy(allowed_asset_prefixes=("/tenant-assets/tenant-a/",))
    registry = TenantBrandingRegistry(asset_policy=policy)
    branding = registry.set(
        TenantBranding(
            tenant_id="tenant-a",
            display_name="Tenant A",
            logo_uri="/tenant-assets/tenant-a/logo.svg",
            primary_color="#005f73",
            allowed_asset_prefixes=policy.allowed_asset_prefixes,
        )
    )

    assert registry.get("tenant-a") == branding
    assert policy.validate_asset_uri("/tenant-assets/tenant-a/logo.svg") == "/tenant-assets/tenant-a/logo.svg"


@pytest.mark.unit
def test_provider_white_label_t1_renders_sanitized_tenant_template() -> None:
    runtime = _runtime()
    request = _request()
    branding = TenantBranding(
        tenant_id="tenant-a",
        display_name="<Tenant A>",
        logo_uri="/assets/tenant-a/logo.svg",
        primary_color="#005f73",
    )

    html = render_login_template(request, branding)
    page = runtime.render_hosted_login(request, branding)

    assert page.html == html
    assert 'data-tenant="tenant-a"' in html
    assert 'data-client="client-a"' in html
    assert 'data-redirect-uri="https://rp.example.test/callback"' in html
    assert "--brand-color:#005f73" in html
    assert 'src="/assets/tenant-a/logo.svg"' in html
    assert "&lt;Tenant A&gt;" in html
    assert "<Tenant A>" not in html
    assert f'value="{request.state}"' in html
    assert f'value="{request.nonce}"' in html


@pytest.mark.unit
def test_provider_white_label_t1_registry_renders_tenant_isolated_pages() -> None:
    registry = TenantBrandingRegistry()
    registry.set(TenantBranding(tenant_id="tenant-a", display_name="Tenant A", logo_uri="/assets/tenant-a/logo.svg", primary_color="#005f73"))
    registry.set(TenantBranding(tenant_id="tenant-b", display_name="Tenant B", logo_uri="/assets/tenant-b/logo.svg", primary_color="#7a1f1f"))
    runtime = _runtime()

    page_a = runtime.render_hosted_login_for_tenant(_request(tenant_id="tenant-a"), registry)
    page_b = runtime.render_hosted_login_for_tenant(
        _request(tenant_id="tenant-b", client_id="client-b", redirect_uri="https://rp-b.example.test/callback"),
        registry,
    )

    assert "Tenant A" in page_a.html
    assert "Tenant B" not in page_a.html
    assert "Tenant B" in page_b.html
    assert "Tenant A" not in page_b.html
    assert "/assets/tenant-a/logo.svg" in page_a.html
    assert "/assets/tenant-b/logo.svg" in page_b.html


@pytest.mark.unit
def test_provider_white_label_t2_rejects_unsafe_branding_and_cross_tenant_use() -> None:
    runtime = _runtime()
    request = _request()

    with pytest.raises(OidcProviderError, match="outside the tenant asset policy"):
        runtime.render_hosted_login(
            request,
            TenantBranding(tenant_id="tenant-a", display_name="Tenant A", logo_uri="https://cdn.example.test/logo.svg"),
        )
    with pytest.raises(OidcProviderError, match="extension"):
        runtime.render_hosted_login(
            request,
            TenantBranding(tenant_id="tenant-a", display_name="Tenant A", logo_uri="/assets/tenant-a/logo.exe"),
        )
    with pytest.raises(OidcProviderError, match="unsafe path"):
        runtime.render_hosted_login(
            request,
            TenantBranding(tenant_id="tenant-a", display_name="Tenant A", logo_uri="/assets/tenant-a/../logo.svg"),
        )
    with pytest.raises(OidcProviderError, match="six-digit hex color"):
        runtime.render_hosted_login(
            request,
            TenantBranding(tenant_id="tenant-a", display_name="Tenant A", primary_color="red"),
        )
    with pytest.raises(OidcProviderError, match="tenant branding mismatch"):
        runtime.render_hosted_login(
            request,
            TenantBranding(tenant_id="tenant-b", display_name="Tenant B"),
        )
    with pytest.raises(OidcProviderError, match="not configured"):
        runtime.render_hosted_login_for_tenant(request, TenantBrandingRegistry())


@pytest.mark.unit
def test_provider_white_label_t2_public_boundary_has_no_forbidden_imports() -> None:
    files = [
        Path("pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/__init__.py"),
        Path("pkgs/50-protocols/tigrbl-auth-protocol-oidc/src/tigrbl_auth_protocol_oidc/provider.py"),
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

from __future__ import annotations

import ast
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_core_t0_exports_public_primitives() -> None:
    import tigrbl_identity_core as core

    assert core.Scope.parse("openid profile").contains("openid")
    assert core.Scope.parse(["openid", "email"]).serialize() == "openid email"
    assert str(core.new_tenant_id())
    assert str(core.new_principal_id())
    assert str(core.new_client_id())
    assert str(core.new_credential_id())
    assert core.TenantRef(core.TenantId("tenant-1")).id == "tenant-1"


def test_core_t1_error_taxonomy_and_clock_primitives() -> None:
    import tigrbl_identity_core as core

    assert issubclass(core.IdentityValidationError, core.IdentityError)
    assert issubclass(core.IdentityAuthorizationError, core.IdentityError)
    frozen = core.FrozenClock(datetime(2026, 1, 2, 3, 4, 5))
    assert frozen.now().tzinfo == timezone.utc
    assert core.unix_seconds(frozen) == int(frozen.now().timestamp())


def test_core_t2_import_dag_clean_room() -> None:
    core_root = ROOT / "pkgs" / "tigrbl-identity-core" / "src" / "tigrbl_identity_core"
    forbidden = {"tigrbl_auth", "tigrbl_identity_server", "tigrbl_identity_runtime", "tigrbl_identity_storage"}
    for path in core_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        assert not (imports & forbidden), path


def test_contracts_t0_oauth_oidc_wire_models_validate() -> None:
    from tigrbl_identity_contracts import (
        OAuthIntrospectionResponse,
        OAuthTokenRequest,
        OAuthTokenResponse,
        OidcDiscoveryDocument,
        OidcIdTokenClaims,
    )

    token_request = OAuthTokenRequest(grant_type="authorization_code", client_id="client", code="code")
    assert token_request.grant_type == "authorization_code"
    assert OAuthTokenResponse(access_token="token").token_type == "Bearer"
    assert OAuthIntrospectionResponse(active=True, sub="subject").active is True
    discovery = OidcDiscoveryDocument(issuer="https://issuer.example", jwks_uri="https://issuer.example/jwks.json")
    assert str(discovery.issuer).startswith("https://issuer.example")
    claims = OidcIdTokenClaims(iss="https://issuer.example", sub="subject", aud="client", exp=10, iat=1)
    assert claims.sub == "subject"


def test_contracts_t1_resource_server_and_rp_protocol_models_validate() -> None:
    from tigrbl_identity_contracts import (
        AccessTokenClaims,
        ResourceServerMetadata,
        RpConfiguration,
        RpLoginRequest,
    )

    resource = ResourceServerMetadata(resource="https://api.example", issuer="https://issuer.example")
    assert resource.bearer_methods_supported == ["header"]
    token_claims = AccessTokenClaims(iss="https://issuer.example", sub="s", aud="https://api.example", exp=10)
    assert token_claims.aud == "https://api.example"
    rp = RpConfiguration(issuer="https://issuer.example", client_id="client", redirect_uri="https://rp.example/cb")
    login = RpLoginRequest(state="state", nonce="nonce", code_challenge="challenge", redirect_uri=rp.redirect_uri)
    assert login.code_challenge_method == "S256"


def test_storage_tables_own_table_backed_admin_contracts() -> None:
    from tigrbl_identity_storage.tables.tenant import AdminTenantOut, AdminTenantProvisionIn

    tenant_request = AdminTenantProvisionIn(slug="test", name="Test", email="admin@example.test")
    assert tenant_request.slug == "test"
    assert AdminTenantOut(id="tenant-id", slug="test", name="Test", email="admin@example.test").slug == "test"


def test_contracts_t2_projection_models_wrap_openapi_only() -> None:
    from tigrbl_identity_contracts import ContractProjection

    openapi = {
        "openapi": "3.1.0",
        "info": {"title": "Identity API", "version": "0.0.0-test"},
        "paths": {"/register": {"post": {"operationId": "register"}}},
    }
    openapi_projection = ContractProjection(kind="openapi", profile="production", version="0.0.0-test", document=openapi)

    assert "/register" in openapi_projection.document["paths"]

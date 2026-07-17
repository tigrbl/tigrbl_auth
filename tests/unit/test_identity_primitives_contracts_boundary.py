from __future__ import annotations

import asyncio
import ast
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_identity_primitives_exports_public_values() -> None:
    import tigrbl_identity_core as core

    class Row:
        status = "active"
        tenant_id = "tenant-1"

    assert core.Scope.parse("openid profile").contains("openid")
    assert core.Scope.parse(["openid", "email"]).serialize() == "openid email"
    assert isinstance(core.uuid_str(), str)
    assert (
        core.StrUUID("00000000-0000-0000-0000-000000000000")
        == "00000000-0000-0000-0000-000000000000"
    )
    assert str(core.new_tenant_id())
    assert str(core.new_principal_id())
    assert str(core.new_client_id())
    assert str(core.new_credential_id())
    assert len(core.new_opaque_id()) == 32
    prefixed_id = core.new_prefixed_id("audit")
    assert prefixed_id.startswith("audit:")
    assert len(prefixed_id.removeprefix("audit:")) == 32
    assert core.TenantRef(core.TenantId("tenant-1")).id == "tenant-1"
    assert core.pick_fields({"a": 1, "b": 2}, ("b", "missing")) == {"b": 2}
    assert core.row_value({"tenant_id": "tenant-1"}, "tenant_id") == "tenant-1"
    assert core.row_value(Row(), "tenant_id") == "tenant-1"
    assert core.row_active(Row())
    assert core.str_tuple(["b", "a", "b", None, ""]) == ("a", "b")
    assert core.str_tuple(["b", "a"], sort=False) == ("b", "a")


def test_identity_primitives_error_taxonomy_and_clock_values() -> None:
    import tigrbl_identity_core as core

    assert issubclass(core.IdentityValidationError, core.IdentityError)
    assert issubclass(core.IdentityAuthorizationError, core.IdentityError)
    frozen = core.FrozenClock(datetime(2026, 1, 2, 3, 4, 5))
    assert frozen.now().tzinfo == timezone.utc
    assert core.unix_seconds(frozen) == int(frozen.now().timestamp())
    assert core.utc_now(frozen) == frozen.now()
    assert core.utc_now_iso(frozen) == "2026-01-02T03:04:05+00:00"
    assert core.parse_time("2026-01-02T03:04:05Z") == datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)


def test_prefixed_identity_rejects_invalid_prefixes() -> None:
    import pytest
    import tigrbl_identity_core as core

    with pytest.raises(ValueError):
        core.new_prefixed_id("")
    with pytest.raises(ValueError):
        core.new_prefixed_id("invalid:prefix")


def test_identity_primitives_export_version_range_helpers() -> None:
    import tigrbl_identity_core as core

    assert core.semver_key("v1.2.3-alpha") == (1, 2, 3)
    assert core.semver_key("1.2") == (1, 2, 0)
    assert core.version_in_range("0.3.5", ("0.3.0", "0.3.9"))
    assert not core.version_in_range("0.4.0", ("0.3.0", "0.3.9"))


def test_identity_primitives_export_dotted_permission_matching() -> None:
    import tigrbl_identity_core as core

    assert core.matches_dotted_pattern("*", "client.read")
    assert core.matches_dotted_pattern("client.*", "client")
    assert core.matches_dotted_pattern("client.*", "client.read")
    assert core.matches_dotted_pattern("client.read", "client.read")
    assert not core.matches_dotted_pattern("client.read", "client.write")


def test_identity_primitives_export_http_and_jsonrpc_helpers() -> None:
    import tigrbl_identity_core as core

    status, headers, body = core.json_response(401, {"error": "missing"})

    assert status == 401
    assert (b"www-authenticate", b"Bearer") in headers
    assert body == b'{"error":"missing"}'
    assert core.headers_from_scope({"headers": [(b"X-API-Key", b"secret")]}) == {"x-api-key": "secret"}
    assert core.jsonrpc_error("1", -32600, "Invalid Request") == {
        "jsonrpc": "2.0",
        "id": "1",
        "error": {"code": -32600, "message": "Invalid Request"},
    }

    messages = iter(
        [
            {"type": "http.request", "body": b"alpha", "more_body": True},
            {"type": "http.request", "body": b"beta", "more_body": False},
        ]
    )

    async def receive() -> dict[str, object]:
        return next(messages)

    assert asyncio.run(core.read_http_body(receive)) == b"alphabeta"
    replay = core.replay_http_body(b"body")
    assert asyncio.run(replay()) == {"type": "http.request", "body": b"body", "more_body": False}
    assert asyncio.run(replay()) == {"type": "http.request", "body": b"", "more_body": False}


def test_authz_policy_admin_gate_package_uses_identity_core_primitives() -> None:
    gate_path = (
        ROOT
        / "pkgs"
        / "80-routers"
        / "tigrbl-auth-router-admin-gate"
        / "src"
        / "tigrbl_auth_router_admin_gate"
        / "gate.py"
    )
    tree = ast.parse(gate_path.read_text(encoding="utf-8"))
    local_functions = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert {
        "_digest",
        "_headers",
        "_json_response",
        "_jsonrpc_error",
        "_read_http_body",
        "_replay_http_body",
    }.isdisjoint(local_functions)
    assert "from tigrbl_identity_core import" in gate_path.read_text(encoding="utf-8")


def test_authz_policy_control_plane_uses_identity_core_primitives() -> None:
    control_plane_path = (
        ROOT
        / "pkgs"
        / "30-storage-runtime"
        / "tigrbl-policy-administration-memory-provider"
        / "src"
        / "tigrbl_policy_administration_memory_provider"
        / "control_plane.py"
    )
    source = control_plane_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    local_functions = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    assert {
        "_permission_matches",
        "_pick_fields",
        "_row_active",
        "_row_value",
        "_str_tuple",
    }.isdisjoint(local_functions)
    assert "pick_fields as _pick_fields" in source


def test_identity_primitives_do_not_own_liveness_contracts() -> None:
    import tigrbl_identity_core as core

    assert not hasattr(core, "ConvergenceEvent")
    assert not hasattr(core, "ConvergenceState")
    assert not hasattr(core, "LivenessConvergenceReport")


def test_identity_primitives_do_not_own_jwt_payload_or_principal_protocol() -> None:
    import tigrbl_identity_core as core
    import tigrbl_identity_core.typing as core_typing
    import tigrbl_identity_contracts as identity_contracts
    from tigrbl_identity_contracts.principals import PrincipalLike
    from tigrbl_security_trust_contracts import JWTPayload

    assert not hasattr(core, "JWTPayload")
    assert not hasattr(core, "Principal")
    assert not hasattr(core_typing, "JWTPayload")
    assert not hasattr(core_typing, "Principal")
    assert not hasattr(identity_contracts, "JWTPayload")
    assert JWTPayload.__module__ == "tigrbl_security_trust_contracts.types"
    assert PrincipalLike.__module__ == "tigrbl_identity_contracts.principals.protocols"


def test_auth_helpers_import_principal_protocol_from_contracts() -> None:
    targets = [
        ROOT
        / "pkgs"
        / "20-providers"
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials"
        / "backends.py",
        ROOT
        / "pkgs"
        / "60-runtime"
        / "tigrbl-identity-server"
        / "src"
        / "tigrbl_identity_server"
        / "security"
        / "auth.py",
        ROOT
        / "pkgs"
        / "60-runtime"
        / "tigrbl-identity-server"
        / "src"
        / "tigrbl_identity_server"
        / "security"
        / "security_deps.py",
    ]

    for path in targets:
        source = path.read_text(encoding="utf-8")
        assert "from tigrbl_identity_core.typing import Principal" not in source
        assert "from tigrbl_identity_contracts.principals import PrincipalLike" in source

    removed_composition = (
        ROOT
        / "pkgs"
        / "20-providers"
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials"
        / "authenticators.py"
    ).read_text(encoding="utf-8")
    assert "Removed runtime composition surface" in removed_composition
    assert "tigrbl_identity_contracts.principals" not in removed_composition


def test_identity_primitives_import_dag_clean_room() -> None:
    core_root = ROOT / "pkgs" / "00-primitives" / "tigrbl-identity-core" / "src" / "tigrbl_identity_core"
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


def test_contracts_do_not_export_wire_request_response_models() -> None:
    import tigrbl_identity_contracts as contracts

    removed_wire_models = {
        "OAuthIntrospectionResponse",
        "OAuthTokenRequest",
        "OAuthTokenResponse",
        "OidcDiscoveryDocument",
        "OidcIdTokenClaims",
        "ResourceServerMetadata",
        "RpConfiguration",
        "RpLoginRequest",
    }

    for model_name in removed_wire_models:
        assert not hasattr(contracts, model_name), model_name


def test_platform_api_owns_tenant_admin_contracts() -> None:
    from tigrbl_auth_backend_app_platform_admin.tenants import AdminTenantOut, AdminTenantProvisionIn

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

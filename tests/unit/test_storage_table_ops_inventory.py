from __future__ import annotations

import ast
from pathlib import Path


TABLES_DIR = (
    Path(__file__).resolve().parents[2]
    / "pkgs"
    / "20-storage"
    / "tigrbl-identity-storage"
    / "src"
    / "tigrbl_identity_storage"
    / "tables"
)


REQUIRED_TABLE_OPS = {
    "auth_session.py": {"AuthSession": {"create_for_user", "list_for_user", "revoke_for_user", "revoke_all_for_user", "touch"}},
    "consent.py": {"Consent": {"grant", "list_for_user", "revoke_for_user", "revoke_for_client"}},
    "token_record.py": {"TokenRecord": {"persist_issued_token", "list_active_for_subject", "revoke_family", "mark_rotated"}},
    "revoked_token.py": {"RevokedToken": {"revoke_token", "is_revoked"}},
    "auth_code.py": {"AuthCode": {"create_for_authorization", "consume", "expire"}},
    "device_code.py": {"DeviceCode": {"create_device_authorization", "approve", "deny", "poll", "consume"}},
    "pushed_authorization_request.py": {
        "PushedAuthorizationRequest": {"create_request", "resolve_request_uri", "consume", "consume_request"}
    },
    "client.py": {"Client": {"new", "verify_secret", "authenticate", "rotate_secret", "enable", "disable"}},
    "client_registration.py": {
        "ClientRegistration": {"register_client", "read_registration", "update_registration", "delete_registration"}
    },
    "audit_event.py": {"AuditEvent": {"record", "list_for_subject", "list_for_tenant"}},
    "logout_state.py": {"LogoutState": {"create_logout", "consume_logout", "expire"}},
    "realm.py": {"Realm": {"create_realm", "update_realm", "list_realms", "lookup_by_slug"}},
    "tenant.py": {"Tenant": {"create_tenant", "update_tenant", "disable_tenant", "list_by_realm", "lookup_by_name"}},
    "user.py": {"User": {"create_user", "update_user", "disable_user", "list_by_tenant", "lookup_by_identifier"}},
    "delegation_grant.py": {
        "DelegationGrantRecord": {"create_grant", "revoke_grant", "list_grants"},
        "DelegationGrantProof": {"persist_provenance"},
        "DelegationGrantTokenLink": {"link_token"},
    },
    "key.py": {"Key": {"create_key", "lookup_by_kid", "list_active", "enable", "disable", "retire", "rotate", "publish_jwks", "sign", "verify"}},
    "key_version.py": {"KeyVersion": {"create_version", "lookup", "list_for_key", "activate", "retire", "export_public_jwk"}},
}


def _class_methods(path: Path, class_name: str) -> set[str]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {item.name for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))}
    raise AssertionError(f"{class_name} not found in {path}")


def test_storage_tables_own_required_operation_methods() -> None:
    missing: list[str] = []

    for filename, class_requirements in REQUIRED_TABLE_OPS.items():
        path = TABLES_DIR / filename
        if not path.exists():
            path = TABLES_DIR / filename.removesuffix(".py") / "_table.py"
        for class_name, operation_names in class_requirements.items():
            defined = _class_methods(path, class_name)
            for name in sorted(operation_names - defined):
                missing.append(f"{class_name}.{name}")

    assert missing == []

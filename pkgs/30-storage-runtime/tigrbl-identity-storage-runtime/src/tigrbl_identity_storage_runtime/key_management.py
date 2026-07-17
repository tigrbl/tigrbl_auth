"""Operator-plane key lifecycle helpers backed by storage-runtime state."""

from __future__ import annotations

import pathlib
from typing import Any


def _operator_context(
    *,
    repo_root: pathlib.Path | str,
    command: str,
    profile: str | None = None,
    tenant: str | None = None,
    issuer: str | None = None,
    actor: str | None = None,
    dry_run: bool = False,
):
    from tigrbl_identity_storage_runtime.operator_store import OperationContext

    return OperationContext(
        repo_root=pathlib.Path(repo_root),
        command=command,
        resource="keys",
        dry_run=dry_run,
        actor=actor or "system",
        profile=profile,
        tenant=tenant,
        issuer=issuer,
    )


def create_operator_key_for_context(
    context, *, patch: dict[str, Any] | None = None
):
    from tigrbl_identity_storage_runtime.resource_service import create_resource

    patch = dict(patch or {})
    record_id = str(
        patch.get("kid") or patch.get("id") or patch.get("name") or "imported-key"
    )
    return create_resource(context, record_id=record_id, patch=patch, if_exists="error")


def seed_operator_key_for_context(
    context,
    *,
    kid: str | None = None,
    patch: dict[str, Any] | None = None,
):
    from tigrbl_identity_storage_runtime.resource_service import create_resource

    patch = dict(patch or {})
    chosen_kid = str(
        kid
        or patch.get("kid")
        or (f"{context.tenant}-jwks-active" if context.tenant else "jwks-active")
    )
    patch.setdefault("kid", chosen_kid)
    patch.setdefault("alg", "EdDSA")
    patch.setdefault("use", "sig")
    patch.setdefault("kty", "OKP")
    patch.setdefault("curve", "Ed25519")
    patch.setdefault("status", "active")
    patch.setdefault("publish", True)
    return create_resource(
        context,
        record_id=chosen_kid,
        patch=patch,
        if_exists="skip",
    )


def update_operator_key_for_context(
    context,
    *,
    record_id: str,
    patch: dict[str, Any] | None = None,
):
    from tigrbl_identity_storage_runtime.resource_service import update_resource

    return update_resource(
        context,
        record_id=record_id,
        patch=dict(patch or {}),
        if_missing="error",
    )


def generate_operator_key_for_context(
    context, *, patch: dict[str, Any] | None = None
):
    from tigrbl_identity_storage_runtime.resource_service import generate_key_record

    return generate_key_record(context, patch=patch)


def import_operator_key_for_context(context, *, patch: dict[str, Any] | None = None):
    from tigrbl_identity_storage_runtime.resource_service import create_resource

    patch = dict(patch or {})
    record_id = str(
        patch.get("kid") or patch.get("id") or patch.get("name") or "imported-key"
    )
    return create_resource(context, record_id=record_id, patch=patch, if_exists="update")


def export_operator_key_for_context(context, *, record_id: str):
    from tigrbl_identity_storage_runtime.resource_service import get_resource

    return get_resource(context, record_id=record_id)


def rotate_operator_key_for_context(context, *, record_id: str):
    from tigrbl_identity_storage_runtime.resource_service import rotate_key_record

    return rotate_key_record(context, record_id=record_id)


def retire_operator_key_for_context(
    context, *, record_id: str, retire_after: str | None = None
):
    from tigrbl_identity_storage_runtime.resource_service import retire_key_record

    return retire_key_record(context, record_id=record_id, retire_after=retire_after)


def publish_operator_jwks_for_context(context, *, output_path: str | None = None):
    from tigrbl_identity_storage_runtime.resource_service import publish_jwks_document

    return publish_jwks_document(context, output_path=output_path)


def list_operator_keys_for_context(
    context,
    *,
    status_filter: str | None = None,
    filter_expr: str | None = None,
    sort: str = "id",
    offset: int = 0,
    limit: int = 50,
):
    from tigrbl_identity_storage_runtime.resource_service import list_resource_result

    return list_resource_result(
        context,
        status_filter=status_filter,
        filter_expr=filter_expr,
        sort=sort,
        offset=offset,
        limit=limit,
    )


def get_operator_key_for_context(context, *, record_id: str):
    from tigrbl_identity_storage_runtime.resource_service import get_resource

    return get_resource(context, record_id=record_id)


def delete_operator_key_for_context(
    context, *, record_id: str, if_missing: str = "error"
):
    from tigrbl_identity_storage_runtime.resource_service import delete_resource

    return delete_resource(context, record_id=record_id, if_missing=if_missing)


__all__ = [
    "_operator_context",
    "create_operator_key_for_context",
    "delete_operator_key_for_context",
    "export_operator_key_for_context",
    "generate_operator_key_for_context",
    "get_operator_key_for_context",
    "import_operator_key_for_context",
    "list_operator_keys_for_context",
    "publish_operator_jwks_for_context",
    "retire_operator_key_for_context",
    "seed_operator_key_for_context",
    "update_operator_key_for_context",
    "rotate_operator_key_for_context",
]

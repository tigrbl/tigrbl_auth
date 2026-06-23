"""Storage adapters for contract-level key usage recipes."""

from __future__ import annotations

from typing import Any, Mapping

from tigrbl_security_trust_contracts import normalize_key_usages, resolve_key_allowed_operations


def normalize_key_usage_record(
    *,
    key_kind: Any,
    key_usages: Any = None,
    allowed_ops: Any = None,
) -> dict[str, list[str] | str]:
    """Return storage values with ops defaulted or narrowed by key usage specs."""

    usages = normalize_key_usages(key_usages)
    ops = resolve_key_allowed_operations(kind=key_kind, usages=usages, allowed_ops=allowed_ops)
    return {
        "key_kind": str(getattr(key_kind, "value", key_kind)),
        "key_usages": [usage.value for usage in usages],
        "allowed_ops": [operation.value for operation in ops],
    }


def normalize_payload_key_usage(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize key usage fields on a create/update payload."""

    cleaned = dict(payload)
    key_kind = cleaned.get("key_kind", "asymmetric")
    normalized = normalize_key_usage_record(
        key_kind=key_kind,
        key_usages=cleaned.get("key_usages"),
        allowed_ops=cleaned.get("allowed_ops") if "allowed_ops" in cleaned else None,
    )
    cleaned.update(normalized)
    return cleaned


def stored_key_usages(values: Any) -> list[str]:
    return [usage.value for usage in normalize_key_usages(values)]


def stored_key_operations(*, key_kind: Any, key_usages: Any, allowed_ops: Any = None) -> list[str]:
    return [
        operation.value
        for operation in resolve_key_allowed_operations(
            kind=key_kind,
            usages=normalize_key_usages(key_usages),
            allowed_ops=allowed_ops,
        )
    ]


__all__ = [
    "normalize_key_usage_record",
    "normalize_payload_key_usage",
    "stored_key_operations",
    "stored_key_usages",
]

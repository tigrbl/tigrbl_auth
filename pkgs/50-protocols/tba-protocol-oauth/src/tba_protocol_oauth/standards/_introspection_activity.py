from __future__ import annotations

from typing import Any, Dict


def header(request: Any, name: str) -> str | None:
    headers = getattr(request, "headers", {}) or {}
    if hasattr(headers, "get"):
        return headers.get(name) or headers.get(name.lower())
    return None


def authorization_snapshot_stale(payload: Dict[str, Any]) -> bool:
    issued_version = payload.get("authz_version")
    current_version = payload.get("current_authz_version")
    if issued_version is None or current_version is None:
        return False
    try:
        return int(issued_version) != int(current_version)
    except (TypeError, ValueError):
        return str(issued_version) != str(current_version)


def apply_introspection_activity_constraints(payload: Dict[str, Any]) -> Dict[str, Any]:
    if payload.get("active") is False:
        return payload
    if not authorization_snapshot_stale(payload):
        return payload
    inactive = dict(payload)
    inactive["active"] = False
    inactive["inactive_reason"] = "authorization_snapshot_stale"
    return inactive

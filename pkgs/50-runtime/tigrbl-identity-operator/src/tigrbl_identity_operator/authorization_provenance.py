"""Deterministic authorization-trace and delegation-lineage artifacts."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


def _normalize(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _normalize(val) for key, val in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, tuple):
        return [_normalize(item) for item in value]
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, set):
        return [_normalize(item) for item in sorted(value, key=lambda item: repr(item))]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def build_authorization_decision_trace(
    *,
    tenant_id: str | None,
    subject: str,
    issuer: str,
    audience: str | list[str] | None,
    resource: str | None,
    scope: str | None,
    subject_token_type: str,
    requested_token_type: str,
    exchange_mode: str,
    actor_subject: str | None,
    source_issuer: str | None,
    sender_constraint: str,
    verifier_logic_id: str | None = None,
    required_claims: tuple[str, ...] = (),
) -> dict[str, Any]:
    request_view = {
        "tenant_id": tenant_id or "",
        "subject": subject,
        "issuer": issuer,
        "audience": audience,
        "resource": resource,
        "scope": scope or "",
        "subject_token_type": subject_token_type,
        "requested_token_type": requested_token_type,
        "exchange_mode": exchange_mode,
        "actor_subject": actor_subject or "",
        "source_issuer": source_issuer or "",
        "sender_constraint": sender_constraint,
    }
    derived_grant = {
        "issuer": issuer,
        "audience": audience,
        "resource": resource,
        "scope": scope or "",
        "token_kind": "access",
        "requested_token_type": requested_token_type,
        "exchange_mode": exchange_mode,
        "actor_subject": actor_subject or "",
    }
    policy_view = {
        "verifier_logic_id": verifier_logic_id or "default-protected-resource-verifier",
        "required_claims": list(required_claims),
        "sender_constraint": sender_constraint,
        "resource": resource,
        "audience": audience,
    }
    request_hash = canonical_hash(request_view)
    policy_hash = canonical_hash(policy_view)
    derivation_hash = canonical_hash(derived_grant)
    return {
        "artifact_type": "authorization_decision_trace",
        "artifact_version": 1,
        "request_hash": request_hash,
        "policy_hash": policy_hash,
        "derivation_hash": derivation_hash,
        "decision_key": canonical_hash(
            {
                "request_hash": request_hash,
                "policy_hash": policy_hash,
                "derivation_hash": derivation_hash,
            }
        ),
        "request": request_view,
        "derived_grant": derived_grant,
    }


def build_delegation_provenance(
    *,
    subject_token: str,
    actor_token: str | None,
    subject_claims: Mapping[str, Any],
    actor_claims: Mapping[str, Any] | None,
    authorization_trace: Mapping[str, Any],
    audience: str | list[str] | None,
    resource: str | None,
    exchange_mode: str,
    sender_constraint: str,
) -> dict[str, Any]:
    subject_token_hash = canonical_hash({"token": subject_token})
    actor_token_hash = canonical_hash({"token": actor_token}) if actor_token else None
    nodes = {
        "subject": {
            "sub": str(subject_claims.get("sub") or ""),
            "iss": str(subject_claims.get("iss") or ""),
            "aud": subject_claims.get("aud"),
        },
        "actor": {
            "sub": str((actor_claims or {}).get("sub") or ""),
            "iss": str((actor_claims or {}).get("iss") or ""),
        } if actor_claims else None,
    }
    edge = {
        "exchange_mode": exchange_mode,
        "audience": audience,
        "resource": resource,
        "sender_constraint": sender_constraint,
        "decision_key": authorization_trace.get("decision_key"),
        "subject_token_hash": subject_token_hash,
        "actor_token_hash": actor_token_hash,
    }
    lineage_id = canonical_hash({"nodes": nodes, "edge": edge})
    return {
        "artifact_type": "delegation_provenance",
        "artifact_version": 1,
        "lineage_id": lineage_id,
        "subject_token_hash": subject_token_hash,
        "actor_token_hash": actor_token_hash,
        "nodes": nodes,
        "edge": edge,
    }


__all__ = [
    "build_authorization_decision_trace",
    "build_delegation_provenance",
    "canonical_hash",
    "canonical_json",
]

"""Deterministic authorization-trace and delegation-lineage builders."""

from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_core.json_canonicalization import canonical_hash, canonical_json
from tigrbl_security_provenance_bases import ProvenanceArtifactBuilderBase
from tigrbl_security_trust_contracts import (
    AuthorizationDecisionTrace,
    CapabilityMap,
    DelegationProvenance,
)


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
    trace = AuthorizationDecisionTrace(
        request_hash=request_hash,
        policy_hash=policy_hash,
        derivation_hash=derivation_hash,
        decision_key=canonical_hash(
            {
                "request_hash": request_hash,
                "policy_hash": policy_hash,
                "derivation_hash": derivation_hash,
            }
        ),
        request=request_view,
        derived_grant=derived_grant,
    )
    return trace.as_dict()


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
        }
        if actor_claims
        else None,
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
    provenance = DelegationProvenance(
        lineage_id=canonical_hash({"nodes": nodes, "edge": edge}),
        subject_token_hash=subject_token_hash,
        actor_token_hash=actor_token_hash,
        nodes=nodes,
        edge=edge,
    )
    return provenance.as_dict()


class DeterministicProvenanceArtifactBuilder(ProvenanceArtifactBuilderBase):
    """Deterministic provider for authorization and delegation provenance."""

    def supports(self) -> CapabilityMap:
        return CapabilityMap(
            ops={
                "build_authorization_decision_trace": ("deterministic",),
                "build_delegation_provenance": ("deterministic",),
            },
            features=("authorization-provenance", "delegation-lineage"),
        )

    def build_authorization_decision_trace(self, **kwargs: Any) -> dict[str, Any]:
        return build_authorization_decision_trace(**kwargs)

    def build_delegation_provenance(self, **kwargs: Any) -> dict[str, Any]:
        return build_delegation_provenance(**kwargs)


__all__ = [
    "AuthorizationDecisionTrace",
    "DelegationProvenance",
    "DeterministicProvenanceArtifactBuilder",
    "build_authorization_decision_trace",
    "build_delegation_provenance",
    "canonical_hash",
    "canonical_json",
]

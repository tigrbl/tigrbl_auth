from __future__ import annotations

from typing import Any, Mapping, Sequence

from .base import CertificationError, _SECRET_KEYS
from tigrbl_release_contracts import AuthorizationEvent, DelegationStep


def assert_delegation_provenance(
    chain: Sequence[DelegationStep],
    *,
    max_depth: int,
    allowed_final_scopes: frozenset[str],
) -> None:
    if not chain:
        raise CertificationError("delegation chain is required")
    if len(chain) > max_depth:
        raise CertificationError("delegation chain exceeds maximum depth")
    seen_actors: set[str] = set()
    previous_subject = chain[0].subject
    for step in chain:
        if not step.proof_id:
            raise CertificationError("delegation step requires proof")
        if step.actor in seen_actors:
            raise CertificationError("delegation chain cycle detected")
        seen_actors.add(step.actor)
        if step.subject != previous_subject:
            raise CertificationError("delegation subject continuity broken")
        previous_subject = step.actor
    if not chain[-1].scopes.issubset(allowed_final_scopes):
        raise CertificationError("delegation final scopes exceed attenuation")


def sanitize_event_attributes(attributes: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: "[REDACTED]" if key.lower() in _SECRET_KEYS else value
        for key, value in attributes.items()
    }


def assert_observable_event(event: AuthorizationEvent) -> dict[str, Any]:
    if event.decision not in {"allow", "deny"}:
        raise CertificationError("authorization event decision must be allow or deny")
    required = [event.event_type, event.subject_id, event.actor_id, event.correlation_id]
    if any(not value for value in required):
        raise CertificationError("authorization event missing required identity fields")
    return {
        "event_type": event.event_type,
        "subject_id": event.subject_id,
        "actor_id": event.actor_id,
        "decision": event.decision,
        "correlation_id": event.correlation_id,
        "occurred_at": event.occurred_at.isoformat(),
        "attributes": sanitize_event_attributes(event.attributes),
    }

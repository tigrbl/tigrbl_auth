from datetime import datetime, timezone

import pytest

from tigrbl_auth.security.certification import (
    AuthorizationEvent,
    CertificationError,
    assert_observable_event,
)


def _event(**overrides: object) -> AuthorizationEvent:
    data: dict[str, object] = {
        "event_type": "policy.decision",
        "subject_id": "user-1",
        "actor_id": "service-a",
        "decision": "allow",
        "correlation_id": "corr-1",
        "occurred_at": datetime.now(timezone.utc),
        "attributes": {"resource": "notes", "token": "secret-token"},
    }
    data.update(overrides)
    return AuthorizationEvent(**data)


def test_authorization_observability_t0_contract_exports_event_check() -> None:
    assert callable(assert_observable_event)


def test_authorization_observability_t1_emits_structured_redacted_event() -> None:
    event = assert_observable_event(_event())

    assert event["event_type"] == "policy.decision"
    assert event["attributes"]["token"] == "[REDACTED]"


def test_authorization_observability_t2_rejects_missing_fields_or_bad_decision() -> None:
    with pytest.raises(CertificationError, match="decision"):
        assert_observable_event(_event(decision="maybe"))

    with pytest.raises(CertificationError, match="missing"):
        assert_observable_event(_event(correlation_id=""))

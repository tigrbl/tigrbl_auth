from __future__ import annotations

from typing import Any, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.redaction import redact_sensitive_mapping

from .models import AnomalySignal, AuthTelemetryEvent


class AuthAnomalyDetector:
    def __init__(self) -> None:
        self._events: list[AuthTelemetryEvent] = []

    @property
    def events(self) -> tuple[AuthTelemetryEvent, ...]:
        return tuple(self._events)

    def record_event(
        self,
        *,
        tenant_id: str,
        subject_id: str,
        event_type: str,
        correlation_id: str,
        ip_country: str,
        trusted_device: bool,
        outcome: str,
        details: Mapping[str, Any],
    ) -> tuple[AuthTelemetryEvent, AnomalySignal | None]:
        event = AuthTelemetryEvent(
            event_id=f"auth-event-{uuid4().hex}",
            tenant_id=tenant_id,
            subject_id=subject_id,
            event_type=event_type,
            correlation_id=correlation_id,
            ip_country=ip_country,
            trusted_device=trusted_device,
            outcome=outcome,
            details=redact_sensitive_mapping(details),
            recorded_at=utc_now_iso(),
        )
        self._events.append(event)
        return event, self._detect_signal(event)

    def _detect_signal(self, event: AuthTelemetryEvent) -> AnomalySignal | None:
        reasons: list[str] = []
        previous_countries = {
            item.ip_country
            for item in self._events[:-1]
            if item.tenant_id == event.tenant_id and item.subject_id == event.subject_id
        }
        failure_count = sum(
            1
            for item in self._events
            if item.tenant_id == event.tenant_id and item.subject_id == event.subject_id and item.outcome == "failure"
        )
        if previous_countries and event.ip_country not in previous_countries:
            reasons.append("impossible travel or first-seen country")
        if not event.trusted_device:
            reasons.append("untrusted device telemetry")
        if failure_count >= 3:
            reasons.append("repeated authentication failures")
        if not reasons:
            return None
        severity = "high" if len(reasons) >= 3 else "medium"
        return AnomalySignal(
            signal_id=f"anomaly-{uuid4().hex}",
            tenant_id=event.tenant_id,
            subject_id=event.subject_id,
            correlation_id=event.correlation_id,
            severity=severity,
            reasons=tuple(reasons),
            recommended_action="step_up" if severity == "medium" else "manual-review",
            redacted_details=event.details,
        )

    def summary(self) -> dict[str, Any]:
        return {
            "event_count": len(self._events),
            "tenant_ids": sorted({event.tenant_id for event in self._events}),
        }

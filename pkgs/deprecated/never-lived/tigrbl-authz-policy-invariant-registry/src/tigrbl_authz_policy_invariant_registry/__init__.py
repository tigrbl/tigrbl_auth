from __future__ import annotations

from typing import Callable, Iterable, Mapping

from tigrbl_identity_contracts.invariants import (
    AuthorizationInvariant,
    InvariantEvaluation,
    InvariantSeverity,
    InvariantViolation,
    VerificationMethod,
)
from tigrbl_identity_core.clock import utc_now_iso


def _stable_tuple(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(value) for value in values if str(value)}))


class InvariantRegistry:
    def __init__(self, invariants: Iterable[AuthorizationInvariant] = ()) -> None:
        self._invariants: dict[str, AuthorizationInvariant] = {}
        for invariant in invariants:
            self.register(invariant)

    @property
    def invariants(self) -> Mapping[str, AuthorizationInvariant]:
        return dict(self._invariants)

    def register(self, invariant: AuthorizationInvariant) -> AuthorizationInvariant:
        if invariant.invariant_id in self._invariants:
            raise ValueError(f"duplicate invariant {invariant.invariant_id!r}")
        self._invariants[invariant.invariant_id] = invariant
        return invariant

    def get(self, invariant_id: str) -> AuthorizationInvariant:
        try:
            return self._invariants[invariant_id]
        except KeyError as exc:
            raise KeyError(f"unknown invariant {invariant_id!r}") from exc

    def list(
        self,
        *,
        property_family: str | None = None,
        enabled_only: bool = False,
        tags: Iterable[str] = (),
    ) -> tuple[AuthorizationInvariant, ...]:
        required_tags = set(_stable_tuple(tags))
        rows = []
        for invariant in self._invariants.values():
            if property_family is not None and invariant.property_family != property_family:
                continue
            if enabled_only and not invariant.enabled:
                continue
            if required_tags and not required_tags.issubset(set(invariant.tags)):
                continue
            rows.append(invariant)
        return tuple(sorted(rows, key=lambda item: item.invariant_id))

    def evaluate(
        self,
        invariant_id: str,
        evaluator: Callable[[AuthorizationInvariant], bool | InvariantEvaluation],
    ) -> InvariantEvaluation:
        invariant = self.get(invariant_id)
        if not invariant.enabled:
            return InvariantEvaluation(
                invariant_id=invariant.invariant_id,
                passed=True,
                message="invariant disabled",
                evaluated_at=utc_now_iso(),
            )
        result = evaluator(invariant)
        if isinstance(result, InvariantEvaluation):
            if result.invariant_id != invariant.invariant_id:
                raise ValueError("evaluation invariant_id mismatch")
            return result
        return InvariantEvaluation(
            invariant_id=invariant.invariant_id,
            passed=bool(result),
            message="invariant passed" if result else "invariant failed",
            evaluated_at=utc_now_iso(),
        )

    def violations(self, evaluations: Iterable[InvariantEvaluation]) -> tuple[InvariantViolation, ...]:
        rows: list[InvariantViolation] = []
        for evaluation in evaluations:
            if evaluation.passed:
                continue
            invariant = self.get(evaluation.invariant_id)
            rows.append(
                InvariantViolation(
                    invariant_id=invariant.invariant_id,
                    severity=invariant.severity,
                    message=evaluation.message,
                    evidence=evaluation.evidence,
                )
            )
        return tuple(rows)


def default_authorization_invariant_registry() -> InvariantRegistry:
    return InvariantRegistry(
        (
            AuthorizationInvariant(
                invariant_id="authz.non_escalation",
                title="Authority does not escalate without an explicit grant",
                property_family="safety",
                statement="Effective authority must not exceed the explicit source grants and derived closure.",
                verification_method=VerificationMethod.GRAPH,
                severity=InvariantSeverity.CRITICAL,
                feature_ids=("feat:authorization-invariant-guard-registry",),
                spec_ids=("spc:1205", "spc:1206", "spc:1207"),
                tags=("authority", "non-escalation"),
            ),
            AuthorizationInvariant(
                invariant_id="authz.tenant_isolation",
                title="Tenant authority remains tenant scoped",
                property_family="isolation",
                statement="A subject scoped to one tenant cannot derive authority over another tenant.",
                verification_method=VerificationMethod.RUNTIME,
                severity=InvariantSeverity.CRITICAL,
                feature_ids=("feat:authorization-invariant-guard-registry",),
                spec_ids=("spc:1205", "spc:1190"),
                tags=("tenant", "isolation"),
            ),
        )
    )


__all__ = [
    "AuthorizationInvariant",
    "InvariantEvaluation",
    "InvariantRegistry",
    "InvariantSeverity",
    "InvariantViolation",
    "VerificationMethod",
    "default_authorization_invariant_registry",
]

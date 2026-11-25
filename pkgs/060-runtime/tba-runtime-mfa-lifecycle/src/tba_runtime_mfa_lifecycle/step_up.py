"""Step-up ceremony and fresh same-subject assurance evaluation."""

from collections.abc import Iterable
from datetime import datetime, timedelta

from .contracts import (
    AssuranceRequirement,
    CeremonyKind,
    FactorAssurance,
    FactorBinding,
    LifecycleResult,
)
from .enrollment import _FactorRuntime


class StepUpRuntime(_FactorRuntime):
    def begin(
        self,
        binding: FactorBinding,
        *,
        credential_reference: str | None = None,
        ttl: timedelta = timedelta(minutes=5),
    ) -> LifecycleResult:
        return self._begin(
            binding,
            CeremonyKind.STEP_UP,
            ttl=ttl,
            credential_reference=credential_reference,
        )

    def complete(
        self, attempt_id: str, binding: FactorBinding, proof: object
    ) -> LifecycleResult:
        return self._complete(attempt_id, binding, proof, CeremonyKind.STEP_UP)

    def cancel(self, attempt_id: str, binding: FactorBinding) -> bool:
        return self._cancel(attempt_id, binding, CeremonyKind.STEP_UP)


def satisfies_assurance(
    proofs: Iterable[FactorAssurance],
    requirement: AssuranceRequirement,
    *,
    scope: str,
    subject: str,
    purpose: str,
    now: datetime,
) -> bool:
    """Evaluate trusted, previously recorded proof for this scope, subject and purpose."""
    if now.utcoffset() is None:
        raise ValueError("assurance evaluation requires a timezone-aware timestamp")
    methods = {
        proof.method
        for proof in proofs
        if proof.binding.scope == scope
        and proof.binding.subject == subject
        and proof.binding.purpose == purpose
        and proof.verified_at.utcoffset() is not None
        and now - requirement.max_age <= proof.verified_at <= now
    }
    return requirement.required_methods.issubset(methods)

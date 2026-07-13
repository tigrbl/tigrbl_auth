from collections.abc import Callable

from tigrbl_attestation_bases import AttestationAppraiserBase
from tigrbl_identity_contracts.attestation import (
    AppraisalResult,
    AttestationEvidence,
    EvidenceVerifierPort,
    ReferenceMaterialProviderPort,
)

AppraisalPolicy = Callable[
    [AttestationEvidence, tuple[dict[str, object], ...]], AppraisalResult
]


def exact_reference_value_policy(
    evidence: AttestationEvidence,
    manifests: tuple[dict[str, object], ...],
) -> AppraisalResult:
    expected: dict[str | int, object] = {}
    for manifest in manifests:
        values = manifest.get("reference-values", {})
        if not isinstance(values, dict):
            return AppraisalResult(False, "reference-values must be an object")
        expected.update(values)
    mismatches = tuple(
        str(name)
        for name, value in expected.items()
        if evidence.claims.get(name) != value
    )
    if mismatches:
        return AppraisalResult(
            False, f"evidence mismatched reference values: {mismatches}"
        )
    return AppraisalResult(
        True, "evidence matched reference values", dict(evidence.claims)
    )


class ReferenceBackedAttestationAppraiser(AttestationAppraiserBase):
    def __init__(
        self,
        evidence_verifier: EvidenceVerifierPort,
        reference_provider: ReferenceMaterialProviderPort,
        profile_manifests: dict[str, str],
        policies: dict[str, AppraisalPolicy] | None = None,
    ):
        self._verifier = evidence_verifier
        self._references = reference_provider
        self._profile_manifests = dict(profile_manifests)
        self._policies = dict(policies or {})

    def appraise(self, evidence: AttestationEvidence, /) -> AppraisalResult:
        verification = self._verifier.verify_evidence(evidence)
        if not verification.verified:
            return AppraisalResult(
                False, f"evidence verification failed: {verification.reason}"
            )
        tag_identity = self._profile_manifests.get(evidence.profile)
        if tag_identity is None:
            return AppraisalResult(
                False, "no reference manifest configured for EAT profile"
            )
        try:
            manifest = self._references.resolve_manifest(tag_identity)
        except LookupError:
            return AppraisalResult(False, "reference manifest is unavailable")
        policy = self._policies.get(evidence.profile, exact_reference_value_policy)
        return policy(evidence, tuple(dict(item) for item in manifest.manifests))


__all__ = [
    "AppraisalPolicy",
    "ReferenceBackedAttestationAppraiser",
    "exact_reference_value_policy",
]

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CertificationEvidence:
    conformance_suite: str
    version: str
    passed: bool
    evidence_uri: str | None = None


def certification_claimable(evidence: CertificationEvidence | None) -> bool:
    return bool(evidence and evidence.passed and evidence.evidence_uri)


__all__ = ["CertificationEvidence", "certification_claimable"]

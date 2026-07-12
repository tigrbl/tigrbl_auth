from collections.abc import Mapping
from typing import Any
from tigrbl_identity_contracts.assurance import (
    AssuranceEvidence,
    VerificationMetadata,
    VerifiedClaims,
)

SCHEMA_SPEC_URL = "https://openid.net/specs/openid-ida-verified-claims-1_0-final.html"
OIDC_SPEC_URL = (
    "https://openid.net/specs/openid-connect-4-identity-assurance-1_0-final.html"
)
CLAIMS_SPEC_URL = "https://openid.net/specs/openid-connect-4-ida-claims-1_0-final.html"


def parse_verified_claims(value: Mapping[str, Any]) -> VerifiedClaims:
    verification = value.get("verification")
    claims = value.get("claims")
    if not isinstance(verification, Mapping) or not isinstance(claims, Mapping):
        raise ValueError(
            "verified_claims requires object-valued verification and claims"
        )
    trust_framework = verification.get("trust_framework")
    if not isinstance(trust_framework, str) or not trust_framework:
        raise ValueError("verification.trust_framework must be a non-empty string")
    raw_evidence = verification.get("evidence", ())
    if not isinstance(raw_evidence, (list, tuple)):
        raise ValueError("verification.evidence must be an array")
    evidence = []
    for item in raw_evidence:
        if not isinstance(item, Mapping) or not isinstance(item.get("type"), str):
            raise ValueError("each evidence item requires a string type")
        evidence.append(
            AssuranceEvidence(
                item["type"], {k: v for k, v in item.items() if k != "type"}
            )
        )
    metadata = VerificationMetadata(
        trust_framework=trust_framework,
        assurance_level=verification.get("assurance_level"),
        assurance_process=verification.get("assurance_process"),
        time=verification.get("time"),
        verification_process=verification.get("verification_process"),
        evidence=tuple(evidence),
    )
    return VerifiedClaims(metadata, dict(claims))


def serialize_verified_claims(value: VerifiedClaims) -> dict[str, Any]:
    verification = {"trust_framework": value.verification.trust_framework}
    for name in (
        "assurance_level",
        "assurance_process",
        "time",
        "verification_process",
    ):
        member = getattr(value.verification, name)
        if member is not None:
            verification[name] = member
    if value.verification.evidence:
        verification["evidence"] = [
            {"type": item.type, **dict(item.attributes)}
            for item in value.verification.evidence
        ]
    return {"verification": verification, "claims": dict(value.claims)}


__all__ = [
    "CLAIMS_SPEC_URL",
    "OIDC_SPEC_URL",
    "SCHEMA_SPEC_URL",
    "parse_verified_claims",
    "serialize_verified_claims",
]

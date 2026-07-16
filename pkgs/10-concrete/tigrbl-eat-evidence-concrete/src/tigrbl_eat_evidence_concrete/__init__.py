from __future__ import annotations

from typing import Mapping

from tigrbl_attestation_bases import AttestationEvidenceBase


class EatEvidence(AttestationEvidenceBase):
    """Environment Attestation Token evidence after carrier decoding.

    Cryptographic verification and trust appraisal remain provider/capability work.
    """

    @classmethod
    def from_claims(
        cls,
        profile: str,
        claims: Mapping[str | int, object],
        protected_token: bytes | str | None = None,
    ) -> "EatEvidence":
        if not isinstance(profile, str) or not profile:
            raise ValueError("EAT evidence requires a non-empty profile")
        if not isinstance(claims, Mapping) or not claims:
            raise ValueError("EAT evidence requires decoded claims")
        return cls(profile, dict(claims), protected_token)

    @classmethod
    def from_payload(
        cls, payload: object, protected_token: bytes | str | None = None
    ) -> "EatEvidence":
        profile = getattr(getattr(payload, "profile", None), "identifier", None)
        claims = getattr(payload, "raw_claims", None)
        return cls.from_claims(str(profile or ""), claims or {}, protected_token)


__all__ = ["EatEvidence"]

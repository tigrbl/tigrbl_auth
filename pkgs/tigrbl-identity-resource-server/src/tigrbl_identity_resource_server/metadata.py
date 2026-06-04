"""Consumer helpers for resource-validation verifier metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .verifier import ResourceRequirement


@dataclass(frozen=True, slots=True)
class VerifierContractProfile:
    issuer: str
    audiences: tuple[str, ...]
    required_scopes: tuple[str, ...]
    allowed_algs: tuple[str, ...]
    jwks_uri: str
    introspection_endpoint: str
    max_authz_staleness_seconds: int
    clock_skew_seconds: int
    fail_closed: bool

    def resource_requirement(self) -> ResourceRequirement:
        if not self.audiences:
            raise ValueError("verifier contract has no accepted audience")
        return ResourceRequirement(
            issuer=self.issuer,
            audience=self.audiences[0],
            scopes=self.required_scopes,
            max_authz_staleness_seconds=self.max_authz_staleness_seconds,
        )


def verifier_contract_from_metadata(
    metadata: Mapping[str, Any],
) -> VerifierContractProfile:
    issuer = str(metadata.get("issuer") or "")
    audiences_value = metadata.get("accepted_audiences") or metadata.get("resource") or ()
    if isinstance(audiences_value, str):
        audiences = (audiences_value,)
    else:
        audiences = tuple(str(value) for value in audiences_value)
    scopes_value = metadata.get("required_scopes") or ()
    scopes = (scopes_value,) if isinstance(scopes_value, str) else tuple(str(value) for value in scopes_value)
    algs_value = metadata.get("allowed_algorithms") or ()
    algs = (algs_value,) if isinstance(algs_value, str) else tuple(str(value) for value in algs_value)
    profile = VerifierContractProfile(
        issuer=issuer,
        audiences=audiences,
        required_scopes=scopes,
        allowed_algs=algs,
        jwks_uri=str(metadata.get("jwks_uri") or ""),
        introspection_endpoint=str(metadata.get("introspection_endpoint") or ""),
        max_authz_staleness_seconds=int(metadata.get("max_authz_staleness_seconds", 0)),
        clock_skew_seconds=int(metadata.get("clock_skew_seconds", 0)),
        fail_closed=bool(metadata.get("fail_closed", False)),
    )
    if not profile.issuer:
        raise ValueError("verifier contract requires issuer")
    if not profile.audiences:
        raise ValueError("verifier contract requires accepted audiences")
    if not profile.allowed_algs:
        raise ValueError("verifier contract requires allowed algorithms")
    if not profile.jwks_uri:
        raise ValueError("verifier contract requires jwks_uri")
    if not profile.fail_closed:
        raise ValueError("verifier contract must fail closed")
    return profile


__all__ = [
    "VerifierContractProfile",
    "verifier_contract_from_metadata",
]

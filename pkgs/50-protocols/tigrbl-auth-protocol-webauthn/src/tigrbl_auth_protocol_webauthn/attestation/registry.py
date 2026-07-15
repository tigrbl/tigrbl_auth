"""Attestation format dispatch without provider dependencies."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

from tigrbl_identity_contracts.public_key_authentication import AttestationTrustResult


@dataclass(frozen=True, slots=True)
class AttestationVerificationInput:
    format: str
    statement: Mapping[object, object]
    authenticator_data: bytes
    client_data_hash: bytes
    rp_id_hash: bytes
    credential_id: bytes
    credential_public_key: bytes
    aaguid: bytes


AttestationVerifier = Callable[[AttestationVerificationInput], AttestationTrustResult]


class AttestationVerifierRegistry:
    def __init__(
        self, verifiers: Mapping[str, AttestationVerifier] | None = None
    ) -> None:
        self._verifiers = dict(verifiers or {})

    def register(self, format_identifier: str, verifier: AttestationVerifier) -> None:
        if format_identifier in self._verifiers:
            raise ValueError(
                f"attestation verifier already registered: {format_identifier}"
            )
        self._verifiers[format_identifier] = verifier

    def verify(self, value: AttestationVerificationInput) -> AttestationTrustResult:
        try:
            verifier = self._verifiers[value.format]
        except KeyError as exc:
            raise ValueError(
                f"attestation format requires a configured provider: {value.format}"
            ) from exc
        result = verifier(value)
        if not isinstance(result, AttestationTrustResult):
            raise TypeError("attestation verifier must return AttestationTrustResult")
        return result

    def supported_formats(self) -> tuple[str, ...]:
        return tuple(sorted(self._verifiers))


__all__ = [
    "AttestationVerificationInput",
    "AttestationVerifier",
    "AttestationVerifierRegistry",
]

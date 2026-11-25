"""Compose WebAuthn protocol verification with atomic MFA credential updates."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime

from tba_contracts_identity.public_key_authentication import (
    PublicKeyCredentialSource,
    VerifiedPublicKeyAssertion,
)
from tba_protocol_webauthn.ceremonies.authentication import (
    AuthenticationExpectation,
    verify_authentication_response,
)
from tba_protocol_webauthn.ceremonies.registration import (
    RegistrationExpectation,
    verify_registration_response,
)
from tba_protocol_webauthn.errors import WebAuthnProtocolError
from tba_protocol_webauthn.schemas import PublicKeyCredential

from .contracts import CeremonyKind, FactorAttempt, FactorVerifier, VerifiedFactor


@dataclass(frozen=True, slots=True)
class WebAuthnAssertionUpdate:
    previous: PublicKeyCredentialSource = field(repr=False)
    assertion: VerifiedPublicKeyAssertion = field(repr=False)


def webauthn_verifier(
    *,
    registration: Callable[[FactorAttempt], RegistrationExpectation | None],
    authentication: Callable[[FactorAttempt], AuthenticationExpectation | None],
    allowed_origins: frozenset[str],
) -> FactorVerifier:
    """Verify the host-provided expectations against the bound MFA attempt.

    Callbacks load RP policy and credentials from trusted host state. The origin
    in the expectation must also be in the configured host allowlist.
    """
    allowed_origins = frozenset(allowed_origins)
    if not allowed_origins:
        raise ValueError("at least one WebAuthn origin is required")

    def verify(
        attempt: FactorAttempt, proof: object, now: datetime
    ) -> VerifiedFactor | None:
        if not isinstance(proof, PublicKeyCredential):
            return None
        expected = (
            registration(attempt)
            if attempt.kind == CeremonyKind.ENROLLMENT
            else authentication(attempt)
        )
        if (
            expected is None
            or (attempt.kind == CeremonyKind.ENROLLMENT)
            != isinstance(expected, RegistrationExpectation)
            or expected.ceremony_id != attempt.attempt_id
            or expected.challenge != attempt.challenge
            or expected.origin not in allowed_origins
        ):
            return None
        try:
            if isinstance(expected, RegistrationExpectation):
                if (
                    expected.tenant_id != attempt.binding.scope
                    or expected.principal_id != attempt.binding.subject
                ):
                    return None
                registration_proof = verify_registration_response(
                    proof, expected=expected
                )
                return VerifiedFactor(
                    "passkey", attempt.attempt_id, registration_proof.credential
                )
            previous = expected.credential
            if (
                previous.credential_id != attempt.credential_reference
                or previous.binding.tenant_id != attempt.binding.scope
                or previous.binding.principal_id != attempt.binding.subject
            ):
                return None
            assertion = verify_authentication_response(proof, expected=expected)
        except WebAuthnProtocolError:
            return None
        return VerifiedFactor(
            "passkey",
            attempt.attempt_id,
            WebAuthnAssertionUpdate(previous, assertion),
        )

    return verify

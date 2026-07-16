"""Reusable authenticator mixins."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from typing import Any

from tigrbl_identity_contracts.authenticators import (
    AuthenticationEvidence,
    AuthenticatorProperty,
)
from tigrbl_identity_contracts.credentials import CredentialKind
from tigrbl_identity_contracts.shared_secrets import (
    SecretHash,
    SecretVerificationPort,
)
from tigrbl_security_trust_contracts import AmrValue


class AmrEmitterMixin:
    amr_validator: Callable[[tuple[str, ...]], bool] | None = None

    def normalize_amr(
        self, values: Iterable[AmrValue | str]
    ) -> tuple[AmrValue | str, ...]:
        normalized = tuple(values)
        validator = getattr(self, "amr_validator", None)
        if validator is not None:
            raw = tuple(str(getattr(value, "value", value)) for value in normalized)
            if not validator(raw):
                raise ValueError("unsupported AMR value")
        return normalized

    def evidence(
        self,
        *,
        amr: Iterable[AmrValue | str] | None = None,
        properties: Iterable[AuthenticatorProperty | str] | None = None,
        credential_id: str | None = None,
        challenge_id: str | None = None,
        subject_id: str | None = None,
        raw_claims: Mapping[str, Any] | None = None,
    ) -> AuthenticationEvidence:
        return AuthenticationEvidence(
            amr=self.normalize_amr(
                amr if amr is not None else getattr(self, "amr", ())
            ),
            properties=tuple(
                properties
                if properties is not None
                else getattr(self, "properties", ())
            ),
            authenticator_kind=getattr(self, "kind", None),
            credential_kind=getattr(self, "credential_kind", None),
            credential_id=credential_id,
            challenge_id=challenge_id,
            subject_id=subject_id,
            raw_claims=raw_claims or {},
        )


class CredentialKindMixin:
    credential_kind: CredentialKind | str | None = None

    def expects_credential_kind(self) -> CredentialKind | str | None:
        return self.credential_kind


class CredentialLookupMixin:
    async def lookup_credential(
        self, credential_id: str | None, context: Mapping[str, Any]
    ) -> Any:
        raise NotImplementedError


class ChallengeLifecycleMixin:
    async def load_challenge(
        self, challenge_id: str, context: Mapping[str, Any]
    ) -> Any:
        raise NotImplementedError

    async def consume_challenge(
        self, challenge: Any, context: Mapping[str, Any]
    ) -> Any:
        raise NotImplementedError


class SecretVerifierMixin:
    secret_verifier: SecretVerificationPort

    def verify_secret(
        self,
        presented: str | bytes,
        expected: SecretHash | bytes | str | None,
    ) -> bool:
        return self.secret_verifier.verify_secret(presented, expected).verified


class OtpVerifierMixin:
    def verify_otp(
        self, code: str, secret: Any, *, context: Mapping[str, Any] | None = None
    ) -> bool:
        raise NotImplementedError


class RecoveryCodeVerifierMixin:
    def verify_recovery_code(self, code: str, expected: Any) -> bool:
        raise NotImplementedError


class SenderConstraintMixin:
    sender_constraint_properties = (
        AuthenticatorProperty.SENDER_CONSTRAINED,
        AuthenticatorProperty.REPLAY_RESISTANT,
    )


class RemoteIntrospectionMixin:
    async def introspect(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        raise NotImplementedError


class AalEvidenceMixin:
    aal: str | None = None

    def achieved_aal(self) -> str | None:
        return self.aal


class PhishingResistanceMixin:
    phishing_resistant_properties = (AuthenticatorProperty.PHISHING_RESISTANT,)


class VerifierNameBindingMixin:
    verifier_name_bound_properties = (AuthenticatorProperty.VERIFIER_NAME_BOUND,)


class UserPresenceMixin:
    user_presence_properties = (AuthenticatorProperty.USER_PRESENT,)


class UserVerificationMixin:
    user_verification_properties = (AuthenticatorProperty.USER_VERIFIED,)


__all__ = [
    "AalEvidenceMixin",
    "AmrEmitterMixin",
    "ChallengeLifecycleMixin",
    "CredentialKindMixin",
    "CredentialLookupMixin",
    "OtpVerifierMixin",
    "PhishingResistanceMixin",
    "RecoveryCodeVerifierMixin",
    "RemoteIntrospectionMixin",
    "SecretVerifierMixin",
    "SenderConstraintMixin",
    "UserPresenceMixin",
    "UserVerificationMixin",
    "VerifierNameBindingMixin",
]

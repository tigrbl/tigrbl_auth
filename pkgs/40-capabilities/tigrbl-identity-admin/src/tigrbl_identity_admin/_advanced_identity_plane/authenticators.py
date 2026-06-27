from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
from typing import Any, Callable, Iterable, Mapping, Sequence
from uuid import uuid4

from tigrbl_identity_contracts.adaptive_access import AdaptiveContext, AdaptiveDecision
from tigrbl_identity_contracts.authentication import AuthenticationChallenge
from tigrbl_identity_core.clock import utc_now, utc_now_iso
from tigrbl_identity_credentials_concrete import MfaFactor, PasswordlessCredential, WebAuthnCredential
from tigrbl_identity_jose.standards.rfc8812 import is_webauthn_algorithm
from tigrbl_identity_storage.tables import (
    AuthenticationChallenge as AuthenticationChallengeTable,
    Credential,
    CredentialMfaFactor,
    CredentialRecoveryCode,
    CredentialWebAuthnPasskey,
)


AMR_VALUES = frozenset(
    {
        "face",
        "fpt",
        "geo",
        "hwk",
        "iris",
        "kba",
        "mca",
        "mfa",
        "otp",
        "pin",
        "pwd",
        "rba",
        "retina",
        "sc",
        "sms",
        "swk",
        "tel",
        "user",
        "vbm",
        "wia",
    }
)

def _default_validate_amr_claim(amr: Sequence[str]) -> bool:
    return all(value in AMR_VALUES for value in amr)


def _evaluate_adaptive_context(context: AdaptiveContext) -> AdaptiveDecision:
    reasons: list[str] = []
    risk_score = 0
    if not context.trusted_network:
        risk_score += 1
        reasons.append("untrusted network context")
    if not context.trusted_device:
        risk_score += 2
        reasons.append("unknown or unhealthy device posture")
    if context.local_hour < 6 or context.local_hour > 22:
        risk_score += 1
        reasons.append("outside normal operating hours")
    if context.known_countries and context.ip_country not in context.known_countries:
        risk_score += 2
        reasons.append("unrecognized location")
    if context.anomaly_detected:
        risk_score += 2
        reasons.append("upstream anomaly signal present")

    if risk_score >= 5:
        return AdaptiveDecision(
            allowed=False,
            step_up_required=True,
            risk_level="high",
            reasons=tuple(reasons or ("bounded contextual risk threshold exceeded",)),
            amr=("mfa", "rba"),
        )
    if risk_score >= 2:
        return AdaptiveDecision(
            allowed=True,
            step_up_required=True,
            risk_level="medium",
            reasons=tuple(reasons or ("adaptive step-up required",)),
            amr=("mfa", "rba"),
        )
    return AdaptiveDecision(
        allowed=True,
        step_up_required=False,
        risk_level="low",
        reasons=tuple(reasons or ("context accepted within bounded policy",)),
        amr=("pwd",),
    )


class AdvancedAuthenticatorRegistry:
    credential_table = Credential
    passwordless_table = Credential
    mfa_factor_table = CredentialMfaFactor
    recovery_code_table = CredentialRecoveryCode
    webauthn_passkey_table = CredentialWebAuthnPasskey
    challenge_table = AuthenticationChallengeTable

    def __init__(
        self,
        *,
        amr_validator: Callable[[Sequence[str]], bool] = _default_validate_amr_claim,
        webauthn_algorithm_validator: Callable[[object], bool] = is_webauthn_algorithm,
    ) -> None:
        self._amr_validator = amr_validator
        self._webauthn_algorithm_validator = webauthn_algorithm_validator
        self._passwordless_credentials: dict[str, PasswordlessCredential] = {}
        self._mfa_factors: dict[str, MfaFactor] = {}
        self._webauthn_credentials: dict[str, WebAuthnCredential] = {}
        self._challenges: dict[str, AuthenticationChallenge] = {}

    @property
    def passwordless_credentials(self) -> Mapping[str, PasswordlessCredential]:
        return dict(self._passwordless_credentials)

    @property
    def mfa_factors(self) -> Mapping[str, MfaFactor]:
        return dict(self._mfa_factors)

    @property
    def webauthn_credentials(self) -> Mapping[str, WebAuthnCredential]:
        return dict(self._webauthn_credentials)

    def table_bindings(self) -> dict[str, Any]:
        return {
            "credential": self.credential_table,
            "passwordless": self.passwordless_table,
            "mfa_factor": self.mfa_factor_table,
            "recovery_code": self.recovery_code_table,
            "webauthn_passkey": self.webauthn_passkey_table,
            "challenge": self.challenge_table,
        }

    def enroll_passwordless_credential(
        self,
        *,
        subject_id: str,
        tenant_id: str,
        credential_kind: str = "magic-link",
        recovery_codes: Iterable[str] = (),
    ) -> PasswordlessCredential:
        credential = PasswordlessCredential(
            credential_id=f"pwdless-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            credential_kind=credential_kind,
            recovery_codes=tuple(sorted(set(recovery_codes))),
            created_at=utc_now_iso(),
        )
        self._passwordless_credentials[credential.credential_id] = credential
        return credential

    def revoke_passwordless_credential(self, credential_id: str) -> PasswordlessCredential:
        credential = self._passwordless_credentials[credential_id]
        updated = replace(credential, revoked=True)
        self._passwordless_credentials[credential_id] = updated
        return updated

    def register_webauthn_credential(
        self,
        *,
        subject_id: str,
        tenant_id: str,
        rp_id: str,
        algorithm: str,
        transports: Iterable[str] = (),
    ) -> WebAuthnCredential:
        if not self._webauthn_algorithm_validator(algorithm):
            raise ValueError(f"unsupported WebAuthn algorithm {algorithm!r}")
        credential = WebAuthnCredential(
            credential_id=f"webauthn-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            rp_id=rp_id,
            algorithm=algorithm.upper(),
            transports=tuple(sorted(set(transports))),
            created_at=utc_now_iso(),
        )
        self._webauthn_credentials[credential.credential_id] = credential
        return credential

    def revoke_webauthn_credential(self, credential_id: str) -> WebAuthnCredential:
        credential = self._webauthn_credentials[credential_id]
        updated = replace(credential, revoked=True)
        self._webauthn_credentials[credential_id] = updated
        return updated

    def enroll_mfa_factor(
        self,
        *,
        subject_id: str,
        tenant_id: str,
        method: str,
        bound_credential_id: str | None = None,
    ) -> MfaFactor:
        if not self._amr_validator((method,)):
            raise ValueError(f"unsupported MFA method {method!r}")
        factor = MfaFactor(
            factor_id=f"mfa-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            method=method,
            created_at=utc_now_iso(),
            bound_credential_id=bound_credential_id,
        )
        self._mfa_factors[factor.factor_id] = factor
        return factor

    def revoke_mfa_factor(self, factor_id: str) -> MfaFactor:
        factor = self._mfa_factors[factor_id]
        updated = replace(factor, revoked=True)
        self._mfa_factors[factor_id] = updated
        return updated

    def begin_passwordless_assertion(
        self,
        *,
        subject_id: str,
        tenant_id: str,
        context: AdaptiveContext,
    ) -> tuple[AuthenticationChallenge, AdaptiveDecision]:
        decision = _evaluate_adaptive_context(context)
        allowed_methods = {"passwordless"}
        if any(
            credential.subject_id == subject_id
            and credential.tenant_id == tenant_id
            and not credential.revoked
            for credential in self._webauthn_credentials.values()
        ):
            allowed_methods.add("webauthn")
        if decision.step_up_required:
            allowed_methods.update(
                factor.method
                for factor in self._mfa_factors.values()
                if factor.subject_id == subject_id and factor.tenant_id == tenant_id and not factor.revoked
            )
        challenge = AuthenticationChallenge(
            challenge_id=f"challenge-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            challenge_kind="passwordless",
            expected_nonce=uuid4().hex,
            issued_at=utc_now_iso(),
            expires_at=(utc_now() + timedelta(minutes=5)).isoformat(),
            allowed_methods=tuple(sorted(allowed_methods)),
            step_up_required=decision.step_up_required,
        )
        self._challenges[challenge.challenge_id] = challenge
        return challenge, decision

    def complete_passwordless_assertion(
        self,
        *,
        challenge_id: str,
        credential_id: str,
        nonce: str,
    ) -> AuthenticationChallenge:
        challenge = self._challenges[challenge_id]
        if challenge.consumed:
            raise PermissionError("authentication challenge already consumed")
        if nonce != challenge.expected_nonce:
            raise PermissionError("authentication challenge nonce mismatch")
        if credential_id in self._webauthn_credentials:
            credential = self._webauthn_credentials[credential_id]
            if credential.revoked:
                raise PermissionError("webauthn credential is revoked")
            if credential.subject_id != challenge.subject_id or credential.tenant_id != challenge.tenant_id:
                raise PermissionError("webauthn credential subject mismatch")
            self._webauthn_credentials[credential_id] = replace(
                credential,
                sign_count=credential.sign_count + 1,
            )
        else:
            credential = self._passwordless_credentials.get(credential_id)
            if credential is None or credential.revoked:
                raise PermissionError("passwordless credential is inactive")
            if credential.subject_id != challenge.subject_id or credential.tenant_id != challenge.tenant_id:
                raise PermissionError("passwordless credential subject mismatch")
        completed = replace(challenge, consumed=True, bound_credential_id=credential_id)
        self._challenges[challenge_id] = completed
        return completed

    def begin_mfa_challenge(self, *, subject_id: str, tenant_id: str) -> AuthenticationChallenge:
        methods = sorted(
            factor.method
            for factor in self._mfa_factors.values()
            if factor.subject_id == subject_id and factor.tenant_id == tenant_id and not factor.revoked
        )
        if not methods:
            raise PermissionError("no active MFA factor available")
        challenge = AuthenticationChallenge(
            challenge_id=f"challenge-{uuid4().hex}",
            subject_id=subject_id,
            tenant_id=tenant_id,
            challenge_kind="mfa",
            expected_nonce=uuid4().hex,
            issued_at=utc_now_iso(),
            expires_at=(utc_now() + timedelta(minutes=5)).isoformat(),
            allowed_methods=tuple(methods),
            step_up_required=True,
        )
        self._challenges[challenge.challenge_id] = challenge
        return challenge

    def complete_mfa_challenge(
        self,
        *,
        challenge_id: str,
        factor_id: str,
        method: str,
        nonce: str,
    ) -> AuthenticationChallenge:
        challenge = self._challenges[challenge_id]
        if challenge.challenge_kind != "mfa":
            raise PermissionError("challenge kind mismatch")
        if challenge.consumed:
            raise PermissionError("mfa challenge already consumed")
        if nonce != challenge.expected_nonce:
            raise PermissionError("mfa challenge nonce mismatch")
        factor = self._mfa_factors[factor_id]
        if factor.revoked or factor.method != method:
            raise PermissionError("mfa factor is inactive")
        if factor.subject_id != challenge.subject_id or factor.tenant_id != challenge.tenant_id:
            raise PermissionError("mfa factor subject mismatch")
        completed = replace(challenge, consumed=True, bound_credential_id=factor_id)
        self._challenges[challenge_id] = completed
        return completed

    def summary(self) -> dict[str, Any]:
        return {
            "passwordless_credential_count": len(self._passwordless_credentials),
            "webauthn_credential_count": len(self._webauthn_credentials),
            "mfa_factor_count": len(self._mfa_factors),
            "active_passwordless_credentials": sum(
                not credential.revoked for credential in self._passwordless_credentials.values()
            ),
            "active_webauthn_credentials": sum(
                not credential.revoked for credential in self._webauthn_credentials.values()
            ),
            "active_mfa_factors": sum(not factor.revoked for factor in self._mfa_factors.values()),
            "table_owned": True,
            "challenge_table": self.challenge_table.__name__,
        }


__all__ = ["AdvancedAuthenticatorRegistry"]

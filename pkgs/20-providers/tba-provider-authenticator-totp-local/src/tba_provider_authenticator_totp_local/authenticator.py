"""Local TOTP possession-factor provider."""

import time
from collections.abc import Mapping
from typing import Any

from tba_bases_authenticator import (
    AmrEmitterMixin,
    ChallengeAuthenticatorBase,
    ChallengeLifecycleMixin,
    CredentialKindMixin,
    OtpVerifierMixin,
)
from tba_concrete_totp import match_step
from tba_contracts_identity.authenticators import AuthenticationFactorClass, AuthenticatorKind
from tba_contracts_identity.credentials import CredentialKind

from .provisioning import decode_secret


class TotpLocalAuthenticator(
    AmrEmitterMixin,
    OtpVerifierMixin,
    ChallengeLifecycleMixin,
    CredentialKindMixin,
    ChallengeAuthenticatorBase,
):
    def __init__(self, *, amr_validator=None) -> None:
        self.amr_validator = amr_validator
        super().__init__(
            kind=AuthenticatorKind.OTP_LOCAL,
            factor_class=AuthenticationFactorClass.POSSESSION,
            credential_kind=CredentialKind.MFA_FACTOR,
            amr=("otp",),
            description="Local time-based one-time password authentication.",
        )

    def verify_step(
        self,
        code: str,
        secret: str,
        *,
        timestamp: int | None = None,
        window: int = 0,
        after_step: int = -1,
    ) -> int | None:
        return match_step(
            decode_secret(secret),
            code,
            int(time.time()) if timestamp is None else timestamp,
            window=window,
            after_step=after_step,
        )

    def verify_otp(
        self, code: str, secret: str, *, context: Mapping[str, Any] | None = None
    ) -> bool:
        context = context or {}
        return self.verify_step(
            code,
            secret,
            timestamp=context.get("timestamp"),
            window=context.get("window", 0),
            after_step=context.get("after_step", -1),
        ) is not None

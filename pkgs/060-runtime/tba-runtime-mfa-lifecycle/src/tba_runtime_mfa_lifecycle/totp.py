"""Compose a TBA TOTP provider with the transactional MFA lifecycle."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from .contracts import FactorAttempt, FactorVerifier, VerifiedFactor


class TotpProvider(Protocol):
    def verify_step(
        self,
        code: str,
        secret: str,
        *,
        timestamp: int | None = None,
        window: int = 0,
        after_step: int = -1,
    ) -> int | None: ...


@dataclass(frozen=True, slots=True)
class TotpCredential:
    reference: str
    secret: str = field(repr=False)
    last_step: int = -1


@dataclass(frozen=True, slots=True)
class TotpProofUpdate:
    reference: str
    previous_step: int
    verified_step: int


def totp_verifier(
    provider: TotpProvider,
    resolve: Callable[[FactorAttempt], TotpCredential | None],
    *,
    window: int = 0,
) -> FactorVerifier:
    """Verify a code using the bound candidate or active factor's current state."""
    if window < 0:
        raise ValueError("TOTP verification window must be nonnegative")

    def verify(
        attempt: FactorAttempt, proof: object, now: datetime
    ) -> VerifiedFactor | None:
        if not isinstance(proof, str) or attempt.credential_reference is None:
            return None
        credential = resolve(attempt)
        if credential is None or credential.reference != attempt.credential_reference:
            return None
        step = provider.verify_step(
            proof,
            credential.secret,
            timestamp=int(now.timestamp()),
            window=window,
            after_step=credential.last_step,
        )
        if step is None or step <= credential.last_step:
            return None
        return VerifiedFactor(
            method="otp",
            replay_key=f"{credential.reference}:{step}",
            credential=TotpProofUpdate(
                credential.reference, credential.last_step, step
            ),
        )

    return verify

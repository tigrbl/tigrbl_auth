"""Base classes for authenticator providers."""

from __future__ import annotations

from tigrbl_identity_contracts.authentication import AuthenticationChallenge
from tigrbl_identity_contracts.authenticators import (
    AuthenticationFactorClass,
    AuthenticationRequest,
    AuthenticationResult,
    AuthenticatorKind,
    AuthenticatorMetadata,
    AuthenticatorProperty,
    ChallengeFinishRequest,
    ChallengeStartRequest,
)
from tigrbl_identity_contracts.credentials import CredentialKind
from tigrbl_security_trust_contracts import AmrValue


class AuthenticatorBase:
    """Base for a single authenticator ceremony or proof verifier."""

    kind: AuthenticatorKind | str
    factor_class: AuthenticationFactorClass | str
    credential_kind: CredentialKind | str | None
    amr: tuple[AmrValue | str, ...]
    properties: tuple[AuthenticatorProperty | str, ...]
    challenge_based: bool
    description: str | None

    def __init__(
        self,
        *,
        kind: AuthenticatorKind | str,
        factor_class: AuthenticationFactorClass | str,
        credential_kind: CredentialKind | str | None = None,
        amr: tuple[AmrValue | str, ...] = (),
        properties: tuple[AuthenticatorProperty | str, ...] = (),
        challenge_based: bool = False,
        description: str | None = None,
    ) -> None:
        self.kind = kind
        self.factor_class = factor_class
        self.credential_kind = credential_kind
        self.amr = amr
        self.properties = properties
        self.challenge_based = challenge_based
        self.description = description

    def metadata(self) -> AuthenticatorMetadata:
        return AuthenticatorMetadata(
            kind=self.kind,
            factor_class=self.factor_class,
            credential_kind=self.credential_kind,
            amr=self.amr,
            properties=self.properties,
            challenge_based=self.challenge_based,
            description=self.description,
        )

    def supported_amr(self) -> tuple[AmrValue | str, ...]:
        return self.amr

    async def authenticate(self, request: AuthenticationRequest) -> AuthenticationResult:
        raise NotImplementedError


class ChallengeAuthenticatorBase(AuthenticatorBase):
    """Base for authenticators that require a start/finish challenge ceremony."""

    def __init__(self, **kwargs: object) -> None:
        kwargs.setdefault("challenge_based", True)
        super().__init__(**kwargs)  # type: ignore[arg-type]

    async def start_challenge(self, request: ChallengeStartRequest) -> AuthenticationChallenge:
        raise NotImplementedError

    async def finish_challenge(self, request: ChallengeFinishRequest) -> AuthenticationResult:
        raise NotImplementedError


__all__ = ["AuthenticatorBase", "ChallengeAuthenticatorBase"]

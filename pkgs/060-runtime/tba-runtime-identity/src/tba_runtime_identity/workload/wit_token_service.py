"""A trust-domain WIT token service using the existing compact JWT signer."""

from collections.abc import Awaitable, Callable, Mapping
from copy import deepcopy
from dataclasses import dataclass
from time import time
from urllib.parse import urlsplit

from tba_profile_workload_credential_wimse_wit import issue_wit
from tba_provider_jose_cryptography.jws import ProtectedEnvelopeIssuerPort
from tba_provider_jose_cryptography.public_jws import public_jwk_key

from .enrollment import ResolveWorkloadIdentity, resolve_enrolled_identity


@dataclass(frozen=True, slots=True)
class WitIssuerConfig:
    trust_domain: str
    issuer: str
    key_reference: str
    key_id: str
    algorithm: str
    lifetime_seconds: int = 900

    def __post_init__(self) -> None:
        if not (
            self.trust_domain
            and urlsplit(self.issuer).scheme
            and self.key_id
            and self.key_reference
            and self.algorithm
            and self.algorithm.lower() != "none"
            and not self.algorithm.startswith("HS")
            and type(self.lifetime_seconds) is int
            and self.lifetime_seconds > 0
        ):
            raise ValueError("invalid WIT issuer configuration")


class WitTokenService:
    def __init__(
        self,
        signer: ProtectedEnvelopeIssuerPort,
        config: WitIssuerConfig,
        *,
        resolve_identity: ResolveWorkloadIdentity,
        authorize_confirmation_key: Callable[
            [str, Mapping[str, object]], Awaitable[bool]
        ],
        clock: Callable[[], float] = time,
    ) -> None:
        self._signer = signer
        self._config = config
        self._resolve_identity = resolve_identity
        self._authorize_key = authorize_confirmation_key
        self._clock = clock

    async def issue(
        self, principal: str, confirmation_jwk: Mapping[str, object]
    ) -> str:
        config = self._config
        identity = await resolve_enrolled_identity(
            principal, config.trust_domain, self._resolve_identity
        )
        key = deepcopy(dict(confirmation_jwk))
        if not isinstance(key.get("alg"), str):
            raise ValueError("confirmation JWK requires an algorithm")
        public_jwk_key(key, key["alg"])
        if await self._authorize_key(principal, deepcopy(key)) is not True:
            raise PermissionError("workload confirmation key is not authorized")
        now = int(self._clock())
        return issue_wit(
            self._signer,
            subject=str(identity),
            confirmation_jwk=key,
            issuer_key_reference=config.key_reference,
            issuer_key_id=config.key_id,
            issuer_algorithm=config.algorithm,
            issued_at=now,
            expires_at=now + config.lifetime_seconds,
            issuer=config.issuer,
        )

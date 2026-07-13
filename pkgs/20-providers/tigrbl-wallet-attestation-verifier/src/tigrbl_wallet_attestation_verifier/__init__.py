from collections.abc import Callable, Mapping
from time import time

from tigrbl_digital_credential_bases import WalletAttestationVerifierBase

WalletTokenVerifier = Callable[
    [str, str], tuple[Mapping[str, object], Mapping[str, object]]
]
ReplayConsumer = Callable[[str, str], bool]


class ProfiledWalletAttestationVerifier(WalletAttestationVerifierBase):
    def __init__(
        self,
        token_verifier: WalletTokenVerifier,
        expected_issuer: str,
        expected_audience: str,
        replay_consumer: ReplayConsumer,
        allowed_key_protections: set[str] | None = None,
    ):
        self._verify = token_verifier
        self._issuer = expected_issuer
        self._audience = expected_audience
        self._replay = replay_consumer
        self._protections = set(
            allowed_key_protections or {"hardware", "tee", "secure-element"}
        )

    def verify_wallet_attestation(self, attestation: bytes | str, /) -> bool:
        if not isinstance(attestation, str):
            return False
        try:
            header, claims = self._verify(attestation, "wallet-attestation")
            if header.get("typ") != "wallet-attestation+jwt":
                return False
            if claims.get("iss") != self._issuer:
                return False
            audience = claims.get("aud")
            audiences = (
                (audience,) if isinstance(audience, str) else tuple(audience or ())
            )
            if self._audience not in audiences:
                return False
            issued_at, expiration, token_id = (
                claims.get("iat"),
                claims.get("exp"),
                claims.get("jti"),
            )
            if any(
                not isinstance(value, int) or isinstance(value, bool)
                for value in (issued_at, expiration)
            ):
                return False
            if (
                expiration <= int(time())
                or not isinstance(token_id, str)
                or not token_id
            ):
                return False
            if claims.get("key_protection") not in self._protections:
                return False
            if not isinstance(claims.get("wallet_instance_id"), str):
                return False
            return self._replay(self._issuer, token_id)
        except (TypeError, ValueError):
            return False


__all__ = ["ProfiledWalletAttestationVerifier", "ReplayConsumer", "WalletTokenVerifier"]

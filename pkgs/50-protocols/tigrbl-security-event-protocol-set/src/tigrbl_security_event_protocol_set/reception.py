from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone

from tigrbl_identity_contracts.replay import ReplayCheckPort
from tigrbl_identity_contracts.security_events import (
    SecurityEvent,
    SecurityEventSubject,
)
from tigrbl_security_event_bases import SecurityEventReceiverBase
from tigrbl_set_concrete import SET_TYP, validate_security_event_claims


@dataclass(frozen=True, slots=True)
class VerifiedSetToken:
    protected_header: Mapping[str, object]
    claims: Mapping[str, object]
    profile: str


SetTokenVerifier = Callable[[str | bytes, str], VerifiedSetToken]


class SetReceiverProvider(SecurityEventReceiverBase):
    """Map a profile-verified RFC 8417 SET into a normalized security event."""

    def __init__(
        self,
        verifier: SetTokenVerifier,
        replay: ReplayCheckPort,
        expected_issuer: str,
        expected_audience: str,
    ):
        self._verifier = verifier
        self._replay = replay
        self._issuer = expected_issuer
        self._audience = expected_audience

    def receive(self, encoded_event: str | bytes, /) -> SecurityEvent:
        verified = self._verifier(encoded_event, "security-event-token")
        if verified.profile != "security-event-token":
            raise ValueError(
                "token was not verified under the Security Event Token profile"
            )
        if verified.protected_header.get("typ") != SET_TYP:
            raise ValueError("SET protected typ must be secevent+jwt")
        claims = validate_security_event_claims(
            verified.claims,
            expected_issuer=self._issuer,
            expected_audience=self._audience,
        )
        replay_key = f"set:{claims['iss']}:{claims['jti']}"
        ttl_s = max(
            1,
            int(claims.get("exp", claims["iat"] + 300)) - int(claims["iat"]),
        )
        if not self._replay.check_and_store(replay_key, ttl_s=ttl_s):
            raise ValueError("Security Event Token replay detected")
        events = claims["events"]
        if len(events) != 1:
            raise ValueError(
                "normalized SecurityEvent requires exactly one SET event type"
            )
        event_type, data = next(iter(events.items()))
        subject = (
            SecurityEventSubject("sub", {"sub": claims["sub"]})
            if isinstance(claims.get("sub"), str)
            else None
        )
        audience = claims["aud"]
        audience = (audience,) if isinstance(audience, str) else tuple(audience)
        return SecurityEvent(
            event_type,
            claims["iss"],
            audience,
            claims["jti"],
            datetime.fromtimestamp(claims["iat"], timezone.utc),
            subject,
            data,
        )


__all__ = ["SetReceiverProvider", "SetTokenVerifier", "VerifiedSetToken"]

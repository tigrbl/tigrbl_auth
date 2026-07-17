from collections.abc import Callable, Mapping

from tigrbl_identity_contracts.security_events import SecurityEvent
from tigrbl_security_event_bases import SecurityEventTransmitterBase
from tigrbl_set_concrete import SET_TYP, build_security_event_claims

SetSigner = Callable[[Mapping[str, object], Mapping[str, object], str], str]


class SetTransmitterProvider(SecurityEventTransmitterBase):
    """Map normalized events into RFC 8417 SETs using an injected signer."""

    def __init__(self, signer: SetSigner):
        self._signer = signer

    def transmit(self, event: SecurityEvent, subscriber: str, /) -> str:
        if subscriber not in event.audience:
            raise ValueError("SET subscriber is not an event audience")
        subject = None
        if event.subject is not None:
            subject = event.subject.identifiers.get("sub")
            if event.subject.format != "sub" or not subject:
                raise ValueError("RFC 8417 SET subject must use the simple sub format")
        claims = build_security_event_claims(
            issuer=event.issuer,
            audience=event.audience,
            events={event.event_type: event.data},
            subject=subject,
            issued_at=int(event.issued_at.timestamp()),
            token_id=event.token_id,
        )
        token = self._signer(claims, {"typ": SET_TYP}, "security-event-token")
        if not isinstance(token, str) or token.count(".") != 2:
            raise ValueError("SET signer must return a compact JWS")
        return token


__all__ = ["SetSigner", "SetTransmitterProvider"]

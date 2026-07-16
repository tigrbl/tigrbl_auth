"""Compatibility exports; EAT profiles and revisions are owned by layer 50."""

from tigrbl_attestation_protocol_eat import EatProfile

RFC_REVISION = "RFC 9711"
EAT_MEDIA_TYPES = frozenset({"application/eat+cwt", "application/eat+jwt"})
__all__ = ["EAT_MEDIA_TYPES", "RFC_REVISION", "EatProfile"]

"""Compatibility exports; EAT claim-set schemas are owned by layer 50."""

from tigrbl_attestation_protocol_eat import (
    EatClaimSetPayload,
    EatEncoding,
    parse_eat_claims,
)

__all__ = ["EatClaimSetPayload", "EatEncoding", "parse_eat_claims"]

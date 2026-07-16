"""Compatibility exports; EAT revision validation is owned by layer 50."""

from tigrbl_attestation_protocol_eat import parse_eat, validate_eat_claims

__all__ = ["parse_eat", "validate_eat_claims"]

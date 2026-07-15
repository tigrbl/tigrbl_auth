"""Compatibility exports for the canonical OAuth verifier-contract mapping."""

from tigrbl_auth_protocol_oauth.standards.resource_verifier_contract import (
    ProtectedResourceVerifierContract,
    build_protected_resource_verifier_contract,
)

__all__ = [
    "ProtectedResourceVerifierContract",
    "build_protected_resource_verifier_contract",
]

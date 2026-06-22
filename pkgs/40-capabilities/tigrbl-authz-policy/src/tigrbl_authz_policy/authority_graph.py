"""Compatibility re-export for authority graph helpers."""

from __future__ import annotations

from .authority import (
    AuthorityDerivationGraph,
    AuthorityEdge,
    AuthorityGraphIntegrityReport,
    AuthorityNode,
    AuthorityPath,
    AuthorityReachabilityProof,
    AuthorityScope,
    authority_matches,
    validate_authority_graph_integrity,
)

__all__ = [
    "AuthorityDerivationGraph",
    "AuthorityEdge",
    "AuthorityGraphIntegrityReport",
    "AuthorityNode",
    "AuthorityPath",
    "AuthorityReachabilityProof",
    "AuthorityScope",
    "authority_matches",
    "validate_authority_graph_integrity",
]

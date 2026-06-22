"""Compatibility re-export for authority semantic helpers."""

from __future__ import annotations

from .authority import (
    AuthorityClosure,
    AuthorityMonotonicityReport,
    AuthorityMutationKind,
    LeastAuthorityDiff,
    compare_authority_monotonicity,
    compute_authority_closure,
    diff_least_authority,
)

__all__ = [
    "AuthorityClosure",
    "AuthorityMutationKind",
    "AuthorityMonotonicityReport",
    "LeastAuthorityDiff",
    "compare_authority_monotonicity",
    "compute_authority_closure",
    "diff_least_authority",
]

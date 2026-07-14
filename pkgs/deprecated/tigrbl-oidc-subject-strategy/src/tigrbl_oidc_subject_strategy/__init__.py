"""Deprecated OIDC-named facade for neutral subject strategies."""

import warnings

from tigrbl_pairwise_subject_identifier_concrete import PairwiseSubjectIdentifierStrategy
from tigrbl_public_subject_identifier_concrete import PublicSubjectIdentifierStrategy

warnings.warn(
    "tigrbl_oidc_subject_strategy is deprecated; use the standalone subject "
    "identifier concrete packages",
    DeprecationWarning,
    stacklevel=2,
)

PublicSubjectStrategy = PublicSubjectIdentifierStrategy
PairwiseSubjectStrategy = PairwiseSubjectIdentifierStrategy

__all__ = [
    "PairwiseSubjectIdentifierStrategy",
    "PairwiseSubjectStrategy",
    "PublicSubjectIdentifierStrategy",
    "PublicSubjectStrategy",
]

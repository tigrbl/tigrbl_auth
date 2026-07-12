"""Deprecated compatibility façade for protocol-neutral subject identifiers."""

from tigrbl_pairwise_subject_identifier_concrete import (
    PairwiseSubjectIdentifierStrategy,
)
from tigrbl_public_subject_identifier_concrete import PublicSubjectIdentifierStrategy

PairwiseSubjectStrategy = PairwiseSubjectIdentifierStrategy
PublicSubjectStrategy = PublicSubjectIdentifierStrategy
__all__ = [
    "PairwiseSubjectIdentifierStrategy",
    "PairwiseSubjectStrategy",
    "PublicSubjectIdentifierStrategy",
    "PublicSubjectStrategy",
]

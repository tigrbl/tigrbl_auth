"""Compatibility re-export for delegation proof helpers."""

from __future__ import annotations

from .delegation import (
    DelegationAttenuationProof,
    DelegationGrantSpec,
    prove_delegation_attenuation,
)

__all__ = [
    "DelegationAttenuationProof",
    "DelegationGrantSpec",
    "prove_delegation_attenuation",
]

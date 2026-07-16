"""Base classes for authorization provenance providers."""

from abc import ABC
from typing import Any, Mapping

from tigrbl_security_trust_contracts import (
    AuthorizationDecisionTrace,
    CapabilityMap,
    DelegationProvenance,
    IProvenanceArtifactBuilder,
)
from tigrbl_capability_bases import CapabilityProviderBase


class ProvenanceArtifactBuilderBase(
    IProvenanceArtifactBuilder,
    CapabilityProviderBase,
    ABC,
):
    def supports(self) -> CapabilityMap:
        raise NotImplementedError

    def build_authorization_decision_trace(
        self, **kwargs: Any
    ) -> AuthorizationDecisionTrace | Mapping[str, Any]:
        raise NotImplementedError

    def build_delegation_provenance(
        self, **kwargs: Any
    ) -> DelegationProvenance | Mapping[str, Any]:
        raise NotImplementedError


__all__ = ["ProvenanceArtifactBuilderBase"]

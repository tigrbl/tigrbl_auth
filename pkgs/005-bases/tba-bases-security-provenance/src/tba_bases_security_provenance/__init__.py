"""Base classes for authorization provenance providers."""

from abc import ABC
from typing import Any, Mapping

from tba_contracts_security_trust import (
    AuthorizationDecisionTrace,
    CapabilityMap,
    DelegationProvenance,
    IProvenanceArtifactBuilder,
)
from tba_bases_capability import CapabilityProviderBase


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

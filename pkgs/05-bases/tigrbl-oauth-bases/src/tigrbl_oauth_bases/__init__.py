"""Base classes for concrete OAuth implementations."""

from abc import ABC

from tigrbl_identity_contracts.oauth import ScopeMatcherPort, ScopeMatchRequest, ScopeMatchResult


class ScopeMatcherBase(ScopeMatcherPort, ABC):
    def match(self, request: ScopeMatchRequest, /) -> ScopeMatchResult:
        raise NotImplementedError


__all__ = ["ScopeMatcherBase"]

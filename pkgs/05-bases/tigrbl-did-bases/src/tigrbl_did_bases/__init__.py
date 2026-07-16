"""Reusable DID resolver behavior."""

from abc import ABC

from tigrbl_did_contracts import Did, DidResolutionResult, DidResolverPort, DidUrl


class DidResolverBase(DidResolverPort, ABC):
    def resolve(self, did: Did, /) -> DidResolutionResult:
        raise NotImplementedError

    def dereference(self, did_url: DidUrl, /):
        raise NotImplementedError


__all__ = ["DidResolverBase"]

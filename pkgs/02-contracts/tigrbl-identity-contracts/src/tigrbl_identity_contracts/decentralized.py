"""Deprecated compatibility imports for canonical DID contracts."""

from __future__ import annotations

from tigrbl_did_contracts import Did, DidResolutionResult, DidResolverPort

DidResolver = DidResolverPort


__all__ = ["Did", "DidResolutionResult", "DidResolver"]

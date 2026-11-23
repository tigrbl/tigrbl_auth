"""Compatibility exports; scope-set semantics are protocol neutral."""

from ..authorization_scopes import ScopeMatcherPort, ScopeMatchRequest, ScopeMatchResult

__all__ = ["ScopeMatchRequest", "ScopeMatchResult", "ScopeMatcherPort"]

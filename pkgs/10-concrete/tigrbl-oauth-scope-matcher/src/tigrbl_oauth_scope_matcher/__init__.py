"""Deprecated compatibility façade for protocol-neutral scope-set matching."""

from tigrbl_authorization_scope_set_matcher_concrete import ScopeSetMatcher

DefaultScopeMatcher = ScopeSetMatcher
__all__ = ["DefaultScopeMatcher", "ScopeSetMatcher"]

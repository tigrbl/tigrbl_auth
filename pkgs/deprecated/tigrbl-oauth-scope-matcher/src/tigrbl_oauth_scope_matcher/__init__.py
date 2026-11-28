"""Deprecated OAuth-named facade for the neutral scope-set matcher."""

import warnings

from tigrbl_authorization_scope_set_matcher_concrete import ScopeSetMatcher

warnings.warn(
    "tigrbl_oauth_scope_matcher is deprecated; use "
    "tigrbl_authorization_scope_set_matcher_concrete",
    DeprecationWarning,
    stacklevel=2,
)

DefaultScopeMatcher = ScopeSetMatcher

__all__ = ["DefaultScopeMatcher", "ScopeSetMatcher"]

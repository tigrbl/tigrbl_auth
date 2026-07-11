from __future__ import annotations

from tigrbl_oauth_bases import ScopeMatcherBase
from tigrbl_identity_contracts.oauth import ScopeMatchRequest, ScopeMatchResult


class DefaultScopeMatcher(ScopeMatcherBase):
    def match(self, request: ScopeMatchRequest, /) -> ScopeMatchResult:
        granted = set(request.granted)
        required = set(request.required)
        if request.mode == "any":
            allowed = not required or bool(granted & required)
            missing = () if allowed else tuple(sorted(required))
        else:
            missing = tuple(sorted(required - granted))
            allowed = not missing
        return ScopeMatchResult(
            allowed=allowed,
            granted=tuple(sorted(granted)),
            required=tuple(sorted(required)),
            missing=missing,
        )


__all__ = ["DefaultScopeMatcher"]

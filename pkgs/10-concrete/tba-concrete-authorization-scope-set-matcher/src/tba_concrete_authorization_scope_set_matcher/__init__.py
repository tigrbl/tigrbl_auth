from tba_bases_authorization_policy import ScopeMatcherBase
from tba_contracts_identity.authorization_scopes import (
    ScopeMatchRequest,
    ScopeMatchResult,
)


class ScopeSetMatcher(ScopeMatcherBase):
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
            allowed, tuple(sorted(granted)), tuple(sorted(required)), missing
        )


__all__ = ["ScopeSetMatcher"]

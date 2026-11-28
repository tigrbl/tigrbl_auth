"""Authority graph service ports."""

from __future__ import annotations

from typing import Mapping, Protocol

from .graph import (
    AuthorityEdge,
    AuthorityNode,
    AuthorityPath,
    AuthorityReachabilityProof,
    AuthorityScope,
)


class AuthorityGraphPort(Protocol):
    @property
    def nodes(self) -> Mapping[str, AuthorityNode]: ...

    @property
    def edges(self) -> Mapping[str, AuthorityEdge]: ...

    def add_node(self, node: AuthorityNode) -> AuthorityNode: ...

    def add_edge(self, edge: AuthorityEdge) -> AuthorityEdge: ...

    def outgoing(self, node_id: str) -> tuple[AuthorityEdge, ...]: ...

    def derive_paths(self, subject: str) -> tuple[AuthorityPath, ...]: ...

    def effective_scopes(self, subject: str) -> tuple[AuthorityScope, ...]: ...

    def prove_reachability(
        self,
        subject: str,
        requested: AuthorityScope,
    ) -> AuthorityReachabilityProof: ...


__all__ = ["AuthorityGraphPort"]

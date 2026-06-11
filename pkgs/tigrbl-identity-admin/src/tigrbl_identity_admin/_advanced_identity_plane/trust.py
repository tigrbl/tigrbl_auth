from __future__ import annotations

from collections import deque
from dataclasses import replace
from typing import Any, Iterable, Mapping

from .models import TrustDomain, TrustEdge, TrustPath, WorkloadIdentity


class TrustFederationGraph:
    def __init__(self) -> None:
        self._domains: dict[str, TrustDomain] = {}
        self._edges: list[TrustEdge] = []

    @property
    def domains(self) -> Mapping[str, TrustDomain]:
        return dict(self._domains)

    @property
    def edges(self) -> tuple[TrustEdge, ...]:
        return tuple(self._edges)

    def add_domain(self, *, name: str, issuers: Iterable[str], clouds: Iterable[str]) -> TrustDomain:
        domain = TrustDomain(
            name=name,
            issuers=tuple(sorted(set(issuers))),
            clouds=tuple(sorted(set(clouds))),
        )
        self._domains[name] = domain
        return domain

    def add_edge(
        self,
        *,
        source_domain: str,
        target_domain: str,
        exchange_kind: str,
        constraints: Mapping[str, Any],
    ) -> TrustEdge:
        if source_domain not in self._domains or target_domain not in self._domains:
            raise KeyError("trust domains must exist before adding an edge")
        edge = TrustEdge(
            source_domain=source_domain,
            target_domain=target_domain,
            exchange_kind=exchange_kind,
            constraints=dict(constraints),
        )
        self._edges.append(edge)
        return edge

    def revoke_edge(self, *, source_domain: str, target_domain: str) -> TrustEdge:
        for index, edge in enumerate(self._edges):
            if edge.source_domain == source_domain and edge.target_domain == target_domain and not edge.revoked:
                updated = replace(edge, revoked=True)
                self._edges[index] = updated
                return updated
        raise KeyError("trust edge not found")

    def resolve_path(self, *, source_domain: str, target_domain: str, max_hops: int = 5) -> TrustPath:
        queue: deque[tuple[str, tuple[str, ...], tuple[str, ...]]] = deque(
            [(source_domain, (), (source_domain,))]
        )
        seen: set[str] = set()
        while queue:
            current, exchange_kinds, hops = queue.popleft()
            if current == target_domain:
                return TrustPath(
                    source_domain=source_domain,
                    target_domain=target_domain,
                    hops=hops,
                    exchange_kinds=exchange_kinds,
                )
            if current in seen or len(hops) > max_hops:
                continue
            seen.add(current)
            for edge in self._edges:
                if edge.revoked or edge.source_domain != current:
                    continue
                queue.append(
                    (
                        edge.target_domain,
                        exchange_kinds + (edge.exchange_kind,),
                        hops + (edge.target_domain,),
                    )
                )
        raise PermissionError("no active trust path found")

    def map_cross_cloud_workload(
        self,
        *,
        workload: WorkloadIdentity,
        target_domain: str,
    ) -> dict[str, Any]:
        path = self.resolve_path(source_domain=workload.trust_domain, target_domain=target_domain)
        target = self._domains[target_domain]
        return {
            "workload_id": workload.workload_id,
            "source_domain": workload.trust_domain,
            "target_domain": target_domain,
            "source_cloud": workload.cloud,
            "target_clouds": list(target.clouds),
            "path": list(path.hops),
            "exchange_kinds": list(path.exchange_kinds),
        }

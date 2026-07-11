from __future__ import annotations

from collections import deque
from dataclasses import replace
from typing import Any, Iterable, Mapping

from tigrbl_identity_contracts.adaptive_access import TrustDomain, TrustEdge, TrustPath

from tigrbl_identity_identities_concrete import WorkloadIdentity
from tigrbl_identity_storage.tables import (
    TrustFederationGraph as TrustFederationGraphTable,
    TrustFederationGraphEdge,
    TrustFederationGraphNode,
)


class TrustFederationGraph:
    graph_table = TrustFederationGraphTable
    node_table = TrustFederationGraphNode
    edge_table = TrustFederationGraphEdge

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


def _field(row: object, key: str, default: object = None) -> object:
    if isinstance(row, Mapping):
        return row.get(key, default)
    return getattr(row, key, default)


def trust_domain_to_graph_node_payload(domain: TrustDomain, *, graph_id: object | None = None) -> dict[str, object]:
    payload: dict[str, object] = {
        "node_key": domain.name,
        "kind": "trust_domain",
        "issuers": list(domain.issuers),
        "clouds": list(domain.clouds),
        "node_metadata": {
            "issuers": list(domain.issuers),
            "clouds": list(domain.clouds),
        },
    }
    if graph_id is not None:
        payload["graph_id"] = graph_id
    return payload


def trust_edge_to_graph_edge_payload(
    edge: TrustEdge,
    *,
    graph_id: object | None = None,
    src_id: object | None = None,
    dst_id: object | None = None,
) -> dict[str, object]:
    edge_key = f"{edge.source_domain}->{edge.target_domain}:{edge.exchange_kind}"
    payload: dict[str, object] = {
        "edge_key": edge_key,
        "kind": edge.exchange_kind,
        "exchange_kind": edge.exchange_kind,
        "constraints": dict(edge.constraints),
        "active": not edge.revoked,
        "revoked": edge.revoked,
        "edge_metadata": {
            "source_domain": edge.source_domain,
            "target_domain": edge.target_domain,
        },
    }
    if graph_id is not None:
        payload["graph_id"] = graph_id
    if src_id is not None:
        payload["src_id"] = src_id
    if dst_id is not None:
        payload["dst_id"] = dst_id
    return payload


def graph_node_to_trust_domain(row: object) -> TrustDomain:
    return TrustDomain(
        name=str(_field(row, "node_key") or ""),
        issuers=tuple(str(value) for value in (_field(row, "issuers", ()) or ())),
        clouds=tuple(str(value) for value in (_field(row, "clouds", ()) or ())),
    )


def graph_edge_to_trust_edge(
    row: object,
    *,
    source_domain: str | None = None,
    target_domain: str | None = None,
) -> TrustEdge:
    metadata = dict(_field(row, "edge_metadata", {}) or {})
    return TrustEdge(
        source_domain=source_domain or str(metadata.get("source_domain") or ""),
        target_domain=target_domain or str(metadata.get("target_domain") or ""),
        exchange_kind=str(_field(row, "exchange_kind") or _field(row, "kind") or ""),
        constraints=dict(_field(row, "constraints", {}) or {}),
        revoked=bool(_field(row, "revoked", False)),
    )


__all__ = [
    "TrustFederationGraph",
    "TrustFederationGraphTable",
    "TrustFederationGraphNode",
    "TrustFederationGraphEdge",
    "graph_edge_to_trust_edge",
    "graph_node_to_trust_domain",
    "trust_domain_to_graph_node_payload",
    "trust_edge_to_graph_edge_payload",
]

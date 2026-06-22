from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_authz_policy_authority_derivation_graph import (
    AuthorityClosure,
    AuthorityDerivationGraph,
    AuthorityEdge,
    AuthorityMutationKind,
    AuthorityNode,
    AuthorityScope,
    authority_matches,
    compare_authority_monotonicity,
    compute_authority_closure,
    diff_least_authority,
)


def _graph(scopes: tuple[AuthorityScope, ...], *, edge_prefix: str = "edge") -> AuthorityDerivationGraph:
    return AuthorityDerivationGraph(
        nodes=(AuthorityNode("subject:alice", "subject"), AuthorityNode("authority:client", "authority")),
        edges=tuple(
            AuthorityEdge(f"{edge_prefix}:{idx}", "subject:alice", "authority:client", "grant", (scope,))
            for idx, scope in enumerate(scopes)
        ),
    )


def test_authority_closure_monotonicity_t2_wildcard_boundaries_and_empty_closure() -> None:
    assert authority_matches("client.*", "client.read") is True
    assert authority_matches("client.*", "tenant.read") is False

    empty_known = compute_authority_closure(AuthorityDerivationGraph(nodes=(AuthorityNode("subject:alice", "subject"),)), "subject:alice")
    empty_unknown = compute_authority_closure(AuthorityDerivationGraph(), "subject:missing")

    assert empty_known.scopes == ()
    assert empty_unknown.scopes == ()


def test_authority_closure_monotonicity_t2_grant_cannot_remove_and_replace_explains_delta() -> None:
    before = compute_authority_closure(
        _graph((AuthorityScope("tenant-a", "client.read"), AuthorityScope("tenant-a", "client.write"))),
        "subject:alice",
    )
    after_grant = compute_authority_closure(_graph((AuthorityScope("tenant-a", "client.read"),)), "subject:alice")

    grant_report = compare_authority_monotonicity(before, after_grant, mutation_kind=AuthorityMutationKind.GRANT)

    assert grant_report.passed is False
    assert tuple(scope.action for scope in grant_report.removed) == ("client.write",)

    after_replace = compute_authority_closure(_graph((AuthorityScope("tenant-a", "client.delete"),)), "subject:alice")
    replace_report = compare_authority_monotonicity(before, after_replace, mutation_kind=AuthorityMutationKind.REPLACE)

    assert replace_report.passed is True
    assert tuple(scope.action for scope in replace_report.added) == ("client.delete",)
    assert tuple(scope.action for scope in replace_report.removed) == ("client.read", "client.write")


def test_authority_closure_monotonicity_t2_least_authority_missing_excess_minimal_and_tenant_boundaries() -> None:
    exact = compute_authority_closure(_graph((AuthorityScope("tenant-a", "client.read"),)), "subject:alice")
    exact_diff = diff_least_authority(required=(AuthorityScope("tenant-a", "client.read"),), effective=exact)

    assert exact_diff.passed is True
    assert exact_diff.missing == ()
    assert exact_diff.excess == ()

    wrong_tenant = compute_authority_closure(_graph((AuthorityScope("tenant-b", "client.read"),)), "subject:alice")
    tenant_diff = diff_least_authority(required=(AuthorityScope("tenant-a", "client.read"),), effective=wrong_tenant)

    assert tuple(scope.tenant_id for scope in tenant_diff.missing) == ("tenant-a",)
    assert tuple(scope.tenant_id for scope in tenant_diff.excess) == ("tenant-b",)


def test_authority_closure_monotonicity_t2_multi_source_excess_provenance_is_preserved() -> None:
    graph = AuthorityDerivationGraph(
        nodes=(AuthorityNode("subject:alice", "subject"), AuthorityNode("authority:client", "authority")),
        edges=(
            AuthorityEdge("edge:role", "subject:alice", "authority:client", "role", (AuthorityScope("tenant-a", "client.*"),)),
            AuthorityEdge("edge:delegation", "subject:alice", "authority:client", "delegation", (AuthorityScope("tenant-a", "client.*"),)),
        ),
    )

    diff = diff_least_authority(
        required=(AuthorityScope("tenant-a", "client.read"),),
        effective=compute_authority_closure(graph, "subject:alice"),
    )

    assert diff.passed is False
    assert diff.excess_provenance[("tenant-a", "", "client.*", "*")] == ("edge:delegation", "edge:role")


def test_authority_closure_monotonicity_t2_deny_precedence_is_not_active_until_deny_semantics_exist() -> None:
    # T2 intentionally records that deny precedence must be tested when deny edges
    # become a runtime authority semantic instead of a future design option.
    assert AuthorityClosure(subject="subject:alice", scopes=()).scopes == ()

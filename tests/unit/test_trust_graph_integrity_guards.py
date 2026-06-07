from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_identity_policy import ReferenceCatalog, TrustEdge, validate_trust_graph_integrity


def test_trust_graph_integrity_t1_accepts_valid_edges() -> None:
    catalog = ReferenceCatalog(
        subjects=("issuer:a", "subject:b"),
        tenants=("tenant-a",),
        trust_domains=("domain-a",),
    )

    report = validate_trust_graph_integrity(
        catalog=catalog,
        edges=(TrustEdge("trust:1", "issuer:a", "subject:b", "tenant-a", "domain-a"),),
    )

    assert report.passed is True
    assert report.checked_count == 1


def test_trust_graph_integrity_t1_rejects_revoked_unknown_and_cycles() -> None:
    catalog = ReferenceCatalog(
        subjects=("issuer:a", "subject:b"),
        tenants=("tenant-a",),
        trust_domains=("domain-a",),
    )

    report = validate_trust_graph_integrity(
        catalog=catalog,
        edges=(
            TrustEdge("trust:1", "issuer:a", "subject:b", "tenant-a", "domain-a", revoked=True),
            TrustEdge("trust:2", "subject:b", "issuer:a", "tenant-a", "domain-a"),
            TrustEdge("trust:3", "issuer:a", "subject:c", "tenant-b", "domain-z"),
        ),
    )

    assert report.passed is False
    assert "trust edge 'trust:1' is revoked and cannot be active" in report.failures
    assert "trust graph cycle detected at 'issuer:a'" in report.failures
    assert "trust edge 'trust:3' has unknown tenant 'tenant-b'" in report.failures

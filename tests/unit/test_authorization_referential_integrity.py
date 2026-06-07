from __future__ import annotations

import tests.unit.formal_auth_helpers  # noqa: F401

from tigrbl_identity_policy import (
    AuthorizationReference,
    ReferenceCatalog,
    validate_authorization_referential_integrity,
)


def test_authorization_referential_integrity_t1_detects_orphans() -> None:
    catalog = ReferenceCatalog(
        subjects=("subject:alice",),
        tenants=("tenant-a",),
        policies=("policy:client-read",),
    )

    report = validate_authorization_referential_integrity(
        catalog=catalog,
        references=(
            AuthorizationReference("ref:subject", "subject", "subject:alice"),
            AuthorizationReference("ref:tenant", "tenant", "tenant-b", source_id="policy:client-read"),
        ),
    )

    assert report.passed is False
    assert report.checked_count == 2
    assert report.failures == ("ref:tenant references unknown tenant 'tenant-b'",)

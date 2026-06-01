import pytest

from tigrbl_auth.security.certification import (
    CertificationError,
    KeyBoundary,
    assert_crypto_boundaries,
)


def test_crypto_boundary_t0_contract_exports_boundary_check() -> None:
    assert callable(assert_crypto_boundaries)


def test_crypto_boundary_t1_accepts_realm_and_tenant_scoped_keys() -> None:
    assert_crypto_boundaries(
        (
            KeyBoundary("realm-key", "realm", "realm-a", "RS256", 1, frozenset({"realm-a"})),
            KeyBoundary("tenant-key", "tenant", "tenant-a", "RS256", 1),
        )
    )


def test_crypto_boundary_t2_rejects_duplicate_or_leaking_tenant_keys() -> None:
    with pytest.raises(CertificationError, match="duplicate"):
        assert_crypto_boundaries(
            (
                KeyBoundary("same", "realm", "realm-a", "RS256", 1),
                KeyBoundary("same", "realm", "realm-b", "RS256", 1),
            )
        )

    with pytest.raises(CertificationError, match="outside"):
        assert_crypto_boundaries(
            (KeyBoundary("tenant-key", "tenant", "tenant-a", "RS256", 1, frozenset({"tenant-b"})),)
        )

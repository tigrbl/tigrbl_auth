import pytest

from tigrbl_auth.security.certification import (
    CertificationError,
    RuntimeQualification,
    assert_runtime_qualified,
    stable_sha256,
)


def _qualification(surface: str = "public-app") -> RuntimeQualification:
    return RuntimeQualification(
        artifact_sha256=stable_sha256("artifact"),
        dependency_lock_sha256=stable_sha256("lock"),
        config_sha256=stable_sha256({"issuer": "https://auth.example.test"}),
        product_surface=surface,
        capabilities=frozenset({"openid-configuration", "jwks"}),
    )


def test_runtime_qualification_t0_contract_exports_snapshot_check() -> None:
    assert callable(assert_runtime_qualified)


def test_runtime_qualification_t1_accepts_exact_deployment_truth_match() -> None:
    snapshot = _qualification()
    assert_runtime_qualified(snapshot, snapshot)


def test_runtime_qualification_t2_rejects_drifted_runtime() -> None:
    with pytest.raises(CertificationError, match="deployment truth"):
        assert_runtime_qualified(_qualification(), _qualification("platform-admin-app"))

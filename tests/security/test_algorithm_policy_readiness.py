from __future__ import annotations

from tigrbl_auth.security.certification import (
    AlgorithmPolicy,
    algorithm_policy_report,
    assert_algorithm_policy,
)


def test_algorithm_policy_t0_exports_pqc_readiness_surface() -> None:
    assert callable(algorithm_policy_report)
    assert callable(assert_algorithm_policy)
    assert isinstance(AlgorithmPolicy.certification_default(), AlgorithmPolicy)


def test_algorithm_policy_t1_reports_ecdsa_warning_and_rsa_refusal() -> None:
    report = algorithm_policy_report(("EdDSA", "ES256", "RS256"))

    assert report["allowed"] == ["EdDSA", "ES256"]
    assert report["refused"] == ["RS256"]
    assert report["pqc"]["ready"] is True
    assert report["warnings"] == ["ES256 is classical ECDSA and not post-quantum resistant"]

from __future__ import annotations

import pytest

from tigrbl_auth.security.certification import (
    AlgorithmPolicy,
    CertificationError,
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


def test_algorithm_policy_t2_refuses_rsa_and_enforces_pqc_required_mode() -> None:
    assert_algorithm_policy("EdDSA")
    assert_algorithm_policy("ES256")

    with pytest.raises(CertificationError, match="RSA signature algorithms are disallowed"):
        assert_algorithm_policy("RS256")

    with pytest.raises(CertificationError, match="post-quantum signature algorithm required"):
        assert_algorithm_policy("EdDSA", AlgorithmPolicy(pqc_required=True))

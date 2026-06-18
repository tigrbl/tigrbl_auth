from __future__ import annotations

import pytest

from tigrbl_auth.security.certification import (
    AlgorithmPolicy,
    CertificationError,
    ML_DSA_65_ALG,
    PQC_JWK_KTY,
    algorithm_policy_report,
    assert_algorithm_policy,
    validate_jwk_set,
)


def test_algorithm_policy_t0_exports_pqc_readiness_surface() -> None:
    assert callable(algorithm_policy_report)
    assert callable(assert_algorithm_policy)
    assert isinstance(AlgorithmPolicy.certification_default(), AlgorithmPolicy)


def test_algorithm_policy_t1_reports_ecdsa_warning_and_rsa_refusal() -> None:
    report = algorithm_policy_report(("EdDSA", "ES256", ML_DSA_65_ALG, "RS256"))

    assert report["allowed"] == ["EdDSA", "ES256", ML_DSA_65_ALG]
    assert report["refused"] == ["RS256"]
    assert report["pqc"]["ready"] is True
    assert report["pqc"]["policy_registered_algs"] == [ML_DSA_65_ALG]
    assert "backend" not in report["pqc"]
    assert report["warnings"] == ["ES256 is classical ECDSA and not post-quantum resistant"]


def test_algorithm_policy_t2_refuses_rsa_and_enforces_pqc_required_mode() -> None:
    assert_algorithm_policy("EdDSA")
    assert_algorithm_policy("ES256")

    with pytest.raises(CertificationError, match="RSA signature algorithms are disallowed"):
        assert_algorithm_policy("RS256")

    with pytest.raises(CertificationError, match="post-quantum signature algorithm required"):
        assert_algorithm_policy("EdDSA", AlgorithmPolicy(pqc_required=True))

    assert_algorithm_policy(ML_DSA_65_ALG, AlgorithmPolicy(pqc_required=True))


def test_pqc_jwk_validation_accepts_ml_dsa_public_key_shape() -> None:
    jwk = {
        "kty": PQC_JWK_KTY,
        "crv": ML_DSA_65_ALG,
        "alg": ML_DSA_65_ALG,
        "kid": "pqc-test-key",
        "x": "cHVibGljLWtleS1ieXRlcw",
    }

    validate_jwk_set({"keys": [jwk]})

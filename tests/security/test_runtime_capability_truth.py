import pytest

from tigrbl_auth.security.certification import (
    CapabilityRecord,
    CertificationError,
    runtime_capability_truth,
)


def test_runtime_capability_truth_t0_contract_exports_runtime_check() -> None:
    assert callable(runtime_capability_truth)


def test_runtime_capability_truth_t1_accepts_evidence_backed_advertising() -> None:
    truth = runtime_capability_truth(
        (
            CapabilityRecord("jwks", True, "evd:jwks"),
            CapabilityRecord("admin", False),
        ),
        advertised={"jwks"},
    )

    assert truth == {"jwks": True, "admin": False}


def test_runtime_capability_truth_t2_rejects_disabled_or_unknown_advertising() -> None:
    configured = (CapabilityRecord("jwks", False, "evd:jwks"),)

    with pytest.raises(CertificationError, match="disabled capability"):
        runtime_capability_truth(configured, advertised={"jwks"})

    with pytest.raises(CertificationError, match="unknown"):
        runtime_capability_truth(configured, advertised={"token"})

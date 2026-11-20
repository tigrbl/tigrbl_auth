import pytest
from tba_contracts_identity.workloads import WorkloadSelector
from tba_concrete_svid import (
    X509SvidStructure,
    normalize_selectors,
    normalize_spiffe_id,
    parse_jwt_svid_claims,
    validate_x509_svid_structure,
)


def test_spiffe_id_is_identity_while_jwt_svid_is_credential_claim_structure():
    identity = normalize_spiffe_id("spiffe://example.org/workload/api")
    credential = parse_jwt_svid_claims(
        {"sub": str(identity), "aud": ["service-a"], "exp": 100}
    )
    assert credential.subject == str(identity)
    assert credential.audience == ("service-a",)


def test_x509_svid_structure_requires_one_spiffe_uri_san_and_leaf_usage():
    identity = validate_x509_svid_structure(
        X509SvidStructure(("spiffe://example.org/workload/api",))
    )
    assert identity.trust_domain.name == "example.org"
    with pytest.raises(ValueError, match="exactly one"):
        validate_x509_svid_structure(X509SvidStructure(()))


def test_workload_selectors_normalize_deterministically():
    selectors = normalize_selectors(
        (
            WorkloadSelector("unix", "uid:1000"),
            WorkloadSelector("k8s", "ns:default"),
            WorkloadSelector("unix", "uid:1000"),
        )
    )
    assert len(selectors) == 2 and selectors[0].selector_type == "k8s"

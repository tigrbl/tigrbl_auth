import pytest
from tigrbl_did_concrete import (
    parse_did_document,
    parse_did_url,
    select_document_resource,
    validate_did_document,
)
from tigrbl_identity_contracts.workloads import WorkloadSelector
from tigrbl_svid_concrete import (
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


def test_did_document_parsing_validation_and_dereferencing():
    document = parse_did_document(
        {
            "id": "did:example:123",
            "verificationMethod": [
                {
                    "id": "did:example:123#key-1",
                    "type": "JsonWebKey2020",
                    "controller": "did:example:123",
                    "publicKeyJwk": {"kty": "OKP", "crv": "Ed25519", "x": "abc"},
                }
            ],
            "authentication": ["did:example:123#key-1"],
            "service": [
                {
                    "id": "#messages",
                    "type": "Messaging",
                    "serviceEndpoint": "https://example.org/messages",
                }
            ],
        }
    )
    validate_did_document(document)
    method = select_document_resource(document, parse_did_url("did:example:123#key-1"))
    service = select_document_resource(
        document, parse_did_url("did:example:123#messages")
    )
    assert method.method_type == "JsonWebKey2020"
    assert service.service_types == ("Messaging",)


def test_did_document_rejects_unknown_relationship_reference():
    document = parse_did_document(
        {"id": "did:example:123", "authentication": ["did:example:123#missing"]}
    )
    with pytest.raises(ValueError, match="unknown"):
        validate_did_document(document)

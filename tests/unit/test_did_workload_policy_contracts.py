import pytest

from tigrbl_authz_policy_bases import (
    AuthzenEvaluationAdapterBase,
    XacmlRequestMapperBase,
)
from tigrbl_identity_contracts.delegation import (
    DelegatedCapability,
    DelegationActor,
    DelegationActorChain,
    DelegationConstraint,
    DelegationConstraints,
)
from tigrbl_identity_contracts.did import (
    Did,
    DidDocument,
    DidService,
    DidUrl,
    DidVerificationMethod,
)
from tigrbl_identity_contracts.policy import (
    PolicyEntity,
    PolicyEntityChain,
    PolicyEvaluationRequest,
    XacmlDecision,
)
from tigrbl_identity_contracts.workloads import SpiffeId, Svid, SvidFormat, TrustDomain
from tigrbl_security_trust_domain_bases import (
    CertificatePathValidatorBase,
    DidResolverBase,
    SvidProviderBase,
    SvidVerifierBase,
    TrustBundleProviderBase,
)


def test_did_document_keeps_identifier_method_and_key_material_separate():
    did = Did.parse("did:example:123")
    method = DidVerificationMethod(
        "did:example:123#key-1", did, "JsonWebKey2020", {"kty": "OKP"}
    )
    document = DidDocument(
        did,
        (method,),
        services=(DidService("#inbox", ("Messaging",), "https://example"),),
    )
    assert str(document.identifier) == "did:example:123"
    assert DidUrl(did, fragment="key-1").fragment == "key-1"


def test_spiffe_id_and_svid_model_identity_and_credential_separately():
    spiffe_id = SpiffeId.parse("spiffe://example.org/service/api")
    svid = Svid(spiffe_id, SvidFormat.JWT, "encoded-jwt")
    assert spiffe_id.trust_domain == TrustDomain("example.org")
    assert svid.spiffe_id is spiffe_id and svid.credential == "encoded-jwt"
    with pytest.raises(ValueError):
        SpiffeId.parse("https://example.org/service/api")


def test_policy_interop_contracts_are_representation_neutral():
    subject = PolicyEntityChain((PolicyEntity("subject", "alice"),))
    action = PolicyEntityChain((PolicyEntity("action", "read"),))
    resource = PolicyEntityChain((PolicyEntity("resource", "document:1"),))
    request = PolicyEvaluationRequest(subject, action, resource)
    assert request.subject.entities[0].identifier == "alice"
    assert XacmlDecision.PERMIT == "Permit"


def test_delegation_actor_chain_capability_and_constraints_are_distinct():
    chain = DelegationActorChain((DelegationActor("alice"), DelegationActor("service")))
    capability = DelegatedCapability("read", "document:1")
    constraints = DelegationConstraints(
        (DelegationConstraint("region", "us"),), max_depth=2
    )
    assert len(chain.actors) == constraints.max_depth
    assert capability.action == "read"


def test_layer_five_exposes_did_svid_policy_and_certificate_extension_points():
    bases = (
        DidResolverBase,
        SvidProviderBase,
        SvidVerifierBase,
        TrustBundleProviderBase,
        CertificatePathValidatorBase,
        AuthzenEvaluationAdapterBase,
        XacmlRequestMapperBase,
    )
    assert all(isinstance(base, type) for base in bases)

import pytest
from tba_contracts_identity.workloads import (
    SpiffeId,
    SpiffeTrustBundle,
    Svid,
    SvidFormat,
    TrustDomain,
    WorkloadSelector,
)
from tba_protocol_workload_spiffe_svid import verify_jwt_svid, verify_x509_svid
from tba_provider_spiffe_bundle import VersionedSpiffeBundleProvider
from tba_provider_spiffe_workload_api import LocalSpiffeWorkloadApiProvider
from tba_testkit_workload_credential_conformance.fixtures import (
    PathValidator,
    _certificate,
    _jwk,
    _jwt,
)


def _identity():
    return SpiffeId.parse("spiffe://example.org/workload/api")


def _bundle_provider():
    provider = VersionedSpiffeBundleProvider()
    provider.publish(
        SpiffeTrustBundle(
            TrustDomain("example.org"),
            "0001",
            x509_authorities=(b"root",),
            jwt_authorities=({"kty": "OKP"},),
        )
    )
    return provider


def test_workload_api_selects_x509_or_jwt_svid_by_use():
    selectors = (WorkloadSelector("unix", "uid:1000"),)
    provider = LocalSpiffeWorkloadApiProvider(lambda: selectors)
    provider.register(selectors, Svid(_identity(), SvidFormat.X509, b"certificate"))
    provider.register(selectors, Svid(_identity(), SvidFormat.JWT, "a.b.c"))
    assert provider.fetch_svid().format is SvidFormat.X509
    assert provider.fetch_svid("service-a").format is SvidFormat.JWT


def test_bundle_versions_must_advance_and_contain_authorities():
    provider = _bundle_provider()
    with pytest.raises(ValueError, match="advance"):
        provider.publish(
            SpiffeTrustBundle(TrustDomain("example.org"), "0001", (b"root",))
        )
    assert provider.bundle_for(TrustDomain("example.org")).version == "0001"


def test_jwt_svid_verification_requires_profile_specific_token_verifier_and_audience():
    from cryptography.hazmat.primitives.asymmetric import ec

    key = ec.generate_private_key(ec.SECP256R1())
    token = _jwt(
        key, {"sub": str(_identity()), "aud": ["service-a"], "exp": 100}, kid="key"
    )
    anchors = {"example.org": [_jwk(key, kid="key", use="jwt-svid")]}
    with pytest.raises(ValueError, match="audience"):
        verify_jwt_svid(
            token, expected_audience="service-b", keys_by_domain=anchors, now=50
        )
    assert verify_jwt_svid(
        token, expected_audience="service-a", keys_by_domain=anchors, now=50
    ) == str(_identity())


def test_x509_svid_verification_requires_path_validation_and_identity_match():
    from cryptography.hazmat.primitives import serialization

    root = _certificate(())
    leaf, _ = _certificate((str(_identity()),), issuer=root)
    chain = (leaf.public_bytes(serialization.Encoding.DER),)
    anchors = {"example.org": PathValidator(root[0])}
    assert verify_x509_svid(chain, validators_by_domain=anchors) == str(_identity())
    with pytest.raises(ValueError, match="identity"):
        verify_x509_svid(
            chain,
            validators_by_domain=anchors,
            expected_identity="spiffe://example.org/workload/other",
        )

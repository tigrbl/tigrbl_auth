import pytest
from tigrbl_identity_contracts.workloads import (
    SpiffeId,
    SpiffeTrustBundle,
    Svid,
    SvidFormat,
    TrustDomain,
    WorkloadSelector,
)
from tigrbl_spiffe_bundle_provider import VersionedSpiffeBundleProvider
from tigrbl_spiffe_workload_api_provider import LocalSpiffeWorkloadApiProvider
from tigrbl_svid_concrete import X509SvidStructure
from tigrbl_svid_verifier_provider import ProfiledSvidVerifier


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
    svid = Svid(_identity(), SvidFormat.JWT, "a.b.c")
    with pytest.raises(ValueError, match="not configured"):
        ProfiledSvidVerifier(_bundle_provider()).verify_svid(svid, "service-a")
    verifier = ProfiledSvidVerifier(
        _bundle_provider(),
        jwt_verifier=lambda token, audience, bundle: {
            "sub": str(_identity()),
            "aud": [audience],
            "exp": 100,
        },
    )
    assert verifier.verify_svid(svid, "service-a") == _identity()


def test_x509_svid_verification_requires_path_validation_and_identity_match():
    svid = Svid(_identity(), SvidFormat.X509, b"certificate")
    verifier = ProfiledSvidVerifier(
        _bundle_provider(),
        x509_verifier=lambda certificate, bundle: X509SvidStructure(
            (str(_identity()),)
        ),
    )
    assert verifier.verify_svid(svid) == _identity()
    mismatch = ProfiledSvidVerifier(
        _bundle_provider(),
        x509_verifier=lambda certificate, bundle: X509SvidStructure(
            ("spiffe://example.org/workload/other",)
        ),
    )
    with pytest.raises(ValueError, match="does not match"):
        mismatch.verify_svid(svid)

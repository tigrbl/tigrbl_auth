import json
import sys
from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from tba_testkit_workload_credential_conformance.profiles import (
    exercise_spiffe,
    exercise_wic,
    exercise_wimse,
)
from tba_testkit_workload_credential_conformance.wheels import run_installed

ROOT = Path(__file__).resolve().parents[4]
WIMSE = (
    "tba-profile-workload-credential-wimse-wit",
    "tba-profile-workload-proof-wimse-wpt",
)
SPIFFE = ("tba-protocol-workload-spiffe-svid",)
SPIFFE_PROVIDERS = ("tba-provider-spiffe-bundle", "tba-provider-spiffe-workload-api")
SPIFFE_REVISION = "5d15e3ee8782e205048d1f206fbf944e075f7bae"


def exercise_x509_carrier():
    from datetime import datetime, timedelta, timezone

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID
    from tba_concrete_certificate_x509 import parse_x509_certificate
    from tba_concrete_x509_svid_credential import X509SvidCredential

    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Fixture")])
    now = datetime.now(timezone.utc)
    identity = "spiffe://example.org/workload"
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(1)
        .not_valid_before(now)
        .not_valid_after(now + timedelta(minutes=1))
        .add_extension(
            x509.SubjectAlternativeName([x509.UniformResourceIdentifier(identity)]),
            False,
        )
        .sign(key, hashes.SHA256())
    )
    der = cert.public_bytes(serialization.Encoding.DER)
    credential = X509SvidCredential(identity, (der,))
    assert credential.certificate == parse_x509_certificate(der)


def exercise_spiffe_providers():
    from tba_contracts_workload_identity import (
        SpiffeId,
        SpiffeTrustBundle,
        Svid,
        SvidFormat,
        TrustDomain,
        WorkloadSelector,
    )
    from tba_protocol_workload_spiffe_svid import validate_jwt_svid
    from tba_provider_spiffe_bundle import VersionedSpiffeBundleProvider
    from tba_provider_spiffe_workload_api import LocalSpiffeWorkloadApiProvider

    domain = TrustDomain("example.org")
    identity = SpiffeId.parse("spiffe://example.org/workload")
    selectors = (WorkloadSelector("unix", "uid:1000"),)
    provider = LocalSpiffeWorkloadApiProvider(lambda: selectors)
    provider.register(selectors, Svid(identity, SvidFormat.JWT, "example-token"))
    bundle_provider = VersionedSpiffeBundleProvider()
    bundle_provider.publish(
        SpiffeTrustBundle(domain, "1", jwt_authorities=({"kty": "EC"},))
    )

    credential = provider.fetch_svid("service")
    assert credential.spiffe_id == identity
    assert bundle_provider.bundle_for(domain).trust_domain == domain
    try:
        bundle_provider.bundle_for(TrustDomain("other.example"))
    except LookupError:
        pass
    else:
        raise AssertionError(
            "Bundle provider returned trust for an unconfigured domain"
        )
    try:
        validate_jwt_svid(
            {"alg": "ES256"},
            {"sub": str(identity), "aud": ["service"], "exp": 2, "iat": 1},
            expected_audience="other-service",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Provider selection changed JWT-SVID audience rules")


def test_t0_specification_ownership(record_property):
    from tba_profile_workload_credential_wimse_wit import CURRENT_VERSION as wit
    from tba_profile_workload_proof_wimse_wpt import CURRENT_VERSION as wpt
    from tba_protocol_workload_spiffe_svid import CURRENT_VERSION as svid

    assert (wit.identifier, wit.specification_uri) == (
        "draft-ietf-wimse-workload-creds-03",
        "https://datatracker.ietf.org/doc/html/draft-ietf-wimse-workload-creds-03",
    )
    assert (wpt.identifier, wpt.specification_uri) == (
        "draft-ietf-wimse-wpt-02",
        "https://datatracker.ietf.org/doc/html/draft-ietf-wimse-wpt-02",
    )
    assert svid.specification_uris == tuple(
        f"https://github.com/spiffe/spiffe/blob/{SPIFFE_REVISION}/standards/{name}.md"
        for name in ("SPIFFE-ID", "X509-SVID", "JWT-SVID")
    )
    record_property(
        "requirement_test_mapping",
        json.dumps(
            {
                "WIT confirmation and audience": [
                    WIMSE[0],
                    wit.identifier,
                    "exercise_wimse",
                ],
                "WPT WIT binding": [WIMSE[1], wpt.identifier, "exercise_wimse"],
                "SPIFFE ID and SVID profile checks": [
                    SPIFFE[0],
                    SPIFFE_REVISION,
                    "exercise_spiffe",
                ],
            },
            sort_keys=True,
        ),
    )
    for package in (*WIMSE, *SPIFFE):
        (manifest,) = ROOT.glob(f"pkgs/*/{package}/pyproject.toml")
        assert (
            tomllib.loads(manifest.read_text(encoding="utf-8"))["project"]["name"]
            == package
        )


@pytest.mark.parametrize("exercise", [exercise_wimse, exercise_spiffe])
def test_t1_specification_ownership(exercise):
    exercise()


@pytest.mark.parametrize(
    ("exercise", "excluded"),
    [
        (exercise_wimse, ("spiffe", "spire")),
        (exercise_spiffe, ("wimse", "spire")),
    ],
)
def test_t1_package_independence(exercise, excluded):
    import importlib
    import importlib.abc

    class ProtocolBoundary(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if set(fullname.split(".")[0].split("_")).intersection(excluded):
                raise ImportError(f"Forbidden protocol import: {fullname}")
            return None

    with pytest.MonkeyPatch.context() as patch:
        for name in tuple(sys.modules):
            if name.startswith(("tba_", "tigrbl_")):
                patch.delitem(sys.modules, name)
        patch.setattr(sys, "meta_path", [ProtocolBoundary(), *sys.meta_path])
        importlib.invalidate_caches()
        exercise()


@pytest.mark.parametrize(
    ("roots", "exercise", "excluded"),
    [
        (WIMSE, exercise_wimse, ("spiffe", "spire")),
        (
            ("tba-profile-workload-authentication-wimse-mtls",),
            exercise_wic,
            ("spiffe", "spire"),
        ),
        (SPIFFE, exercise_spiffe, ("wimse", "spire")),
    ],
    ids=["wimse", "wic", "spiffe"],
)
def test_t2_package_independence(
    wheelhouse, tmp_path, record_property, roots, exercise, excluded
):
    inventory = run_installed(wheelhouse, tmp_path, roots, (exercise,), excluded)
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))
    record_property("entry_point_check", exercise.__name__)


def test_t2_specification_ownership(wheelhouse, tmp_path, record_property):
    inventory = run_installed(
        wheelhouse,
        tmp_path,
        (*SPIFFE, *SPIFFE_PROVIDERS),
        (exercise_spiffe, exercise_spiffe_providers),
        ("wimse", "spire"),
    )
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))
    record_property("spiffe_specification_revision", SPIFFE_REVISION)
    record_property("entry_point_check", "exercise_spiffe + exercise_spiffe_providers")


def test_t2_shared_x509_consumers(wheelhouse, tmp_path, record_property):
    for label, packages, exercise, excluded in (
        ("spiffe", SPIFFE, exercise_x509_carrier, ("wimse", "spire")),
        (
            "wic",
            ("tba-profile-workload-credential-wimse-wic",),
            exercise_wic,
            ("spiffe", "spire"),
        ),
    ):
        directory = tmp_path / label
        directory.mkdir()
        inventory = run_installed(
            wheelhouse, directory, packages, (exercise,), excluded
        )
        record_property(
            label + "_wheel_inventory", json.dumps(inventory, sort_keys=True)
        )


def test_expanded_protocol_specification_ownership():
    from tba_profile_workload_authentication_wimse_mtls import (
        SPECIFICATION_VERSION as mtls_revision,
    )
    from tba_profile_workload_authentication_wimse_mtls import (
        verify_wimse_peer,
    )
    from tba_profile_workload_credential_spiffe_wit_svid import (
        CURRENT_VERSION as wit_svid_revision,
    )
    from tba_profile_workload_credential_spiffe_wit_svid import (
        verify_wit_svid,
    )
    from tba_profile_workload_credential_wimse_wic import (
        SPECIFICATION_VERSION as wic_revision,
    )
    from tba_profile_workload_credential_wimse_wic import (
        validate_wic,
    )
    from tba_profile_workload_credential_wimse_wit import (
        CURRENT_VERSION as wit_revision,
    )
    from tba_profile_workload_credential_wimse_wit import (
        verify_wit,
    )
    from tba_profile_workload_proof_wimse_wpt import (
        CURRENT_VERSION as wpt_revision,
    )
    from tba_profile_workload_proof_wimse_wpt import (
        authenticate_wpt_request,
    )
    from tba_protocol_workload_spiffe_svid import verify_jwt_svid, verify_x509_svid
    from tba_protocol_workload_wimse_identifier import (
        SPECIFICATION_VERSION,
        WorkloadIdentifier,
    )

    targets = (
        (1231, SPIFFE_REVISION, verify_x509_svid),
        (1231, SPIFFE_REVISION, verify_jwt_svid),
        (1232, SPIFFE_REVISION, verify_wit_svid),
        (1233, SPECIFICATION_VERSION, WorkloadIdentifier),
        (1234, wic_revision, validate_wic),
        (1235, mtls_revision, verify_wimse_peer),
        (1236, wit_revision.identifier, verify_wit),
        (1236, wpt_revision.identifier, authenticate_wpt_request),
    )
    assert SPIFFE_REVISION in wit_svid_revision.specification_uri
    for number, revision, entry_point in targets:
        (document,) = ROOT.glob(f".ssot/specs/SPEC-{number}-*.yaml")
        assert revision in document.read_text(encoding="utf-8")
        owner = entry_point.__module__.split(".", 1)[0].replace("_", "-")
        (manifest,) = ROOT.glob(f"pkgs/*/{owner}/pyproject.toml")
        assert (
            tomllib.loads(manifest.read_text(encoding="utf-8"))["project"]["name"]
            == owner
        )

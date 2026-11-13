"""Acceptance tests for the workload protocol capabilities scoped by SPEC-1230."""

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]
WIMSE = (
    "tba-profile-workload-credential-wimse-wit",
    "tba-profile-workload-proof-wimse-wpt",
)
SPIFFE = ("tba-protocol-workload-spiffe-svid",)
SPIFFE_PROVIDERS = ("tba-provider-spiffe-bundle", "tba-provider-spiffe-workload-api")
SPIFFE_REVISION = "5d15e3ee8782e205048d1f206fbf944e075f7bae"


def exercise_wimse():
    from tba_profile_workload_credential_wimse_wit import validate_wit
    from tba_profile_workload_proof_wimse_wpt import validate_wpt

    wit_header = {"typ": "wit+jwt", "alg": "ES256"}
    wit = {
        "iss": "https://example.org/issuer",
        "sub": "wimse://example.org/workload",
        "cnf": {"jkt": "test-key-thumbprint"},
        "exp": 2,
        "iat": 1,
    }
    validate_wit(wit_header, wit)
    try:
        validate_wit(wit_header, {**wit, "aud": "service"})
    except ValueError as error:
        assert "aud" in str(error)
    else:
        raise AssertionError("WIT profile accepted an audience")

    wpt_header = {"typ": "wpt+jwt", "alg": "ES256"}
    wpt = {"aud": "service", "exp": 2, "jti": "proof", "wth": "expected-hash"}
    validate_wpt(
        wpt_header, wpt, expected_audience="service", expected_wit_hash="expected-hash"
    )
    try:
        validate_wpt(
            wpt_header, wpt, expected_audience="service", expected_wit_hash="wrong-hash"
        )
    except ValueError as error:
        assert "bind" in str(error)
    else:
        raise AssertionError("WPT profile accepted a mismatched WIT hash")


def exercise_wic():
    from datetime import datetime, timedelta, timezone
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID
    from tba_concrete_certificate_x509 import parse_x509_certificate
    from tba_profile_workload_credential_wimse_wic import validate_wic

    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Fixture")])
    now = datetime.now(timezone.utc)
    identity = "wimse://example.org/workload"
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
    parsed = parse_x509_certificate(cert.public_bytes(serialization.Encoding.DER))
    assert validate_wic(parsed).workload_identifier == identity


def exercise_spiffe():
    from tba_protocol_workload_spiffe_svid import (
        validate_jwt_svid,
        validate_spiffe_id,
        validate_x509_svid,
    )

    subject = "spiffe://example.org/workload"
    assert validate_spiffe_id(subject) == ("example.org", "/workload")
    header = {"alg": "ES256"}
    jwt_svid = {"sub": subject, "aud": ["service"], "exp": 2, "iat": 1}
    validate_jwt_svid(header, jwt_svid, expected_audience="service")
    try:
        validate_jwt_svid(header, jwt_svid, expected_audience="other-service")
    except ValueError as error:
        assert "audience" in str(error)
    else:
        raise AssertionError("JWT-SVID profile accepted a different audience")

    options = {
        "dns_sans": (),
        "key_usage_digital_signature": True,
        "basic_constraints_ca": False,
    }
    assert validate_x509_svid(uri_sans=(subject,), **options) == subject
    try:
        validate_x509_svid(uri_sans=("wimse://example.org/workload",), **options)
    except ValueError:
        pass
    else:
        raise AssertionError("X.509-SVID profile accepted a WIMSE identifier")


def exercise_shared_svid():
    from tba_concrete_jwt import decode_jwt_unverified
    from tba_concrete_jwt_svid_credential import JwtSvidCredential
    from tba_concrete_svid import SvidIdentity
    from tba_concrete_x509_svid_credential import X509SvidCredential
    from tba_primitives_identity import base64url_encode

    subject = "spiffe://example.org/workload"
    jwt = decode_jwt_unverified(
        ".".join(
            base64url_encode(value)
            for value in (
                b'{"alg":"ES256"}',
                json.dumps({"sub": subject}).encode(),
                b"fixture",
            )
        )
    )
    assert isinstance(
        JwtSvidCredential(jwt, subject, ("service",)).identity, SvidIdentity
    )
    assert isinstance(X509SvidCredential(subject, (b"fixture",)).identity, SvidIdentity)


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


def exercise_optional_wit_svid():
    from tba_concrete_jwt import decode_jwt_unverified
    from tba_concrete_svid import SvidIdentity
    from tba_concrete_wit import WorkloadIdentityToken
    from tba_concrete_wit_svid_credential import WitSvidCredential
    from tba_primitives_identity import base64url_encode

    subject = "spiffe://example.org/workload"
    claims = {"sub": subject, "cnf": {"jwk": {}}, "exp": 100}
    jwt = decode_jwt_unverified(
        ".".join(
            base64url_encode(value)
            for value in (
                b'{"alg":"ES256"}',
                json.dumps(claims).encode(),
                b"fixture",
            )
        )
    )
    assert isinstance(
        WitSvidCredential(WorkloadIdentityToken(jwt), subject).identity, SvidIdentity
    )


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


def run_command(*args, cwd, env=None):
    result = subprocess.run(
        args, cwd=cwd, env=env, capture_output=True, text=True, timeout=180
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


@pytest.fixture(scope="module")
def wheelhouse(tmp_path_factory):
    directory = tmp_path_factory.mktemp("workload_wheels")
    manifests = {}
    for manifest in ROOT.glob("pkgs/*/*/pyproject.toml"):
        project = tomllib.loads(manifest.read_text(encoding="utf-8")).get("project")
        if project:
            manifests[canonicalize_name(project["name"])] = (manifest.parent, project)
    return directory, manifests


def run_installed(wheelhouse, directory, roots, exercises, excluded):
    import inspect

    wheels, manifests = wheelhouse
    pending = list(roots)
    built = set()
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.setdefault("UV_CACHE_DIR", str(wheels / "uv-cache"))
    env.setdefault("UV_LINK_MODE", "copy")
    while pending:
        name = pending.pop()
        if name in built or name not in manifests:
            continue
        source, project = manifests[name]
        if not list(wheels.glob(f"{name.replace('-', '_')}-*.whl")):
            if env.get("TBA_TEST_POETRY_CORE_PATH"):
                build_env = {**env, "PYTHONPATH": env["TBA_TEST_POETRY_CORE_PATH"]}
                run_command(
                    sys.executable,
                    "-c",
                    "from poetry.core.masonry.api import build_wheel; import sys; build_wheel(sys.argv[1])",
                    str(wheels),
                    cwd=source,
                    env=build_env,
                )
            else:
                run_command(
                    "uv",
                    "build",
                    "--wheel",
                    "--out-dir",
                    str(wheels),
                    str(source),
                    cwd=directory,
                    env=env,
                )
        built.add(name)
        pending.extend(
            canonicalize_name(Requirement(dep).name)
            for dep in project.get("dependencies", [])
        )

    venv = directory / "venv"
    run_command(
        "uv", "venv", "--python", sys.executable, str(venv), cwd=directory, env=env
    )
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    wheel_source = env.get("TBA_TEST_EXTERNAL_WHEELS")
    dependency_links = ("--find-links", wheel_source) if wheel_source else ()
    run_command(
        "uv",
        "pip",
        "install",
        "--python",
        str(python),
        "--find-links",
        str(wheels),
        *dependency_links,
        *(f"{name}=={manifests[name][1]['version']}" for name in roots),
        cwd=directory,
        env=env,
    )
    run_command("uv", "pip", "check", "--python", str(python), cwd=directory, env=env)
    script = directory / "verify.py"
    script.write_text(
        "from importlib.metadata import distributions\nimport json\n"
        + "\n".join(
            textwrap.dedent(inspect.getsource(exercise)) for exercise in exercises
        )
        + "\n".join(f"{exercise.__name__}()" for exercise in exercises)
        + "\nprint(json.dumps({d.metadata['Name']: d.version for d in distributions()}, sort_keys=True))\n",
        encoding="utf-8",
    )
    inventory = json.loads(
        run_command(str(python), "-I", str(script), cwd=directory, env=env)
    )
    assert set(roots) <= {canonicalize_name(name) for name in inventory}
    assert not {
        name
        for name in inventory
        if set(canonicalize_name(name).split("-")).intersection(excluded)
    }
    return inventory


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


def test_t2_shared_svid_compositions(wheelhouse, tmp_path, record_property):
    for label, packages, exercise, excluded in (
        ("standalone", SPIFFE, exercise_shared_svid, ("wimse", "spire")),
        (
            "optional-wit",
            ("tba-concrete-wit-svid-credential",),
            exercise_optional_wit_svid,
            ("spire",),
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


def test_t2_shared_wimse_consumers(wheelhouse, tmp_path, record_property):
    inventory = run_installed(
        wheelhouse,
        tmp_path,
        (*WIMSE, "tba-profile-workload-authentication-wimse-mtls"),
        (exercise_wimse, exercise_wic),
        ("spiffe", "spire"),
    )
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))


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


def exercise_wit_rotation():
    import base64
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec, utils
    from tba_profile_workload_credential_wimse_wit import verify_wit

    def encode(value):
        return base64.urlsafe_b64encode(value).rstrip(b"=").decode()

    def create_key(kid):
        private = ec.generate_private_key(ec.SECP256R1())
        numbers = private.public_key().public_numbers()
        return private, {
            "kid": kid,
            "alg": "ES256",
            "kty": "EC",
            "crv": "P-256",
            "x": encode(numbers.x.to_bytes(32, "big")),
            "y": encode(numbers.y.to_bytes(32, "big")),
        }

    def token(key, jwk):
        header = {"alg": "ES256", "kid": jwk["kid"], "typ": "wit+jwt"}
        claims = {
            "sub": "wimse://example.org/workload",
            "exp": 200,
            "cnf": {"jwk": confirmation},
        }
        message = ".".join(
            encode(json.dumps(value).encode()) for value in (header, claims)
        )
        r, s = utils.decode_dss_signature(
            key.sign(message.encode(), ec.ECDSA(hashes.SHA256()))
        )
        return message + "." + encode(r.to_bytes(32, "big") + s.to_bytes(32, "big"))

    _, confirmation = create_key("workload")
    old, old_jwk = create_key("old")
    new, new_jwk = create_key("new")
    old_wit, new_wit = token(old, old_jwk), token(new, new_jwk)
    trust = {"example.org": [old_jwk, new_jwk]}
    assert verify_wit(old_wit, trust_by_domain=trust, now=100).jwt.integrity_verified
    assert verify_wit(new_wit, trust_by_domain=trust, now=100).jwt.integrity_verified
    trust["example.org"] = [new_jwk]
    assert verify_wit(new_wit, trust_by_domain=trust, now=100).jwt.integrity_verified
    try:
        verify_wit(old_wit, trust_by_domain=trust, now=100)
    except ValueError as error:
        assert "signing key" in str(error)
    else:
        raise AssertionError("retired WIT issuer remained trusted")


def test_t2_wit_issuer_rotation(wheelhouse, tmp_path, record_property):
    inventory = run_installed(
        wheelhouse, tmp_path, WIMSE, (exercise_wit_rotation,), ("spiffe", "spire")
    )
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))


def test_expanded_protocol_specification_ownership():
    from tba_profile_workload_authentication_wimse_mtls import (
        SPECIFICATION_VERSION as mtls_revision,
        verify_wimse_peer,
    )
    from tba_profile_workload_credential_spiffe_wit_svid import (
        CURRENT_VERSION as wit_svid_revision,
        verify_wit_svid,
    )
    from tba_profile_workload_credential_wimse_wic import (
        SPECIFICATION_VERSION as wic_revision,
        validate_wic,
    )
    from tba_profile_workload_credential_wimse_wit import (
        CURRENT_VERSION as wit_revision,
        verify_wit,
    )
    from tba_profile_workload_proof_wimse_wpt import (
        CURRENT_VERSION as wpt_revision,
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

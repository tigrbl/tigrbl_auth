"""Exercise native WIC checks through the TLS peer identity handoff."""

import json
from contextlib import contextmanager
from importlib.metadata import version

from cryptography import x509
from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_contracts_security_trust import CertificatePathValidationResult, CertificateStatus
from tba_profile_workload_authentication_wimse_mtls import TLSPeer, verify_wimse_peer
from tba_provider_certificate_status import SnapshotCertificateStatusProvider
from tba_testkit_workload_credential_conformance.fixtures import _mutual_tls_peers

from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.observations import Observation
from tba_test_interop_wimse.runner import run_inventory


IDENTITY = "wimse://example.org/workload"


class WicFixture:
    def __init__(self, directory, case):
        self.case = case
        variant = case["variant"]
        subjects = {
            "missing-workload-uri": (),
            "multiple-workload-uris": (IDENTITY, IDENTITY + "/other"),
        }.get(variant)
        self.ca, self.client, self.server = _mutual_tls_peers(
            directory, IDENTITY, client_identifiers=subjects
        )
        self.effects = []

    def observe(self):
        server = self.case["checker"] == "caller"
        der = self.server if server else self.client
        expected = IDENTITY + "/different-server" if server else IDENTITY
        ca = self.ca

        class DirectPath:
            def validate(self, request):
                leaf = x509.load_der_x509_certificate(request.leaf.der)
                leaf.verify_directly_issued_by(ca)
                return CertificatePathValidationResult(True, request.leaf.profile)

        status = SnapshotCertificateStatusProvider()
        status.publish(der, CertificateStatus.GOOD, "test-ca")
        try:
            identity = verify_wimse_peer(
                TLSPeer(parse_x509_certificate(der),
                        server_name="service.example.org" if server else None),
                expected_identity=expected,
                validators_by_domain={"example.org": DirectPath()},
                status_provider=status,
            ).workload_identifier
        except ValueError as error:
            return Observation("deny", self.case["target_hop"], reason=str(error))
        self.effects.append(identity)
        return Observation("allow", self.case["target_hop"], effects=len(self.effects),
                           reason=identity)


class NativeWicAdapter:
    def __init__(self, tmp_path):
        self.tmp_path = tmp_path

    def supports(self, case):
        return all(hop["profile"] == "wic-mtls" and hop["identifier_scheme"] == "wimse"
                   and hop["wic_issuer"] == "baseline" for hop in case["hops"].values())

    def setup_key(self, case, execution):
        return "native-wimse-wic"

    def check_setup(self, case, execution):
        control = dict(case, variant="valid-peer", checker="receiver")
        with self.isolated(control, execution) as fixture:
            assert fixture.observe().reason == IDENTITY

    @contextmanager
    def isolated(self, case, execution):
        from tempfile import TemporaryDirectory
        from pathlib import Path

        with TemporaryDirectory(dir=self.tmp_path) as directory:
            yield WicFixture(Path(directory), case)


def test_native_wic_setup_and_effects(tmp_path, record_property):
    adapter = NativeWicAdapter(tmp_path)
    cases = [case for case in generate_matrix()["scenarios"]
             if case["scenario_id"] in {"01", "03"} and adapter.supports(case)]
    assert {case["variant"] for case in cases} == {
        "valid-peer", "missing-workload-uri", "multiple-workload-uris", "wrong-server-identity",
    }
    runs = [{"id": case["id"], "scenario_id": case["id"], "status": "qualified"} for case in cases]
    actual = list(run_inventory(cases, runs, {"01": adapter, "03": adapter}))
    assert {item["status"] for item in actual} == {"passed"}, actual
    reasons = {
        "valid-peer": IDENTITY,
        "missing-workload-uri": "exactly one",
        "multiple-workload-uris": "exactly one",
        "wrong-server-identity": "unexpected WIMSE peer identity",
    }
    for case, item in zip(cases, actual):
        assert reasons[case["variant"]] in item["observation"]["reason"]
    record_property("installed_wimse_mtls_version",
                    version("tba-profile-workload-authentication-wimse-mtls"))
    record_property("native_results", json.dumps(actual, sort_keys=True))

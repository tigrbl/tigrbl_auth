"""Native WIC cases using the same TCP fixtures exposed to partners."""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import asdict
from importlib.metadata import version
from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.runner import run_inventory

from support.wic_fixture import DNS, IDENTITY, SERVER, WicFixture


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
            observed = fixture.observe()
            assert observed.decision == "allow" and observed.effects == 1

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
    reasons = {
        "valid-peer": IDENTITY, "missing-workload-uri": "exactly one",
        "multiple-workload-uris": "exactly one", "wrong-server-identity": "unexpected WIMSE peer identity",
    }
    assert {case["variant"] for case in cases} == reasons.keys()
    runs = [{"id": case["id"], "scenario_id": case["id"], "status": "qualified"} for case in cases]
    actual = list(run_inventory(cases, runs, {"01": adapter, "03": adapter}))
    assert {item["status"] for item in actual} == {"passed"}, actual
    for case, item in zip(cases, actual):
        assert reasons[case["variant"]] in item["observation"]["reason"]
    record_property("installed_wimse_mtls_version",
                    version("tba-profile-workload-authentication-wimse-mtls"))
    record_property("native_results", json.dumps(actual, sort_keys=True))


def test_partner_cli_roles(tmp_path):
    fixture = WicFixture(tmp_path, {"variant": "valid-peer"})
    command = [sys.executable, "-B", "-m", "tba_test_interop_wimse.wic_cli"]
    package_root = os.path.dirname(os.path.dirname(sys.modules["tba_test_interop_wimse"].__file__))
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(
        filter(None, (package_root, os.getenv("PYTHONPATH")))
    )}

    def config(tls, expected, good):
        return {
            "tls": asdict(tls), "expected_peer": expected,
            "domain_anchors": {"example.org": tls.trust_anchor},
            "good_certificates": [good.certificate], "dns_name": DNS,
        }

    server = tmp_path / "receiver.json"
    client = tmp_path / "caller.json"
    server.write_text(json.dumps(config(fixture.server_tls, IDENTITY, fixture.client_tls)),
                      encoding="utf-8")
    receiver = subprocess.Popen([*command, "receive", str(server)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            line = executor.submit(receiver.stdout.readline).result(timeout=10)
            assert line, receiver.stderr.read()
            address = json.loads(line)
            client.write_text(json.dumps({
                **config(fixture.client_tls, SERVER, fixture.server_tls), **address,
            }), encoding="utf-8")
            for role, status, payload in [
                ("call", 201, {"decision": "allow", "identity": IDENTITY}),
                ("readback", 200, {"decision": "allow", "writes": [IDENTITY]}),
            ]:
                output = subprocess.run([*command, role, str(client)], check=True, env=env,
                                        capture_output=True, text=True, timeout=10)
                assert json.loads(output.stdout) == {"http_status": status, "response": payload}
        finally:
            receiver.terminate()
            receiver.communicate(timeout=10)

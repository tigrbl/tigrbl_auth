"""Native WIC cases using the same TCP fixtures exposed to partners."""

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from importlib.metadata import version
from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.coverage import inventory_report
from tba_test_interop_wimse.runner import run_inventory

from support.wic_fixture import DNS, IDENTITY, SERVER, NativeWicAdapter, WicFixture


def test_native_wic_setup_and_effects(tmp_path, record_property):
    adapter = NativeWicAdapter(tmp_path)
    cases = [case for case in generate_matrix()["scenarios"]
             if adapter.supports(case)]
    reasons = {
        "valid-peer": IDENTITY, "missing-workload-uri": "exactly one",
        "multiple-workload-uris": "exactly one", "wrong-server-identity": "unexpected WIMSE peer identity",
        "untrusted-domain": "unexpected WIMSE peer identity", "wrong-anchor": "path",
    }
    assert {case["variant"] for case in cases} == reasons.keys()
    declared = {row["id"] for row in inventory_report(generate_matrix())["scenarios"]
                if any(binding.startswith("native_wic") for binding in row["local_fixtures"])}
    assert declared == {case["id"] for case in cases}
    runs = [{"id": case["id"], "scenario_id": case["id"], "status": "qualified"} for case in cases]
    actual = list(run_inventory(cases, runs, dict.fromkeys(("01", "02", "03"), adapter)))
    assert {item["status"] for item in actual} == {"passed"}, actual
    for case, item in zip(cases, actual):
        reason = reasons[case["variant"]].replace("wimse:", adapter.setup_key(case, None) + ":")
        assert reason in item["observation"]["reason"]
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

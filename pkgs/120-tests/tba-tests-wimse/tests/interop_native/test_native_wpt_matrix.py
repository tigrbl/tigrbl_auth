"""Native WIT/WPT and HTTP Signature matrix and CLI checks."""

from concurrent.futures import ThreadPoolExecutor
from importlib.metadata import version
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from cryptography.hazmat.primitives import serialization

from tba_test_interop_wimse.coverage import inventory_report
from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.runner import run_inventory

from support.wic_fixture import DNS, IDENTITY
from support.wpt_fixture import NativeWptAdapter, WptFixture


CASES = [case for case in generate_matrix()["scenarios"]
         if NativeWptAdapter(None).supports(case)]
REASONS = {
    "valid-peer": IDENTITY, "untrusted-domain": "trust domain", "wrong-anchor": "signature",
    "missing-proof": "WPT authorization", "wrong-proof-key": "signature",
    "wrong-audience": "audience", "first-presentation": IDENTITY, "duplicate-presentation": "replay",
    "identity-equality-policy": "TLS and application identities differ",
}


def test_native_wpt_inventory():
    assert {case["variant"] for case in CASES} == REASONS.keys()
    assert len({case["hops"][case["target_hop"]]["profile"] for case in CASES}) == 4
    declared = {row["id"] for row in inventory_report(generate_matrix())["scenarios"]
                if any(not binding.startswith("native_wic") for binding in row["local_fixtures"])}
    assert declared == {case["id"] for case in CASES}


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_native_wpt_matrix(case, tmp_path, record_property):
    run = {"id": case["id"], "scenario_id": case["id"], "status": "qualified"}
    result, = run_inventory([case], [run], {case["scenario_id"]: NativeWptAdapter(tmp_path)})
    assert result["status"] == "passed", result
    profile, scheme = NativeWptAdapter(None).setup_key(case, run)
    reason = REASONS[case["variant"]]
    if "signature" in profile and case["variant"] == "missing-proof":
        reason = "missing HTTP signature"
    assert reason in result["observation"]["reason"]
    record_property("native_result", json.dumps(result, sort_keys=True))
    record_property("installed_wimse_wpt_version", version("tba-profile-workload-proof-wimse-wpt"))


def test_wpt_cli_roles(tmp_path):
    fixture = WptFixture(tmp_path, {})
    caller = fixture.caller("valid-peer")
    key = tmp_path / "proof.key"
    key.write_bytes(fixture.workload_key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ))
    wit = tmp_path / "wit.txt"
    wit.write_text(caller.wit, encoding="utf-8")
    receiver_config = tmp_path / "receiver.json"
    receiver_config.write_text(json.dumps({
        "certificate": fixture.tls.certificate, "private_key": fixture.tls.private_key,
        "dns_name": DNS, "trust_by_domain": fixture.trust,
    }), encoding="utf-8")
    package = Path(sys.modules["tba_test_interop_wimse"].__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(
        filter(None, (str(package), os.getenv("PYTHONPATH")))
    )}
    cmd = [sys.executable, "-B", "-m", "tba_test_interop_wimse.wpt_cli"]
    from concurrent.futures import ThreadPoolExecutor

    with subprocess.Popen([*cmd, "receive", str(receiver_config)], env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as server:
        with ThreadPoolExecutor(max_workers=1) as reader:
            try:
                line = reader.submit(server.stdout.readline).result(timeout=10)
                assert line, server.stderr.read()
                caller_config = tmp_path / "caller.json"
                caller_config.write_text(json.dumps({
                    **json.loads(line), "dns_name": DNS, "private_key": str(key),
                    "trust_anchor": str(fixture.anchor), "wit_file": str(wit),
                }), encoding="utf-8")
                for role, code, body in (
                    ("call", 201, {"decision": "allow", "identity": IDENTITY}),
                    ("readback", 200, {"decision": "allow", "writes": [IDENTITY]}),
                ):
                    result = subprocess.run([*cmd, role, str(caller_config)], env=env,
                                            capture_output=True, text=True, timeout=10)
                    assert result.returncode == 0, result.stderr
                    assert json.loads(result.stdout) == {"http_status": code, "response": body}
            finally:
                server.terminate()
                server.communicate(timeout=10)

"""Run native WIT/WPT matrix cases over HTTPS with a fresh receiver per row."""

from contextlib import contextmanager
from importlib.metadata import version
from tempfile import TemporaryDirectory
from pathlib import Path
from threading import Thread
from time import time
import json
import os
import subprocess
import sys

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from tba_concrete_jwt import decode_jwt_unverified
from tba_primitives_identity import base64url_encode
from tba_profile_workload_credential_wimse_wit import issue_wit
from tba_provider_jose_cryptography import JwsCryptographyProvider
from tba_provider_jose_cryptography.jws import sign_compact_jwt
from tba_testkit_workload_credential_conformance.fixtures import _certificate

from tba_test_interop_wimse.catalog import read_catalog
from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.observations import Observation
from tba_test_interop_wimse.runner import run_inventory
from tba_test_interop_wimse.wpt import WptCaller, WptReceiver

from support.wic_fixture import DNS, IDENTITY, write_leaf


def public_jwk(key):
    return {"kty": "OKP", "crv": "Ed25519", "alg": "EdDSA",
            "x": base64url_encode(key.public_key().public_bytes_raw())}


class NativeWptAdapter:
    binding = read_catalog("fixtures.toml")["local"]["native_wpt"]

    def __init__(self, directory):
        self.directory = directory

    def supports(self, case):
        return (
            case["scenario_id"] in self.binding["families"] and len(case["hops"]) == 1
            and case["hops"][case["target_hop"]]["profile"] == "wit-wpt"
            and case["hops"][case["target_hop"]]["wit_issuer"] == "baseline"
        )

    def setup_key(self, case, execution):
        return "native-wit-wpt-https"

    def check_setup(self, case, execution):
        with self.isolated(dict(case, variant="valid-peer"), execution) as fixture:
            observation = fixture.observe()
            assert observation.decision == "allow" and observation.effects == 1

    @contextmanager
    def isolated(self, case, execution):
        with TemporaryDirectory(dir=self.directory) as work:
            yield WptFixture(Path(work), case)


class WptFixture:
    def __init__(self, directory, case):
        self.case = case
        issuer, workload, alternate = (Ed25519PrivateKey.generate() for _ in range(3))
        self.signer = JwsCryptographyProvider(
            {"issuer": issuer, "workload": workload, "alternate": alternate}
        )
        self.workload = public_jwk(workload)
        self.workload_key = workload
        self.trust = {"example.org": [{**public_jwk(issuer), "kid": "fixture-issuer"}]}
        ca = _certificate(())
        self.anchor = directory / "ca.pem"
        self.anchor.write_bytes(ca[0].public_bytes(serialization.Encoding.PEM))
        self.tls = write_leaf(directory, "server", _certificate((), issuer=ca, dns=DNS), self.anchor)

    def caller(self, variant):
        now = int(time())
        subject = "wimse://other.example/workload" if variant == "untrusted-domain" else IDENTITY
        wit = issue_wit(
            self.signer, subject=subject, confirmation_jwk=self.workload,
            issuer_key_reference="alternate" if variant == "wrong-anchor" else "issuer",
            issuer_key_id="fixture-issuer", issuer_algorithm="EdDSA",
            issued_at=now, expires_at=now + 120,
        )
        return WptCaller(self.signer, wit, "workload", str(self.anchor))

    def observe(self):
        variant = self.case["variant"]
        with WptReceiver(0, self.tls.certificate, self.tls.private_key, DNS, self.trust) as receiver:
            thread = Thread(target=receiver.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
            thread.start()
            try:
                caller = self.caller(variant)
                port = receiver.server_port
                headers = caller.present("other.example" if variant == "wrong-audience" else DNS, port)
                if variant == "missing-proof":
                    headers.pop("Authorization")
                if variant == "wrong-proof-key":
                    claims = decode_jwt_unverified(headers["Authorization"].split(" ", 1)[1]).claims
                    proof = sign_compact_jwt(self.signer, claims,
                                             headers={"typ": "wpt+jwt", "alg": "EdDSA"},
                                             key_reference="alternate")
                    headers["Authorization"] = "WPT " + proof
                result = caller.request("127.0.0.1", port, DNS, headers=headers)
                events = ()
                additional = 0
                decision = result["response"]["decision"]
                if variant == "duplicate-presentation":
                    assert result["http_status"] == 201
                    assert receiver.ledger.snapshot() == (IDENTITY,)
                    result = caller.request("127.0.0.1", port, DNS, headers=headers)
                    assert result["http_status"] == 401
                    assert result["response"]["decision"] == "deny"
                    additional = len(receiver.ledger.snapshot()) - 1
                    events = ("initial-allow", "initial-effect", "duplicate-refused")
                    decision = "allow-then-deny"
                elif decision == "allow":
                    assert result["http_status"] == 201
                    assert result["response"]["identity"] == IDENTITY
                else:
                    assert result["http_status"] == 401
                readback = self.caller("valid-peer").request("127.0.0.1", port, DNS, readback=True)
                assert readback["http_status"] == 200
                writes = readback["response"]["writes"]
                assert writes == list(receiver.ledger.snapshot())
                return Observation(decision, self.case["target_hop"], events,
                                   effects=len(writes), additional_effects=additional,
                                   reason=result["response"].get("reason", IDENTITY))
            finally:
                receiver.shutdown()
                thread.join(timeout=5)


CASES = [case for case in generate_matrix()["scenarios"]
         if NativeWptAdapter(None).supports(case)]
REASONS = {
    "valid-peer": IDENTITY, "untrusted-domain": "trust domain", "wrong-anchor": "signature",
    "missing-proof": "WPT authorization", "wrong-proof-key": "signature",
    "wrong-audience": "audience", "first-presentation": IDENTITY, "duplicate-presentation": "replay",
}


def test_native_wpt_inventory():
    assert len(CASES) == len(REASONS)
    assert {case["variant"] for case in CASES} == REASONS.keys()


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_native_wpt_matrix(case, tmp_path, record_property):
    run = {"id": case["id"], "scenario_id": case["id"], "status": "qualified"}
    result, = run_inventory([case], [run], {case["scenario_id"]: NativeWptAdapter(tmp_path)})
    assert result["status"] == "passed", result
    assert REASONS[case["variant"]] in result["observation"]["reason"]
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

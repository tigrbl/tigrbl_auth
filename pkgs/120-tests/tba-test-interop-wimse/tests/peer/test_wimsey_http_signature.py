"""Two-way request-signature compatibility with the pinned wimsey CLI."""

import json
import os
from hashlib import sha256
from pathlib import Path
import subprocess
from time import time

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from tba_primitives_identity import base64url_encode
from tba_profile_workload_credential_wimse_wit import issue_wit
from tba_provider_jose_cryptography import JwsCryptographyProvider
from tba_provider_replay_memory import MemoryReplayCheckProvider

from tba_test_interop_wimse.adapters.wimsey_wic import WIMSEY_REVISION
from tba_test_interop_wimse.signatures import authenticate_signature, sign_request


def jwk(key):
    return {"kty": "OKP", "crv": "Ed25519", "alg": "EdDSA",
            "x": base64url_encode(key.public_key().public_bytes_raw())}


def test_wimsey_http_signature_both_directions(tmp_path, record_property):
    checkout = os.getenv("TBA_WIMSEY_CHECKOUT")
    if not checkout:
        pytest.skip("Set TBA_WIMSEY_CHECKOUT to the built pinned wimsey checkout.")
    revision = subprocess.check_output(["git", "-C", checkout, "rev-parse", "HEAD"],
                                       text=True, timeout=10).strip()
    assert revision == WIMSEY_REVISION
    binary = Path(checkout) / "target/debug" / ("wimsey.exe" if os.name == "nt" else "wimsey")
    record_property("peer_revision", revision)
    record_property("peer_binary_sha256", sha256(binary.read_bytes()).hexdigest())
    record_property("scope", "bidirectional request-signature component over synthetic input")

    issuer, proof = Ed25519PrivateKey.generate(), Ed25519PrivateKey.generate()
    issuer_path = tmp_path / "issuer.json"
    issuer_path.write_text(json.dumps(jwk(issuer)), encoding="utf-8")
    proof_path = tmp_path / "proof.json"
    proof_path.write_text(json.dumps({**jwk(proof), "d": base64url_encode(proof.private_bytes_raw())}),
                          encoding="utf-8")
    now = int(time())
    subject = "wimse://example.org/interop"
    audience = "https://service.example.org/writes"
    wit = issue_wit(JwsCryptographyProvider({"issuer": issuer}), subject=subject,
                    confirmation_jwk=jwk(proof), issuer_key_reference="issuer",
                    issuer_key_id="fixture", issuer_algorithm="EdDSA",
                    issued_at=now, expires_at=now + 120)
    args = ["--method", "POST", "--authority", "service.example.org", "--path", "/writes",
            "--aud", audience, "--wit", wit]
    headers = sign_request(proof, wit, "POST", "/writes", audience, now)
    result = subprocess.run(
        [str(binary), "httpsig", "verify", *args, "--issuer-jwk", str(issuer_path),
         "--now", str(now), "--signature-input", headers["signature-input"], "--signature", headers["signature"]],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["sub"] == subject

    result = subprocess.run(
        [str(binary), "httpsig", "sign", *args, "--pop-key", str(proof_path), "--created", str(now)],
        capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    incoming = [("Workload-Identity-Token", wit)]
    incoming.extend(line.split(": ", 1) for line in result.stdout.splitlines())
    assert authenticate_signature(
        incoming, method="POST", path="/writes", audience=audience, now=now,
        trust_by_domain={"example.org": [{**jwk(issuer), "kid": "fixture"}]},
        replay_store=MemoryReplayCheckProvider(),
    ) == subject

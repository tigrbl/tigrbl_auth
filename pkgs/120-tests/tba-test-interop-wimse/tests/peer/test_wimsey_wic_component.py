"""External wimsey WIC component checks under the peer evidence track."""

import json
import os
import subprocess

from tba_test_interop_wimse.adapters.wimsey_wic import WIMSEY_REVISION, WimseyVerifier

from support.wic_fixture import WicFixture


def test_wimsey_wic_component(tmp_path, record_property):
    import pytest
    from hashlib import sha256
    from pathlib import Path

    checkout = os.getenv("TBA_WIMSEY_CHECKOUT")
    if not checkout:
        pytest.skip("Set TBA_WIMSEY_CHECKOUT to the built, pinned wimsey checkout.")
    revision = subprocess.check_output(
        ["git", "-C", checkout, "rev-parse", "HEAD"], text=True, timeout=10
    ).strip()
    assert revision == WIMSEY_REVISION
    binary = Path(checkout) / "target" / "debug" / ("wimsey.exe" if os.name == "nt" else "wimsey")
    record_property("wimsey_revision", revision)
    record_property("wimsey_binary_sha256", sha256(binary.read_bytes()).hexdigest())
    for direction in ("forward", "reverse"):
        for variant, checker in (
            ("valid-peer", "receiver"), ("missing-workload-uri", "receiver"),
            ("multiple-workload-uris", "receiver"), ("wrong-server-identity", "caller"),
        ):
            directory = tmp_path / f"{direction}-{variant}"
            directory.mkdir()
            case = {"variant": variant, "checker": checker, "target_hop": "enforcing"}
            def verifier(anchor, expected):
                return WimseyVerifier(binary, anchor, expected)

            bindings = {"receiver_verifier" if direction == "forward" else "server_verifier": verifier}
            actual = WicFixture(directory, case, **bindings).observe()
            accepted = variant == "valid-peer"
            assert actual.decision == ("allow" if accepted else "deny")
            assert actual.effects == int(accepted)
            record_property(f"{direction}-{variant}", json.dumps({
                "decision": actual.decision, "effects": actual.effects, "reason": actual.reason,
                "wic_verifier": "wimsey" if (checker == "caller") == (direction == "reverse") else "tba",
                "tls_transport": "shared-python-ssl-fixture",
            }))

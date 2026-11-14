"""Opt-in peer component checks, with explicit transport and resource scope."""

import json
import os
from pathlib import Path

import pytest

from tba_test_interop_wimse.adapters.cred_wpt import check_protected_read


@pytest.mark.parametrize("variant", [
    "valid-peer", "missing-proof", "wrong-proof-key", "wrong-audience",
    "first-presentation", "duplicate-presentation",
])
def test_cred_wpt_component(variant, tmp_path, record_property):
    checkout = os.getenv("CRED_SDK_CHECKOUT")
    if not checkout:
        pytest.skip("Set CRED_SDK_CHECKOUT to the built pinned peer.")
    from tba_testkit_wimse_cred_interop.peer import CRED_REVISION, start_cred
    from tba_testkit_wimse_cred_interop.tokens import WorkloadTokens

    tokens = WorkloadTokens()
    with start_cred(Path(checkout).resolve(), tmp_path, tokens.trust_bundle) as peer:
        result = check_protected_read(peer, tokens, variant)
    record_property("component_result", json.dumps({
        "direction": "tba-to-cred", "peer_revision": CRED_REVISION,
        "transport": "http-loopback", "resource": "seeded-connections-read",
        **result,
    }))

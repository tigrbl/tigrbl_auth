"""Prove each native baseline workload profile over the local lab wire."""

import pytest

from support.typed_workload_chain import native_workload_hop
CONFIGURATION = "shared-python-tls-direct-ca-ledger-v1"


@pytest.mark.parametrize("profile,scheme", [
    ("wic-mtls", "wimse"), ("wic-mtls", "spiffe"),
    ("wic-mtls-wpt", "wimse"), ("wic-mtls-wpt", "spiffe"),
    ("wic-mtls-http-signature", "wimse"), ("wic-mtls-http-signature", "spiffe"),
    ("wit-wpt", "none"), ("wit-http-signature", "none"),
])
@pytest.mark.parametrize("allowed", [True, False])
def test_native_baseline_workload(tmp_path, profile, scheme, allowed, record_property):
    transport_only = profile == "wic-mtls"
    hop = {"profile": profile, "identifier_scheme": scheme,
           "wic_issuer": "none" if scheme == "none" else "baseline",
           "wit_issuer": "none" if transport_only else "baseline"}
    refusal = "wrong-anchor" if transport_only else "wrong-proof-key"
    case = {"variant": "valid-peer" if allowed else refusal,
            "layer": "tls" if transport_only else "application",
            "target_hop": "enforcing", "hops": {"enforcing": hop}}
    with native_workload_hop(tmp_path, case, hop,
                             {"caller_name": "workload", "receiver_name": "workload/server"}) as fixture:
        observed = fixture.observe()
    for name, value in (("profile", profile), ("identifier_scheme", scheme), ("configuration", CONFIGURATION),
                        ("decision", observed.decision), ("effects", observed.effects)):
        record_property(name, value)
    assert (observed.hop, observed.decision, observed.effects) == (
        ("enforcing", "allow", 1) if allowed else ("enforcing", "deny", 0)
    )

"""Qualify native X.509-SVID transport with and without application proof."""

import pytest

from support.typed_workload_chain import native_workload_hop


@pytest.mark.parametrize("profile", ["wic-mtls", "wic-mtls-wpt", "wic-mtls-http-signature"])
@pytest.mark.parametrize("variant", ["valid-peer", "wrong-anchor", "wrong-server-identity"])
def test_native_x509_svid_presentation(tmp_path, profile, variant, record_property):
    hop = {"profile": profile, "identifier_scheme": "spiffe",
           "wic_issuer": "tba-x509-svid", "wit_issuer": "none" if profile == "wic-mtls" else "baseline"}
    case = {
        "variant": variant, "layer": "tls", "target_hop": "enforcing",
        "hops": {"enforcing": hop},
    }
    names = {"caller_name": "workload", "receiver_name": "workload/server"}
    with native_workload_hop(tmp_path, case, hop, names) as fixture:
        observed = fixture.observe()
    record_property("profile", profile)
    record_property("identifier_scheme", "spiffe")
    record_property("issuer", "tba-x509-svid")
    record_property("decision", observed.decision)
    record_property("effects", observed.effects)
    assert (observed.decision, observed.effects) == (
        ("allow", 1) if variant == "valid-peer" else ("deny", 0)
    )

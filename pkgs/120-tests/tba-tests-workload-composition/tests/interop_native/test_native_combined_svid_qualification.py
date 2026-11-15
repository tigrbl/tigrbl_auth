"""Qualify both native SVID issuers on the same authenticated request."""

import pytest

from support.typed_workload_chain import native_workload_hop
from tba_test_interop_wimse.native_expansion import COMBINED_SCOPE


@pytest.mark.parametrize("profile", ["wic-mtls-wpt", "wic-mtls-http-signature"])
@pytest.mark.parametrize("variant,layer", [
    ("valid-peer", "operation"), ("wrong-anchor", "tls"), ("wrong-proof-key", "application"),
])
def test_native_combined_svid_presentation(tmp_path, profile, variant, layer, record_property):
    hop = {"profile": profile, "identifier_scheme": "spiffe",
           "wic_issuer": "tba-x509-svid", "wit_issuer": "tba-wit-svid"}
    case = {"variant": variant, "layer": layer, "target_hop": "enforcing", "hops": {"enforcing": hop}}
    names = {"caller_name": "workload", "receiver_name": "workload/server"}
    with native_workload_hop(tmp_path, case, hop, names) as fixture:
        observed = fixture.observe()
    record_property("profile", profile)
    record_property("identifier_scheme", "spiffe")
    record_property("issuer", COMBINED_SCOPE)
    record_property("decision", observed.decision)
    record_property("effects", observed.effects)
    assert (observed.decision, observed.effects) == (
        ("allow", 1) if variant == "valid-peer" else ("deny", 0)
    )

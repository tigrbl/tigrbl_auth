"""Native issuer controls for WIT-SVID presentations over the local lab wire."""

import pytest

from support.typed_workload_chain import native_workload_hop


@pytest.mark.parametrize("profile,scheme", [
    ("wit-wpt", "none"), ("wit-http-signature", "none"),
    ("wic-mtls-wpt", "wimse"), ("wic-mtls-wpt", "spiffe"),
    ("wic-mtls-http-signature", "wimse"), ("wic-mtls-http-signature", "spiffe"),
])
@pytest.mark.parametrize("variant", ["valid-peer", "wrong-anchor", "wrong-proof-key"])
def test_native_wit_svid_presentation(tmp_path, profile, scheme, variant, record_property):
    case = {
        "variant": variant, "layer": "operation", "target_hop": "enforcing",
        "hops": {"enforcing": {"profile": profile, "identifier_scheme": scheme,
                              "wit_issuer": "tba-wit-svid",
                              "wic_issuer": "none" if scheme == "none" else "baseline"}},
    }
    with native_workload_hop(tmp_path, case, case["hops"]["enforcing"],
                             {"caller_name": "workload", "receiver_name": "workload/server"}) as fixture:
        observed = fixture.observe()
    allowed = variant == "valid-peer"
    record_property("profile", profile)
    record_property("identifier_scheme", scheme)
    record_property("issuer", "tba-wit-svid")
    record_property("decision", observed.decision)
    record_property("effects", observed.effects)
    assert (observed.decision, observed.effects) == (("allow", 1) if allowed else ("deny", 0))

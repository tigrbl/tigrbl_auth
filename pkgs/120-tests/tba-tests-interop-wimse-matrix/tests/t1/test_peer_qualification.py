from tba_tests_interop_wimse.catalog import read_catalog
from tba_tests_interop_wimse.matrix import endpoint_pairs, profile_options
from tba_tests_interop_wimse.qualification import pair_has_baseline


def test_endpoint_catalog_and_directional_joins():
    peers = read_catalog("peers.toml")
    factors = read_catalog("factors.toml")
    assert len(peers["capabilities"]) == 34
    options = profile_options(factors["hop_profiles"], factors)
    baseline = [hop for hop in options if all(hop[key] in {"baseline", "none"}
                for key in ("wit_issuer", "wic_issuer"))]
    assert len(baseline) == 8
    for hop in baseline:
        forward, reverse = sorted(endpoint_pairs(peers, hop),
                                  key=lambda pair: pair["caller"]["implementation"] != "tba")
        assert forward["caller"]["implementation"] == reverse["receiver"]["implementation"]
        assert forward["receiver"]["implementation"] == reverse["caller"]["implementation"]

    http = next(hop for hop in baseline if hop["profile"] == "wit-http-signature")
    for family in ("01", "07"):
        cred_pairs = [pair for pair in endpoint_pairs(peers, http, scenario_family=family)
                      if any(endpoint["implementation"] == "cred" for endpoint in pair.values())]
        assert {side for pair in cred_pairs for side in pair if pair[side]["implementation"] == "cred"} == {
            "caller", "receiver",
        }


def test_baseline_matches_exact_order_and_configuration():
    shared = dict(version="fixture-1", profile="wic-mtls", identifier_scheme="wimse",
                  configuration="fixture-config")
    caller = dict(shared, implementation="tba")
    receiver = dict(shared, implementation="peer")
    peers = {"baselines": [{"caller": caller, "receiver": receiver,
                            "outcome": "pass", "evidence": "artifact.json"}]}
    assert pair_has_baseline(peers, {"caller": caller, "receiver": receiver})
    assert not pair_has_baseline(peers, {"caller": receiver, "receiver": caller})
    assert not pair_has_baseline(peers, {"caller": caller,
                                         "receiver": dict(receiver, configuration="other")})

"""Independent enumeration using atomic hop settings."""
from itertools import product


def structural_keys(catalog, factors, exclusions):
    profiles = factors["hop_profiles"]
    canonical = {(item["tls"], item["proof"]): key for key, item in profiles.items()}
    raw = product(factors["factors"]["tls"]["levels"], factors["factors"]["proof"]["levels"],
                  ("none", "wimse", "spiffe"), ("none", "baseline", "spire-x509-svid"),
                  ("none", "baseline", "spire-wit-svid"))
    options = []
    for tls, proof, scheme, certificate, token in raw:
        if (tls, proof) not in canonical:
            continue
        if (scheme == "none") != (tls == "Server-authenticated TLS"):
            continue
        if (certificate == "none") != (scheme == "none"):
            continue
        if certificate == "spire-x509-svid" and scheme != "spiffe":
            continue
        if (token == "none") != (proof == "None"):
            continue
        options.append((canonical[tls, proof], scheme, certificate, token))
    for family in catalog["scenarios"]:
        for variant in family["variants"]:
            ruled_out = any(
                rule["scenario_id"] == family["id"] and variant["id"] in rule["variants"]
                and rule["event"] in variant.get("events", [])
                for rule in exclusions.get("trace_exclusions", [])
            )
            if ruled_out:
                continue
            hops = variant.get("hops", family["hops"])
            target = hops.index(variant.get("target", hops[-1]))
            available = [item for item in options if item[0] in family["profiles"]]
            for selected in product(available, repeat=len(hops)):
                for layer in variant.get("layers", ["operation"]):
                    if layer == "tls" and selected[target][2] == "none":
                        continue
                    if layer == "application" and selected[target][3] == "none":
                        continue
                    pairs = ",".join(hop + "=" + "/".join(item)
                                     for hop, item in zip(hops, selected))
                    yield f"{family['id']}:{variant['id']}:{layer}:{pairs}"

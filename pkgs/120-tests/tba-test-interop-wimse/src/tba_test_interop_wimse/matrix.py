"""Expand scoped scenario variants and join candidate endpoint capabilities."""

import json
from itertools import product
from .catalog import read_catalog, validate_catalog
from .qualification import pair_has_baseline


def profile_options(profiles, factors):
    """Expand WIC identifier schemes and issuer options on each applicable hop."""
    for name in profiles:
        profile = factors["hop_profiles"][name]
        uses_wic = profile["tls"] == "WIC mutual TLS"
        uses_wit = profile["proof"] != "None"
        for scheme in (("wimse", "spiffe") if uses_wic else ("none",)):
            wic_issuers = ["baseline"] if uses_wic else ["none"]
            if scheme == "spiffe":
                wic_issuers.append("spire-x509-svid")
            wit_issuers = ["baseline", "spire-wit-svid"] if uses_wit else ["none"]
            for wic_issuer, wit_issuer in product(wic_issuers, wit_issuers):
                yield {
                    "profile": name,
                    **profile,
                    "identifier_scheme": scheme,
                    "wic_issuer": wic_issuer,
                    "wit_issuer": wit_issuer,
                }


def validate_events(scenario_id, variant):
    events = variant.get("events", [])
    required = {
        ("12", "revocation-before-effect"):
            ["initial-allow", "revocation-observed", "commit-refused"],
        ("18", "revocation-before-release"):
            ["initial-allow", "revocation-observed", "release-refused"],
        ("18", "revocation-after-release"):
            ["initial-allow", "bearer-released", "revocation-observed", "provider-decision"],
    }
    expected = required.get((scenario_id, variant["id"]))
    if expected and events != expected:
        raise ValueError(f"Unexpected event ordering in {scenario_id}/{variant['id']}")
    if not len(events) == len(set(events)):
        raise ValueError(f"Duplicate events in {scenario_id}/{variant['id']}")


def expand_scenarios(catalog, factors, exclusions):
    """Enumerate all modeled hop options for each explicit scenario variant."""
    for family in catalog["scenarios"]:
        for variant in family["variants"]:
            validate_events(family["id"], variant)
            hops = variant.get("hops", family["hops"])
            target = variant.get("target", hops[-1])
            options = list(profile_options(family["profiles"], factors))
            for profiles in product(options, repeat=len(hops)):
                by_hop = dict(zip(hops, profiles))
                if len(by_hop) != len(hops) or target not in by_hop:
                    raise ValueError(f"Invalid hop layout in {family['id']}/{variant['id']}")
                hop = by_hop[target]
                layers = variant.get("layers", ["operation"])
                for layer in layers:
                    if layer == "tls" and hop["wic_issuer"] == "none":
                        continue
                    if layer == "application" and hop["wit_issuer"] == "none":
                        continue
                    trace = {
                        "scenario_id": family["id"],
                        "variant": variant["id"],
                        "events": variant.get("events", []),
                    }
                    if any(
                        trace["scenario_id"] == rule["scenario_id"]
                        and trace["variant"] in rule["variants"]
                        and rule["event"] in trace["events"]
                        for rule in exclusions.get("trace_exclusions", [])
                    ):
                        continue
                    hop_id = ",".join(
                        f"{name}={item['profile']}/{item['identifier_scheme']}/"
                        f"{item['wic_issuer']}/{item['wit_issuer']}"
                        for name, item in by_hop.items()
                    )
                    yield {
                        "id": f"{family['id']}:{variant['id']}:{layer}:{hop_id}",
                        "family": family["name"],
                        "topology": family["topology"],
                        "hops": by_hop,
                        "target_hop": target,
                        "layer": layer,
                        "checker": variant.get("checker", "receiver"),
                        "support_roles": family.get("support_roles", []),
                        **trace,
                        "decision": variant["decision"],
                        "effect": variant["effect"],
                        "accounting": variant.get("accounting", ""),
                        "schedule": variant.get("schedule", ""),
                    }


def endpoint_pairs(peers, hop):
    capabilities = [
        row for row in peers["capabilities"]
        if row["profile"] == hop["profile"]
        and row["identifier_scheme"] == hop["identifier_scheme"]
    ]
    for caller, receiver in product(capabilities, repeat=2):
        if caller["role"] != "caller" or receiver["role"] != "receiver":
            continue
        if (caller["implementation"] == "tba") == (receiver["implementation"] == "tba"):
            continue
        if "unsupported" in (caller["status"], receiver["status"]):
            continue
        yield {"caller": caller, "receiver": receiver}


def expand_executions(scenario, peers):
    hop_ids = list(scenario["hops"])
    choices = [list(endpoint_pairs(peers, hop)) for hop in scenario["hops"].values()]
    for pairs in product(*choices):
        if any(
            left["receiver"]["implementation"] != right["caller"]["implementation"]
            or left["receiver"].get("version") != right["caller"].get("version")
            or left["receiver"].get("configuration") != right["caller"].get("configuration")
            for left, right in zip(pairs, pairs[1:])
        ):
            continue
        issuer_roles = [
            f"{name}:{kind}:{hop[kind]}"
            for name, hop in scenario["hops"].items()
            for kind in ("wic_issuer", "wit_issuer")
            if hop[kind] != "none"
        ]
        pending_roles = [
            role for role in issuer_roles + scenario["support_roles"]
            if role not in peers.get("qualified_support", {})
        ]
        endpoints_qualified = all(
            row["status"] == "qualified" for pair in pairs for row in pair.values()
        )
        baselines = all(pair_has_baseline(peers, pair) for pair in pairs)
        status = "qualified" if endpoints_qualified and baselines and not pending_roles else "pending"
        direction = "forward" if pairs[0]["caller"]["implementation"] == "tba" else "reverse"
        endpoints = ";".join(
            json.dumps([pair[side]["implementation"], pair[side].get("version"),
                        pair[side].get("configuration")], separators=(",", ":"))
            for pair in pairs for side in ("caller", "receiver")
        )
        yield {
            "id": f"{scenario['id']}:{endpoints}",
            "scenario_id": scenario["id"],
            "direction": direction,
            "pairs": dict(zip(hop_ids, pairs)),
            "pending_roles": pending_roles,
            "status": status,
        }


def generate_matrix():
    factors = read_catalog("factors.toml")
    exclusions = read_catalog("exclusions.toml")
    peers = read_catalog("peers.toml")
    catalog = read_catalog("scenarios.toml")
    validate_catalog(factors, catalog, exclusions)
    keys = set()
    for role, qualification in peers.get("qualified_support", {}).items():
        if not all(qualification.get(field) for field in ("implementation", "version", "configuration", "evidence")):
            raise ValueError(f"Incomplete support qualification for {role}")
    for peer in peers["capabilities"]:
        key = tuple(peer.get(k) for k in (
            "implementation", "version", "configuration", "role", "profile", "identifier_scheme"
        ))
        implementation = peers["implementations"][peer["implementation"]]
        if key in keys or peer["status"] not in {"pending", "qualified", "unsupported"}:
            raise ValueError(f"Invalid or duplicate peer capability {key}")
        if peer["status"] == "qualified" and (
            not all(peer.get(field) for field in ("version", "configuration", "evidence"))
            or implementation.get("placeholder")
        ):
            raise ValueError(f"Unpinned, placeholder, or unevidenced qualification {key}")
        keys.add(key)
    scenarios = list(expand_scenarios(catalog, factors, exclusions))
    executions = [row for scenario in scenarios for row in expand_executions(scenario, peers)]
    if len({row["id"] for row in scenarios}) != len(scenarios):
        raise ValueError("Duplicate structural scenario ID")
    if len({row["id"] for row in executions}) != len(executions):
        raise ValueError("Duplicate execution row ID")
    return {
        "counts": {
            "scenario_families": len(catalog["scenarios"]),
            "endpoint_capabilities": len(keys),
            "structural_scenarios": len(scenarios),
            "pending_execution_rows": sum(row["status"] == "pending" for row in executions),
            "qualified_execution_rows": sum(row["status"] == "qualified" for row in executions),
        },
        "scenarios": scenarios,
        "executions": executions,
        "capabilities": peers["capabilities"],
    }

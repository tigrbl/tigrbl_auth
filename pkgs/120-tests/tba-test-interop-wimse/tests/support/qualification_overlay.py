"""Create a scoped lab qualification snapshot from four executed WIC controls."""

from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
from contextlib import nullcontext
import json
import os
import platform
import ssl
from tempfile import TemporaryDirectory

from tba_test_interop_wimse.catalog import read_catalog
from tba_test_interop_wimse.matrix import generate_matrix
from tba_test_interop_wimse.observations import mismatches

from support.wimsey_endpoint import CONFIGURATION, WIMSEY_REVISION, WimseyWicAdapter
from support.spire_issuer import IMAGE, spire_issuer, spire_wit_issuers
from support.wic_support_cases import SUPPORT_FAMILIES
from support.wimsey_signature_endpoint import (
    CONFIGURATION as SIGNATURE_CONFIGURATION, PROFILE as SIGNATURE_PROFILE, SLOT as SIGNATURE_SLOT,
    WimseySignatureAdapter,
)
from support.wimsey_wpt import PROFILE as WPT_PROFILE, SLOT as WPT_SLOT, build_bridge
from support.cofide_endpoint import PROFILE as COFIDE_PROFILE, SLOT as COFIDE_SLOT, REVISION as COFIDE_REVISION, binary_digest
from support.cred_endpoint import (
    PROFILE as CRED_PROFILE, SLOT as CRED_SLOT, REVISION as CRED_REVISION,
    bridge_digest, build_cred_bridge,
)


def wic_source_digest():
    package = Path(__file__).resolve().parents[2]
    packages = package.parents[1]
    profiles = packages / "55-profiles"
    roots = [
        package / "src/tba_test_interop_wimse",
        Path(__file__).parent,
        profiles / "tba-profile-workload-proof-wimse-http-signature" / "src",
        profiles / "tba-profile-workload-proof-wimse-wpt" / "src",
    ]
    files = sorted(path for root in roots for pattern in ("*.py", "*.rs", "*.go", "*.mjs") for path in root.rglob(pattern))
    digest = sha256()
    for path in files:
        digest.update(path.relative_to(packages).as_posix().encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def qualify_wic(adapter, evidence):
    """Run both directions before qualifying the direct baseline composition."""
    peers = read_catalog("peers.toml")
    pins = {"tba": "sha256:" + wic_source_digest(), "wimsey": WIMSEY_REVISION}
    baseline_fields = ("implementation", "version", "configuration", "profile", "identifier_scheme")
    controls = []
    scenarios = generate_matrix()["scenarios"]
    for scheme in ("wimse", "spiffe"):
        control, = [case for case in scenarios if case["scenario_id"] == "01"
                    and adapter.supports(case)
                    and case["hops"]["enforcing"]["wic_issuer"] == "baseline"
                    and case["hops"]["enforcing"]["identifier_scheme"] == scheme]
        for direction in ("forward", "reverse"):
            observed = adapter.check_setup(control, {"direction": direction})
            controls.append({"direction": direction, "identifier_scheme": scheme,
                             "observation": asdict(observed)})
    qualified = {}
    for row in peers["capabilities"]:
        name = row["implementation"]
        if row["profile"] == "wic-mtls" and name in pins:
            row.update(status="qualified", version=pins[name],
                       configuration=CONFIGURATION, evidence=evidence)
            qualified[name, row["role"], row["identifier_scheme"]] = {
                field: row[field] for field in baseline_fields
            }
    peers["baselines"] = [{
        "outcome": "pass", "evidence": evidence,
        "caller": qualified[caller, "caller", control["identifier_scheme"]],
        "receiver": qualified[receiver, "receiver", control["identifier_scheme"]],
    } for control in controls
      for caller, receiver in [("tba", "wimsey") if control["direction"] == "forward"
                               else ("wimsey", "tba")]]
    peers["qualified_support"] = {"enforcing:wic_issuer:baseline": {
        "implementation": "direct-test-ca", "version": pins["tba"], "configuration": CONFIGURATION,
        "evidence": evidence, "profile": "wic-mtls", "identifier_schemes": ["wimse", "spiffe"],
    }}
    return {
        "peers": peers, "controls": controls, "wimsey_binary_sha256": adapter.binary_sha256,
        "runtime": {"python": platform.python_version(), "tls": ssl.OPENSSL_VERSION},
        "scope": "Local operator, wimsey WIC verifier composed with shared Python TLS and ledger",
    }


def qualify_support(adapter, snapshot, evidence):
    peers = snapshot["peers"]
    version = "sha256:" + wic_source_digest()
    controls = snapshot["support_controls"] = []
    matrix = generate_matrix(peers=peers)
    cases = {case["id"]: case for case in matrix["scenarios"]}
    candidates = [(cases[row["scenario_id"]], row) for row in matrix["executions"]
                  if not row["missing_baselines"] and row["pending_roles"]]

    def binding(name, *, schemes=("wimse", "spiffe"), implementation="wic-lab-fixture",
                role_version=version, configuration=CONFIGURATION, **fields):
        peers["qualified_support"][name] = {
            "implementation": implementation, "version": role_version,
            "configuration": configuration, "endpoint_configuration": CONFIGURATION,
            "evidence": evidence, "profile": "wic-mtls", "identifier_schemes": list(schemes),
            **fields,
        }

    seen_issuers = set()
    for case, execution in candidates:
        if not adapter.supports(case):
            continue
        issuer_key = tuple((name, hop["identifier_scheme"], hop["wic_issuer"])
                           for name, hop in case["hops"].items()), execution["direction"]
        if issuer_key in seen_issuers:
            continue
        seen_issuers.add(issuer_key)
        observations = adapter.check_issuers(case, execution)
        controls.append({"configuration": issuer_key,
                         "observations": {name: asdict(value) for name, value in observations.items()}})
    binding("ingress:wic_issuer:baseline", implementation="direct-test-ca")
    if adapter.issuer is not None:
        for hop in ("ingress", "enforcing"):
            binding(f"{hop}:wic_issuer:spire-x509-svid", schemes=("spiffe",),
                    implementation="spire-server", role_version=IMAGE, configuration="server-minted-x509-svid")
        snapshot["spire_image"] = IMAGE
    family_roles = {}
    for family, roles in SUPPORT_FAMILIES.items():
        if not roles:
            continue
        variants_seen = set()
        for case, execution in candidates:
            variant = case["variant"]
            if (case["scenario_id"] != family or variant in variants_seen
                    or any(hop["wic_issuer"] != "baseline" for hop in case["hops"].values())):
                continue
            with adapter.isolated(case, execution) as fixture:
                observed = fixture.observe()
            errors = mismatches(case, observed)
            if errors:
                raise ValueError(f"Support control {case['id']} failed: {errors}; {observed}")
            controls.append({"scenario": case["id"], "execution": execution["id"],
                             "roles": list(roles), "observation": asdict(observed)})
            variants_seen.add(variant)
        expected = {case["variant"] for case, _ in candidates if case["scenario_id"] == family}
        if not expected or variants_seen != expected:
            raise ValueError(f"Missing support controls for {family}: {expected - variants_seen}")
        for role in roles:
            family_roles.setdefault(role, []).append(family)
    for role, families in family_roles.items():
        binding(role, scenario_families=families)


def qualify_combined(wic, snapshot, evidence, *, profile=SIGNATURE_PROFILE, bridge=None, scheme="spiffe",
                     cofide_binary=None, cred_bridge=None):
    slot, proof, proof_name = {
        SIGNATURE_PROFILE: (SIGNATURE_SLOT, "signature", "HTTP signatures"),
        WPT_PROFILE: (WPT_SLOT, "wpt", "WPT"),
        COFIDE_PROFILE: (COFIDE_SLOT, "cofide", "HTTP signatures"),
        CRED_PROFILE: (CRED_SLOT, "cred", "WPT"),
    }[profile]
    suffix = "_wimse" if scheme == "wimse" else ""
    standalone = profile in {COFIDE_PROFILE, CRED_PROFILE}
    control_key = f"{proof}_controls" if standalone else f"combined_{proof}{suffix}_controls"
    adapter = WimseySignatureAdapter(wic.directory, wic.binary, wic.issuer, wpt_bridge=bridge,
                                    signature=profile == SIGNATURE_PROFILE or any(
                                        snapshot.get(key) for key in (
                                            "combined_signature_controls", "combined_signature_wimse_controls")),
                                    wimse_signatures=(profile == SIGNATURE_PROFILE and scheme == "wimse"
                                                      or bool(snapshot.get("combined_signature_wimse_controls"))),
                                    wimse_wpt=(profile == WPT_PROFILE and scheme == "wimse"
                                               or bool(snapshot.get("combined_wpt_wimse_controls"))),
                                    cofide_bridge=cofide_binary, cred_bridge=cred_bridge)
    peers = snapshot["peers"]
    revision = {CRED_PROFILE: CRED_REVISION, COFIDE_PROFILE: COFIDE_REVISION}.get(profile, WIMSEY_REVISION)
    pins = {"tba": "sha256:" + wic_source_digest(), slot: revision}
    fields = ("implementation", "version", "configuration", "profile", "identifier_scheme")
    peers["implementations"][slot] = {
        "name": {
            COFIDE_PROFILE: "Cofide WIMSE PoC (HTTPS request signature lab)",
            CRED_PROFILE: "Cred (HTTPS WIT/WPT lab)",
        }.get(profile, f"wimsey (combined WIC and {proof_name} in the shared lab)"),
        "candidate_ref": revision,
    }
    capabilities = {}
    for row in peers["capabilities"]:
        name = row["implementation"]
        if row["profile"] == profile and row["identifier_scheme"] == scheme and name in pins:
            row.update(status="qualified", version=pins[name], configuration=SIGNATURE_CONFIGURATION,
                       evidence=evidence)
            capabilities[name, row["role"]] = {field: row[field] for field in fields}

    controls = snapshot[control_key] = []
    scenarios = generate_matrix()["scenarios"]
    for direction, caller, receiver in (("forward", "tba", slot), ("reverse", slot, "tba")):
        pair = {"caller": capabilities[caller, "caller"], "receiver": capabilities[receiver, "receiver"]}
        for case in scenarios:
            if (case["scenario_id"] != "01" or case["hops"]["enforcing"]["profile"] != profile
                    or case["hops"]["enforcing"]["identifier_scheme"] != scheme
                    or not adapter.supports(case)):
                continue
            observed = adapter.check_setup(case, {"direction": direction, "pairs": {"enforcing": pair}})
            controls.append({"direction": direction, "case": case["id"], "pair": pair,
                             "observation": asdict(observed)})
        peers["baselines"].append(dict(pair, evidence=evidence, outcome="pass"))

    wit_svid = wic.issuer is not None and wic.issuer.alternate is not None
    issuer_levels = (2 if wit_svid else 1) * (2 if scheme == "spiffe" and wic.issuer is not None else 1)
    assert len(controls) == 2 * issuer_levels, controls
    if wit_svid:
        snapshot["spire_wit_svid"] = True
    support = peers["qualified_support"]
    def add_binding(key, implementation, version, **scope):
        new = {"implementation": implementation, "version": version, "configuration": SIGNATURE_CONFIGURATION,
               "evidence": evidence, "profile": profile, "identifier_schemes": [scheme], **scope}
        existing = support.get(key)
        support[key] = {**new, "bindings": [*existing.get("bindings", [existing]), new]} if existing else new

    for hop in ("ingress", "enforcing"):
        if not standalone:
            add_binding(f"{hop}:wic_issuer:baseline", "direct-test-ca", pins["tba"])
        add_binding(f"{hop}:wit_issuer:baseline", "lab-wit-issuer", pins["tba"])
        if wic.issuer and scheme == "spiffe":
            add_binding(f"{hop}:wic_issuer:spire-x509-svid", "spire-server", IMAGE)
        if wit_svid:
            add_binding(f"{hop}:wit_issuer:spire-wit-svid", "spire-server-wit-mint", IMAGE)

    matrix = generate_matrix(peers=peers)
    cases = {case["id"]: case for case in matrix["scenarios"]}
    families = {"08", "12", "14", "17", "18", "20"} if standalone else {"08", "12"}
    seen = set()
    for row in matrix["executions"]:
        case = cases[row["scenario_id"]]
        family = case["scenario_id"]
        if (family not in families or row["missing_baselines"]
                or not any((hop["profile"], hop["identifier_scheme"]) == (profile, scheme)
                           for hop in case["hops"].values())
                or set(row["pending_roles"]) - set(SUPPORT_FAMILIES[family])):
            continue
        key = (family, case["variant"], row["direction"], case["layer"],
               tuple((hop["profile"], hop["identifier_scheme"]) for hop in case["hops"].values()))
        if key in seen:
            continue
        if not adapter.supports(case) or not adapter.supports_execution(case, row):
            raise ValueError(f"Missing combined support adapter for {row['id']}")
        try:
            with adapter.isolated(case, row) as fixture:
                observed = fixture.observe()
        except (AssertionError, OSError, ValueError) as error:
            raise ValueError(f"Combined support control failed for {row['id']}") from error
        errors = mismatches(case, observed)
        if errors:
            raise ValueError(f"Combined support control {case['id']} failed: {errors}; {observed}")
        controls.append({"direction": row["direction"], "case": case["id"], "roles": SUPPORT_FAMILIES[family],
                         "observation": asdict(observed)})
        seen.add(key)
    expected = {(case["scenario_id"], case["variant"], direction)
                for case in scenarios if case["scenario_id"] in families
                for direction in ("forward", "reverse")}
    assert {key[:3] for key in seen} == expected, seen
    for family in sorted(families):
        for role in SUPPORT_FAMILIES[family]:
            add_binding(role, "wic-lab-fixture", pins["tba"], scenario_families=[family])


def main():
    destination = Path(os.environ["TBA_WIMSE_PEER_SNAPSHOT"]).resolve()
    with TemporaryDirectory(dir=destination.parent) as directory:
        use_spire = os.environ.get("TBA_WIMSE_SPIRE") == "1"
        use_wit = use_spire and os.environ.get("TBA_WIMSE_SPIRE_WIT") == "1"
        issuer_context = spire_wit_issuers(directory) if use_wit else spire_issuer(directory) if use_spire else nullcontext()
        with issuer_context as issuer:
            adapter = WimseyWicAdapter(directory, os.environ["TBA_WIMSEY_CHECKOUT"], issuer)
            snapshot = qualify_wic(adapter, destination.name)
            qualify_support(adapter, snapshot, destination.name)
            if os.environ.get("TBA_WIMSE_COMBINED_SIGNATURE") == "1":
                qualify_combined(adapter, snapshot, destination.name)
            bridge = None
            wpt_spiffe = os.environ.get("TBA_WIMSE_COMBINED_WPT") == "1"
            wpt_wimse = os.environ.get("TBA_WIMSE_COMBINED_WPT_WIMSE") == "1"
            if wpt_spiffe or wpt_wimse:
                bridge = build_bridge(os.environ["TBA_WIMSEY_CHECKOUT"], directory)
                if wpt_spiffe:
                    qualify_combined(adapter, snapshot, destination.name, profile=WPT_PROFILE, bridge=bridge)
                snapshot["wimsey_wpt_bridge_sha256"] = sha256(bridge.read_bytes()).hexdigest()
            if os.environ.get("TBA_WIMSE_COMBINED_SIGNATURE_WIMSE") == "1":
                qualify_combined(adapter, snapshot, destination.name, bridge=bridge, scheme="wimse")
            if wpt_wimse:
                qualify_combined(adapter, snapshot, destination.name, profile=WPT_PROFILE, bridge=bridge, scheme="wimse")
            cofide = os.environ.get("TBA_WIMSE_COFIDE_BRIDGE")
            cofide_binary = Path(cofide).resolve() if cofide else None
            if cofide_binary:
                qualify_combined(adapter, snapshot, destination.name, profile=COFIDE_PROFILE,
                                 bridge=bridge, scheme="none", cofide_binary=cofide_binary)
                snapshot["cofide_bridge_sha256"] = binary_digest(cofide_binary)
            if cred_checkout := os.environ.get("TBA_WIMSE_CRED_CHECKOUT"):
                cred_bridge = build_cred_bridge(cred_checkout, destination.with_suffix(".cred"))
                qualify_combined(adapter, snapshot, destination.name, profile=CRED_PROFILE,
                                 bridge=bridge, scheme="none", cofide_binary=cofide_binary, cred_bridge=cred_bridge)
                snapshot["cred_bridge_sha256"] = bridge_digest(cred_bridge)
    destination.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print(f"Passed controls: {len(snapshot['controls'])} baseline, {len(snapshot['support_controls'])} issuer/support")
    print(f"Combined signature controls: {len(snapshot.get('combined_signature_controls', ()))}")
    print(f"Combined WPT controls: {len(snapshot.get('combined_wpt_controls', ()))}")
    print(f"WIMSE-ID signature controls: {len(snapshot.get('combined_signature_wimse_controls', ()))}")
    print(f"WIMSE-ID WPT controls: {len(snapshot.get('combined_wpt_wimse_controls', ()))}")
    print(f"Cofide controls: {len(snapshot.get('cofide_controls', ()))}")
    print(f"Cred controls: {len(snapshot.get('cred_controls', ()))}")


if __name__ == "__main__":
    main()

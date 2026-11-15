"""Qualify and execute the SPIFFE workload peer flows with available support services."""

import argparse
from dataclasses import asdict
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

import pytest

from external_workload_selection import defakto_digest, spiffe_emilia_rows, spiffe_peer_rows, spiffe_support_rows
from run_native_wit_svid_batch import AttemptJournal
from support.go_spiffe_endpoint import PEER, REVISION, go_spiffe_hop, spiffe_peer_hop
from support.qualification_overlay import wic_source_digest
from support.spire_issuer import docker, spire_issuer
from support.spire_workload_api import SOCKET, spire_workload_api
from support.wimsey_endpoint import CONFIGURATION
from tba_test_interop_wimse.evidence import audit_pytest_report
from tba_test_interop_wimse.hop_expansion import include_candidate_endpoints
from tba_test_interop_wimse.native_expansion import expanded_plan


def qualify(snapshot, binary, linux_binary, directory):
    peers = include_candidate_endpoints(snapshot["peers"])
    snapshot["peers"] = peers
    controls = []
    names = {"caller_name": "workload-0", "receiver_name": "workload-1"}
    with spire_issuer(directory) as issuer:
        agent_dir = directory / "agent"
        agent_dir.mkdir()
        with spire_workload_api(issuer, agent_dir) as agent:
            docker("cp", linux_binary, f"{agent.container}:/tmp/go-spiffe")
            fetched = docker("exec", agent.container, "/tmp/go-spiffe", "fetch", f"unix://{SOCKET}")
            assert json.loads(fetched.stdout) == "spiffe://example.org/workload-0"
            acquired = agent.with_acquired(agent.fetch(enrolled=True))
        for kind in ("baseline", "spire-x509-svid"):
            hop = {"profile": "wic-mtls", "identifier_scheme": "spiffe", "wic_issuer": kind, "wit_issuer": "none"}
            for direction in ("forward", "reverse"):
                refusal = "wrong-anchor" if direction == "forward" else "wrong-server-identity"
                for variant in ("valid-peer", refusal):
                    case = {"scenario_id": "01", "variant": variant, "layer": "tls", "target_hop": "enforcing"}
                    with go_spiffe_hop(directory, binary, issuer, case, direction, hop, names) as fixture:
                        observed = fixture.observe()
                    expected = ("allow", 1) if variant == "valid-peer" else ("deny", 0)
                    assert (observed.decision, observed.effects) == expected, observed
                    controls.append({"issuer": kind, "direction": direction, "variant": variant,
                                     "observation": asdict(observed)})
        case = {"scenario_id": "01", "variant": "valid-peer", "layer": "tls", "target_hop": "enforcing"}
        with go_spiffe_hop(directory, binary, acquired, case, "forward", hop, names) as fixture:
            observed = fixture.observe()
            assert acquired.used and (observed.decision, observed.effects) == ("allow", 1)
        controls.append({"issuer": "spire-agent-workload-api", "direction": "forward",
                         "variant": "valid-peer", "observation": asdict(observed)})
    record_baselines(peers, PEER, REVISION, "go_spiffe_qualification")
    snapshot["go_spiffe_qualification"] = {
        "revision": REVISION, "binary_sha256": sha256(binary.read_bytes()).hexdigest(),
        "linux_binary_sha256": sha256(linux_binary.read_bytes()).hexdigest(), "controls": controls,
        "workload_api_identity": "spiffe://example.org/workload-0",
    }


def record_baselines(peers, implementation, revision, evidence):
    version = "sha256:" + wic_source_digest()
    endpoints = {}
    fields = ("implementation", "version", "configuration", "profile", "identifier_scheme")
    for row in peers["capabilities"]:
        if (row["implementation"] not in {"tba", implementation} or row["profile"] != "wic-mtls"
                or row["identifier_scheme"] != "spiffe"):
            continue
        if row["implementation"] == implementation:
            row.update(status="qualified", version=revision, configuration=CONFIGURATION, evidence=evidence)
        else:
            assert row.get("version") == version and row["configuration"] == CONFIGURATION and row["status"] == "qualified"
        endpoints[row["implementation"], row["role"]] = {key: row[key] for key in fields}
    for caller, receiver in (("tba", implementation), (implementation, "tba")):
        peers["baselines"].append({"caller": endpoints[caller, "caller"], "receiver": endpoints[receiver, "receiver"],
                                   "outcome": "pass", "evidence": evidence})


def qualify_defakto(snapshot, bridge, directory):
    lock = json.loads((bridge.parent / "package-lock.json").read_text(encoding="utf-8"))
    sdk = lock["packages"]["node_modules/@defakto/spiffe"]
    installed = json.loads((bridge.parent / "node_modules/@defakto/spiffe/package.json").read_text(encoding="utf-8"))
    assert sdk["version"] == installed["version"] == "0.7.0"
    revision = f"npm:@defakto/spiffe@{sdk['version']}"
    node = subprocess.check_output(["node", "--version"], text=True).strip()
    names = {"caller_name": "workload-0", "receiver_name": "workload-1"}
    controls = []
    with spire_issuer(directory) as issuer:
        for kind in ("baseline", "spire-x509-svid"):
            hop = {"profile": "wic-mtls", "identifier_scheme": "spiffe", "wic_issuer": kind, "wit_issuer": "none"}
            for direction in ("forward", "reverse"):
                refusal = "wrong-anchor" if direction == "forward" else "wrong-server-identity"
                for variant in ("valid-peer", refusal):
                    case = {"scenario_id": "01", "variant": variant, "layer": "tls", "target_hop": "enforcing"}
                    with spiffe_peer_hop(directory, ["node", str(bridge)], issuer, case, direction, hop, names) as fixture:
                        observed = fixture.observe()
                    assert (observed.decision, observed.effects) == (
                        ("allow", 1) if variant == "valid-peer" else ("deny", 0)
                    ), observed
                    controls.append({"issuer": kind, "direction": direction, "variant": variant,
                                     "observation": asdict(observed)})
    record_baselines(snapshot["peers"], "defakto", revision, "defakto_qualification")
    snapshot["defakto_qualification"] = {
        "revision": revision, "npm_integrity": sdk["integrity"], "node": node,
        "bridge_sha256": defakto_digest(bridge), "controls": controls,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--linux-binary", type=Path, required=True)
    parser.add_argument("--defakto-bridge", type=Path)
    support = parser.add_mutually_exclusive_group()
    support.add_argument("--emilia-bridge", type=Path)
    support.add_argument("--teleport-container")
    support.add_argument("--mintid-container")
    parser.add_argument("--manifest", type=Path,
                        help="Frozen expanded manifest used to reconcile external support executions")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    isolated_support = args.teleport_container or args.mintid_container
    if (args.emilia_bridge or isolated_support) and not args.defakto_bridge:
        parser.error("external support mode requires --defakto-bridge to qualify both SPIFFE peers")
    if isolated_support and not args.manifest:
        parser.error("isolated external support mode requires --manifest")
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    args.output.mkdir(parents=True, exist_ok=False)
    with TemporaryDirectory(dir=args.output) as directory:
        if isolated_support:
            # A new fixture digest requires fresh directional controls for these endpoints.
            current_pin = "sha256:" + wic_source_digest()
            for row in snapshot["peers"]["capabilities"]:
                if (row["implementation"], row["profile"], row["identifier_scheme"]) == ("tba", "wic-mtls", "spiffe"):
                    row["version"] = current_pin
        qualify(snapshot, args.binary.resolve(), args.linux_binary.resolve(), Path(directory))
        if args.defakto_bridge:
            qualify_defakto(snapshot, args.defakto_bridge.resolve(), Path(directory))
        if args.teleport_container:
            from support.teleport_endpoint import ISSUER, TeleportWorkloadAPI, fingerprint

            agent = TeleportWorkloadAPI(args.teleport_container, directory)
            credential = agent.fetch(enrolled=True)
            if agent.fetch(enrolled=False) is not None:
                raise ValueError("Teleport authorized the unregistered workload")
            snapshot["teleport_qualification"] = {
                "image": agent.image(), "identity": "spiffe://example.org/workload-0",
                "control_certificate_sha256": fingerprint(credential), "unregistered_uid_refused": True,
            }
            snapshot["peers"]["qualified_support"][f"enforcing:wic_issuer:{ISSUER}"] = {
                "implementation": "teleport-tbot", "version": agent.image(), "configuration": CONFIGURATION,
                "profile": "wic-mtls", "identifier_schemes": ["spiffe"],
                "evidence": "teleport_qualification",
            }
        if args.mintid_container:
            from mintid_endpoint import BRIDGE, RUNTIME_BRIDGE

            bridge_sha = sha256(BRIDGE.read_bytes()).hexdigest()
            actual = docker("exec", args.mintid_container, "sha256sum", RUNTIME_BRIDGE).stdout.split()[0]
            if actual != bridge_sha:
                raise ValueError("MintID bridge differs from the local test source")
            snapshot["mintid_qualification"] = {
                "bridge_sha256": bridge_sha,
                "driver_image": docker("inspect", "--format", "{{.Image}}", args.mintid_container).stdout.strip(),
            }
    if args.emilia_bridge:
        from support.emilia_endpoint import bridge_digest, gate_decision

        bridge = args.emilia_bridge.resolve()
        snapshot["emilia_qualification"] = {
            "version": "@emilia-protocol/gate@0.30.0", "bridge_sha256": bridge_digest(bridge),
            "controls": [gate_decision(bridge, "qualification", revoke=revoke) for revoke in (False, True)],
        }
    runtime = (args.output / "qualification.json").resolve()
    runtime.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    if not isolated_support:
        shutil.copytree(args.snapshot.with_suffix(".cred"), runtime.with_suffix(".cred"))
    plan = expanded_plan(snapshot["peers"], include_candidates=True, include_executions=True)
    if isolated_support:
        if args.teleport_container:
            mode, support_peer, total = "teleport", "teleport-tbot", 32
            os.environ["TBA_WIMSE_TELEPORT_CONTAINER"] = args.teleport_container
        else:
            mode, support_peer, total = "mintid", "mintid", 76
            os.environ["TBA_WIMSE_MINTID_CONTAINER"] = args.mintid_container
        label = f"SPIFFE workloads with {support_peer}"
        workload, typed, expected = [], spiffe_support_rows(plan, support_peer), (0, total)
        from expanded_blockers import case_key

        with gzip.open(args.manifest, "rt", encoding="utf-8") as stream:
            published = {case_key(row): row["id"] for row in spiffe_support_rows(json.load(stream), support_peer)}
        if len(published) != expected[1] or {case_key(row) for row in typed} != published.keys():
            raise ValueError(f"{support_peer} runtime cases differ from the frozen inventory")
        (args.output / "published-ids.json").write_text(
            json.dumps({row["id"]: published[case_key(row)] for row in typed}, indent=2), encoding="utf-8",
        )
    elif args.emilia_bridge:
        workload, typed, expected = [], spiffe_emilia_rows(plan), (0, 64)
        mode, label = "emilia", "SPIFFE workloads with EMILIA"
        os.environ["TBA_WIMSE_EMILIA_BRIDGE"] = str(args.emilia_bridge.resolve())
    elif args.defakto_bridge:
        workload, typed = spiffe_peer_rows(plan, defakto=True)
        expected, mode, label = (1072, 4700), "defakto", "Defakto and mixed SPIFFE"
    else:
        workload, typed = spiffe_peer_rows(plan)
        expected, mode, label = (952, 4412), "1", "go-spiffe"
    if (len(workload), len(typed)) != expected:
        raise ValueError(f"Unexpected SPIFFE workload inventory: {len(workload)} workload, {len(typed)} typed")
    ids = {row["id"] for row in workload + typed}
    (args.output / "selection.json").write_text(json.dumps(sorted(ids)), encoding="utf-8")
    os.environ.update(TBA_WIMSE_PEER_SNAPSHOT=str(runtime), TBA_WIMSE_EXPANDED="1",
                      TBA_WIMSE_GO_SPIFFE_ONLY=mode,
                      TBA_WIMSE_GO_SPIFFE_BRIDGE=str(args.binary.resolve()))
    if args.defakto_bridge:
        os.environ["TBA_WIMSE_DEFAKTO_BRIDGE"] = str(args.defakto_bridge.resolve())
    for variable in ("TBA_WIMSE_EXECUTION_ID", "TBA_WIMSE_HOP_PATH", "TBA_WIMSE_INCLUDE_NATIVE",
                     "TBA_WIMSE_TYPED_SERVICE", "TBA_WIMSE_NATIVE_BASELINE_POLICY", "TBA_WIMSE_NATIVE_ACQUISITION"):
        os.environ.pop(variable, None)
    target = Path(__file__).parent / "peer/test_candidate_executions.py"
    report = args.output / "results.xml"
    with (args.output / "attempts.jsonl").open("x", encoding="utf-8") as stream:
        tracker = AttemptJournal(stream, ids, label)
        options = ["-o", "addopts=", "-o", "junit_family=xunit1", "-p", "no:cacheprovider",
                   "-qq", "--junitxml", str(report), "--basetemp", str(args.output / "pytest-runtime"), str(target)]
        if args.workers > 1:
            options.extend(("-n", str(args.workers)))
        print(f"Running {len(ids)} {label} cases", flush=True)
        code = pytest.main(options, plugins=[tracker])
    audit = audit_pytest_report(workload + typed, report)
    summary = {key: value for key, value in audit.items() if key != "results"}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary), flush=True)
    return code or int(not audit["complete"])


if __name__ == "__main__":
    raise SystemExit(main())

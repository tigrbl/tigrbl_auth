"""Qualify one native SVID issuer and run its workload cases."""

import argparse
from collections import Counter
import json
import os
from pathlib import Path
from xml.etree import ElementTree

import pytest

from support.qualification_overlay import wic_source_digest
from tba_test_interop_wimse.evidence import audit_pytest_report
from tba_test_interop_wimse.native_expansion import (
    COMBINED_RECORD, COMBINED_SCOPE, NATIVE_ISSUERS, expanded_plan, native_issuer_rows,
)


SCOPE = {"tba-wit-svid": (6, 16710), "tba-x509-svid": (3, 6261), COMBINED_SCOPE: (2, 23878)}


class AttemptJournal:
    def __init__(self, stream, selected, label="Native SVID"):
        self.stream, self.selected = stream, selected
        self.seen = set()
        self.counts = Counter()
        self.label = label

    def pytest_runtest_logreport(self, report):
        if report.when != "call":
            return
        value = dict(report.user_properties).get("execution_result")
        if value is None:
            return
        result = json.loads(value)
        identifier = result["execution_id"]
        if identifier not in self.selected or identifier in self.seen:
            raise ValueError(f"Unexpected runtime result for {identifier}")
        self.seen.add(identifier)
        self.stream.write(value + "\n")
        self.stream.flush()
        self.counts[result["status"]] += 1
        if len(self.seen) % 250 == 0 or len(self.seen) == 1:
            print(f"{self.label} {len(self.seen)}/{len(self.selected)} {dict(self.counts)}", flush=True)


def qualify(snapshot, controls, issuer):
    profiles = Counter()
    for item in ElementTree.parse(controls).iter("testcase"):
        if any(item.find(name) is not None for name in ("failure", "error", "skipped")):
            raise ValueError(f"{issuer} controls did not pass")
        properties = {prop.get("name"): prop.get("value") for prop in item.findall("./properties/property")}
        if properties["issuer"] != issuer:
            raise ValueError("Unexpected control issuer")
        profiles[properties["profile"], properties["identifier_scheme"], properties["decision"], properties["effects"]] += 1
    combinations = {(profile, scheme) for profile, scheme, _, _ in profiles}
    expected_profiles, _ = SCOPE[issuer]
    if len(combinations) != expected_profiles or any(
        profiles[profile, scheme, "allow", "1"] != 1 or profiles[profile, scheme, "deny", "0"] != 2
        for profile, scheme in combinations
    ) or sum(profiles.values()) != 3 * expected_profiles:
        raise ValueError(f"Expected one acceptance and two refusals for each of {expected_profiles} profiles")
    version = "sha256:" + wic_source_digest()
    peers = snapshot["peers"]
    caps = {(r["profile"], r["identifier_scheme"], r["role"]) for r in peers["capabilities"]
            if r["implementation"] == "tba" and r["status"] == "qualified" and r.get("version") == version}
    if any((profile, scheme, role) not in caps for profile, scheme in combinations for role in ("caller", "receiver")):
        raise ValueError("Control profiles do not match the fresh endpoint snapshot")
    record = COMBINED_RECORD if issuer == COMBINED_SCOPE else NATIVE_ISSUERS[issuer][1]
    peers[record] = {"version": version, "profiles": sorted(combinations), "evidence": str(controls)}


def select(plan, issuer):
    workloads, typed = native_issuer_rows(plan, issuer)
    _, expected = SCOPE[issuer]
    if len(workloads) + len(typed) != expected:
        raise ValueError(f"{issuer} selection differs from the agreed manifest")
    if any(row["status"] != "qualified" for row in workloads):
        pending = [row for row in workloads if row["status"] != "qualified"]
        raise ValueError(f"{len(pending)} short cases have pending qualifications: {pending[0]['pending_roles']}")
    return workloads + typed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--controls", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--issuer", choices=SCOPE, default="tba-wit-svid")
    parser.add_argument("--wit-controls", type=Path, help="WIT-SVID component controls for combined qualification")
    parser.add_argument("--x509-controls", type=Path, help="X.509-SVID component controls for combined qualification")
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    if args.issuer == COMBINED_SCOPE:
        if not args.wit_controls or not args.x509_controls:
            parser.error("Combined qualification requires --wit-controls and --x509-controls")
        qualify(snapshot, args.wit_controls, "tba-wit-svid")
        qualify(snapshot, args.x509_controls, "tba-x509-svid")
    qualify(snapshot, args.controls, args.issuer)
    selected = select(expanded_plan(snapshot["peers"], include_candidates=True,
                                    include_native=True, include_executions=True), args.issuer)
    args.output.mkdir(parents=True, exist_ok=False)
    runtime = (args.output / "qualification.json").resolve()
    runtime.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    ids = {row["id"] for row in selected}
    (args.output / "selection.json").write_text(json.dumps(sorted(ids)), encoding="utf-8")
    os.environ.update(TBA_WIMSE_PEER_SNAPSHOT=str(runtime), TBA_WIMSE_EXPANDED="1",
                      TBA_WIMSE_INCLUDE_NATIVE="1", TBA_WIMSE_NATIVE_ISSUER=args.issuer)
    for variable in ("TBA_WIMSE_EXECUTION_ID", "TBA_WIMSE_HOP_PATH"):
        os.environ.pop(variable, None)
    target = Path(__file__).parent / "peer/test_candidate_executions.py"
    results = args.output / "results.xml"
    with (args.output / "attempts.jsonl").open("x", encoding="utf-8") as stream:
        tracker = AttemptJournal(stream, ids)
        options = ["-o", "addopts=", "-o", "junit_family=xunit1", "-p", "no:cacheprovider",
                   "-qq", "--junitxml", str(results),
                   "--basetemp", str(args.output / "pytest-runtime"), str(target)]
        if args.workers > 1:
            options.extend(("-n", str(args.workers)))
        print(f"Running {len(ids)} {args.issuer} IDs", flush=True)
        code = pytest.main(options, plugins=[tracker])
    audit = audit_pytest_report(selected, results)
    summary = {key: val for key, val in audit.items() if key != "results"}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary), flush=True)
    return code or int(not audit["complete"])


if __name__ == "__main__":
    raise SystemExit(main())

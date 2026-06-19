from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.artifacts import deployment_from_options
from tigrbl_auth.cli.reports import (
    build_release_bundle,
    run_final_release_readiness_gate,
    sign_release_bundle,
    verify_release_bundle_signatures,
)
from tigrbl_auth.cli.truth import materialize_truth_chain
from tigrbl_identity_author.release_signing import load_signer

PROFILES = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")


def _run(script_name: str, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("TIGRBL_AUTH_RUNTIME_REPORT_MODE", "validated-runs")
    env.setdefault("TIGRBL_AUTH_SKIP_EXECUTION_PROBES", "1")
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script_name)],
        check=check,
        text=True,
        capture_output=True,
        env=env,
    )


def _emit(completed: subprocess.CompletedProcess[str]) -> None:
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, end="")


def _load(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _current_version() -> str:
    for line in (ROOT / "pyproject.toml").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0"


def main() -> int:
    for script in [
        "generate_openapi_contract.py",
        "generate_openrpc_contract.py",
        "generate_discovery_snapshots.py",
        "generate_cli_docs.py",
        "materialize_tier3_evidence.py",
        "generate_state_reports.py",
        "generate_release_decision_record.py",
        "generate_package_review_gap_analysis.py",
    ]:
        _emit(_run(script, check=True))

    _emit(_run("run_release_gates.py", check=False))

    signer = load_signer(
        signing_key=os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY"),
        signer_id=os.environ.get("TIGRBL_AUTH_RELEASE_SIGNER_ID"),
    )
    shared_key = signer.private_key_pem()
    version = _current_version()

    for profile in PROFILES:
        deployment = deployment_from_options(profile=profile)
        build_release_bundle(ROOT, deployment)
    for profile in PROFILES:
        deployment = deployment_from_options(profile=profile)
        bundle_dir = ROOT / "dist" / "release-bundles" / version / deployment.profile
        sign_release_bundle(bundle_dir, signing_key=shared_key, signer_id=signer.identity.signer_id)
        verify_release_bundle_signatures(bundle_dir)

    run_final_release_readiness_gate(ROOT)
    materialize_truth_chain(ROOT)
    final_status = _load(ROOT / "docs" / "compliance" / "FINAL_RELEASE_STATUS_2026-03-25.json")

    for profile in PROFILES:
        deployment = deployment_from_options(profile=profile)
        build_release_bundle(ROOT, deployment)
    for profile in PROFILES:
        deployment = deployment_from_options(profile=profile)
        bundle_dir = ROOT / "dist" / "release-bundles" / version / deployment.profile
        sign_release_bundle(bundle_dir, signing_key=shared_key, signer_id=signer.identity.signer_id)
        verify_release_bundle_signatures(bundle_dir)

    release_set = {
        "schema_version": 1,
        "passed": bool(final_status.get("passed", False)),
        "summary": {
            "version": version,
            "profile_count": len(PROFILES),
            "signed_release_bundle_count": len(PROFILES),
            "ready_for_certification_release": bool(final_status.get("passed", False)),
            "final_release_gate_passed": bool(final_status.get("summary", {}).get("final_release_gate_passed", False)),
        },
        "profiles": [],
    }
    for profile in PROFILES:
        bundle_dir = ROOT / "dist" / "release-bundles" / version / profile
        verified = verify_release_bundle_signatures(bundle_dir)
        release_set["profiles"].append(
            {
                "profile": profile,
                "bundle_dir": str(bundle_dir.relative_to(ROOT)),
                "bundle_exists": bundle_dir.exists(),
                "attestations_verified": bool(verified.get("passed", False)),
            }
        )
    release_root = ROOT / "dist" / "release-bundles" / version
    release_root.mkdir(parents=True, exist_ok=True)
    (release_root / "release-set-status.json").write_text(json.dumps(release_set, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# Release Set Status - {version}",
        "",
        f"- Passed: `{release_set['passed']}`",
        "",
        "## Summary",
        "",
    ]
    lines.extend(f"- {key}: `{value}`" for key, value in release_set["summary"].items())
    lines.extend(["", "## Profiles", ""])
    for entry in release_set["profiles"]:
        lines.append(
            f"- {entry['profile']}: bundle_exists=`{entry['bundle_exists']}`, attestations_verified=`{entry['attestations_verified']}` ({entry['bundle_dir']})"
        )
    lines.append("")
    (release_root / "release-set-status.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(final_status, indent=2))
    return 0 if final_status.get("passed", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.artifacts import deployment_from_options
from tigrbl_auth.cli.reports import verify_release_bundle_signatures


PROFILES = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")


def _version(repo_root: Path) -> str:
    pyproject = repo_root / "pyproject.toml"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0"


def main() -> int:
    version = _version(ROOT)
    details = []
    failures = []
    for profile in PROFILES:
        deployment = deployment_from_options(profile=profile)
        bundle_dir = ROOT / "dist" / "release-bundles" / version / deployment.profile
        if not bundle_dir.exists():
            failures.append(f"Missing signed bundle directory: {bundle_dir.relative_to(ROOT)}")
            continue
        payload = verify_release_bundle_signatures(bundle_dir)
        details.append({
            "profile": profile,
            "bundle_dir": str(bundle_dir.relative_to(ROOT)),
            **payload,
        })
        if not payload.get("passed", False):
            failures.append(f"Release signing verification failed for profile: {profile}")
    summary = {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "profile_count": len(PROFILES),
            "verified_profile_count": len(details),
        },
        "details": details,
    }
    report_dir = ROOT / "docs" / "compliance"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "release_signing_report.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = ["# Release Signing Report", "", f"- Passed: `{summary['passed']}`", "", "## Summary", ""]
    for key, value in summary["summary"].items():
        lines.append(f"- {key}: `{value}`")
    if failures:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {item}" for item in failures)
    (report_dir / "release_signing_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

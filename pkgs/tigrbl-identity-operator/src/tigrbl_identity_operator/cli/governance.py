
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_DIRS = [
    "docs/adr",
    "compliance/targets",
    "compliance/mappings",
    "compliance/claims",
    "compliance/evidence",
    "compliance/gates",
    "compliance/waivers",
]

REQUIRED_FILES = [
    "docs/architecture/README.md",
    "docs/architecture/FEATURE_FLAGS_AND_SURFACES.md",
    "docs/architecture/BOUNDARY_AND_MODULARITY_PLAN.md",
    "docs/adr/ADR-0015-feature-flags-and-profile-gating.md",
    "docs/adr/ADR-0016-installable-surfaces-and-partial-feature-consumption.md",
    "docs/adr/ADR-0017-plane-modularity.md",
    "compliance/targets/target-buckets.yaml",
    "compliance/targets/public-operator-surface.yaml",
    "compliance/targets/modularity-planes.yaml",
    "compliance/mappings/feature-flag-to-target.yaml",
    "compliance/mappings/flag-to-feature.yaml",
    "compliance/mappings/feature-to-test.yaml",
    "compliance/mappings/feature-to-evidence.yaml",
    "compliance/mappings/surface-to-module.yaml",
    "compliance/mappings/plane-to-module.yaml",
    "tigrbl_auth/config/feature_flags.py",
    "tigrbl_auth/config/surfaces.py",
    "docs/adr/README.md",
    "docs/adr/ADR-0003-tigrbl-native-shape.md",
    "docs/adr/ADR-0006-release-gates-as-code.md",
    "docs/adr/ADR-0008-evidence-retention-and-peer-claims.md",
    "docs/adr/ADR-0009-package-boundary-strict-core.md",
    "docs/adr/ADR-0010-standards-boundary-and-label-hygiene.md",
    "docs/adr/ADR-0011-evidence-model-and-tier-promotion.md",
    "docs/adr/ADR-0012-independent-peer-claims.md",
    "docs/adr/ADR-0013-vendor-removal-and-no-private-shims.md",
    "compliance/README.md",
    "compliance/targets/README.md",
    "compliance/targets/boundaries.yaml",
    "compliance/targets/profiles.yaml",
    "compliance/targets/rfc-targets.yaml",
    "compliance/targets/oidc-targets.yaml",
    "compliance/targets/openapi-targets.yaml",
    "compliance/targets/openrpc-targets.yaml",
    "compliance/targets/extension-targets.yaml",
    "compliance/targets/alignment-targets.yaml",
    "compliance/targets/legacy-label-corrections.yaml",
    "compliance/mappings/README.md",
    "compliance/mappings/feature-to-target.yaml",
    "compliance/mappings/target-to-adr.yaml",
    "compliance/mappings/target-to-endpoint.yaml",
    "compliance/mappings/target-to-test.yaml",
    "compliance/mappings/target-to-evidence.yaml",
    "compliance/mappings/target-to-module.yaml",
    "compliance/mappings/target-to-gate.yaml",
    "compliance/mappings/module-to-boundary.yaml",
    "compliance/claims/README.md",
    "compliance/claims/repository-state.yaml",
    "compliance/claims/declared-target-claims.yaml",
    "compliance/claims/feature-registry.yaml",
    "compliance/claims/claim-registry.yaml",
    "compliance/claims/issue-registry.yaml",
    "compliance/claims/risk-registry.yaml",
    "compliance/claims/claim-tiers.yaml",
    "compliance/claims/promotion-policy.yaml",
    "compliance/evidence/README.md",
    "compliance/evidence/manifest.yaml",
    "compliance/evidence/retention-policy.yaml",
    "compliance/evidence/tier3/README.md",
    "compliance/evidence/tier4/README.md",
    "compliance/evidence/schemas/bundle.schema.yaml",
    "compliance/gates/README.md",
    "compliance/gates/gate-00-structure.yaml",
    "compliance/gates/gate-05-governance.yaml",
    "compliance/gates/gate-10-static.yaml",
    "compliance/gates/gate-20-tests.yaml",
    "compliance/gates/gate-30-contracts.yaml",
    "compliance/gates/gate-40-evidence.yaml",
    "compliance/gates/gate-90-release.yaml",
    "compliance/waivers/README.md",
    "compliance/waivers/register.yaml",
    "compliance/waivers/template.yaml",
    "CURRENT_STATE.md",
    "CERTIFICATION_STATUS.md",
]

REQUIRED_ADR_COVERAGE = {
    "package-boundary": "docs/adr/ADR-0009-package-boundary-strict-core.md",
    "standards-scope": "docs/adr/ADR-0010-standards-boundary-and-label-hygiene.md",
    "tigrbl-native-shape": "docs/adr/ADR-0003-tigrbl-native-shape.md",
    "vendor-removal": "docs/adr/ADR-0013-vendor-removal-and-no-private-shims.md",
    "release-gates": "docs/adr/ADR-0006-release-gates-as-code.md",
    "evidence-retention": "docs/adr/ADR-0008-evidence-retention-and-peer-claims.md",
}

def run_governance_install_check(repo_root: Path, *, strict: bool = True, report_dir: Path | None = None) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)

    missing_dirs: list[str] = []
    missing_files: list[str] = []
    missing_adr_coverage: dict[str, str] = {}

    for rel in REQUIRED_DIRS:
        if not (repo_root / rel).is_dir():
            missing_dirs.append(rel)

    for rel in REQUIRED_FILES:
        if not (repo_root / rel).exists():
            missing_files.append(rel)

    for concern, rel in REQUIRED_ADR_COVERAGE.items():
        if not (repo_root / rel).exists():
            missing_adr_coverage[concern] = rel

    failures: list[str] = []
    if missing_dirs:
        failures.append("Missing required governance directories.")
    if missing_files:
        failures.append("Missing required governance files.")
    if missing_adr_coverage:
        failures.append("Missing required ADR coverage.")

    report: dict[str, Any] = {
        "scope": "governance-install",
        "strict": strict,
        "passed": not failures,
        "summary": {
            "required_directory_count": len(REQUIRED_DIRS),
            "required_file_count": len(REQUIRED_FILES),
            "missing_directory_count": len(missing_dirs),
            "missing_file_count": len(missing_files),
            "missing_adr_coverage_count": len(missing_adr_coverage),
        },
        "missing": {
            "directories": missing_dirs,
            "files": missing_files,
            "adr_coverage": missing_adr_coverage,
        },
    }

    json_path = report_dir / "governance_install_report.json"
    md_path = report_dir / "governance_install_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Governance Install Report",
        "",
        f"- Scope: `{report['scope']}`",
        f"- Strict: `{strict}`",
        f"- Passed: `{report['passed']}`",
        f"- Required directories: `{report['summary']['required_directory_count']}`",
        f"- Required files: `{report['summary']['required_file_count']}`",
        "",
    ]
    if missing_dirs:
        lines.extend(["## Missing directories", ""])
        lines.extend([f"- `{item}`" for item in missing_dirs])
        lines.append("")
    if missing_files:
        lines.extend(["## Missing files", ""])
        lines.extend([f"- `{item}`" for item in missing_files])
        lines.append("")
    if missing_adr_coverage:
        lines.extend(["## Missing ADR coverage", ""])
        lines.extend([f"- `{concern}` → `{path}`" for concern, path in sorted(missing_adr_coverage.items())])
        lines.append("")
    if not failures:
        lines.extend([
            "## Result",
            "",
            "Governance directories, required manifests, and the bootstrap ADR set are present.",
            "",
        ])

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return 1 if failures and strict else 0

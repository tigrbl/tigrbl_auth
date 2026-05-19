from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from tigrbl_auth.cli.metadata import COMMAND_SPECS

REQUIRED_TARGET_BUCKETS = {
    "baseline": {
        "RFC 6749",
        "RFC 6750",
        "RFC 7636",
        "RFC 8414",
        "RFC 8615",
        "RFC 7515",
        "RFC 7516",
        "RFC 7517",
        "RFC 7518",
        "RFC 7519",
        "OIDC Core 1.0",
        "OIDC Discovery 1.0",
    },
    "production": {
        "RFC 7009",
        "RFC 7662",
        "RFC 7591",
        "RFC 7592",
        "RFC 8252",
        "RFC 9068",
        "RFC 9207",
        "RFC 6265",
        "OIDC UserInfo",
        "OIDC Session Management",
        "OIDC RP-Initiated Logout",
        "RFC 9728",
    },
    "hardening": {
        "RFC 8628",
        "RFC 8693",
        "RFC 8707",
        "RFC 9101",
        "RFC 9126",
        "RFC 9396",
        "RFC 9449",
        "RFC 8705",
        "OIDC Front-Channel Logout",
        "OIDC Back-Channel Logout",
        "RFC 9700",
    },
    "alignment_only": {"OAuth 2.1 alignment profile"},
}
REQUIRED_PLANES = {"api", "tables", "ops", "services", "standards", "security", "config", "adapters", "cli", "plugin", "gateway"}
REQUIRED_SURFACES = {"public_auth_plane", "admin_control_plane", "operator_plane", "rpc_control_plane", "diagnostics_plane", "plugin_plane"}
REQUIRED_SCOPE = {"evidence", "claims", "tenant", "client", "identity", "flow", "session", "token", "keys", "discovery", "import", "export"}


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def run_feature_surface_modularity_check(
    repo_root: Path,
    *,
    strict: bool = True,
    report_dir: Path | None = None,
) -> int:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    warnings: list[str] = []

    required_files = [
        repo_root / "compliance" / "targets" / "target-buckets.yaml",
        repo_root / "compliance" / "targets" / "public-operator-surface.yaml",
        repo_root / "compliance" / "targets" / "modularity-planes.yaml",
        repo_root / "compliance" / "mappings" / "feature-flag-to-target.yaml",
        repo_root / "compliance" / "mappings" / "surface-to-module.yaml",
        repo_root / "compliance" / "mappings" / "plane-to-module.yaml",
        repo_root / "docs" / "architecture" / "FEATURE_FLAGS_AND_SURFACES.md",
        repo_root / "docs" / "architecture" / "BOUNDARY_AND_MODULARITY_PLAN.md",
        repo_root / "compliance" / "targets" / "partial-feature-consumption.yaml",
        repo_root / "tigrbl_auth" / "config" / "feature_flags.py",
        repo_root / "tigrbl_auth" / "config" / "surfaces.py",
        repo_root / "tigrbl_auth" / "config" / "deployment.py",
        repo_root / "tigrbl_auth" / "cli" / "metadata.py",
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"Missing required feature/surface/modularity artifact: {path.relative_to(repo_root)}")

    if not failures:
        buckets = _load_yaml(repo_root / "compliance" / "targets" / "target-buckets.yaml")
        surfaces = _load_yaml(repo_root / "compliance" / "targets" / "public-operator-surface.yaml")
        planes = _load_yaml(repo_root / "compliance" / "targets" / "modularity-planes.yaml")

        actual_buckets = buckets.get("buckets", {})
        for bucket_name, required_labels in REQUIRED_TARGET_BUCKETS.items():
            present_labels = set(actual_buckets.get(bucket_name, {}).get("labels", []))
            missing_labels = required_labels - present_labels
            if missing_labels:
                failures.append(f"Bucket {bucket_name} missing labels: {', '.join(sorted(missing_labels))}")

        actual_surfaces = set(surfaces.get("surfaces", {}).keys())
        missing_surfaces = REQUIRED_SURFACES - actual_surfaces
        if missing_surfaces:
            failures.append(f"Missing required public/operator surfaces: {', '.join(sorted(missing_surfaces))}")

        actual_planes = set(planes.get("planes", {}).keys())
        missing_planes = REQUIRED_PLANES - actual_planes
        if missing_planes:
            failures.append(f"Missing required modularity planes: {', '.join(sorted(missing_planes))}")

    command_names = {spec.name for spec in COMMAND_SPECS}
    command_names.update(alias for spec in COMMAND_SPECS for alias in spec.aliases)
    missing_commands = REQUIRED_SCOPE - command_names
    if missing_commands:
        failures.append(f"CLI surface missing expected command tokens: {', '.join(sorted(missing_commands))}")

    openapi_path = repo_root / "specs" / "openapi" / "tigrbl_auth.public.openapi.json"
    openrpc_path = repo_root / "specs" / "openrpc" / "tigrbl_auth.admin.openrpc.json"
    if not openapi_path.exists():
        failures.append("OpenAPI contract missing")
    if not openrpc_path.exists():
        failures.append("OpenRPC contract missing")

    report = {
        "scope": "feature-flags-targets-public-surface-modularity",
        "strict": strict,
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
    }
    (report_dir / "feature_flags_surface_modularity_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Feature Flags, Targets, Surface, and Modularity Report",
        "",
        f"- Scope: `{report['scope']}`",
        f"- Strict: `{strict}`",
        f"- Passed: `{report['passed']}`",
        "",
    ]
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend([f"- {failure}" for failure in failures])
        lines.append("")
    else:
        lines.extend([
            "## Result",
            "",
            "The flag registry, target buckets, public operator surface, modularity planes, and metadata-driven CLI surface are installed and mapped.",
            "",
        ])
    (report_dir / "feature_flags_surface_modularity_report.md").write_text("\n".join(lines), encoding="utf-8")
    return 1 if failures and strict else 0

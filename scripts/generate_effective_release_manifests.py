from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json

import yaml

from tigrbl_auth.cli.artifacts import (
    deployment_from_options,
    write_discovery_artifacts,
    write_effective_claims_manifest,
    write_effective_evidence_manifest,
    write_openapi_contract,
    write_openrpc_contract,
)
from tigrbl_auth.cli.metadata import (
    build_cli_conformance_snapshot,
    build_cli_contract_manifest,
    render_cli_conformance_markdown,
    render_cli_markdown,
)
from tigrbl_identity_contracts.protocol_configuration import bind_protocol_settings
from tigrbl_identity_runtime.settings import settings


def _write_cli_artifacts(repo_root: Path) -> None:
    reference_target = repo_root / "docs" / "reference" / "CLI_SURFACE.md"
    reference_target.parent.mkdir(parents=True, exist_ok=True)
    reference_target.write_text(render_cli_markdown(), encoding="utf-8")

    contract = build_cli_contract_manifest()
    spec_root = repo_root / "specs" / "cli"
    spec_root.mkdir(parents=True, exist_ok=True)
    (spec_root / "cli_contract.json").write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (spec_root / "cli_contract.yaml").write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")

    snapshot = build_cli_conformance_snapshot()
    compliance_root = repo_root / "docs" / "compliance"
    compliance_root.mkdir(parents=True, exist_ok=True)
    (compliance_root / "cli_conformance_snapshot.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (compliance_root / "cli_conformance_snapshot.md").write_text(render_cli_conformance_markdown(snapshot), encoding="utf-8")


def _write_discovery_reference(repo_root: Path) -> None:
    lines = [
        "# Discovery Profile Snapshots",
        "",
        "The following profile-specific discovery snapshots are committed from executable deployment metadata:",
        "",
    ]
    for profile_name in ("baseline", "production", "hardening", "fapi2-security", "peer-claim"):
        lines.append(f"- `{profile_name}`")
        profile_dir = repo_root / "specs" / "discovery" / "profiles" / profile_name
        for name in sorted(path.name for path in profile_dir.glob("*.json")):
            lines.append(f"  - `specs/discovery/profiles/{profile_name}/{name}`")
    lines.extend([
        "",
        "## Notes",
        "",
        "- snapshot files are generated from `tigrbl_auth.cli.artifacts.write_discovery_artifacts` using executable deployment metadata",
        "- JWKS snapshots intentionally omit live signing material and record only a deterministic public-artifact shape",
        "- current authoritative CLI/runtime/discovery docs are those listed in `docs/reference/README.md`",
        "",
    ])
    (repo_root / "docs" / "reference" / "DISCOVERY_PROFILE_SNAPSHOTS.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    bind_protocol_settings(settings)
    repo_root = ROOT
    _write_cli_artifacts(repo_root)
    active = deployment_from_options()
    write_openapi_contract(repo_root, active)
    write_openrpc_contract(repo_root, active)
    write_effective_claims_manifest(repo_root, active)
    write_effective_evidence_manifest(repo_root, active)
    for profile_name in ("baseline", "production", "hardening", "fapi2-security", "peer-claim"):
        deployment = deployment_from_options(profile=profile_name)
        write_openapi_contract(repo_root, deployment, profile_label=profile_name)
        write_openrpc_contract(repo_root, deployment, profile_label=profile_name)
        write_discovery_artifacts(repo_root, deployment, profile_label=profile_name)
        write_effective_claims_manifest(repo_root, deployment, profile_label=profile_name)
        write_effective_evidence_manifest(repo_root, deployment, profile_label=profile_name)
    _write_discovery_reference(repo_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

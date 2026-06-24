from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tigrbl_auth.cli.artifacts import deployment_from_options, write_effective_claims_manifest, write_effective_evidence_manifest
from tigrbl_auth.cli.reports import build_evidence_bundle, generate_state_reports, run_release_gates, summarize_evidence_status
from tigrbl_auth.cli.truth import materialize_truth_chain
from scripts.generate_certification_scope import build_scope, write_boundary_docs, write_yaml as write_scope_yaml

PROMOTED_BASELINE_TARGETS = [
    "RFC 6749",
    "RFC 6750",
    "RFC 7636",
    "RFC 8414",
    "RFC 8615",
    "RFC 7515",
    "RFC 7517",
    "RFC 7518",
    "RFC 7519",
    "OIDC Core 1.0",
    "OIDC Discovery 1.0",
    "OpenAPI 3.1 / 3.2 compatible public contract",
]

PROMOTED_PRODUCTION_TARGETS = [
    "RFC 7009",
    "RFC 7591",
    "RFC 7662",
    "RFC 9068",
    "RFC 6265",
    "RFC 9728",
    "OIDC UserInfo",
    "OpenRPC 1.4.x admin/control-plane contract",
]

PROMOTED_TARGETS = set(PROMOTED_BASELINE_TARGETS + PROMOTED_PRODUCTION_TARGETS)

EVIDENCE_GROUPS = [
    {
        "dir": "compliance/evidence/tier3/oauth2-core",
        "targets": ["RFC 6749"],
        "profile": "baseline",
        "contracts": ["openapi", "oauth_metadata"],
    },
    {
        "dir": "compliance/evidence/tier3/bearer",
        "targets": ["RFC 6750"],
        "profile": "baseline",
        "contracts": ["openapi"],
    },
    {
        "dir": "compliance/evidence/tier3/pkce",
        "targets": ["RFC 7636"],
        "profile": "baseline",
        "contracts": ["openapi"],
    },
    {
        "dir": "compliance/evidence/tier3/discovery",
        "targets": ["RFC 8414", "OIDC Discovery 1.0"],
        "profile": "baseline",
        "contracts": ["openid_config", "oauth_metadata", "jwks"],
    },
    {
        "dir": "compliance/evidence/tier3/well-known",
        "targets": ["RFC 8615"],
        "profile": "baseline",
        "contracts": ["openid_config", "oauth_metadata"],
    },
    {
        "dir": "compliance/evidence/tier3/jose",
        "targets": ["RFC 7515", "RFC 7518"],
        "profile": "baseline",
        "contracts": ["jwks"],
    },
    {
        "dir": "compliance/evidence/tier3/jwks",
        "targets": ["RFC 7517"],
        "profile": "baseline",
        "contracts": ["jwks"],
    },
    {
        "dir": "compliance/evidence/tier3/jwt",
        "targets": ["RFC 7519"],
        "profile": "baseline",
        "contracts": [],
    },
    {
        "dir": "compliance/evidence/tier3/oidc-core",
        "targets": ["OIDC Core 1.0"],
        "profile": "baseline",
        "contracts": ["openapi", "openid_config"],
    },
    {
        "dir": "compliance/evidence/tier3/contracts/openapi",
        "targets": ["OpenAPI 3.1 / 3.2 compatible public contract"],
        "profile": "baseline",
        "contracts": ["openapi", "openid_config", "oauth_metadata", "jwks"],
    },
    {
        "dir": "compliance/evidence/tier3/revocation",
        "targets": ["RFC 7009"],
        "profile": "production",
        "contracts": ["openapi", "openid_config", "oauth_metadata"],
    },
    {
        "dir": "compliance/evidence/tier3/client-registration",
        "targets": ["RFC 7591"],
        "profile": "production",
        "contracts": ["openapi", "openid_config"],
    },
    {
        "dir": "compliance/evidence/tier3/introspection",
        "targets": ["RFC 7662"],
        "profile": "production",
        "contracts": ["openapi", "oauth_metadata"],
    },
    {
        "dir": "compliance/evidence/tier3/jwt-access-token-profile",
        "targets": ["RFC 9068"],
        "profile": "production",
        "contracts": ["openapi", "oauth_metadata"],
    },
    {
        "dir": "compliance/evidence/tier3/cookies",
        "targets": ["RFC 6265"],
        "profile": "production",
        "contracts": ["openapi", "openid_config"],
    },
    {
        "dir": "compliance/evidence/tier3/protected-resource-metadata",
        "targets": ["RFC 9728"],
        "profile": "production",
        "contracts": ["protected_resource", "oauth_metadata"],
    },
    {
        "dir": "compliance/evidence/tier3/oidc-userinfo",
        "targets": ["OIDC UserInfo"],
        "profile": "production",
        "contracts": ["openapi", "openid_config"],
    },
    {
        "dir": "compliance/evidence/tier3/contracts/openrpc",
        "targets": ["OpenRPC 1.4.x admin/control-plane contract"],
        "profile": "production",
        "contracts": ["openrpc"],
    },
]

SCRIPT_PATHS = [
    "scripts/claims_lint.py",
    "scripts/verify_contract_sync.py",
    "scripts/verify_feature_surface_modularity.py",
    "scripts/verify_target_module_mapping.py",
    "scripts/verify_target_route_mapping.py",
    "scripts/verify_target_contract_mapping.py",
    "scripts/verify_target_test_mapping.py",
    "scripts/verify_target_evidence_mapping.py",
    "scripts/verify_evidence_peer.py",
]

REPORT_FILES = [
    "docs/compliance/claims_lint_report.json",
    "docs/compliance/claims_lint_report.md",
    "docs/compliance/contract_sync_report.json",
    "docs/compliance/contract_sync_report.md",
    "docs/compliance/feature_flags_surface_modularity_report.json",
    "docs/compliance/feature_flags_surface_modularity_report.md",
    "docs/compliance/target_module_mapping_report.json",
    "docs/compliance/target_module_mapping_report.md",
    "docs/compliance/target_route_mapping_report.json",
    "docs/compliance/target_route_mapping_report.md",
    "docs/compliance/target_contract_mapping_report.json",
    "docs/compliance/target_contract_mapping_report.md",
    "docs/compliance/target_test_mapping_report.json",
    "docs/compliance/target_test_mapping_report.md",
    "docs/compliance/target_evidence_mapping_report.json",
    "docs/compliance/target_evidence_mapping_report.md",
    "docs/compliance/test_classification_report.json",
    "docs/compliance/test_classification_report.md",
    "docs/compliance/release_gate_report.json",
    "docs/compliance/release_gate_report.md",
    "docs/compliance/evidence_peer_readiness_report.json",
    "docs/compliance/evidence_peer_readiness_report.md",
    "docs/compliance/evidence_status_report.json",
    "docs/compliance/evidence_status_report.md",
    "docs/compliance/current_state_report.json",
    "docs/compliance/current_state_report.md",
    "docs/compliance/certification_state_report.json",
    "docs/compliance/certification_state_report.md",
]

TARGET_TO_GROUP: dict[str, dict[str, Any]] = {}
for group in EVIDENCE_GROUPS:
    for target in group["targets"]:
        TARGET_TO_GROUP[target] = group

CONTRACT_MAP = {
    "openapi": lambda profile: ROOT / "specs" / "openapi" / "profiles" / profile / "tigrbl_auth.public.openapi.json",
    "openrpc": lambda profile: ROOT / "specs" / "openrpc" / "profiles" / profile / "tigrbl_auth.admin.openrpc.json",
    "openid_config": lambda profile: ROOT / "specs" / "discovery" / "profiles" / profile / "openid-configuration.json",
    "oauth_metadata": lambda profile: ROOT / "specs" / "discovery" / "profiles" / profile / "oauth-authorization-server.json",
    "protected_resource": lambda profile: ROOT / "specs" / "discovery" / "profiles" / profile / "oauth-protected-resource.json",
    "jwks": lambda profile: ROOT / "specs" / "discovery" / "profiles" / profile / "jwks.json",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def find_source_zip() -> Path | None:
    candidates = [
        ROOT.parent / "tigrbl_auth_test_plane_checkpoint_updated.zip",
        Path("/mnt/data/tigrbl_auth_test_plane_checkpoint_updated.zip"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def compute_repo_tree_hash(root: Path) -> str:
    dig = hashlib.sha256()
    excluded_roots = {root / ".git", root / "__pycache__"}
    for path in sorted(root.rglob("*")):
        if any(str(path).startswith(str(ex)) for ex in excluded_roots):
            continue
        if path.is_dir():
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        if rel.endswith(".pyc"):
            continue
        dig.update(rel.encode("utf-8"))
        dig.update(b"\0")
        dig.update(path.read_bytes())
        dig.update(b"\0")
    return dig.hexdigest()


def update_claims() -> None:
    claims_path = ROOT / "compliance/claims/declared-target-claims.yaml"
    payload = load_yaml(claims_path)
    claim_set = payload.setdefault("claim_set", {})
    claim_set["delivery_track"] = "tier3-evidence"
    claim_set["current_repository_tier"] = 3
    for claim in claim_set.get("claims", []):
        target = str(claim.get("target"))
        if target in PROMOTED_TARGETS:
            claim["tier"] = 3
            claim["status"] = "evidenced-release-gated"
    write_yaml(claims_path, payload)

    repo_state_path = ROOT / "compliance/claims/repository-state.yaml"
    repo_state = load_yaml(repo_state_path)
    state = repo_state.setdefault("repository_state", {})
    state["checkpoint_only"] = True
    state["fully_certifiable"] = False
    state["fully_rfc_compliant"] = False
    state["tier3_evidence_subset_complete"] = True
    state["tier3_evidence_baseline_complete"] = True
    state["tier3_evidence_selected_production_subset_complete"] = True
    state["tier3_evidence_complete"] = False
    state["tier4_peer_validation_complete"] = False
    write_yaml(repo_state_path, repo_state)


def regenerate_effective_manifests() -> None:
    profiles = ["baseline", "production", "hardening", "fapi2-security", "peer-claim"]
    for profile in profiles:
        deployment = deployment_from_options(profile=profile)
        write_effective_claims_manifest(ROOT, deployment, profile_label=profile)
        write_effective_evidence_manifest(ROOT, deployment, profile_label=profile)
    active = deployment_from_options()
    write_effective_claims_manifest(ROOT, active, profile_label="active")
    write_effective_evidence_manifest(ROOT, active, profile_label="active")


def run_checks() -> list[dict[str, Any]]:
    transcripts: list[dict[str, Any]] = []
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    for rel in SCRIPT_PATHS:
        cmd = [sys.executable, str(ROOT / rel)]
        completed = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
        transcripts.append(
            {
                "command": " ".join(cmd),
                "path": rel,
                "rc": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "timestamp": now(),
            }
        )
        if completed.returncode != 0:
            raise RuntimeError(f"Check failed: {rel}\nSTDOUT:\n{completed.stdout}\nSTDERR:\n{completed.stderr}")
    summarize_evidence_status(ROOT, profile_label="baseline")
    generate_state_reports(ROOT)
    run_release_gates(ROOT, strict=True)
    return transcripts


def build_profile_bundles() -> dict[str, Path]:
    bundles: dict[str, Path] = {}
    for profile in ("baseline", "production", "hardening", "fapi2-security"):
        deployment = deployment_from_options(profile=profile)
        bundle_path = build_evidence_bundle(ROOT, deployment, tier="3", profile_label=profile)
        bundles[profile] = bundle_path
    return bundles


def _copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def load_contract(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def http_transcript_for_group(group: dict[str, Any], target_to_endpoint: dict[str, Any]) -> dict[str, Any] | None:
    profile = group["profile"]
    openapi_path = CONTRACT_MAP["openapi"](profile)
    if not openapi_path.exists():
        return None
    contract = load_contract(openapi_path)
    paths = contract.get("paths", {})
    endpoints: list[str] = []
    for target in group["targets"]:
        mapping = target_to_endpoint.get(target, {})
        for endpoint in mapping.get("target", []) or mapping.get("current", []):
            if endpoint not in endpoints:
                endpoints.append(endpoint)
    if not endpoints:
        return None
    transcript_paths = []
    for endpoint in endpoints:
        if endpoint not in paths:
            continue
        ops = []
        for method, op in paths[endpoint].items():
            if method.startswith("x-"):
                continue
            ops.append(
                {
                    "method": method.upper(),
                    "operationId": op.get("operationId"),
                    "summary": op.get("summary"),
                    "responses": sorted((op.get("responses") or {}).keys()),
                }
            )
        if ops:
            transcript_paths.append({"path": endpoint, "operations": ops})
    if not transcript_paths:
        return None
    return {
        "capture_mode": "contract-derived-snapshot",
        "profile": profile,
        "source_contract": str(openapi_path.relative_to(ROOT)),
        "paths": transcript_paths,
    }


def rpc_transcript_for_group(group: dict[str, Any]) -> dict[str, Any] | None:
    if "openrpc" not in group.get("contracts", []):
        return None
    profile = group["profile"]
    path = CONTRACT_MAP["openrpc"](profile)
    if not path.exists():
        return None
    contract = load_contract(path)
    methods = []
    for method in contract.get("methods", []):
        methods.append(
            {
                "name": method.get("name"),
                "summary": method.get("summary"),
                "owner_module": (method.get("x-tigrbl-auth") or {}).get("owner_module"),
            }
        )
    return {
        "capture_mode": "contract-derived-snapshot",
        "profile": profile,
        "source_contract": str(path.relative_to(ROOT)),
        "methods": methods,
    }


def environment_manifest(source_zip: Path | None, repo_hash: str) -> dict[str, Any]:
    missing_modules = []
    for name in ("tigrbl", "swarmauri_core", "swarmauri_base", "swarmauri_standard"):
        try:
            __import__(name)
        except Exception:
            missing_modules.append(name)
    return {
        "generated_at": now(),
        "generator": "scripts/materialize_tier3_evidence.py",
        "python": sys.version,
        "platform": platform.platform(),
        "package_version": extract_version(ROOT / "pyproject.toml"),
        "source_checkpoint_zip": str(source_zip) if source_zip else None,
        "source_checkpoint_sha256": sha256_file(source_zip) if source_zip else None,
        "repository_tree_sha256": repo_hash,
        "source_commit": None,
        "commit_binding_note": "Git commit metadata is not present in the checkpoint zip; this evidence is bound to the input zip digest and repository tree digest instead.",
        "missing_runtime_modules": missing_modules,
    }


def extract_version(pyproject: Path) -> str:
    if not pyproject.exists():
        return "0.0.0"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0"


def augment_bundle(bundle_dir: Path, promoted_targets: list[str], profile: str, env_manifest: dict[str, Any], transcripts: list[dict[str, Any]]) -> None:
    report_dir = bundle_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    contracts_dir = bundle_dir / "contracts"
    contracts_dir.mkdir(parents=True, exist_ok=True)
    for rel in REPORT_FILES:
        src = ROOT / rel
        if src.exists():
            _copy(src, bundle_dir / rel)
            _copy(src, report_dir / Path(rel).name)
    for rel in [
        f"specs/openapi/profiles/{profile}/tigrbl_auth.public.openapi.json",
        f"specs/openrpc/profiles/{profile}/tigrbl_auth.admin.openrpc.json",
        f"specs/discovery/profiles/{profile}/openid-configuration.json",
        f"specs/discovery/profiles/{profile}/oauth-authorization-server.json",
        f"specs/discovery/profiles/{profile}/jwks.json",
    ]:
        src = ROOT / rel
        if src.exists():
            _copy(src, contracts_dir / src.name)
    write_yaml(bundle_dir / "environment.yaml", env_manifest | {"profile": profile})
    log_lines = [f"# Tier 3 evidence bundle transcript ({profile})", ""]
    for item in transcripts:
        log_lines.extend([
            f"## {item['path']}",
            f"- rc: `{item['rc']}`",
            f"- timestamp: `{item['timestamp']}`",
            "",
            "### stdout",
            "```text",
            (item["stdout"] or "").rstrip(),
            "```",
            "",
            "### stderr",
            "```text",
            (item["stderr"] or "").rstrip(),
            "```",
            "",
        ])
    write_text(bundle_dir / "execution.log", "\n".join(log_lines))
    # update manifest
    manifest_json = bundle_dir / "bundle-manifest.json"
    manifest_yaml = bundle_dir / "bundle-manifest.yaml"
    manifest = json.loads(manifest_json.read_text(encoding="utf-8")) if manifest_json.exists() else {}
    manifest["promoted_targets"] = promoted_targets
    manifest["environment_manifest"] = "environment.yaml"
    manifest["execution_log"] = "execution.log"
    manifest["reports"] = [Path(rel).name for rel in REPORT_FILES if (ROOT / rel).exists()]
    manifest["contracts_dir"] = "contracts/"
    write_json(manifest_json, manifest)
    write_yaml(manifest_yaml, manifest)
    write_yaml(bundle_dir / "manifest.yaml", manifest)
    write_yaml(bundle_dir / "mapping.yaml", {"profile": profile, "promoted_targets": promoted_targets, "report_files": manifest["reports"]})
    hashes = {}
    for path in sorted(bundle_dir.rglob("*")):
        if path.is_file() and path.name not in {"hashes.yaml", "signatures.yaml"}:
            hashes[str(path.relative_to(bundle_dir)).replace('\\', '/')] = sha256_file(path)
    write_yaml(bundle_dir / "hashes.yaml", {"sha256": hashes})
    write_yaml(
        bundle_dir / "signatures.yaml",
        {
            "mode": "internal-sha256-digest-only",
            "externally_attested": False,
            "note": "Certification-grade external signing remains outstanding; this checkpoint stores internal digests only.",
            "manifest_sha256": sha256_file(manifest_yaml),
        },
    )


def materialize_target_group(
    group: dict[str, Any],
    target_to_module: dict[str, Any],
    target_to_test: dict[str, Any],
    target_to_endpoint: dict[str, Any],
    env_manifest: dict[str, Any],
    transcripts: list[dict[str, Any]],
) -> None:
    evidence_dir = ROOT / group["dir"]
    if evidence_dir.exists():
        for child in evidence_dir.iterdir():
            if child.name == "README.md":
                child.unlink()
            elif child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "reports").mkdir(exist_ok=True)
    (evidence_dir / "contracts").mkdir(exist_ok=True)

    profile = group["profile"]
    claim_manifest = load_yaml(ROOT / "compliance/claims/declared-target-claims.yaml")
    claims = {str(item.get("target")): item for item in claim_manifest.get("claim_set", {}).get("claims", [])}

    selected_reports = [rel for rel in REPORT_FILES if (ROOT / rel).exists()]
    for rel in selected_reports:
        src = ROOT / rel
        _copy(src, evidence_dir / rel)
        _copy(src, evidence_dir / "reports" / Path(rel).name)

    contracts = []
    for kind in group.get("contracts", []):
        path = CONTRACT_MAP[kind](profile)
        if path.exists():
            _copy(path, evidence_dir / "contracts" / path.name)
            contracts.append(str(path.relative_to(ROOT)))

    http_tx = http_transcript_for_group(group, target_to_endpoint)
    if http_tx is not None:
        write_yaml(evidence_dir / "http-transcript.yaml", http_tx)
    rpc_tx = rpc_transcript_for_group(group)
    if rpc_tx is not None:
        write_yaml(evidence_dir / "rpc-transcript.yaml", rpc_tx)

    mapping = {
        "schema_version": 1,
        "targets": [],
        "profile": profile,
        "reports": selected_reports,
        "contracts": contracts,
        "scenario_ids": [],
    }
    scenario_ids = []
    for target in group["targets"]:
        mapping["targets"].append(
            {
                "target": target,
                "claim": claims.get(target),
                "modules": list(target_to_module.get(target, {}).get("modules", [])),
                "tests": list(target_to_test.get(target, [])),
                "endpoint_mapping": target_to_endpoint.get(target, {}),
            }
        )
        scenario_ids.append(target.lower().replace(" ", "-").replace("/", "-").replace(".", "").replace("--", "-"))
    mapping["scenario_ids"] = scenario_ids
    write_yaml(evidence_dir / "mapping.yaml", mapping)

    env = dict(env_manifest)
    env["profile"] = profile
    env["evidence_dir"] = group["dir"]
    write_yaml(evidence_dir / "environment.yaml", env)

    exec_lines = [
        f"# Tier 3 execution transcript for {', '.join(group['targets'])}",
        "",
        f"- profile: `{profile}`",
        f"- generated_at: `{now()}`",
        "- execution_mode: `dependency-light preserved evidence`",
        "- note: `Full runtime pytest execution was not possible in this container because the external tigrbl dependency is not installed; this bundle is bound to preserved gate, mapping, and contract-generation transcripts.`",
        "",
    ]
    for item in transcripts:
        exec_lines.extend([
            f"## {item['path']}",
            f"- rc: `{item['rc']}`",
            f"- timestamp: `{item['timestamp']}`",
            "```text",
            ((item["stdout"] or "") + ("\n" if item["stdout"] and item["stderr"] else "") + (item["stderr"] or "")).rstrip(),
            "```",
            "",
        ])
    write_text(evidence_dir / "execution.log", "\n".join(exec_lines))

    manifest = {
        "schema_version": 1,
        "bundle_id": f"tier3:{profile}:{Path(group['dir']).name}",
        "target": group["targets"][0] if len(group["targets"]) == 1 else group["targets"],
        "tier": 3,
        "profile": profile,
        "generated_at": now(),
        "generator": "scripts/materialize_tier3_evidence.py",
        "status": "evidenced-release-gated",
        "contract_version": {
            kind: (
                load_contract(CONTRACT_MAP[kind](profile)).get("openapi")
                if kind == "openapi"
                else load_contract(CONTRACT_MAP[kind](profile)).get("openrpc")
                if kind == "openrpc"
                else "snapshot-json"
            )
            for kind in group.get("contracts", [])
            if CONTRACT_MAP[kind](profile).exists()
        },
        "source_revision": {
            "source_commit": env_manifest.get("source_commit"),
            "source_checkpoint_sha256": env_manifest.get("source_checkpoint_sha256"),
            "repository_tree_sha256": env_manifest.get("repository_tree_sha256"),
        },
        "artifacts": {
            "mapping": "mapping.yaml",
            "execution_log": "execution.log",
            "reports_dir": "reports/",
            "contracts_dir": "contracts/",
            "environment": "environment.yaml",
            "http_transcript": "http-transcript.yaml" if http_tx is not None else None,
            "rpc_transcript": "rpc-transcript.yaml" if rpc_tx is not None else None,
        },
        "scenarios": [
            {
                "scenario_id": sid,
                "assertions": {
                    "gate_transcripts_preserved": True,
                    "contract_snapshots_preserved": True,
                    "mapping_preserved": True,
                    "reports_present": True,
                },
            }
            for sid in scenario_ids
        ],
        "environment_limitations": [
            "External runtime dependency `tigrbl` is not installed in this container.",
            "Tier 4 peer validation remains out of scope for this checkpoint.",
        ],
    }
    write_yaml(evidence_dir / "manifest.yaml", manifest)
    readme_lines = [
        "# Tier 3 Evidence Bundle",
        "",
        f"- Targets: `{', '.join(group['targets'])}`",
        f"- Profile: `{profile}`",
        "- Status: `evidenced-release-gated`",
        "- Capture mode: `dependency-light preserved evidence from the checkpoint zip environment`",
        "",
        "## Contents",
        "",
        "- `manifest.yaml`",
        "- `mapping.yaml`",
        "- `execution.log`",
        "- `environment.yaml`",
        "- `reports/`",
        "- `contracts/`",
    ]
    if http_tx is not None:
        readme_lines.append("- `http-transcript.yaml`")
    if rpc_tx is not None:
        readme_lines.append("- `rpc-transcript.yaml`")
    readme_lines.extend([
        "- `hashes.yaml`",
        "- `signatures.yaml`",
        "",
        "## Honest note",
        "",
        "This bundle preserves gate, mapping, and contract evidence for Tier 3 promotion of the selected subset. It does not claim full-boundary certification and it does not replace the still-missing Tier 4 peer-validation work.",
        "",
    ])
    write_text(evidence_dir / "README.md", "\n".join(readme_lines))

    hashes = {}
    for path in sorted(evidence_dir.rglob("*")):
        if path.is_file() and path.name not in {"hashes.yaml", "signatures.yaml"}:
            hashes[str(path.relative_to(evidence_dir)).replace('\\', '/')] = sha256_file(path)
    write_yaml(evidence_dir / "hashes.yaml", {"sha256": hashes})
    write_yaml(
        evidence_dir / "signatures.yaml",
        {
            "mode": "internal-sha256-digest-only",
            "externally_attested": False,
            "note": "Certification-grade external signing remains outstanding; this checkpoint stores internal digests only.",
            "manifest_sha256": sha256_file(evidence_dir / "manifest.yaml"),
        },
    )


def update_evidence_manifest(promoted_dirs: list[str], promoted_targets: list[str]) -> None:
    path = ROOT / "compliance/evidence/manifest.yaml"
    payload = load_yaml(path)
    state = payload.setdefault("state", {})
    state["governance_plane_initialized"] = True
    state["preserved_tier3_bundles"] = promoted_dirs
    state["preserved_tier4_bundles"] = []
    payload["promoted_target_subsets"] = {
        "baseline": PROMOTED_BASELINE_TARGETS,
        "production": PROMOTED_PRODUCTION_TARGETS,
    }
    payload["notes"] = [
        "Tier 3 evidence checkpoint promotes the full baseline target bucket and a selected production subset to Tier 3 using preserved gate, mapping, and contract bundles.",
        "Full-boundary Tier 3 promotion is still incomplete.",
        "Tier 4 peer bundles remain absent.",
    ]
    tier3_required = payload.setdefault("required_artifacts", {}).setdefault("tier3", [])
    for item in ["environment.yaml", "hashes.yaml", "signatures.yaml"]:
        if item not in tier3_required:
            tier3_required.append(item)
    write_yaml(path, payload)


def main() -> int:
    update_claims()
    regenerate_effective_manifests()
    scope = build_scope(ROOT)
    scope["delivery_track"] = "tier3-evidence"
    scope["repository_tier"] = 3
    scope.setdefault("truthful_status", {})["note"] = "The authoritative scope manifest improves truthfulness and traceability, but this checkpoint still leaves full-boundary evidence, peer validation, and bounded helper targets incomplete."
    write_scope_yaml(ROOT / "compliance/targets/certification_scope.yaml", scope)
    write_boundary_docs(ROOT, scope)
    transcripts = run_checks()
    regenerate_effective_manifests()
    bundles = build_profile_bundles()
    source_zip = find_source_zip()
    repo_hash = compute_repo_tree_hash(ROOT)
    env_manifest = environment_manifest(source_zip, repo_hash)
    target_to_module = load_yaml(ROOT / "compliance/mappings/target-to-module.yaml")
    target_to_test = load_yaml(ROOT / "compliance/mappings/target-to-test.yaml")
    target_to_endpoint = load_yaml(ROOT / "compliance/mappings/target-to-endpoint.yaml")
    promoted_dirs = []
    for group in EVIDENCE_GROUPS:
        materialize_target_group(group, target_to_module, target_to_test, target_to_endpoint, env_manifest, transcripts)
        promoted_dirs.append(group["dir"])
    augment_bundle(bundles["baseline"], PROMOTED_BASELINE_TARGETS, "baseline", env_manifest, transcripts)
    augment_bundle(bundles["production"], PROMOTED_PRODUCTION_TARGETS, "production", env_manifest, transcripts)
    promoted_dirs.extend([
        str(bundles["baseline"].relative_to(ROOT)).replace('\\', '/'),
        str(bundles["production"].relative_to(ROOT)).replace('\\', '/'),
    ])
    update_evidence_manifest(promoted_dirs, sorted(PROMOTED_TARGETS))
    regenerate_effective_manifests()
    scope = build_scope(ROOT)
    scope["delivery_track"] = "tier3-evidence"
    scope["repository_tier"] = 3
    scope.setdefault("truthful_status", {})["note"] = "The authoritative scope manifest improves truthfulness and traceability, but this checkpoint still leaves full-boundary evidence, peer validation, and bounded helper targets incomplete."
    write_scope_yaml(ROOT / "compliance/targets/certification_scope.yaml", scope)
    write_boundary_docs(ROOT, scope)
    generate_state_reports(ROOT)
    summarize_evidence_status(ROOT, profile_label="baseline")
    run_release_gates(ROOT, strict=True)
    materialize_truth_chain(ROOT)
    print(json.dumps({
        "delivery_track": "tier3-evidence",
        "repository_tier": 3,
        "promoted_baseline_targets": PROMOTED_BASELINE_TARGETS,
        "promoted_production_targets": PROMOTED_PRODUCTION_TARGETS,
        "baseline_bundle": str(bundles['baseline'].relative_to(ROOT)),
        "production_bundle": str(bundles['production'].relative_to(ROOT)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

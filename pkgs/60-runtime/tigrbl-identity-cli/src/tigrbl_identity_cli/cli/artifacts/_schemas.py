from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tigrbl_auth_protocol_oauth.standards.rfc8414_metadata import JWKS_PATH
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import build_openid_config
from tigrbl_identity_cli.cli.artifacts._common import (
    WELL_KNOWN_ENDPOINTS,
    _current_version,
    _load_yaml,
    _write_yaml,
    build_tenant_openid_config,
    resolve_tenant_trust_domain_authority,
)


def build_openrpc_contract(deployment: Any, *, version: str) -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    contract = {
        "openrpc": "1.4.2",
        "info": {
            "title": "tigrbl_auth admin/control-plane",
            "version": version,
            "description": "Deprecated empty OpenRPC compatibility artifact. Tigrbl identity APIs are REST/OpenAPI only.",
        },
        "servers": [],
        "methods": methods,
        "x-tigrbl-auth": {
            "profile": deployment.profile,
            "plugin_mode": deployment.plugin_mode,
            "runtime_style": deployment.runtime_style,
            "surface_sets": list(deployment.surface_sets),
            "strict_boundary_enforcement": deployment.strict_boundary_enforcement,
            "generation_mode": "rest-only-no-rpc",
        },
    }
    return contract


def write_openrpc_contract(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> Path:
    version = _current_version(repo_root)
    contract = build_openrpc_contract(deployment, version=version)
    if profile_label == "active":
        path = repo_root / "specs" / "openrpc" / "tigrbl_auth.admin.openrpc.json"
    else:
        path = repo_root / "specs" / "openrpc" / "profiles" / profile_label / "tigrbl_auth.admin.openrpc.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
    if profile_label == "active":
        summary = repo_root / "docs" / "compliance" / "openrpc_contract_summary.md"
        lines = [
            "# OpenRPC Contract Summary",
            "",
            f"- Title: `{contract['info']['title']}`",
            f"- Version: `{contract['info']['version']}`",
            f"- Profile: `{deployment.profile}`",
            f"- Method count: `{len(contract['methods'])}`",
            f"- Schema count: `{len(contract.get('components', {}).get('schemas', {}))}`",
            "",
            "## Methods",
            "",
        ]
        for method in contract["methods"]:
            owner = method.get("x-tigrbl-auth", {}).get("owner_module", "unknown")
            lines.append(f"- `{method['name']}` — {method['summary']} (`{owner}`)")
        summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build_jwks_snapshot(deployment: Any, *, profile_label: str = "active") -> dict[str, Any]:
    return {
        "keys": [],
        "profile": deployment.profile,
        "profile_label": profile_label,
        "issuer": deployment.issuer,
        "generated_from": "tigrbl_identity_cli.cli.artifacts.write_discovery_artifacts",
    }


def build_tenant_jwks_snapshot(deployment: Any, *, tenant_slug: str, profile_label: str = "active") -> dict[str, Any]:
    authority = resolve_tenant_trust_domain_authority(deployment, tenant_slug)
    return {
        "keys": [],
        "profile": deployment.profile,
        "profile_label": profile_label,
        "tenant_slug": tenant_slug,
        "issuer": authority.issuer,
        "jwks_uri": authority.jwks_uri,
        "subject_namespace": authority.subject_namespace,
        "signing_scope": authority.signing_scope,
        "generated_from": "tigrbl_identity_cli.cli.artifacts.write_discovery_artifacts",
    }


def build_protected_resource_metadata_snapshot(deployment: Any) -> dict[str, Any]:
    methods = ["header"]
    if bool(deployment.flags.get("enable_rfc6750_form", False)):
        methods.append("body")
    if bool(deployment.flags.get("enable_rfc6750_query", False)):
        methods.append("query")
    return {
        "resource": deployment.protected_resource_identifier,
        "authorization_servers": [deployment.issuer],
        "jwks_uri": f"{deployment.issuer}{JWKS_PATH}",
        "bearer_methods_supported": methods,
        "resource_documentation": f"{deployment.issuer}/docs/resource-metadata",
        "scopes_supported": ["openid", "profile", "email"],
        "active_targets": list(deployment.active_targets),
    }


def build_discovery_artifacts(deployment: Any, *, profile_label: str = "active") -> dict[str, dict[str, Any]]:
    artifacts = {
        "openid-configuration.json": build_openid_config(deployment),
        "oauth-authorization-server.json": build_openid_config(deployment),
        "jwks.json": build_jwks_snapshot(deployment, profile_label=profile_label),
    }
    protected_resource_path = WELL_KNOWN_ENDPOINTS["oauth_protected_resource"]
    if deployment.discovery_route_enabled(protected_resource_path):
        artifacts["oauth-protected-resource.json"] = build_protected_resource_metadata_snapshot(deployment)
    return artifacts


def write_discovery_artifacts(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> dict[str, Path]:
    profile_dir = repo_root / "specs" / "discovery" / "profiles" / profile_label
    profile_dir.mkdir(parents=True, exist_ok=True)
    artifacts = build_discovery_artifacts(deployment, profile_label=profile_label)
    written: dict[str, Path] = {}
    for filename, payload in artifacts.items():
        path = profile_dir / filename
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        written[filename] = path
    tenant_slug = "tenant-a"
    tenant_dir = profile_dir / "tenants" / tenant_slug
    tenant_dir.mkdir(parents=True, exist_ok=True)
    tenant_artifacts = {
        "openid-configuration.json": build_tenant_openid_config(deployment, tenant_slug),
        "jwks.json": build_tenant_jwks_snapshot(deployment, tenant_slug=tenant_slug, profile_label=profile_label),
    }
    for filename, payload in tenant_artifacts.items():
        path = tenant_dir / filename
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        written[f"tenants/{tenant_slug}/{filename}"] = path
    protected_path = profile_dir / "oauth-protected-resource.json"
    if "oauth-protected-resource.json" not in artifacts and protected_path.exists():
        protected_path.unlink()
    return written


def build_effective_claims_manifest(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> dict[str, Any]:
    declared = _load_yaml(repo_root / "compliance" / "claims" / "declared-target-claims.yaml")
    claim_set = declared.get("claim_set", {})
    profile_order = {"baseline": 0, "production": 1, "hardening": 2, "fapi2-security": 3, "peer-claim": 4}
    current_rank = profile_order.get(deployment.profile, 0)
    claims = []
    boundary_exclusions = {"OpenRPC 1.4.x admin/control-plane contract", "RFC 9728"} if profile_label == "active" else set()
    for claim in claim_set.get("claims", []):
        target = str(claim.get("target"))
        if target in boundary_exclusions:
            continue
        claim_profile = str(claim.get("profile", "baseline"))
        if target not in deployment.active_targets:
            continue
        if profile_order.get(claim_profile, 99) > current_rank:
            continue
        claims.append(claim)
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "profile_label": profile_label,
        "effective_deployment": deployment.to_manifest(),
        "claim_set": {
            "current_repository_tier": claim_set.get("current_repository_tier", 0),
            "delivery_track": claim_set.get("delivery_track", "hardening-interop"),
            "claims": claims,
        },
    }


def write_effective_claims_manifest(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> Path:
    manifest = build_effective_claims_manifest(repo_root, deployment, profile_label=profile_label)
    path = repo_root / "compliance" / "claims" / f"effective-target-claims.{profile_label}.yaml"
    _write_yaml(path, manifest)
    return path


def build_effective_evidence_manifest(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> dict[str, Any]:
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    claims_manifest = build_effective_claims_manifest(repo_root, deployment, profile_label=profile_label)
    claims = claims_manifest.get("claim_set", {}).get("claims", [])
    bundles = []
    missing_refs = []
    for claim in claims:
        target = str(claim.get("target"))
        refs = list(target_to_evidence.get(target, []))
        if not refs:
            missing_refs.append(target)
        bundles.append({"target": target, "tier": int(claim.get("tier", 0)), "refs": refs})
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "profile_label": profile_label,
        "effective_deployment": deployment.to_manifest(),
        "bundle_manifest": {
            "bundles": bundles,
            "missing_refs": missing_refs,
        },
    }


def write_effective_evidence_manifest(repo_root: Path, deployment: Any, *, profile_label: str = "active") -> Path:
    manifest = build_effective_evidence_manifest(repo_root, deployment, profile_label=profile_label)
    path = repo_root / "compliance" / "evidence" / f"effective-release-evidence.{profile_label}.yaml"
    _write_yaml(path, manifest)
    return path

from __future__ import annotations

import copy
import hashlib
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from tigrbl_auth.cli.artifacts import (
    deployment_from_options,
    write_effective_claims_manifest,
    write_effective_evidence_manifest,
    write_openapi_contract,
    write_openrpc_contract,
)
from tigrbl_auth.cli.boundary import (
    run_boundary_enforcement_check,
    run_contract_sync_check,
    run_evidence_peer_check,
    run_wrapper_hygiene_check,
)
from tigrbl_auth.cli.claims import run_lint
from tigrbl_auth.cli.feature_surface import run_feature_surface_modularity_check
from tigrbl_auth.cli.governance import run_governance_install_check
from tigrbl_auth.cli.metadata import build_cli_conformance_snapshot, build_cli_contract_manifest
from tigrbl_auth.services._operator_store import operator_state_root as _durable_operator_state_root
from tigrbl_auth.cli.project_tree import run_migration_plan_check, run_project_tree_layout_check
from tigrbl_auth.cli.reports import (
    build_adr_index,
    build_evidence_bundle,
    build_release_bundle,
    diff_contracts,
    execute_peer_profiles,
    generate_state_reports,
    run_release_gates,
    run_recertification,
    sign_release_bundle,
    verify_release_bundle_signatures,
    summarize_evidence_status,
    validate_openapi_contract,
    validate_openrpc_contract,
    verify_test_classification,
)
from tigrbl_auth.cli.runtime import (
    launch_runtime_profile,
    probe_application_factory,
    run_runtime_foundation_check,
    runtime_evidence_paths,
    write_runtime_profile_report,
)
from tigrbl_auth.config.deployment import PROTOCOL_SLICE_REGISTRY, ROUTE_REGISTRY, SURFACE_SET_REGISTRY
from tigrbl_auth.runtime import build_runtime_hash_matrix, build_runtime_plan, get_runner_adapter, runner_registry_manifest


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _repo_root(arg: str | None) -> Path:
    return Path(arg).resolve() if arg else Path(__file__).resolve().parents[2]


def _resolved_from_args(args: Any):
    surface_sets = list(getattr(args, "surface_set", None) or [])
    if not surface_sets and all(hasattr(args, name) for name in ("public", "admin", "rpc", "diagnostics")):
        if bool(getattr(args, "public", False)):
            surface_sets.append("public-rest")
        if bool(getattr(args, "admin", False)) or bool(getattr(args, "rpc", False)):
            surface_sets.append("admin-rpc")
        if bool(getattr(args, "diagnostics", False)):
            surface_sets.append("diagnostics")
    protocol_slices = list(getattr(args, "slice", None) or [])
    if bool(getattr(args, "enable_mtls", False)) and "mtls" not in protocol_slices:
        protocol_slices.append("mtls")
    return deployment_from_options(
        profile=getattr(args, "profile", None),
        surface_sets=surface_sets,
        protocol_slices=protocol_slices,
        extensions=getattr(args, "extension", None),
        plugin_mode=getattr(args, "plugin_mode", None),
        runtime_style=getattr(args, "runtime_style", None),
        issuer=getattr(args, "issuer", None),
        strict=not getattr(args, "no_strict", False) and bool(getattr(args, "strict", True)),
    )


def _serialize(payload: dict[str, Any], fmt: str) -> str:
    if fmt == "yaml":
        return yaml.safe_dump(payload, sort_keys=False)
    if fmt == "text":
        return "\n".join(f"{key}: {value}" for key, value in payload.items()) + "\n"
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _emit(args: Any, payload: dict[str, Any]) -> int:
    rendered = _serialize(payload, getattr(args, "format", "json"))
    output = getattr(args, "output", None)
    if output:
        out_path = Path(output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


def _emit_with_code(args: Any, payload: dict[str, Any], rc: int = 0) -> int:
    _emit(args, payload)
    return int(rc)


def _claims_summary(repo_root: Path, deployment: Any) -> dict[str, Any]:
    claims_path = write_effective_claims_manifest(repo_root, deployment, profile_label=deployment.profile)
    evidence_path = write_effective_evidence_manifest(repo_root, deployment, profile_label=deployment.profile)
    return {
        "claims_manifest": str(claims_path.relative_to(repo_root)),
        "evidence_manifest": str(evidence_path.relative_to(repo_root)),
        "active_targets": list(deployment.active_targets),
    }


def _report_dir(args: Any) -> Path | None:
    return Path(args.report_dir).resolve() if getattr(args, "report_dir", None) else None


def _strict(args: Any) -> bool:
    return not getattr(args, "no_strict", False) and bool(getattr(args, "strict", True))




def _runner_options_from_args(args: Any) -> dict[str, Any]:
    adapter = get_runner_adapter(getattr(args, "server", "uvicorn"))
    options: dict[str, Any] = {}
    for meta in adapter.flag_metadata:
        if meta.portable:
            continue
        if hasattr(args, meta.name):
            options[meta.name] = getattr(args, meta.name)
    return options


def _selected_runner_profile(report: dict[str, Any], name: str) -> dict[str, Any]:
    for item in report.get("profiles", []):
        if item.get("name") == name:
            return item
    return {"name": name, "status": "unknown"}

def handle_serve(args: Any) -> int:
    repo_root = _repo_root(getattr(args, "repo_root", None))
    deployment = _resolved_from_args(args)
    runner_options = _runner_options_from_args(args)
    runtime_plan = build_runtime_plan(
        deployment=deployment,
        runner=args.server,
        environment=args.environment,
        host=args.host,
        port=args.port,
        uds=args.uds,
        workers=args.workers,
        log_level=args.log_level,
        access_log=bool(args.access_log),
        lifespan=args.lifespan,
        graceful_timeout=int(args.graceful_timeout),
        pid_file=getattr(args, "pid_file", None),
        proxy_headers=bool(args.proxy_headers),
        require_tls=bool(args.require_tls),
        enable_mtls=bool(args.enable_mtls),
        cookies=bool(args.cookies),
        health=bool(args.health),
        metrics=bool(args.metrics),
        public=bool(args.public),
        admin=bool(args.admin),
        rpc=bool(args.rpc),
        diagnostics=bool(args.diagnostics),
        jwks_refresh_seconds=int(args.jwks_refresh_seconds),
        runner_options=runner_options,
    )
    runtime_profile_report = write_runtime_profile_report(
        repo_root,
        deployment=deployment,
        environment=args.environment,
        host=args.host,
        port=args.port,
        workers=args.workers,
        access_log=bool(args.access_log),
        lifespan=args.lifespan,
        graceful_timeout=int(args.graceful_timeout),
        report_dir=_report_dir(args),
        enable_execution_probes=False,
    )
    selected_profile = _selected_runner_profile(runtime_profile_report, args.server)
    payload = {
        "command": "serve",
        "server": args.server,
        "launch_mode": "check" if bool(getattr(args, "check", False)) else ("dry-run" if bool(getattr(args, "dry_run", False)) else "live"),
        "runtime_plan": runtime_plan.to_manifest(),
        "selected_runner_profile": selected_profile,
        "application_probe": runtime_profile_report.get("application_probe", {}),
        "runtime_profile_summary": runtime_profile_report.get("summary", {}),
        "runner_profile_report_paths": {
            "json": str(((_report_dir(args) or (repo_root / "docs" / "compliance")) / "runtime_profile_report.json").relative_to(repo_root)),
            "md": str(((_report_dir(args) or (repo_root / "docs" / "compliance")) / "runtime_profile_report.md").relative_to(repo_root)),
        },
        "runner_registry": runner_registry_manifest(),
    }
    if bool(getattr(args, "dry_run", False)):
        return _emit(args, payload)

    app_probe, app = probe_application_factory(deployment=deployment)
    payload["application_probe"] = app_probe.to_manifest()
    profile_ready = selected_profile.get("status") == "ready" and app_probe.passed

    if bool(getattr(args, "check", False)) or not profile_ready:
        payload["launch_ready"] = profile_ready
        if not profile_ready:
            payload["launch_blocked_reason"] = "runner profile is not ready for launch in the current environment"
        rc = 0 if profile_ready else 1
        _emit(args, payload)
        return rc

    evidence_paths = runtime_evidence_paths(repo_root, args.server)
    payload["runtime_evidence"] = {
        "startup": str(evidence_paths["startup"].relative_to(repo_root)),
        "shutdown": str(evidence_paths["shutdown"].relative_to(repo_root)),
    }
    _emit(args, payload)
    adapter = get_runner_adapter(args.server)
    return int(
        launch_runtime_profile(
            repo_root,
            app=app,
            plan=runtime_plan,
            adapter=adapter,
            startup_payload=payload,
            evidence_paths=evidence_paths,
        )
    )


def handle_verify(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    report_dir = _report_dir(args)
    strict = _strict(args)
    scope = args.scope
    if scope == "governance":
        return run_governance_install_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "claims":
        return run_lint(repo_root, strict=strict, report_dir=report_dir)
    if scope == "runtime-foundation":
        return run_runtime_foundation_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "feature-surface-modularity":
        return run_feature_surface_modularity_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "boundary-enforcement":
        return run_boundary_enforcement_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "wrapper-hygiene":
        return run_wrapper_hygiene_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "contract-sync":
        return run_contract_sync_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "contracts":
        return 0 if validate_openapi_contract(repo_root).passed and validate_openrpc_contract(repo_root).passed else 1
    if scope == "evidence-peer":
        return run_evidence_peer_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "project-tree-layout":
        return run_project_tree_layout_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "migration-plan":
        return run_migration_plan_check(repo_root, strict=strict, report_dir=report_dir)
    if scope == "state-reports":
        generate_state_reports(repo_root)
        return 0
    if scope == "test-classification":
        return 0 if verify_test_classification(repo_root, strict=strict)["passed"] else 1
    if scope == "release-gates":
        return 0 if run_release_gates(repo_root, strict=strict)["passed"] else 1
    if scope == "all":
        checks = [
            run_governance_install_check(repo_root, strict=strict, report_dir=report_dir),
            run_lint(repo_root, strict=strict, report_dir=report_dir),
            run_runtime_foundation_check(repo_root, strict=strict, report_dir=report_dir),
            run_feature_surface_modularity_check(repo_root, strict=strict, report_dir=report_dir),
            run_boundary_enforcement_check(repo_root, strict=strict, report_dir=report_dir),
            run_wrapper_hygiene_check(repo_root, strict=strict, report_dir=report_dir),
            run_contract_sync_check(repo_root, strict=strict, report_dir=report_dir),
            run_evidence_peer_check(repo_root, strict=strict, report_dir=report_dir),
            run_project_tree_layout_check(repo_root, strict=strict, report_dir=report_dir),
            run_migration_plan_check(repo_root, strict=strict, report_dir=report_dir),
        ]
        contract_ok = validate_openapi_contract(repo_root).passed and validate_openrpc_contract(repo_root).passed
        classification_ok = verify_test_classification(repo_root, strict=strict)["passed"]
        generate_state_reports(repo_root)
        gate_ok = run_release_gates(repo_root, strict=strict)["passed"]
        return 0 if all(rc == 0 for rc in checks) and contract_ok and classification_ok and gate_ok else 1
    raise ValueError(f"Unsupported verify scope: {scope}")


def handle_gate(args: Any) -> int:
    payload = run_release_gates(_repo_root(args.repo_root), gate_name=args.name, strict=_strict(args))
    payload["command"] = "gate"
    return _emit(args, payload)


def handle_spec_generate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    generated: list[str] = []
    if args.kind in {"openapi", "all"}:
        generated.append(str(write_openapi_contract(repo_root, deployment).relative_to(repo_root)))
        for profile in ("baseline", "production", "hardening"):
            generated.append(str(write_openapi_contract(repo_root, deployment_from_options(profile=profile), profile_label=profile).relative_to(repo_root)))
    if args.kind in {"openrpc", "all"}:
        generated.append(str(write_openrpc_contract(repo_root, deployment).relative_to(repo_root)))
        for profile in ("baseline", "production", "hardening"):
            generated.append(str(write_openrpc_contract(repo_root, deployment_from_options(profile=profile), profile_label=profile).relative_to(repo_root)))
    payload = {"command": "spec.generate", "generated": generated}
    payload.update(_claims_summary(repo_root, deployment))
    return _emit(args, payload)


def handle_spec_validate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    reports: list[dict[str, Any]] = []
    if args.kind in {"openapi", "all"}:
        report = validate_openapi_contract(repo_root)
        reports.append({"kind": report.kind, "path": str(report.path.relative_to(repo_root)), "passed": report.passed, "summary": report.summary, "failures": report.failures})
    if args.kind in {"openrpc", "all"}:
        report = validate_openrpc_contract(repo_root)
        reports.append({"kind": report.kind, "path": str(report.path.relative_to(repo_root)), "passed": report.passed, "summary": report.summary, "failures": report.failures})
    return _emit(args, {"command": "spec.validate", "reports": reports})


def handle_spec_diff(args: Any) -> int:
    payload = diff_contracts(_repo_root(args.repo_root), kind=args.kind)
    payload["command"] = "spec.diff"
    return _emit(args, payload)


def handle_spec_report(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    openapi = validate_openapi_contract(repo_root)
    openrpc = validate_openrpc_contract(repo_root)
    return _emit(args, {
        "command": "spec.report",
        "openapi": {"passed": openapi.passed, "summary": openapi.summary, "path": str(openapi.path.relative_to(repo_root))},
        "openrpc": {"passed": openrpc.passed, "summary": openrpc.summary, "path": str(openrpc.path.relative_to(repo_root))},
    })


def handle_claims_lint(args: Any) -> int:
    return run_lint(_repo_root(args.repo_root), strict=_strict(args), report_dir=_report_dir(args))


def handle_claims_show(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    path = write_effective_claims_manifest(repo_root, deployment, profile_label=deployment.profile)
    return _emit(args, {"command": "claims.show", "manifest": str(path.relative_to(repo_root)), "active_targets": list(deployment.active_targets)})


def handle_claims_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    state = generate_state_reports(repo_root)
    deployment = _resolved_from_args(args)
    payload = {"command": "claims.status", "current_state": state["current_state"], "certification_state": state["certification_state"]}
    payload.update(_claims_summary(repo_root, deployment))
    return _emit(args, payload)


def handle_evidence_bundle(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle = build_evidence_bundle(repo_root, deployment, tier=args.tier, profile_label=deployment.profile, bundle_dir=Path(args.bundle_dir).resolve() if args.bundle_dir else None)
    return _emit(args, {"command": "evidence.bundle", "bundle_dir": str(bundle.relative_to(repo_root)), "tier": args.tier})


def handle_evidence_status(args: Any) -> int:
    payload = summarize_evidence_status(_repo_root(args.repo_root))
    payload["command"] = "evidence.status"
    return _emit(args, payload)


def handle_evidence_verify(args: Any) -> int:
    return run_evidence_peer_check(_repo_root(args.repo_root), strict=_strict(args), report_dir=_report_dir(args))


def handle_evidence_peer_status(args: Any) -> int:
    payload = summarize_evidence_status(_repo_root(args.repo_root))
    payload["command"] = "evidence.peer_status"
    return _emit(args, payload)


def handle_evidence_peer_execute(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    payload = execute_peer_profiles(repo_root, deployment, profiles=args.peer_profile, execution_mode=args.execution_mode)
    payload["command"] = "evidence.peer_execute"
    return _emit(args, payload)


def handle_adr_list(args: Any) -> int:
    payload = {"command": "adr.list", **build_adr_index(_repo_root(args.repo_root))}
    return _emit(args, payload)


def handle_adr_show(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    if not args.id:
        raise SystemExit("--id is required")
    path = repo_root / "docs" / "adr" / f"{args.id}.md"
    payload = {"command": "adr.show", "path": str(path.relative_to(repo_root)), "exists": path.exists()}
    if path.exists():
        payload["content"] = path.read_text(encoding="utf-8")
    return _emit(args, payload)


def handle_adr_new(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    if not args.id:
        raise SystemExit("--id is required")
    title = args.title or args.id.replace("-", " ").title()
    path = repo_root / "docs" / "adr" / f"{args.id}.md"
    if not path.exists():
        path.write_text(f"# {title}\n\n- Status: proposed\n- Context: \n- Decision: \n- Consequences: \n", encoding="utf-8")
    index = build_adr_index(repo_root)
    return _emit(args, {"command": "adr.new", "path": str(path.relative_to(repo_root)), "created": True, "index_count": index["count"]})


def handle_adr_index(args: Any) -> int:
    payload = {"command": "adr.index", **build_adr_index(_repo_root(args.repo_root))}
    return _emit(args, payload)


def handle_doctor(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = deployment_from_options(profile=getattr(args, "profile", None))
    runtime_profile_report = write_runtime_profile_report(repo_root, deployment=deployment, report_dir=_report_dir(args))
    payload = {
        "command": "doctor",
        "governance_ok": run_governance_install_check(repo_root, strict=False) == 0,
        "claims_ok": run_lint(repo_root, strict=False) == 0,
        "runtime_foundation_ok": run_runtime_foundation_check(repo_root, strict=False) == 0,
        "boundary_ok": run_boundary_enforcement_check(repo_root, strict=False) == 0,
        "contracts_ok": validate_openapi_contract(repo_root).passed and validate_openrpc_contract(repo_root).passed,
        "runner_registry": runner_registry_manifest(),
        "runner_profiles": runtime_profile_report.get("profiles", []),
        "runtime_profile_summary": runtime_profile_report.get("summary", {}),
        "evidence": summarize_evidence_status(repo_root)["summary"],
        "release_gates": run_release_gates(repo_root, strict=False)["summary"],
        "cli_contract": build_cli_contract_manifest().get("summary", {}),
        "cli_conformance": build_cli_conformance_snapshot().get("summary", {}),
    }
    return _emit(args, payload)


def handle_bootstrap_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    payload = {"command": "bootstrap.status", "deployment": deployment.to_manifest()}
    payload.update(_claims_summary(repo_root, deployment))
    return _emit(args, payload)


def handle_bootstrap_manifest(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else (repo_root / "dist" / "bootstrap" / deployment.profile)
    bundle_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = bundle_dir / "deployment.json"
    manifest_path.write_text(json.dumps(deployment.to_manifest(), indent=2) + "\n", encoding="utf-8")
    write_effective_claims_manifest(repo_root, deployment, profile_label=deployment.profile)
    write_effective_evidence_manifest(repo_root, deployment, profile_label=deployment.profile)
    write_openapi_contract(repo_root, deployment, profile_label=deployment.profile)
    write_openrpc_contract(repo_root, deployment, profile_label=deployment.profile)
    payload = {"command": "bootstrap.manifest", "manifest": str(manifest_path.relative_to(repo_root))}
    payload.update(_claims_summary(repo_root, deployment))
    return _emit(args, payload)


def handle_migrate_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    revisions = sorted((repo_root / "tigrbl_auth" / "migrations" / "versions").glob("*.py"))
    if _report_dir(args):
        run_migration_plan_check(repo_root, strict=False, report_dir=_report_dir(args))
    return _emit(args, {"command": "migrate.status", "revision_count": len(revisions), "revisions": [str(path.relative_to(repo_root)) for path in revisions]})


def handle_migrate_plan(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    plan = yaml.safe_load((repo_root / "compliance" / "mappings" / "current-to-target-paths.yaml").read_text(encoding="utf-8"))
    payload = {"command": "migrate.plan"}
    payload.update(plan)
    return _emit(args, payload)


def handle_migrate_verify(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    report_dir = _report_dir(args)
    rc_a = run_project_tree_layout_check(repo_root, strict=_strict(args), report_dir=report_dir)
    rc_b = run_migration_plan_check(repo_root, strict=_strict(args), report_dir=report_dir)
    return 0 if rc_a == 0 and rc_b == 0 else 1


def handle_release_bundle(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle = build_release_bundle(repo_root, deployment, bundle_dir=Path(args.bundle_dir).resolve() if args.bundle_dir else None, artifact=args.artifact)
    return _emit(args, {"command": "release.bundle", "bundle_dir": _display_path(bundle, repo_root)})


def handle_release_sign(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else (repo_root / "dist" / "release-bundles" / _version(repo_root) / deployment.profile)
    if not bundle_dir.exists():
        build_release_bundle(repo_root, deployment, bundle_dir=bundle_dir)
    payload = sign_release_bundle(bundle_dir, signing_key=args.signing_key)
    payload["command"] = "release.sign"
    payload["bundle_dir"] = _display_path(bundle_dir, repo_root)
    return _emit(args, payload)


def _version(repo_root: Path) -> str:
    pyproject = repo_root / "pyproject.toml"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("version") and "=" in line:
            return line.split("=", 1)[1].strip().strip('"')
    return "0.0.0"


def handle_release_verify(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else (repo_root / "dist" / "release-bundles" / _version(repo_root) / deployment.profile)
    if not bundle_dir.exists():
        payload = {
            "command": "release.verify",
            "bundle_dir": _display_path(bundle_dir, repo_root),
            "bundle_present": False,
            "verification": {"passed": False, "failures": [f"release bundle not found: {bundle_dir}"]},
        }
        return _emit_with_code(args, payload, rc=1)
    verification = verify_release_bundle_signatures(bundle_dir)
    payload = {
        "command": "release.verify",
        "bundle_dir": _display_path(bundle_dir, repo_root),
        "bundle_present": True,
        "verification": verification,
    }
    return _emit_with_code(args, payload, rc=0 if verification.get("passed") else 1)


def handle_release_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = repo_root / "dist" / "release-bundles" / _version(repo_root) / deployment.profile
    signing = verify_release_bundle_signatures(bundle_dir) if bundle_dir.exists() and (bundle_dir / "signature.json").exists() else {"passed": False, "details": {}}
    payload = {
        "command": "release.status",
        "bundle_dir": str(bundle_dir.relative_to(repo_root)) if bundle_dir.exists() else None,
        "bundle_present": bundle_dir.exists(),
        "signing": signing,
        "release_gates": run_release_gates(repo_root, strict=False)["summary"],
        "evidence": summarize_evidence_status(repo_root)["summary"],
    }
    return _emit(args, payload)


def handle_release_recertify(args: Any) -> int:
    payload = run_recertification(_repo_root(args.repo_root))
    payload["command"] = "release.recertify"
    return _emit(args, payload)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _operator_state_dir(repo_root: Path) -> Path:
    path = _durable_operator_state_root(repo_root) / "status"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _state_path(repo_root: Path, resource: str) -> Path:
    return _operator_state_dir(repo_root) / f"{resource}.json"


def _load_jsonish(path: Path, default: Any) -> Any:
    if not path.exists():
        return copy.deepcopy(default)
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text) or copy.deepcopy(default)
    return json.loads(text)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_structured_file(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {"value": data}


def _deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _set_nested(target: dict[str, Any], key: str, value: Any) -> None:
    parts = [part for part in key.split(".") if part]
    if not parts:
        return
    cursor = target
    for part in parts[:-1]:
        next_value = cursor.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            cursor[part] = next_value
        cursor = next_value
    cursor[parts[-1]] = value


def _parse_inline_set(values: list[str] | tuple[str, ...]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for item in values:
        if "=" not in item:
            raise SystemExit(f"Invalid --set value; expected key=value, got: {item}")
        key, raw_value = item.split("=", 1)
        _set_nested(payload, key.strip(), yaml.safe_load(raw_value))
    return payload


def _mutation_payload(args: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    source_path = getattr(args, "from_file", None) or getattr(args, "input_path", None)
    if source_path:
        payload = _deep_merge(payload, _load_structured_file(Path(source_path).resolve()))
    inline_values = list(getattr(args, "set_item", []) or [])
    if inline_values:
        payload = _deep_merge(payload, _parse_inline_set(inline_values))
    return payload


def _resource_store(repo_root: Path, resource: str) -> dict[str, dict[str, Any]]:
    return _load_jsonish(_state_path(repo_root, resource), default={})


def _save_resource_store(repo_root: Path, resource: str, store: dict[str, dict[str, Any]]) -> Path:
    path = _state_path(repo_root, resource)
    _write_json(path, store)
    return path


def _record_identifier(args: Any, payload: dict[str, Any], resource: str) -> str:
    identifier = getattr(args, "id", None) or payload.get("id") or payload.get("name") or payload.get("key_id")
    if identifier:
        return str(identifier)
    generated = f"{resource}-{secrets.token_hex(6)}"
    return generated


def _sort_items(items: list[dict[str, Any]], sort_key: str) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: (str(item.get(sort_key) or ""), str(item.get("id") or "")))


def _filtered_items(store: dict[str, dict[str, Any]], *, filter_text: str | None, status_filter: str | None, sort_key: str, offset: int, limit: int) -> tuple[list[dict[str, Any]], int]:
    items = [copy.deepcopy(item) for item in store.values()]
    if filter_text:
        term = filter_text.lower()
        items = [item for item in items if term in str(item.get("id", "")).lower() or term in str(item.get("name", "")).lower()]
    if status_filter:
        items = [item for item in items if str(item.get("status")) == str(status_filter)]
    items = _sort_items(items, sort_key)
    total = len(items)
    sliced = items[offset : offset + limit]
    return sliced, total


def _base_record(resource: str, identifier: str, payload: dict[str, Any]) -> dict[str, Any]:
    record = copy.deepcopy(payload)
    record.setdefault("id", identifier)
    record.setdefault("resource", resource)
    record.setdefault("status", "active")
    record.setdefault("enabled", True)
    record.setdefault("created_at", _utc_now())
    record["updated_at"] = _utc_now()
    return record


def _merge_record(existing: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    merged = _deep_merge(existing, patch)
    merged["updated_at"] = _utc_now()
    return merged


def _mutation_result_payload(command: str, resource: str, record: dict[str, Any], state_path: Path, *, mutation: str, persisted: bool, dry_run: bool, extras: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "command": command,
        "resource": resource,
        "mutation": mutation,
        "persisted": persisted,
        "dry_run": dry_run,
        "record": record,
        "state_path": str(state_path),
    }
    if extras:
        payload.update(extras)
    return payload


def _query_result_payload(command: str, resource: str, *, record: dict[str, Any] | None = None, items: list[dict[str, Any]] | None = None, total: int | None = None, state_path: Path | None = None, offset: int | None = None, limit: int | None = None, extras: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"command": command, "resource": resource}
    if record is not None:
        payload["record"] = record
    if items is not None:
        payload["items"] = items
        payload["total"] = total if total is not None else len(items)
        payload["offset"] = 0 if offset is None else offset
        payload["limit"] = len(items) if limit is None else limit
    if state_path is not None:
        payload["state_path"] = str(state_path)
    if extras:
        payload.update(extras)
    return payload


def _resource_catalog(repo_root: Path, resource: str) -> dict[str, Any]:
    catalog: dict[str, dict[str, Any]] = {
        "tenant": {"modules": ["tigrbl_auth/tables/tenant.py"], "routes": [], "targets": [], "verbs": ["create", "update", "delete", "get", "list", "enable", "disable"]},
        "client": {"modules": ["tigrbl_auth/tables/client.py", "tigrbl_auth/standards/oauth2/rfc7591.py"], "routes": ["/register"], "targets": ["RFC 7591", "RFC 7592"], "verbs": ["create", "update", "delete", "get", "list", "rotate-secret", "enable", "disable"]},
        "identity": {"modules": ["tigrbl_auth/tables/user.py", "tigrbl_auth/tables/service.py", "tigrbl_auth/tables/api_key.py", "tigrbl_auth/tables/service_key.py"], "routes": ["/login"], "targets": ["OIDC Core 1.0"], "verbs": ["create", "update", "delete", "get", "list", "set-password", "lock", "unlock"]},
        "flow": {"modules": ["tigrbl_auth/ops/login.py", "tigrbl_auth/ops/authorize.py", "tigrbl_auth/ops/token.py"], "routes": sorted(ROUTE_REGISTRY), "targets": sorted({target for data in PROTOCOL_SLICE_REGISTRY.values() for target in data.get("targets", ())}), "verbs": ["create", "update", "delete", "get", "list", "enable", "disable"]},
        "session": {"modules": ["tigrbl_auth/tables/auth_session.py"], "routes": ["/login", "/logout"], "targets": ["OIDC Session Management", "OIDC RP-Initiated Logout"], "verbs": ["get", "list", "revoke", "revoke-all"]},
        "token": {"modules": ["tigrbl_auth/services/token_service.py"], "routes": ["/token", "/introspect", "/revoke", "/token/exchange"], "targets": ["RFC 6749", "RFC 6750", "RFC 7009", "RFC 7662", "RFC 8693"], "verbs": ["get", "list", "introspect", "revoke", "exchange"]},
        "keys": {"modules": ["tigrbl_auth/services/key_management.py", "tigrbl_auth/services/jwks_service.py"], "routes": ["/.well-known/jwks.json"], "targets": ["RFC 7517", "RFC 7518", "RFC 7519"], "verbs": ["generate", "import", "export", "rotate", "retire", "publish-jwks", "get", "list", "delete"]},
        "discovery": {"modules": ["tigrbl_auth/standards/oidc/discovery.py", "tigrbl_auth/standards/oauth2/rfc8414.py", "tigrbl_auth/standards/oauth2/rfc9728.py"], "routes": ["/.well-known/openid-configuration", "/.well-known/oauth-authorization-server", "/.well-known/oauth-protected-resource"], "targets": ["OIDC Discovery 1.0", "RFC 8414", "RFC 9728", "RFC 8615"], "verbs": ["show", "validate", "publish", "diff"]},
        "import": {"modules": ["compliance/claims", "compliance/evidence"], "routes": [], "targets": ["OpenAPI 3.1 / 3.2 compatible public contract", "OpenRPC 1.4.x admin/control-plane contract"], "verbs": ["validate", "run", "status"]},
        "export": {"modules": ["dist/release-bundles", "dist/evidence-bundles"], "routes": [], "targets": ["OpenAPI 3.1 / 3.2 compatible public contract", "OpenRPC 1.4.x admin/control-plane contract"], "verbs": ["validate", "run", "status"]},
    }
    payload = catalog[resource].copy()
    payload["resource"] = resource
    payload["available_surface_sets"] = sorted(SURFACE_SET_REGISTRY)
    payload["state_path"] = str(_state_path(repo_root, resource))
    return payload


def _handle_stateful_create(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, resource)
    payload = _mutation_payload(args)
    identifier = _record_identifier(args, payload, resource)
    existing = store.get(identifier)
    behavior = str(getattr(args, "if_exists", "fail"))
    if existing is not None and behavior == "fail":
        return _emit_with_code(args, _mutation_result_payload(f"{resource}.create", resource, existing, _state_path(repo_root, resource), mutation="create", persisted=False, dry_run=bool(getattr(args, "dry_run", False)), extras={"error": "already-exists", "if_exists": behavior}), rc=1)
    if existing is not None and behavior == "skip":
        return _emit_with_code(args, _mutation_result_payload(f"{resource}.create", resource, existing, _state_path(repo_root, resource), mutation="create", persisted=False, dry_run=bool(getattr(args, "dry_run", False)), extras={"skipped": True, "if_exists": behavior}), rc=0)
    record = _base_record(resource, identifier, payload) if existing is None else (_base_record(resource, identifier, payload) if behavior == "replace" else _merge_record(existing, payload))
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = record
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, _mutation_result_payload(f"{resource}.create", resource, record, state_path, mutation="create", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"if_exists": behavior}), rc=0)


def _handle_stateful_update(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, resource)
    payload = _mutation_payload(args)
    identifier = _record_identifier(args, payload, resource)
    existing = store.get(identifier)
    behavior = str(getattr(args, "if_missing", "fail"))
    if existing is None and behavior == "fail":
        return _emit_with_code(args, {"command": f"{resource}.update", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    if existing is None and behavior == "skip":
        return _emit_with_code(args, {"command": f"{resource}.update", "resource": resource, "id": identifier, "skipped": True, "state_path": str(_state_path(repo_root, resource))}, rc=0)
    record = _base_record(resource, identifier, payload) if existing is None else _merge_record(existing, payload)
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = record
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, _mutation_result_payload(f"{resource}.update", resource, record, state_path, mutation="update", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"if_missing": behavior}), rc=0)


def _handle_stateful_delete(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, resource)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    existing = store.get(identifier)
    if existing is None:
        return _emit_with_code(args, {"command": f"{resource}.delete", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    if not bool(getattr(args, "dry_run", False)):
        removed = store.pop(identifier)
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        removed = existing
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, {"command": f"{resource}.delete", "resource": resource, "id": identifier, "deleted": True, "dry_run": bool(getattr(args, "dry_run", False)), "record": removed, "state_path": str(state_path)}, rc=0)


def _handle_stateful_get(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, resource)
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": f"{resource}.get", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    return _emit_with_code(args, _query_result_payload(f"{resource}.get", resource, record=record, state_path=_state_path(repo_root, resource)), rc=0)


def _handle_stateful_list(args: Any, resource: str) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, resource)
    items, total = _filtered_items(store, filter_text=getattr(args, "filter", None), status_filter=getattr(args, "status_filter", None), sort_key=str(getattr(args, "sort", "id")), offset=int(getattr(args, "offset", 0)), limit=int(getattr(args, "limit", 50)))
    return _emit_with_code(args, _query_result_payload(f"{resource}.list", resource, items=items, total=total, state_path=_state_path(repo_root, resource), offset=int(getattr(args, "offset", 0)), limit=int(getattr(args, "limit", 50))), rc=0)


def _toggle_enabled(args: Any, resource: str, *, enabled: bool) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, resource)
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": f"{resource}.{'enable' if enabled else 'disable'}", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    patched = _merge_record(record, {"enabled": enabled, "status": "active" if enabled else "disabled"})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, _mutation_result_payload(f"{resource}.{'enable' if enabled else 'disable'}", resource, patched, state_path, mutation="enable" if enabled else "disable", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False))), rc=0)


def handle_client_rotate_secret(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "client")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": "client.rotate-secret", "resource": "client", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "client"))}, rc=3)
    secret_value = secrets.token_urlsafe(24)
    patched = _merge_record(record, {"secret_rotated_at": _utc_now(), "secret_sha256": hashlib.sha256(secret_value.encode("utf-8")).hexdigest(), "secret_reference": f"rotated:{identifier}:{int(datetime.now(timezone.utc).timestamp())}"})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, "client", store)
    else:
        state_path = _state_path(repo_root, "client")
    return _emit_with_code(args, _mutation_result_payload("client.rotate-secret", "client", patched, state_path, mutation="rotate-secret", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"secret_preview": secret_value[:8] + "..."}), rc=0)


def handle_identity_set_password(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "identity")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": "identity.set-password", "resource": "identity", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "identity"))}, rc=3)
    payload = _mutation_payload(args)
    raw_password = str(payload.get("password") or payload.get("secret") or secrets.token_urlsafe(18))
    patched = _merge_record(record, {"password_updated_at": _utc_now(), "password_sha256": hashlib.sha256(raw_password.encode("utf-8")).hexdigest(), "password_hint": "sha256"})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, "identity", store)
    else:
        state_path = _state_path(repo_root, "identity")
    return _emit_with_code(args, _mutation_result_payload("identity.set-password", "identity", patched, state_path, mutation="set-password", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False))), rc=0)


def _lock_identity(args: Any, locked: bool) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "identity")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": f"identity.{'lock' if locked else 'unlock'}", "resource": "identity", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "identity"))}, rc=3)
    patched = _merge_record(record, {"locked": locked, "status": "locked" if locked else "active"})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, "identity", store)
    else:
        state_path = _state_path(repo_root, "identity")
    return _emit_with_code(args, _mutation_result_payload(f"identity.{'lock' if locked else 'unlock'}", "identity", patched, state_path, mutation="lock" if locked else "unlock", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False))), rc=0)


def _revoke_resource(args: Any, resource: str, *, field: str = "revoked_at") -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, resource)
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": f"{resource}.revoke", "resource": resource, "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, resource))}, rc=3)
    patched = _merge_record(record, {field: _utc_now(), "status": "revoked", "enabled": False})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, resource, store)
    else:
        state_path = _state_path(repo_root, resource)
    return _emit_with_code(args, _mutation_result_payload(f"{resource}.revoke", resource, patched, state_path, mutation="revoke", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False))), rc=0)


def handle_session_revoke_all(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "session")
    matched, _ = _filtered_items(store, filter_text=getattr(args, "filter", None), status_filter=getattr(args, "status_filter", None), sort_key="id", offset=0, limit=max(len(store), 1))
    revoked_ids: list[str] = []
    if not bool(getattr(args, "dry_run", False)):
        for item in matched:
            identifier = str(item["id"])
            store[identifier] = _merge_record(store[identifier], {"revoked_at": _utc_now(), "status": "revoked", "enabled": False})
            revoked_ids.append(identifier)
        state_path = _save_resource_store(repo_root, "session", store)
    else:
        revoked_ids = [str(item["id"]) for item in matched]
        state_path = _state_path(repo_root, "session")
    return _emit_with_code(args, {"command": "session.revoke-all", "resource": "session", "revoked_ids": revoked_ids, "revoked_count": len(revoked_ids), "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(state_path)}, rc=0)


def handle_token_introspect(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "token")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": "token.introspect", "resource": "token", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "token"))}, rc=3)
    active = str(record.get("status")) not in {"revoked", "retired", "expired"} and not bool(record.get("revoked_at"))
    payload = _query_result_payload("token.introspect", "token", record=record, state_path=_state_path(repo_root, "token"), extras={"active": active})
    return _emit_with_code(args, payload, rc=0)


def handle_token_exchange(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    source_id = getattr(args, "id", None)
    if not source_id:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "token")
    source = store.get(source_id)
    if source is None:
        return _emit_with_code(args, {"command": "token.exchange", "resource": "token", "id": source_id, "error": "not-found", "state_path": str(_state_path(repo_root, "token"))}, rc=3)
    payload = _mutation_payload(args)
    new_id = str(payload.get("new_id") or f"{source_id}-xchg-{secrets.token_hex(4)}")
    record = _base_record("token", new_id, payload)
    record.update({"exchanged_from": source_id, "token_type": payload.get("token_type", "urn:ietf:params:oauth:token-type:access_token")})
    if not bool(getattr(args, "dry_run", False)):
        store[new_id] = record
        state_path = _save_resource_store(repo_root, "token", store)
    else:
        state_path = _state_path(repo_root, "token")
    return _emit_with_code(args, _mutation_result_payload("token.exchange", "token", record, state_path, mutation="exchange", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"source_id": source_id}), rc=0)


def _jwks_public_keys(store: dict[str, dict[str, Any]], *, include_secrets: bool = False) -> list[dict[str, Any]]:
    keys: list[dict[str, Any]] = []
    for record in _sort_items(list(store.values()), "id"):
        if str(record.get("status")) == "retired":
            continue
        key = {
            "kid": record.get("kid") or record.get("id"),
            "kty": record.get("kty", "OKP"),
            "use": record.get("use", "sig"),
            "alg": record.get("alg") or ("EdDSA" if record.get("kty", "OKP") == "OKP" else None),
            "crv": record.get("curve") if record.get("kty") in {"EC", "OKP"} else None,
            "status": record.get("status", "active"),
        }
        if include_secrets and record.get("material") is not None:
            key["material"] = record["material"]
        keys.append({k: v for k, v in key.items() if v is not None})
    return keys


def _jwks_publish_path(repo_root: Path, profile: str) -> Path:
    return repo_root / "dist" / "jwks" / profile / "jwks.json"


def _publish_jwks(repo_root: Path, profile: str, *, include_secrets: bool = False) -> Path:
    store = _resource_store(repo_root, "keys")
    payload = {"keys": _jwks_public_keys(store, include_secrets=include_secrets)}
    path = _jwks_publish_path(repo_root, profile)
    _write_json(path, payload)
    return path


def handle_keys_generate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "keys")
    payload = _mutation_payload(args)
    identifier = _record_identifier(args, payload, "key")
    key_id = str(getattr(args, "kid", None) or payload.get("kid") or identifier)
    record = _base_record("keys", identifier, payload)
    record.update({
        "kid": key_id,
        "alg": getattr(args, "alg", None) or payload.get("alg") or ("EdDSA" if (getattr(args, "kty", "OKP") or payload.get("kty")) == "OKP" else "RS256"),
        "use": getattr(args, "use", None) or payload.get("use") or "sig",
        "kty": getattr(args, "kty", None) or payload.get("kty") or "OKP",
        "curve": getattr(args, "curve", None) or payload.get("curve") or "Ed25519",
        "status": "active" if bool(getattr(args, "activate", False)) else "staged",
        "material": {"reference": f"generated:{key_id}:{secrets.token_hex(8)}"},
        "retire_after": getattr(args, "retire_after", None) or payload.get("retire_after"),
    })
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = record
        state_path = _save_resource_store(repo_root, "keys", store)
        published_path = str(_publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=False).relative_to(repo_root)) if bool(getattr(args, "publish", False)) else None
    else:
        state_path = _state_path(repo_root, "keys")
        published_path = None
    return _emit_with_code(args, _mutation_result_payload("keys.generate", "keys", record, state_path, mutation="generate", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"published_jwks": published_path}), rc=0)


def handle_keys_import(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "keys")
    source_path = getattr(args, "from_file", None) or getattr(args, "input_path", None)
    if not source_path:
        raise SystemExit("--from-file or --input is required")
    payload = _load_structured_file(Path(source_path).resolve())
    identifier = _record_identifier(args, payload, "key")
    record = _base_record("keys", identifier, payload)
    record.update({
        "kid": payload.get("kid") or getattr(args, "kid", None) or identifier,
        "alg": payload.get("alg") or getattr(args, "alg", None),
        "use": payload.get("use") or getattr(args, "use", None) or "sig",
        "kty": payload.get("kty") or getattr(args, "kty", None) or "OKP",
        "curve": payload.get("crv") or payload.get("curve") or getattr(args, "curve", None),
        "status": "active" if bool(getattr(args, "activate", False)) else payload.get("status", "staged"),
        "material": payload,
    })
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = record
        state_path = _save_resource_store(repo_root, "keys", store)
        published_path = str(_publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=False).relative_to(repo_root)) if bool(getattr(args, "publish", False)) else None
    else:
        state_path = _state_path(repo_root, "keys")
        published_path = None
    return _emit_with_code(args, _mutation_result_payload("keys.import", "keys", record, state_path, mutation="import", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"source": str(Path(source_path).resolve()), "published_jwks": published_path}), rc=0)


def handle_keys_export(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "keys")
    identifier = getattr(args, "id", None)
    if identifier:
        record = store.get(identifier)
        if record is None:
            return _emit_with_code(args, {"command": "keys.export", "resource": "keys", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "keys"))}, rc=3)
        export_payload: Any = record
    else:
        export_payload = {"keys": list(_sort_items(list(store.values()), "id"))}
    checksum_value = hashlib.sha256(json.dumps(export_payload, sort_keys=True).encode("utf-8")).hexdigest()
    if getattr(args, "output", None):
        out_path = Path(args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if getattr(args, "format", "json") == "yaml":
            out_path.write_text(yaml.safe_dump(export_payload, sort_keys=False), encoding="utf-8")
        else:
            out_path.write_text(json.dumps(export_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        output_path = str(out_path)
    else:
        output_path = None
    return _emit_with_code(args, _query_result_payload("keys.export", "keys", record=export_payload if identifier else None, items=export_payload.get("keys") if isinstance(export_payload, dict) and "keys" in export_payload else None, total=len(export_payload.get("keys", [])) if isinstance(export_payload, dict) and "keys" in export_payload else None, state_path=_state_path(repo_root, "keys"), extras={"checksum": checksum_value, "output_path": output_path}), rc=0)


def handle_keys_rotate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    store = _resource_store(repo_root, "keys")
    target_id = getattr(args, "id", None)
    if target_id is None:
        active = [item for item in store.values() if str(item.get("status")) == "active"]
        if not active:
            return _emit_with_code(args, {"command": "keys.rotate", "resource": "keys", "error": "no-active-key", "state_path": str(_state_path(repo_root, "keys"))}, rc=3)
        target_id = str(_sort_items(active, "updated_at")[0]["id"])
    current = store.get(target_id)
    if current is None:
        return _emit_with_code(args, {"command": "keys.rotate", "resource": "keys", "id": target_id, "error": "not-found", "state_path": str(_state_path(repo_root, "keys"))}, rc=3)
    successor_id = f"{target_id}-rotated-{secrets.token_hex(4)}"
    successor = _base_record("keys", successor_id, {})
    successor.update({
        "kid": getattr(args, "kid", None) or successor_id,
        "alg": getattr(args, "alg", None) or current.get("alg"),
        "use": getattr(args, "use", None) or current.get("use"),
        "kty": getattr(args, "kty", None) or current.get("kty"),
        "curve": getattr(args, "curve", None) or current.get("curve"),
        "status": "active" if bool(getattr(args, "activate", True)) else "staged",
        "material": {"reference": f"rotated:{successor_id}:{secrets.token_hex(8)}"},
        "rotates": target_id,
        "retire_after": getattr(args, "retire_after", None) or current.get("retire_after"),
    })
    retired = _merge_record(current, {"status": "retired", "retired_at": _utc_now()})
    if not bool(getattr(args, "dry_run", False)):
        store[target_id] = retired
        store[successor_id] = successor
        state_path = _save_resource_store(repo_root, "keys", store)
        published_path = str(_publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=False).relative_to(repo_root)) if bool(getattr(args, "publish", False)) else None
    else:
        state_path = _state_path(repo_root, "keys")
        published_path = None
    return _emit_with_code(args, {"command": "keys.rotate", "resource": "keys", "previous_record": retired, "record": successor, "dry_run": bool(getattr(args, "dry_run", False)), "persisted": not bool(getattr(args, "dry_run", False)), "state_path": str(state_path), "published_jwks": published_path}, rc=0)


def handle_keys_retire(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    identifier = getattr(args, "id", None)
    if not identifier:
        raise SystemExit("--id is required")
    store = _resource_store(repo_root, "keys")
    record = store.get(identifier)
    if record is None:
        return _emit_with_code(args, {"command": "keys.retire", "resource": "keys", "id": identifier, "error": "not-found", "state_path": str(_state_path(repo_root, "keys"))}, rc=3)
    patched = _merge_record(record, {"status": "retired", "retired_at": _utc_now()})
    if not bool(getattr(args, "dry_run", False)):
        store[identifier] = patched
        state_path = _save_resource_store(repo_root, "keys", store)
        published_path = str(_publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=False).relative_to(repo_root)) if bool(getattr(args, "publish", False)) else None
    else:
        state_path = _state_path(repo_root, "keys")
        published_path = None
    return _emit_with_code(args, _mutation_result_payload("keys.retire", "keys", patched, state_path, mutation="retire", persisted=not bool(getattr(args, "dry_run", False)), dry_run=bool(getattr(args, "dry_run", False)), extras={"published_jwks": published_path}), rc=0)


def handle_keys_publish_jwks(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    include_secrets = bool(getattr(args, "include_secrets", False)) and not bool(getattr(args, "redact", False))
    path = _publish_jwks(repo_root, getattr(args, "profile", "baseline"), include_secrets=include_secrets)
    payload = json.loads(path.read_text(encoding="utf-8"))
    checksum_value = hashlib.sha256(path.read_bytes()).hexdigest()
    if getattr(args, "output", None):
        out_path = Path(args.output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if getattr(args, "format", "json") == "yaml":
            out_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        else:
            out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        emitted_path = str(out_path)
    else:
        emitted_path = str(path)
    return _emit_with_code(args, {"command": "keys.publish-jwks", "resource": "keys", "jwks": payload, "published_path": emitted_path, "checksum": checksum_value, "state_path": str(_state_path(repo_root, "keys"))}, rc=0)


def handle_discovery_show(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    profile = getattr(args, "profile", "baseline")
    discovery_root = repo_root / "specs" / "discovery" / "profiles" / profile
    payload = {"command": "discovery.show", "resource": "discovery", "profile": profile, "paths": {}, "documents": {}}
    for name in ("openid-configuration.json", "oauth-authorization-server.json", "oauth-protected-resource.json"):
        path = discovery_root / name
        if path.exists():
            payload["paths"][name] = str(path.relative_to(repo_root))
            payload["documents"][name] = json.loads(path.read_text(encoding="utf-8"))
    payload["state_path"] = str(_state_path(repo_root, "discovery"))
    return _emit_with_code(args, payload, rc=0)


def handle_discovery_validate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    openapi = validate_openapi_contract(repo_root)
    openrpc = validate_openrpc_contract(repo_root)
    profile = getattr(args, "profile", "baseline")
    discovery_root = repo_root / "specs" / "discovery" / "profiles" / profile
    required = [discovery_root / "openid-configuration.json", discovery_root / "oauth-authorization-server.json", discovery_root / "oauth-protected-resource.json"]
    missing = [str(path.relative_to(repo_root)) for path in required if not path.exists()]
    passed = openapi.passed and openrpc.passed and not missing
    payload = {
        "command": "discovery.validate",
        "resource": "discovery",
        "passed": passed,
        "summary": {
            "openapi_passed": openapi.passed,
            "openrpc_passed": openrpc.passed,
            "missing_discovery_files": missing,
        },
        "failures": missing,
        "state_path": str(_state_path(repo_root, "discovery")),
    }
    return _emit_with_code(args, payload, rc=0 if passed else 1)


def handle_discovery_publish(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    profile = getattr(args, "profile", "baseline")
    source_root = repo_root / "specs" / "discovery" / "profiles" / profile
    destination_root = Path(getattr(args, "output", None)).resolve() if getattr(args, "output", None) else (repo_root / "dist" / "discovery" / profile)
    destination_root.mkdir(parents=True, exist_ok=True)
    published: list[str] = []
    for name in ("openid-configuration.json", "oauth-authorization-server.json", "oauth-protected-resource.json"):
        source = source_root / name
        if source.exists() and not bool(getattr(args, "dry_run", False)):
            target = destination_root / name
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            published.append(str(target))
        elif source.exists():
            published.append(str((destination_root / name)))
    status_path = _state_path(repo_root, "discovery")
    if not bool(getattr(args, "dry_run", False)):
        _write_json(status_path, {"profile": profile, "published_at": _utc_now(), "published": published})
    return _emit_with_code(args, {"command": "discovery.publish", "resource": "discovery", "profile": profile, "published": published, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(status_path)}, rc=0)


def _json_diff(current: Any, baseline: Any, prefix: str = "") -> list[dict[str, Any]]:
    diffs: list[dict[str, Any]] = []
    if isinstance(current, dict) and isinstance(baseline, dict):
        keys = sorted(set(current) | set(baseline))
        for key in keys:
            new_prefix = f"{prefix}.{key}" if prefix else key
            if key not in baseline:
                diffs.append({"path": new_prefix, "change": "added", "value": current[key]})
            elif key not in current:
                diffs.append({"path": new_prefix, "change": "removed", "value": baseline[key]})
            else:
                diffs.extend(_json_diff(current[key], baseline[key], new_prefix))
        return diffs
    if current != baseline:
        diffs.append({"path": prefix or "$", "change": "changed", "current": current, "baseline": baseline})
    return diffs


def handle_discovery_diff(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    profile = getattr(args, "profile", "baseline")
    current_path = repo_root / "specs" / "discovery" / "profiles" / profile / "openid-configuration.json"
    if not current_path.exists():
        return _emit_with_code(args, {"command": "discovery.diff", "resource": "discovery", "error": "missing-current-discovery", "state_path": str(_state_path(repo_root, "discovery"))}, rc=1)
    current = json.loads(current_path.read_text(encoding="utf-8"))
    baseline_path = Path(getattr(args, "input_path", None)).resolve() if getattr(args, "input_path", None) else (repo_root / "dist" / "discovery" / profile / "openid-configuration.json")
    baseline = json.loads(baseline_path.read_text(encoding="utf-8")) if baseline_path.exists() else {}
    diffs = _json_diff(current, baseline)
    return _emit_with_code(args, {"command": "discovery.diff", "resource": "discovery", "profile": profile, "current_path": str(current_path.relative_to(repo_root)), "baseline_path": str(baseline_path) if baseline_path.exists() else None, "diffs": diffs, "state_path": str(_state_path(repo_root, "discovery"))}, rc=0)


def _portability_status_path(repo_root: Path, resource: str) -> Path:
    return _state_path(repo_root, resource)


def _export_payload(repo_root: Path) -> dict[str, Any]:
    resources = {}
    for resource in ("tenant", "client", "identity", "flow", "session", "token", "keys"):
        resources[resource] = _resource_store(repo_root, resource)
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "exported_at": _utc_now(),
        "resources": resources,
    }


def handle_import_validate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    source_path = getattr(args, "input_path", None)
    if not source_path:
        raise SystemExit("--input is required")
    path = Path(source_path).resolve()
    if not path.exists():
        return _emit_with_code(args, {"command": "import.validate", "resource": "import", "passed": False, "failures": [f"missing input: {path}"], "state_path": str(_portability_status_path(repo_root, "import"))}, rc=1)
    payload = _load_structured_file(path)
    checksum_value = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = getattr(args, "checksum", None)
    passed = "resources" in payload and (expected in {None, checksum_value})
    failures = [] if passed else (["input payload does not contain resources"] if "resources" not in payload else ["checksum mismatch"])
    return _emit_with_code(args, {"command": "import.validate", "resource": "import", "passed": passed, "summary": {"checksum": checksum_value}, "failures": failures, "state_path": str(_portability_status_path(repo_root, "import"))}, rc=0 if passed else 1)


def handle_import_run(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    source_path = getattr(args, "input_path", None)
    if not source_path:
        raise SystemExit("--input is required")
    path = Path(source_path).resolve()
    payload = _load_structured_file(path)
    resources = payload.get("resources", {}) if isinstance(payload, dict) else {}
    applied_resources: list[str] = []
    if not bool(getattr(args, "dry_run", False)):
        for resource, store in resources.items():
            if isinstance(store, dict):
                _save_resource_store(repo_root, resource, store)
                applied_resources.append(resource)
        _write_json(_portability_status_path(repo_root, "import"), {"last_run_at": _utc_now(), "input": str(path), "applied_resources": applied_resources})
    else:
        applied_resources = sorted(resources)
    return _emit_with_code(args, {"command": "import.run", "resource": "import", "input": str(path), "applied_resources": applied_resources, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(_portability_status_path(repo_root, "import"))}, rc=0)


def handle_import_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    status = _load_jsonish(_portability_status_path(repo_root, "import"), default={})
    return _emit_with_code(args, {"command": "import.status", "resource": "import", "record": status, "state_path": str(_portability_status_path(repo_root, "import"))}, rc=0)


def handle_export_validate(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    payload = _export_payload(repo_root)
    checksum_value = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    expected = getattr(args, "checksum", None)
    passed = expected in {None, checksum_value}
    failures = [] if passed else ["checksum mismatch"]
    return _emit_with_code(args, {"command": "export.validate", "resource": "export", "passed": passed, "summary": {"checksum": checksum_value, "resource_count": len(payload["resources"])}, "failures": failures, "state_path": str(_portability_status_path(repo_root, "export"))}, rc=0 if passed else 1)


def handle_export_run(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    payload = _export_payload(repo_root)
    output_path = Path(getattr(args, "output", None)).resolve() if getattr(args, "output", None) else (repo_root / "dist" / "operator-export" / f"export-{getattr(args, 'profile', 'baseline')}.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    checksum_value = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    if not bool(getattr(args, "dry_run", False)):
        if getattr(args, "format", "json") == "yaml":
            output_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        else:
            output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _write_json(_portability_status_path(repo_root, "export"), {"last_run_at": _utc_now(), "output": str(output_path), "checksum": checksum_value})
    return _emit_with_code(args, {"command": "export.run", "resource": "export", "output": str(output_path), "checksum": checksum_value, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(_portability_status_path(repo_root, "export"))}, rc=0)


def handle_export_status(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    status = _load_jsonish(_portability_status_path(repo_root, "export"), default={})
    return _emit_with_code(args, {"command": "export.status", "resource": "export", "record": status, "state_path": str(_portability_status_path(repo_root, "export"))}, rc=0)


def handle_bootstrap_apply(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = Path(args.bundle_dir).resolve() if args.bundle_dir else (repo_root / "dist" / "bootstrap" / deployment.profile)
    bundle_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = bundle_dir / "deployment.json"
    manifest_path.write_text(json.dumps(deployment.to_manifest(), indent=2) + "\n", encoding="utf-8")
    write_effective_claims_manifest(repo_root, deployment, profile_label=deployment.profile)
    write_effective_evidence_manifest(repo_root, deployment, profile_label=deployment.profile)
    write_openapi_contract(repo_root, deployment, profile_label=deployment.profile)
    write_openrpc_contract(repo_root, deployment, profile_label=deployment.profile)
    status_path = _portability_status_path(repo_root, "bootstrap")
    record = {"applied_at": _utc_now(), "profile": deployment.profile, "bundle_dir": str(bundle_dir.relative_to(repo_root)), "manifest": str(manifest_path.relative_to(repo_root))}
    if not bool(getattr(args, "dry_run", False)):
        _write_json(status_path, record)
    return _emit_with_code(args, {"command": "bootstrap.apply", "record": record, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(status_path)}, rc=0)


def handle_bootstrap_verify(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    deployment = _resolved_from_args(args)
    bundle_dir = repo_root / "dist" / "bootstrap" / deployment.profile
    required = [bundle_dir / "deployment.json", repo_root / "compliance" / "claims" / f"effective-target-claims.{deployment.profile}.yaml", repo_root / "compliance" / "evidence" / f"effective-release-evidence.{deployment.profile}.yaml"]
    missing = [str(path.relative_to(repo_root)) for path in required if not path.exists()]
    passed = not missing
    return _emit_with_code(args, {"command": "bootstrap.verify", "passed": passed, "summary": {"bundle_dir": str(bundle_dir.relative_to(repo_root)), "missing": missing}, "failures": missing, "state_path": str(_portability_status_path(repo_root, "bootstrap"))}, rc=0 if passed else 1)


def handle_migrate_apply(args: Any) -> int:
    repo_root = _repo_root(args.repo_root)
    plan = yaml.safe_load((repo_root / "compliance" / "mappings" / "current-to-target-paths.yaml").read_text(encoding="utf-8"))
    status_path = _portability_status_path(repo_root, "migrate")
    record = {"applied_at": _utc_now(), "plan_summary": plan.get("summary", {}), "moved_paths": plan.get("target_paths", [])}
    if not bool(getattr(args, "dry_run", False)):
        _write_json(status_path, record)
    return _emit_with_code(args, {"command": "migrate.apply", "record": record, "dry_run": bool(getattr(args, "dry_run", False)), "state_path": str(status_path)}, rc=0)


def _generic_resource_handler(resource: str, action: str):
    def _handler(args: Any) -> int:
        if action == "create":
            return _handle_stateful_create(args, resource)
        if action == "update":
            return _handle_stateful_update(args, resource)
        if action == "delete":
            return _handle_stateful_delete(args, resource)
        if action == "get":
            return _handle_stateful_get(args, resource)
        if action == "list":
            return _handle_stateful_list(args, resource)
        if action == "enable":
            return _toggle_enabled(args, resource, enabled=True)
        if action == "disable":
            return _toggle_enabled(args, resource, enabled=False)
        raise KeyError(f"Unsupported generic resource action: {resource}.{action}")

    return _handler


HANDLER_MAP = {
    "serve": handle_serve,
    "verify": handle_verify,
    "gate": handle_gate,
    "spec.generate": handle_spec_generate,
    "spec.validate": handle_spec_validate,
    "spec.diff": handle_spec_diff,
    "spec.report": handle_spec_report,
    "claims.lint": handle_claims_lint,
    "claims.show": handle_claims_show,
    "claims.status": handle_claims_status,
    "evidence.bundle": handle_evidence_bundle,
    "evidence.status": handle_evidence_status,
    "evidence.verify": handle_evidence_verify,
    "evidence.peer_status": handle_evidence_peer_status,
    "evidence.peer_execute": handle_evidence_peer_execute,
    "adr.list": handle_adr_list,
    "adr.show": handle_adr_show,
    "adr.new": handle_adr_new,
    "adr.index": handle_adr_index,
    "doctor": handle_doctor,
    "bootstrap.status": handle_bootstrap_status,
    "bootstrap.manifest": handle_bootstrap_manifest,
    "bootstrap.apply": handle_bootstrap_apply,
    "bootstrap.verify": handle_bootstrap_verify,
    "migrate.status": handle_migrate_status,
    "migrate.plan": handle_migrate_plan,
    "migrate.apply": handle_migrate_apply,
    "migrate.verify": handle_migrate_verify,
    "release.bundle": handle_release_bundle,
    "release.sign": handle_release_sign,
    "release.verify": handle_release_verify,
    "release.status": handle_release_status,
    "release.recertify": handle_release_recertify,
    "client.rotate_secret": handle_client_rotate_secret,
    "identity.set_password": handle_identity_set_password,
    "identity.lock": lambda args: _lock_identity(args, True),
    "identity.unlock": lambda args: _lock_identity(args, False),
    "session.revoke": lambda args: _revoke_resource(args, "session"),
    "session.revoke_all": handle_session_revoke_all,
    "token.introspect": handle_token_introspect,
    "token.revoke": lambda args: _revoke_resource(args, "token"),
    "token.exchange": handle_token_exchange,
    "keys.generate": handle_keys_generate,
    "keys.import": handle_keys_import,
    "keys.export": handle_keys_export,
    "keys.rotate": handle_keys_rotate,
    "keys.retire": handle_keys_retire,
    "keys.publish_jwks": handle_keys_publish_jwks,
    "discovery.show": handle_discovery_show,
    "discovery.validate": handle_discovery_validate,
    "discovery.publish": handle_discovery_publish,
    "discovery.diff": handle_discovery_diff,
    "import.validate": handle_import_validate,
    "import.run": handle_import_run,
    "import.status": handle_import_status,
    "export.validate": handle_export_validate,
    "export.run": handle_export_run,
    "export.status": handle_export_status,
}
for resource in ("tenant", "client", "identity", "flow"):
    for action in ("create", "update", "delete", "get", "list", "enable", "disable"):
        HANDLER_MAP[f"{resource}.{action}"] = _generic_resource_handler(resource, action)
for resource in ("session", "token"):
    for action in ("get", "list"):
        HANDLER_MAP[f"{resource}.{action}"] = _generic_resource_handler(resource, action)
for action in ("get", "list", "delete"):
    HANDLER_MAP[f"keys.{action}"] = _generic_resource_handler("keys", action)


__all__ = ["HANDLER_MAP"]

# -----------------------------------------------------------------------------
# Service-layer overrides
# -----------------------------------------------------------------------------

from tigrbl_auth.services._operator_store import OperationContext, TransactionResult, ArtifactResult
from tigrbl_auth.services.operator_service import (
    OperatorStateError,
    create_resource as _svc_create_resource,
    delete_resource as _svc_delete_resource,
    get_resource as _svc_get_resource,
    list_resource_result as _svc_list_resource_result,
    rotate_client_secret as _svc_rotate_client_secret,
    toggle_resource as _svc_toggle_resource,
    update_resource as _svc_update_resource,
)
from tigrbl_auth.services.key_management import (
    delete_operator_key_for_context,
    export_operator_key_for_context,
    generate_operator_key_for_context,
    get_operator_key_for_context,
    import_operator_key_for_context,
    list_operator_keys_for_context,
    publish_operator_jwks_for_context,
    retire_operator_key_for_context,
    rotate_operator_key_for_context,
)
from tigrbl_auth.services.identity_service import lock_identity as _svc_lock_identity, set_identity_password as _svc_set_identity_password
from tigrbl_auth.services.session_service import (
    exchange_token_for_context as _svc_exchange_token_for_context,
    get_session_for_context as _svc_get_session_for_context,
    get_token_for_context as _svc_get_token_for_context,
    introspect_token_for_context as _svc_introspect_token_for_context,
    list_sessions_for_context as _svc_list_sessions_for_context,
    list_tokens_for_context as _svc_list_tokens_for_context,
    revoke_all_sessions_for_context as _svc_revoke_all_sessions_for_context,
    revoke_all_tokens_for_context as _svc_revoke_all_tokens_for_context,
    revoke_session_for_context as _svc_revoke_session_for_context,
    revoke_token_for_context as _svc_revoke_token_for_context,
)
from tigrbl_auth.services.discovery_service import (
    diff_discovery as _svc_diff_discovery,
    publish_discovery as _svc_publish_discovery,
    show_discovery as _svc_show_discovery,
    validate_discovery as _svc_validate_discovery,
)
from tigrbl_auth.services.import_export_service import (
    export_status as _svc_export_status,
    import_status as _svc_import_status,
    run_export_file as _svc_run_export_file,
    run_import_file as _svc_run_import_file,
    validate_export_plan as _svc_validate_export_plan,
    validate_import_file as _svc_validate_import_file,
)


def _svc_context(args: Any, resource: str, command: str | None = None) -> OperationContext:
    return OperationContext(
        repo_root=_repo_root(getattr(args, "repo_root", None)),
        command=command or f"{resource}.{getattr(args, 'action', '')}".strip("."),
        resource=resource,
        dry_run=bool(getattr(args, "dry_run", False)),
        actor=getattr(args, "actor", None) or "system",
        profile=getattr(args, "profile", None),
        tenant=getattr(args, "tenant", None),
        issuer=getattr(args, "issuer", None),
    )


def _svc_payload(result: Any) -> dict[str, Any]:
    if isinstance(result, (TransactionResult, ArtifactResult)):
        return result.to_payload()
    if isinstance(result, dict):
        return result
    return {"result": result}


def _svc_emit(args: Any, result: Any, rc: int = 0) -> int:
    return _emit_with_code(args, _svc_payload(result), rc=rc)


def _svc_failure(args: Any, context: OperationContext, exc: OperatorStateError) -> int:
    return _emit_with_code(args, exc.to_payload(context.command, context.resource), rc=exc.code)


def _svc_patch(args: Any) -> dict[str, Any]:
    return _mutation_payload(args)


def _handle_service_create(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.create")
    patch = _svc_patch(args)
    record_id = getattr(args, "id", None) or patch.get("id")
    if_exists = str(getattr(args, "if_exists", "error")).replace("fail", "error")
    if if_exists == "replace":
        if_exists = "replace"
    elif if_exists not in {"error", "skip", "update", "replace"}:
        if_exists = "error"
    try:
        result = _svc_create_resource(context, record_id=record_id, patch=patch, if_exists=if_exists)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_update(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.update")
    patch = _svc_patch(args)
    record_id = getattr(args, "id", None) or patch.get("id")
    if_missing = str(getattr(args, "if_missing", "error")).replace("fail", "error")
    try:
        result = _svc_update_resource(context, record_id=record_id, patch=patch, if_missing=if_missing)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_delete(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.delete")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_delete_resource(context, record_id=record_id, if_missing="error")
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_get(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.get")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        if resource == "session":
            result = _svc_get_session_for_context(context, record_id=record_id)
        elif resource == "token":
            result = _svc_get_token_for_context(context, record_id=record_id)
        elif resource == "keys":
            result = get_operator_key_for_context(context, record_id=record_id)
        else:
            result = _svc_get_resource(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_list(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.list")
    kwargs = {
        "status_filter": getattr(args, "status_filter", None),
        "filter_expr": getattr(args, "filter", None),
        "sort": str(getattr(args, "sort", "id")),
        "offset": int(getattr(args, "offset", 0)),
        "limit": int(getattr(args, "limit", 50)),
    }
    try:
        if resource == "session":
            result = _svc_list_sessions_for_context(context, **kwargs)
        elif resource == "token":
            result = _svc_list_tokens_for_context(context, **kwargs)
        elif resource == "keys":
            result = list_operator_keys_for_context(context, **kwargs)
        else:
            result = _svc_list_resource_result(context, **kwargs)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _handle_service_toggle(args: Any, resource: str, *, enabled: bool) -> int:
    context = _svc_context(args, resource, f"{resource}.{'enable' if enabled else 'disable'}")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_toggle_resource(context, record_id=record_id, enabled=enabled)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _generic_resource_handler(resource: str, action: str):
    def _handler(args: Any) -> int:
        if action == "create":
            return _handle_service_create(args, resource)
        if action == "update":
            return _handle_service_update(args, resource)
        if action == "delete":
            return _handle_service_delete(args, resource)
        if action == "get":
            return _handle_service_get(args, resource)
        if action == "list":
            return _handle_service_list(args, resource)
        if action == "enable":
            return _handle_service_toggle(args, resource, enabled=True)
        if action == "disable":
            return _handle_service_toggle(args, resource, enabled=False)
        raise KeyError(f"Unsupported generic resource action: {resource}.{action}")

    return _handler


def handle_client_rotate_secret(args: Any) -> int:
    context = _svc_context(args, "client", "client.rotate-secret")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_rotate_client_secret(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_identity_set_password(args: Any) -> int:
    context = _svc_context(args, "identity", "identity.set-password")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    patch = _svc_patch(args)
    try:
        result = _svc_set_identity_password(context, record_id=record_id, password=patch.get("password"))
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _lock_identity(args: Any, locked: bool) -> int:
    context = _svc_context(args, "identity", f"identity.{'lock' if locked else 'unlock'}")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_lock_identity(context, record_id=record_id, locked=locked)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def _revoke_resource(args: Any, resource: str) -> int:
    context = _svc_context(args, resource, f"{resource}.revoke")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_revoke_session_for_context(context, record_id=record_id) if resource == "session" else _svc_revoke_token_for_context(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_session_revoke_all(args: Any) -> int:
    context = _svc_context(args, "session", "session.revoke-all")
    try:
        result = _svc_revoke_all_sessions_for_context(context, status_filter=getattr(args, "status_filter", None), filter_expr=getattr(args, "filter", None))
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_token_introspect(args: Any) -> int:
    context = _svc_context(args, "token", "token.introspect")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = _svc_introspect_token_for_context(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_token_exchange(args: Any) -> int:
    context = _svc_context(args, "token", "token.exchange")
    patch = _svc_patch(args)
    try:
        result = _svc_exchange_token_for_context(
            context,
            subject_token=getattr(args, "subject_token", None) or patch.get("subject_token"),
            requested_token_type=getattr(args, "requested_token_type", None) or patch.get("requested_token_type"),
            audience=getattr(args, "audience", None) or patch.get("audience"),
            resource=getattr(args, "resource", None) or patch.get("resource"),
            actor_token=getattr(args, "actor_token", None) or patch.get("actor_token"),
            extras=patch,
        )
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_generate(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.generate")
    patch = _svc_patch(args)
    for source, target in (("kid", "kid"), ("alg", "alg"), ("use", "use"), ("kty", "kty"), ("curve", "curve")):
        value = getattr(args, source, None)
        if value is not None:
            patch[target] = value
    if bool(getattr(args, "activate", False)):
        patch["status"] = "active"
        patch["enabled"] = True
    try:
        result = generate_operator_key_for_context(context, patch=patch)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_import(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.import")
    patch = _svc_patch(args)
    try:
        result = import_operator_key_for_context(context, patch=patch)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_export(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.export")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = export_operator_key_for_context(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_rotate(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.rotate")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = rotate_operator_key_for_context(context, record_id=record_id)
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_retire(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.retire")
    record_id = getattr(args, "id", None)
    if not record_id:
        raise SystemExit("--id is required")
    try:
        result = retire_operator_key_for_context(context, record_id=record_id, retire_after=getattr(args, "retire_after", None))
    except OperatorStateError as exc:
        return _svc_failure(args, context, exc)
    return _svc_emit(args, result)


def handle_keys_publish_jwks(args: Any) -> int:
    context = _svc_context(args, "keys", "keys.publish-jwks")
    result = publish_operator_jwks_for_context(context, output_path=getattr(args, "output", None))
    return _svc_emit(args, result)


def handle_discovery_show(args: Any) -> int:
    payload = {"command": "discovery.show", **_svc_show_discovery(_repo_root(getattr(args, "repo_root", None)), profile=getattr(args, "profile", None))}
    return _emit(args, payload)


def handle_discovery_validate(args: Any) -> int:
    payload = {"command": "discovery.validate", **_svc_validate_discovery(_repo_root(getattr(args, "repo_root", None)), profile=getattr(args, "profile", None))}
    return _emit(args, payload)


def handle_discovery_publish(args: Any) -> int:
    context = _svc_context(args, "discovery", "discovery.publish")
    result = _svc_publish_discovery(context, output_dir=Path(getattr(args, "output", None)).resolve() if getattr(args, "output", None) else None)
    return _svc_emit(args, result)


def handle_discovery_diff(args: Any) -> int:
    payload = {"command": "discovery.diff", **_svc_diff_discovery(_repo_root(getattr(args, "repo_root", None)), left_profile=getattr(args, "left_profile", None) or getattr(args, "profile", None), right_profile=getattr(args, "right_profile", None))}
    return _emit(args, payload)


def handle_import_validate(args: Any) -> int:
    input_path = getattr(args, "input", None) or getattr(args, "from_file", None)
    if not input_path:
        raise SystemExit("--input is required")
    payload = {"command": "import.validate", **_svc_validate_import_file(Path(input_path).resolve())}
    return _emit(args, payload)


def handle_import_run(args: Any) -> int:
    input_path = getattr(args, "input", None) or getattr(args, "from_file", None)
    if not input_path:
        raise SystemExit("--input is required")
    context = _svc_context(args, "import", "import.run")
    result = _svc_run_import_file(context, path=Path(input_path).resolve())
    return _svc_emit(args, result)


def handle_import_status(args: Any) -> int:
    payload = {"command": "import.status", **_svc_import_status(_repo_root(getattr(args, "repo_root", None)))}
    return _emit(args, payload)


def handle_export_validate(args: Any) -> int:
    context = _svc_context(args, "export", "export.validate")
    payload = {"command": "export.validate", **_svc_validate_export_plan(context, redact=bool(getattr(args, "redact", False)))}
    return _emit(args, payload)


def handle_export_run(args: Any) -> int:
    output_path = Path(getattr(args, "output", None) or (_repo_root(getattr(args, "repo_root", None)) / "dist" / "exports" / "export.json")).resolve()
    context = _svc_context(args, "export", "export.run")
    result = _svc_run_export_file(context, path=output_path, redact=bool(getattr(args, "redact", False)))
    return _svc_emit(args, result)


def handle_export_status(args: Any) -> int:
    payload = {"command": "export.status", **_svc_export_status(_repo_root(getattr(args, "repo_root", None)))}
    return _emit(args, payload)


# refresh the dispatch table so surface variants resolve to the service layer
HANDLER_MAP.update(
    {
        "client.rotate_secret": handle_client_rotate_secret,
        "identity.set_password": handle_identity_set_password,
        "identity.lock": lambda args: _lock_identity(args, True),
        "identity.unlock": lambda args: _lock_identity(args, False),
        "session.revoke": lambda args: _revoke_resource(args, "session"),
        "session.revoke_all": handle_session_revoke_all,
        "token.introspect": handle_token_introspect,
        "token.revoke": lambda args: _revoke_resource(args, "token"),
        "token.exchange": handle_token_exchange,
        "keys.generate": handle_keys_generate,
        "keys.import": handle_keys_import,
        "keys.export": handle_keys_export,
        "keys.rotate": handle_keys_rotate,
        "keys.retire": handle_keys_retire,
        "keys.publish_jwks": handle_keys_publish_jwks,
        "discovery.show": handle_discovery_show,
        "discovery.validate": handle_discovery_validate,
        "discovery.publish": handle_discovery_publish,
        "discovery.diff": handle_discovery_diff,
        "import.validate": handle_import_validate,
        "import.run": handle_import_run,
        "import.status": handle_import_status,
        "export.validate": handle_export_validate,
        "export.run": handle_export_run,
        "export.status": handle_export_status,
    }
)
for _resource in ("tenant", "client", "identity", "flow"):
    for _action in ("create", "update", "delete", "get", "list", "enable", "disable"):
        HANDLER_MAP[f"{_resource}.{_action}"] = _generic_resource_handler(_resource, _action)
for _resource in ("session", "token"):
    for _action in ("get", "list"):
        HANDLER_MAP[f"{_resource}.{_action}"] = _generic_resource_handler(_resource, _action)
for _action in ("get", "list", "delete"):
    HANDLER_MAP[f"keys.{_action}"] = _generic_resource_handler("keys", _action)

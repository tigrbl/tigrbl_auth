from __future__ import annotations

def write_runtime_profile_report(
    repo_root: Path,
    *,
    deployment: Any,
    environment: str = "development",
    host: str = "127.0.0.1",
    port: int = 8000,
    workers: int = 1,
    access_log: bool = True,
    lifespan: str = "auto",
    graceful_timeout: int = 30,
    report_dir: Path | None = None,
    enable_execution_probes: bool | None = None,
    report_mode: str | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)
    payload = build_runner_profile_report(
        repo_root,
        deployment=deployment,
        environment=environment,
        host=host,
        port=port,
        workers=workers,
        access_log=access_log,
        lifespan=lifespan,
        graceful_timeout=graceful_timeout,
        enable_execution_probes=enable_execution_probes,
        report_mode=report_mode,
    )
    payload = sanitize_local_paths(payload, repo_root)
    _write_json(report_dir / "runtime_profile_report.json", payload)
    lines = [
        "# Runtime Profile Report",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Deployment profile: `{payload['deployment_profile']}`",
        f"- Report mode: `{payload.get('report_mode', payload.get('summary', {}).get('source_mode', 'live-probe'))}`",
        f"- Validated artifact source: `{payload.get('validated_artifact_source')}`",
        f"- Application factory probe passed: `{payload['application_probe']['passed']}`",
        f"- Ready profiles: `{payload['summary']['ready_count']}`",
        f"- Missing profiles: `{payload['summary']['missing_count']}`",
        f"- Invalid profiles: `{payload['summary']['invalid_count']}`",
        f"- Application hash invariant: `{payload['summary']['application_hash_invariant']}`",
        f"- Pyproject requires-python: `{payload['summary']['pyproject_requires_python']}`",
        f"- Supported Python versions: `{', '.join(payload['summary']['supported_python_versions'])}`",
        f"- Placeholder-supported runners: `{payload['summary']['placeholder_supported_runner_count']}`",
        f"- Declared CI-installable runners: `{payload['summary']['declared_ci_installable_runner_count']}`",
        f"- Declared CI install/probe complete: `{payload['summary']['declared_ci_install_probe_complete']}`",
        f"- Execution probes enabled: `{payload['summary']['execution_probes_enabled']}`",
        f"- Surface probe passed: `{payload['summary']['surface_probe_passed']}`",
        f"- Surface probe endpoints: `{payload['summary']['surface_probe_endpoint_count']}`",
        f"- Serve-check passes: `{payload['summary']['serve_check_passed_count']}`",
        f"- Execution probe complete: `{payload['summary']['execution_probe_complete']}`",
        f"- Required runtime cells: `{payload['summary'].get('required_runtime_cell_count')}`",
        f"- Validated runtime cells present: `{payload['summary'].get('validated_runtime_cell_count')}`",
        f"- Validated runtime cells passed: `{payload['summary'].get('validated_runtime_cell_passed_count')}`",
        f"- Validated runtime matrix green: `{payload['summary'].get('validated_runtime_matrix_green')}`",
        "",
        "## Application Probe",
        "",
        f"- App factory: `{payload['application_probe'].get('app_factory', 'tigrbl_identity_server.api.app.build_app')}`",
        f"- Message: {payload['application_probe']['message']}",
        "",
        "## Surface Probe",
        "",
        f"- Executed: `{payload['surface_probe']['executed']}`",
        f"- Passed: `{payload['surface_probe']['passed']}`",
        f"- Message: {payload['surface_probe']['message']}",
        f"- Endpoint count: `{payload['surface_probe']['endpoint_count']}`",
        f"- Passed endpoints: `{payload['surface_probe']['passed_count']}`",
        f"- Failed endpoints: `{payload['surface_probe']['failed_count']}`",
        "",
        "## Runner Profiles",
        "",
    ]
    for item in payload["profiles"]:
        lines.extend(
            [
                f"### {item['display_name']} (`{item['name']}`)",
                "",
                f"- Status: `{item['status']}`",
                f"- Installed: `{item['installed']}`",
                f"- Module: `{item['available_module']}`",
                f"- Placeholder-supported: `{item.get('placeholder_supported')}`",
                f"- Declared CI-installable: `{item.get('declared_installable_from_repository')}`",
                f"- Serve check passed: `{item.get('serve_check', {}).get('passed')}`",
                f"- Serve check message: {item.get('serve_check', {}).get('message', '')}",
            ]
        )
        validated_matrix = item.get("validated_matrix") or {}
        if validated_matrix:
            lines.extend(
                [
                    f"- Validated matrix profile: `{validated_matrix.get('matrix_profile')}`",
                    f"- Expected identities: `{', '.join(validated_matrix.get('expected_identities', []))}`",
                    f"- Present identities: `{', '.join(validated_matrix.get('present_identities', []))}`",
                    f"- Passed identities: `{', '.join(validated_matrix.get('passed_identities', []))}`",
                    f"- Missing identities: `{', '.join(validated_matrix.get('missing_identities', []))}`",
                    f"- Failed identities: `{', '.join(validated_matrix.get('failed_identities', []))}`",
                ]
            )
        lines.append("")
    (report_dir / "runtime_profile_report.md").write_text("\n".join(lines), encoding="utf-8")
    return payload



def runtime_evidence_paths(repo_root: Path, runner: str) -> dict[str, Path]:
    stamp = _utc_timestamp()
    root = repo_root.resolve() / "dist" / "runtime-profiles" / runner
    root.mkdir(parents=True, exist_ok=True)
    return {
        "root": root,
        "startup": root / f"{stamp}-startup.json",
        "shutdown": root / f"{stamp}-shutdown.json",
    }


async def _serve_with_signal_handlers(
    *,
    adapter: Any,
    app: Any,
    plan: Any,
    startup_path: Path,
    shutdown_path: Path,
    startup_payload: dict[str, Any],
) -> int:
    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()
    signal_state: dict[str, Any] = {"received": []}
    startup_details: dict[str, Any] = {}

    def _request_shutdown(signame: str) -> None:
        signal_state["received"].append(signame)
        shutdown_event.set()

    registered: list[signal.Signals] = []
    for sig in (signal.SIGINT, signal.SIGTERM):
        with suppress(NotImplementedError, RuntimeError, ValueError):
            loop.add_signal_handler(sig, _request_shutdown, sig.name)
            registered.append(sig)

    def _startup_callback(details: dict[str, Any]) -> None:
        startup_details.update(details)
        payload = dict(startup_payload)
        payload["adapter_startup"] = dict(startup_details)
        payload["event"] = "runtime-starting"
        _write_json(startup_path, payload)

    if not startup_path.exists():
        _write_json(startup_path, dict(startup_payload, event="runtime-starting"))

    exit_code = 1
    failure: dict[str, str] | None = None
    try:
        exit_code = await adapter.serve(app, plan, shutdown_event=shutdown_event, startup_callback=_startup_callback)
    except KeyboardInterrupt:
        shutdown_event.set()
        exit_code = 130
    except Exception as exc:  # pragma: no cover - depends on selected runner runtime
        failure = _error_manifest(exc)
        exit_code = 1
    finally:
        for sig in registered:
            with suppress(NotImplementedError, RuntimeError, ValueError):
                loop.remove_signal_handler(sig)
        shutdown_payload = {
            "event": "runtime-stopped",
            "runner": plan.runner,
            "application_hash": plan.application_hash,
            "runtime_hash": plan.runtime_hash,
            "exit_code": exit_code,
            "signals": signal_state["received"],
            "adapter_startup": dict(startup_details),
        }
        if failure is not None:
            shutdown_payload["failure"] = failure
        _write_json(shutdown_path, shutdown_payload)
    return exit_code


def launch_runtime_profile(
    repo_root: Path,
    *,
    app: Any,
    plan: Any,
    adapter: Any,
    startup_payload: dict[str, Any],
    evidence_paths: dict[str, Path] | None = None,
) -> int:
    repo_root = repo_root.resolve()
    evidence_paths = evidence_paths or runtime_evidence_paths(repo_root, plan.runner)
    payload = dict(startup_payload)
    payload.setdefault(
        "runtime_evidence",
        {
            "startup": str(evidence_paths["startup"].relative_to(repo_root)),
            "shutdown": str(evidence_paths["shutdown"].relative_to(repo_root)),
        },
    )
    pid_path: Path | None = None
    if plan.pid_file:
        pid_path = Path(plan.pid_file).resolve()
        pid_path.parent.mkdir(parents=True, exist_ok=True)
        pid_path.write_text(f"{os.getpid()}\n", encoding="utf-8")
    try:
        return asyncio.run(
            _serve_with_signal_handlers(
                adapter=adapter,
                app=app,
                plan=plan,
                startup_path=evidence_paths["startup"],
                shutdown_path=evidence_paths["shutdown"],
                startup_payload=payload,
            )
        )
    finally:
        if pid_path is not None and pid_path.exists():
            pid_path.unlink()


__all__ = [
    "build_runner_profile_report",
    "launch_runtime_profile",
    "probe_application_factory",
    "probe_http_surface_endpoints",
    "probe_runner_serve_check",
    "run_runtime_foundation_check",
    "runtime_evidence_paths",
    "write_runtime_profile_report",
]

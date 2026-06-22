from __future__ import annotations


def _runtime_pyproject_manifest(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "pkgs" / "60-runtime" / "tigrbl-identity-runtime" / "pyproject.toml"
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _extras_consistency(repo_root: Path, dependency_manifest: dict[str, Any]) -> dict[str, Any]:
    optional = dependency_manifest["optional_dependencies"]
    runtime_manifest = _runtime_pyproject_manifest(repo_root)
    runtime_project = runtime_manifest.get("project", {}) if isinstance(runtime_manifest, dict) else {}
    runtime_version = str(runtime_project.get("version", ""))
    runtime_optional = {
        str(name): [_normalize_requirement(str(item)) for item in values]
        for name, values in (runtime_project.get("optional-dependencies") or {}).items()
    }
    expected_runtime_runner_extras = {
        "uvicorn": [_normalize_requirement("uvicorn[standard]==0.41.0")],
        "hypercorn": [_normalize_requirement("hypercorn==0.18.0")],
        "tigrcorn": [_normalize_requirement("tigrcorn==0.3.8; python_version >= '3.11'")],
        "servers": [
            _normalize_requirement("uvicorn[standard]==0.41.0"),
            _normalize_requirement("hypercorn==0.18.0"),
            _normalize_requirement("tigrcorn==0.3.8; python_version >= '3.11'"),
        ],
    }
    expected_root_runner_extras = {
        name: [_normalize_requirement(f"tigrbl-identity-runtime[{name}]=={runtime_version}")]
        for name in expected_runtime_runner_extras
    }
    mismatches: list[str] = []

    for name, expected in expected_runtime_runner_extras.items():
        if runtime_optional.get(name, []) != expected:
            mismatches.append(
                f"tigrbl-identity-runtime optional-dependencies.{name} does not match expected runner pins"
            )

    for name, expected in expected_root_runner_extras.items():
        if optional.get(name, []) != expected:
            mismatches.append(
                f"workspace optional-dependencies.{name} must delegate to tigrbl-identity-runtime[{name}]"
            )

    profile_extra_coverage: dict[str, dict[str, Any]] = {}
    for profile, details in PROFILE_TOGGLES.items():
        extras = [str(item) for item in details.get("extras", [])]
        missing = [extra for extra in extras if extra not in optional]
        profile_extra_coverage[profile] = {
            "extras": extras,
            "missing_extras": missing,
            "passed": not missing,
        }
        if missing:
            mismatches.append(
                f"profile {profile} references undeclared workspace extras: {', '.join(missing)}"
            )

    return {
        "passed": not mismatches,
        "mismatches": mismatches,
        "runtime_pyproject": "pkgs/60-runtime/tigrbl-identity-runtime/pyproject.toml",
        "runtime_runner_extras": {
            name: runtime_optional.get(name, []) for name in expected_runtime_runner_extras
        },
        "workspace_runner_extras": {
            name: optional.get(name, []) for name in expected_root_runner_extras
        },
        "profile_extra_coverage": profile_extra_coverage,
    }


def _uv_lock_consistency(repo_root: Path, dependency_manifest: dict[str, Any]) -> dict[str, Any]:
    uv_lock = repo_root / "uv.lock"
    failures: list[str] = []
    if not uv_lock.exists():
        failures.append("uv.lock is missing")
    return {
        "passed": not failures,
        "failures": failures,
        "python_support_blockers": [],
        "missing_profiles": [],
        "install_profile_count": len(PROFILE_TOGGLES),
        "dependencies_source": "pyproject.toml",
        "lockfile": "uv.lock",
        "uv_lock_present": uv_lock.exists(),
    }


def _current_python_supported() -> bool:
    current = sys.version_info[:3]
    return (3, 10, 0) <= current < (3, 13, 0)


def _probe_python_version(executable: list[str]) -> tuple[str | None, str | None]:
    try:
        completed = subprocess.run(
            [*executable, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    if completed.returncode != 0:
        return None, (completed.stderr or completed.stdout or "python probe failed").strip()
    return completed.stdout.strip(), None


def _detect_supported_pythons() -> list[dict[str, Any]]:
    detections: dict[str, dict[str, Any]] = {}
    if _current_python_supported():
        current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        detections[current_version] = {
            "version": current_version,
            "available": True,
            "path": sys.executable,
            "source": "current-interpreter",
        }
    for version in SUPPORTED_PYTHON_VERSIONS:
        for executable, source in (
            ([f"python{version}"], "path"),
            (["py", f"-{version}"], "py-launcher"),
        ):
            if version in detections:
                break
            candidate = shutil.which(executable[0])
            if not candidate:
                continue
            detected_version, error = _probe_python_version(executable)
            if detected_version == version:
                detections[version] = {
                    "version": version,
                    "available": True,
                    "path": candidate if source == "path" else " ".join(executable),
                    "source": source,
                }
            elif error:
                detections.setdefault(
                    version,
                    {
                        "version": version,
                        "available": False,
                        "path": None,
                        "source": source,
                        "message": error,
                    },
                )

    results: list[dict[str, Any]] = []
    for version in SUPPORTED_PYTHON_VERSIONS:
        results.append(
            detections.get(
                version,
                {
                    "version": version,
                    "available": False,
                    "path": None,
                    "source": None,
                },
            )
        )
    return results




def _module_supported(module: dict[str, Any]) -> bool:
    current = sys.version_info[:2]
    python_min = tuple(module.get("python_min", (0, 0)))
    python_max_exclusive = tuple(module.get("python_max_exclusive", (99, 99)))
    return python_min <= current < python_max_exclusive


def _expected_modules_for_profile(profile: str) -> list[dict[str, Any]]:
    groups = PROFILE_IMPORT_GROUPS.get(profile, PROFILE_IMPORT_GROUPS["base"])
    expected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            if not _module_supported(item):
                continue
            module = str(item["module"])
            if module in seen:
                continue
            seen.add(module)
            expected.append(dict(item))
    return expected


def _probe_modules(expected_modules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not expected_modules:
        return []
    code = (
        "import importlib, json, sys\n"
        "if sys.version_info < (3, 11):\n"
        "    try:\n"
        "        import tomllib  # noqa: F401\n"
        "    except ModuleNotFoundError:\n"
        "        import tomli as tomllib\n"
        "        sys.modules['tomllib'] = tomllib\n"
        "payload = json.loads(sys.argv[1])\n"
        "results = []\n"
        "for item in payload:\n"
        "    try:\n"
        "        importlib.import_module(item['module'])\n"
        "        results.append({'module': item['module'], 'package': item['package'], 'passed': True, 'category': item['category'], 'message': 'import ok', 'error_type': None})\n"
        "    except Exception as exc:\n"
        "        results.append({'module': item['module'], 'package': item['package'], 'passed': False, 'category': item['category'], 'message': str(exc), 'error_type': exc.__class__.__name__})\n"
        "print(json.dumps(results))\n"
    )
    completed = subprocess.run(
        [sys.executable, "-I", "-c", code, json.dumps(expected_modules)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        message = (completed.stderr or completed.stdout or "subprocess probe failed").strip()
        return [
            ModuleProbeResult(
                module=str(item["module"]),
                package=str(item["package"]),
                category=str(item["category"]),
                passed=False,
                message=message,
                error_type="SubprocessProbeFailure",
            ).as_dict()
            for item in expected_modules
        ]
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return [
            ModuleProbeResult(
                module=str(item["module"]),
                package=str(item["package"]),
                category=str(item["category"]),
                passed=False,
                message="invalid module probe payload",
                error_type="JSONDecodeError",
            ).as_dict()
            for item in expected_modules
        ]
    return payload


def _runtime_surface_source_roots(repo_root: Path) -> list[Path]:
    roots = [repo_root]
    roots.extend(sorted((repo_root / "pkgs").glob("*/src")))
    roots.extend(sorted((repo_root / "pkgs").glob("*/*/src")))
    roots.extend(sorted((repo_root / "pkgs" / "deprecated").glob("*/src")))
    roots.extend(sorted((repo_root / "pkgs" / "deprecated").glob("*/*/src")))
    return list(dict.fromkeys(roots))


def _runtime_surface_probe(repo_root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    source_roots = _runtime_surface_source_roots(repo_root)
    for module in RUNTIME_IMPORT_SURFACES:
        module_parts = module.split(".")
        passed = any(
            source_root.joinpath(*module_parts).with_suffix(".py").exists()
            or source_root.joinpath(*module_parts, "__init__.py").exists()
            for source_root in source_roots
        )
        results.append(
            {
                "module": module,
                "passed": passed,
                "message": "import surface resolvable" if passed else "module source missing",
            }
        )
    return results

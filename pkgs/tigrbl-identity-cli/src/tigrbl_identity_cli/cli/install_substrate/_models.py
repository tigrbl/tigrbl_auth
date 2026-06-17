from __future__ import annotations

def _constraint_consistency(repo_root: Path, dependency_manifest: dict[str, Any]) -> dict[str, Any]:
    base_path = repo_root / "constraints" / "base.txt"
    test_path = repo_root / "constraints" / "test.txt"
    uvicorn_path = repo_root / "constraints" / "runner-uvicorn.txt"
    hypercorn_path = repo_root / "constraints" / "runner-hypercorn.txt"
    tigrcorn_path = repo_root / "constraints" / "runner-tigrcorn.txt"

    base_constraints = _parse_constraints(base_path)
    test_constraints = _parse_constraints(test_path)
    uvicorn_constraints = _parse_constraints(uvicorn_path)
    hypercorn_constraints = _parse_constraints(hypercorn_path)
    tigrcorn_constraints = _parse_constraints(tigrcorn_path)
    optional = dependency_manifest["optional_dependencies"]
    mismatches: list[str] = []

    illegal_constraint_extras = {
        "base": _constraint_lines_with_extras(base_path),
        "test": _constraint_lines_with_extras(test_path),
        "uvicorn": _constraint_lines_with_extras(uvicorn_path),
        "hypercorn": _constraint_lines_with_extras(hypercorn_path),
        "tigrcorn": _constraint_lines_with_extras(tigrcorn_path),
    }
    for scope, items in illegal_constraint_extras.items():
        if items:
            mismatches.append(f"constraints/{'runner-' + scope if scope in {'uvicorn', 'hypercorn', 'tigrcorn'} else scope}.txt contains extras syntax that pip constraints mode does not accept")

    if set(base_constraints) != {_constraint_safe_requirement(item) for item in dependency_manifest["dependencies"]}:
        mismatches.append("constraints/base.txt does not match pyproject runtime dependencies when normalized to pip-legal constraint form")
    if set(test_constraints) != {_constraint_safe_requirement(item) for item in optional.get("test", [])}:
        mismatches.append("constraints/test.txt does not match pyproject optional-dependencies.test")
    if set(uvicorn_constraints) != {_constraint_safe_requirement(item) for item in optional.get("uvicorn", [])}:
        mismatches.append("constraints/runner-uvicorn.txt does not match pyproject optional-dependencies.uvicorn when normalized to pip-legal constraint form")
    if set(hypercorn_constraints) != {_constraint_safe_requirement(item) for item in optional.get("hypercorn", [])}:
        mismatches.append("constraints/runner-hypercorn.txt does not match pyproject optional-dependencies.hypercorn")
    if set(tigrcorn_constraints) != {_constraint_safe_requirement(item) for item in optional.get("tigrcorn", [])}:
        mismatches.append("constraints/runner-tigrcorn.txt does not match pyproject optional-dependencies.tigrcorn")
    return {
        "passed": not mismatches,
        "mismatches": mismatches,
        "illegal_constraint_extras": illegal_constraint_extras,
        "base_count": len(base_constraints),
        "test_count": len(test_constraints),
        "uvicorn_count": len(uvicorn_constraints),
        "hypercorn_count": len(hypercorn_constraints),
        "tigrcorn_count": len(tigrcorn_constraints),
    }


def _dependency_lock_consistency(repo_root: Path, dependency_manifest: dict[str, Any]) -> dict[str, Any]:
    payload = _load_json(repo_root / "constraints" / "dependency-lock.json") or {}
    install_profiles = payload.get("install_profiles", {}) if isinstance(payload, dict) else {}
    failures: list[str] = []
    if not payload:
        failures.append("constraints/dependency-lock.json is missing")
        return {
            "passed": False,
            "failures": failures,
            "install_profile_count": 0,
            "missing_profiles": sorted(PROFILE_TOGGLES),
        }
    if set(_normalize_requirement(str(item)) for item in payload.get("base", [])) != set(dependency_manifest["dependencies"]):
        failures.append("dependency lock base set drifts from pyproject runtime dependencies")
    lock_extras = {
        str(name): [_normalize_requirement(str(item)) for item in values]
        for name, values in (payload.get("extras") or {}).items()
    }
    for extra_name in ("test", "sqlite", "postgres", "uvicorn", "hypercorn", "tigrcorn", "servers"):
        if set(lock_extras.get(extra_name, [])) != set(dependency_manifest["optional_dependencies"].get(extra_name, [])):
            failures.append(f"dependency lock extra '{extra_name}' drifts from pyproject optional dependencies")
    missing_profiles: list[str] = []
    for profile_name, expected in PROFILE_TOGGLES.items():
        actual = install_profiles.get(profile_name)
        if actual is None:
            missing_profiles.append(profile_name)
            continue
        actual_constraints = [_normalize_requirement(str(item)) for item in actual.get("constraints", [])]
        actual_extras = [str(item) for item in actual.get("extras", [])]
        if actual_constraints != expected["constraints"]:
            failures.append(f"dependency lock install profile '{profile_name}' has unexpected constraints")
        if actual_extras != expected["extras"]:
            failures.append(f"dependency lock install profile '{profile_name}' has unexpected extras")
    if missing_profiles:
        failures.append("dependency lock install profiles are incomplete")
    return {
        "passed": not failures,
        "failures": failures,
        "python_support_blockers": list(
            (payload.get("published_dependency_verification") or {}).get("python_support_blockers", [])
        ),
        "missing_profiles": missing_profiles,
        "install_profile_count": len(install_profiles),
    }


def _current_python_supported() -> bool:
    current = sys.version_info[:3]
    return (3, 10, 0) <= current < (3, 15, 0)


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
    roots.extend(sorted((repo_root / "pkgs" / "deprecated").glob("*/src")))
    return roots


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

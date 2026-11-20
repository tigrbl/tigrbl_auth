"""Plan affected-package PR checks and full package checks on master."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import tomllib
from collections import defaultdict, deque
from pathlib import Path

from monorepo_release import (
    ROOT,
    Package,
    SUPPORTED_PYTHON_VERSIONS,
    _dependency_name,
    _find_package,
    _normalize_dist_name,
    _python_tag,
    _supported_package_python_versions,
    _write_github_output,
    discover_packages,
)

NODE_VERSIONS = ("22", "24", "26")
PYTHON_SHARED = {"pyproject.toml", "uv.lock", "conftest.py", "tox.ini", "scripts/monorepo_release.py"}
NODE_SHARED = {".npmrc", "tsconfig.json", "tsconfig.base.json", "vite.config.ts", "vitest.config.ts"}
NODE_DEPENDENCIES = ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies")


def git(*args: str) -> str:
    return subprocess.check_output(("git", *args), cwd=ROOT).decode("utf-8")


def changed_paths(base: str) -> set[str]:
    return set(git("diff", "--no-renames", "--name-only", "-z", base, "HEAD", "--").split("\0")) - {""}


def previous_manifests(base: str, paths: set[str]) -> dict[str, str]:
    if not paths:
        return {}
    tracked = set(git("ls-tree", "-r", "--name-only", "-z", base, "--", *sorted(paths)).split("\0"))
    return {path: git("show", f"{base}:{path}") for path in paths & tracked}


def affected_packages(changed: set[str], dependencies: dict[str, set[str]]) -> set[str]:
    dependents: dict[str, set[str]] = defaultdict(set)
    for name, requirements in dependencies.items():
        for requirement in requirements:
            dependents[requirement].add(name)
    affected = set(changed)
    queue = deque(changed)
    while queue:
        name = queue.popleft()
        new = dependents[name] - affected
        affected.update(new)
        queue.extend(new)
    return affected


def package_roots(paths: set[str]) -> set[str]:
    return {"/".join(path.split("/", 3)[:3]) for path in paths if path.startswith("pkgs/") and path.count("/") >= 3}


def python_dependencies(project: dict) -> set[str]:
    metadata = project.get("project", {})
    requirements = [
        *metadata.get("dependencies", ()),
        *project.get("build-system", {}).get("requires", ()),
    ]
    for group in (
        *metadata.get("optional-dependencies", {}).values(),
        *project.get("dependency-groups", {}).values(),
    ):
        requirements.extend(item for item in group if isinstance(item, str))
    return {name for item in requirements if (name := _dependency_name(item))}


def python_selection(packages: list[Package], base: str, paths: set[str]) -> list[Package]:
    if not base or paths & PYTHON_SHARED or any(path.startswith("tests/") for path in paths):
        return packages
    roots = package_roots(paths)
    old_manifests = previous_manifests(base, {f"{root}/pyproject.toml" for root in roots})
    changed = {
        _normalize_dist_name(name)
        for content in old_manifests.values()
        if (name := tomllib.loads(content).get("project", {}).get("name"))
    }
    dependencies = {}
    for package in packages:
        name = _normalize_dist_name(package.name)
        if package.path.as_posix() in roots:
            changed.add(name)
        manifest = ROOT / package.path / "pyproject.toml"
        dependencies[name] = python_dependencies(tomllib.loads(manifest.read_text(encoding="utf-8")))

    # Backend package tests are kept separately from the packages they exercise.
    test_prefix = "pkgs/120-tests/tba-tests-backend-apps/tests/packages/"
    changed.update(
        _normalize_dist_name(path[len(test_prefix):].split("/")[0])
        for path in paths if path.startswith(test_prefix)
    )
    names = affected_packages(changed, dependencies)
    return [package for package in packages if _normalize_dist_name(package.name) in names]


def lock_without_workspaces(lock: dict, workspaces: set[str]) -> dict:
    # Workspace links and manifest records are covered by the package diff.
    # A change to resolved third-party packages can affect the entire tree.
    entries = lock["packages"]
    return {
        **lock,
        "packages": {
            path: {key: value for key, value in entry.items() if path or key != "workspaces"}
            for path, entry in entries.items()
            if path not in workspaces and not (entry.get("link") and entry.get("resolved") in workspaces)
        },
    }


def node_selection(base: str, paths: set[str]) -> list[dict]:
    root_manifest = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    workspaces = set(root_manifest["workspaces"])
    manifests = {
        path: json.loads((ROOT / path / "package.json").read_text(encoding="utf-8"))
        for path in sorted(workspaces)
    }
    if not base or paths & NODE_SHARED:
        return list(manifests.values())
    old_root = json.loads(git("show", f"{base}:package.json"))
    old_workspaces = set(old_root["workspaces"])
    if {k: v for k, v in old_root.items() if k != "workspaces"} != {
        k: v for k, v in root_manifest.items() if k != "workspaces"
    }:
        return list(manifests.values())
    if "package-lock.json" in paths:
        old_lock = json.loads(git("show", f"{base}:package-lock.json"))
        lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
        if lock_without_workspaces(old_lock, old_workspaces) != lock_without_workspaces(lock, workspaces):
            return list(manifests.values())

    roots = package_roots(paths) | (workspaces ^ old_workspaces)
    old_manifests = previous_manifests(base, {f"{path}/package.json" for path in roots & old_workspaces})
    changed = {json.loads(content)["name"] for content in old_manifests.values()}
    changed.update(manifests[path]["name"] for path in roots & workspaces)
    dependencies = {
        manifest["name"]: {name for field in NODE_DEPENDENCIES for name in manifest.get(field, {})}
        for manifest in manifests.values()
    }
    names = affected_packages(changed, dependencies)
    return [manifest for manifest in manifests.values() if manifest["name"] in names]


def python_batches(packages: list[Package], versions: list[str]) -> tuple[list[dict], list[list[dict]]]:
    by_python: dict[str, list[dict[str, str]]] = defaultdict(list)
    for package in packages:
        for version in _supported_package_python_versions(package, versions):
            by_python[version].append({
                "name": package.name,
                "path": package.path.as_posix(),
                "cell_id": f"{package.name}-{_python_tag(version)}",
            })
    cell_count = sum(len(group) for group in by_python.values())
    batch_size = max(20, math.ceil(cell_count / 250))
    matrix, plan = [], []
    for version, group in sorted(by_python.items()):
        for offset in range(0, len(group), batch_size):
            matrix.append({"batch": len(plan), "python": version})
            plan.append(group[offset:offset + batch_size])
    if len(matrix) > 256:
        raise ValueError("Python package matrix exceeds GitHub's job limit")
    return matrix, plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ecosystem", choices=("python", "node"))
    parser.add_argument("--base", default="", help="Base commit of the checked-out PR merge")
    parser.add_argument("--package", default="all")
    parser.add_argument("--version", default="all")
    parser.add_argument("--plan", type=Path)
    args = parser.parse_args()
    paths = changed_paths(args.base) if args.base else set()
    if args.ecosystem == "python":
        if args.plan is None:
            parser.error("--plan is required for the Python matrix")
        if args.version not in ("all", *SUPPORTED_PYTHON_VERSIONS):
            parser.error("unsupported Python version")
        packages = (
            python_selection(discover_packages(), args.base, paths)
            if args.package == "all"
            else [_find_package(args.package)]
        )
        versions = list(SUPPORTED_PYTHON_VERSIONS) if args.version == "all" else [args.version]
        matrix, plan = python_batches(packages, versions)
        args.plan.write_text(json.dumps(plan), encoding="utf-8")
    else:
        if args.version not in ("all", *NODE_VERSIONS):
            parser.error("unsupported Node version")
        manifests = node_selection(args.base, paths)
        if args.package != "all" and not any(manifest["name"] == args.package for manifest in manifests):
            parser.error(f"unknown Node workspace: {args.package}")
        versions = NODE_VERSIONS if args.version == "all" else (args.version,)
        matrix = [
            {"name": manifest["name"], "node_version": version}
            for manifest in manifests
            if args.package in ("all", manifest["name"]) and {"test", "build"} & manifest.get("scripts", {}).keys()
            for version in versions
        ]
    print(f"Selected {len(matrix)} {args.ecosystem} matrix jobs")
    _write_github_output({"matrix": json.dumps(matrix, separators=(",", ":")), "count": str(len(matrix))})


if __name__ == "__main__":
    main()

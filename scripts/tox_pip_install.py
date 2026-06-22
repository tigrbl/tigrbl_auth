from __future__ import annotations

import ast
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIN_RE = re.compile(
    r"^(?P<name>[A-Za-z0-9_.-]+)(?P<extras>\[[^\]]+\])?==(?P<version>[^;\s]+)$"
)


@dataclass(frozen=True)
class LocalProject:
    name: str
    version: str
    path: Path


def _normalize_dist_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _project_identity(pyproject: Path) -> tuple[str, str]:
    in_project = False
    name = ""
    version = ""
    for raw_line in pyproject.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "[project]":
            in_project = True
            continue
        if line.startswith("[") and line.endswith("]"):
            in_project = False
            continue
        if not in_project or "=" not in line:
            continue

        key, value = [part.strip() for part in line.split("=", 1)]
        if key == "name":
            name = str(ast.literal_eval(value))
        elif key == "version":
            version = str(ast.literal_eval(value))
        if name and version:
            return name, version

    raise SystemExit(f"missing project.name or project.version in {pyproject.relative_to(ROOT)}")


def discover_local_projects() -> dict[str, LocalProject]:
    projects: dict[str, LocalProject] = {}
    for pyproject in sorted((ROOT / "pkgs").rglob("pyproject.toml")):
        name, version = _project_identity(pyproject)
        projects[_normalize_dist_name(name)] = LocalProject(
            name=name,
            version=version,
            path=pyproject.parent,
        )
    return projects


def rewrite_install_args(args: list[str], projects: dict[str, LocalProject] | None = None) -> list[str]:
    local_projects = projects if projects is not None else discover_local_projects()
    rewritten: list[str] = []

    for arg in args:
        match = PIN_RE.match(arg)
        if match is None:
            rewritten.append(arg)
            continue

        project = local_projects.get(_normalize_dist_name(match.group("name")))
        if project is None:
            rewritten.append(arg)
            continue

        requested_version = match.group("version")
        if requested_version != project.version:
            raise SystemExit(
                f"{project.name} pin {requested_version!r} does not match "
                f"local pyproject version {project.version!r}"
            )
        rewritten.append(f"{project.path}{match.group('extras') or ''}")

    return rewritten


def main(argv: list[str]) -> int:
    command = [sys.executable, "-I", "-m", "pip", "install", *rewrite_install_args(argv)]
    return subprocess.run(command, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

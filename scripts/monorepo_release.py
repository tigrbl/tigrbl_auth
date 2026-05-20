from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG_RE = re.compile(r"^(?P<name>[A-Za-z0-9_.-]+)==(?P<version>\d+\.\d+\.\d+(?:[-+][A-Za-z0-9_.-]+)?)$")


@dataclass(frozen=True)
class Package:
    name: str
    version: str
    path: Path
    import_root: str

    def as_cell(self) -> dict[str, str]:
        return {
            "name": self.name,
            "version": self.version,
            "path": self.path.as_posix(),
            "import_root": self.import_root,
            "tag": f"{self.name}=={self.version}",
        }


def _load_pyproject(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _package_import_root(package_path: Path, name: str) -> str:
    src = package_path / "src"
    if src.exists():
        roots = sorted(item.name for item in src.iterdir() if item.is_dir())
        if roots:
            return roots[0]
    return name.replace("-", "_")


def discover_packages() -> list[Package]:
    packages: list[Package] = []
    for pyproject in sorted((ROOT / "pkgs").glob("*/pyproject.toml")):
        data = _load_pyproject(pyproject)
        project = data.get("project", {})
        name = str(project.get("name") or "").strip()
        version = str(project.get("version") or "").strip()
        if not name or not version:
            raise SystemExit(f"missing project.name or project.version in {pyproject.relative_to(ROOT)}")
        package_path = pyproject.parent.relative_to(ROOT)
        packages.append(
            Package(
                name=name,
                version=version,
                path=package_path,
                import_root=_package_import_root(pyproject.parent, name),
            )
        )
    return packages


def _find_package(name: str) -> Package:
    matches = [item for item in discover_packages() if item.name == name]
    if not matches:
        known = ", ".join(item.name for item in discover_packages())
        raise SystemExit(f"unknown package {name!r}; known packages: {known}")
    return matches[0]


def _write_github_output(values: dict[str, str]) -> None:
    output_name = os.environ.get("GITHUB_OUTPUT", "")
    if not output_name:
        print(json.dumps(values, indent=2))
        return
    output = Path(output_name)
    with output.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def cmd_matrix(args: argparse.Namespace) -> int:
    cells = [item.as_cell() for item in discover_packages()]
    payload = json.dumps(cells, separators=(",", ":"))
    _write_github_output({"matrix": payload, "count": str(len(cells))})
    if args.print:
        print(json.dumps(cells, indent=2))
    return 0


def cmd_resolve_tag(args: argparse.Namespace) -> int:
    match = TAG_RE.match(args.tag)
    if match is None:
        raise SystemExit(f"tag must match <package>==<version>; got {args.tag!r}")
    package = _find_package(match.group("name"))
    version = match.group("version")
    if package.version != version:
        raise SystemExit(
            f"tag version {version!r} does not match {package.name} pyproject version {package.version!r}"
        )
    cell = package.as_cell()
    _write_github_output(
        {
            "package_name": package.name,
            "package_version": package.version,
            "package_path": package.path.as_posix(),
            "import_root": package.import_root,
            "tag": cell["tag"],
            "matrix": json.dumps([cell], separators=(",", ":")),
        }
    )
    print(json.dumps(cell, indent=2))
    return 0


def _run(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def cmd_create_tags(args: argparse.Namespace) -> int:
    packages = discover_packages() if args.package == "all" else [_find_package(args.package)]
    created: list[str] = []
    for package in packages:
        version = args.version or package.version
        if version != package.version:
            raise SystemExit(
                f"requested version {version!r} does not match {package.name} pyproject version {package.version!r}"
            )
        tag = f"{package.name}=={version}"
        exists = subprocess.run(
            ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0
        if exists and not args.force:
            print(f"tag exists, skipping: {tag}")
            continue
        if exists:
            _run(["git", "tag", "-d", tag])
            _run(["git", "push", "--delete", "origin", tag])
        _run(["git", "tag", "-a", tag, "-m", f"Release {tag}"])
        _run(["git", "push", "origin", tag])
        created.append(tag)
    print(json.dumps({"created": created}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monorepo package release helpers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    matrix = subparsers.add_parser("matrix")
    matrix.add_argument("--print", action="store_true")
    matrix.set_defaults(func=cmd_matrix)

    resolve = subparsers.add_parser("resolve-tag")
    resolve.add_argument("tag")
    resolve.set_defaults(func=cmd_resolve_tag)

    tags = subparsers.add_parser("create-tags")
    tags.add_argument("--package", default="all", help="Package name or 'all'.")
    tags.add_argument("--version", default="", help="Optional explicit version; must match pyproject.")
    tags.add_argument("--force", action="store_true", help="Replace existing tags.")
    tags.set_defaults(func=cmd_create_tags)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

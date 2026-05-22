from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib

VERSION_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:\.dev(?P<dev>0|[1-9]\d*))?$"
)


def _parse_version(version: str) -> tuple[int, int, int, int | None]:
    match = VERSION_RE.match(version)
    if match is None:
        raise SystemExit(f"unsupported version {version!r}; expected X.Y.Z or X.Y.Z.devN")
    dev = match.group("dev")
    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
        int(dev) if dev is not None else None,
    )


def _version_sort_key(version: tuple[int, int, int, int | None]) -> tuple[int, int, int, int, int]:
    major, minor, patch, dev = version
    if dev is None:
        return major, minor, patch, 1, 0
    return major, minor, patch, 0, dev


def _read_version(path: Path) -> str:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    version = data.get("project", {}).get("version")
    if not version:
        raise SystemExit(f"missing project.version in {path}")
    return str(version)


def _replace_version(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    old_line = f'version = "{old}"'
    new_line = f'version = "{new}"'
    if old_line not in text:
        raise SystemExit(f"could not locate {old_line!r} in {path}")
    path.write_text(text.replace(old_line, new_line, 1), encoding="utf-8")


def bump_version(current: str, bump_type: str) -> str:
    major, minor, patch, dev = _parse_version(current)
    is_dev = dev is not None

    if bump_type == "finalize":
        if not is_dev:
            raise SystemExit("current version is stable; nothing to finalize")
        return f"{major}.{minor}.{patch}"
    if bump_type == "minor":
        return f"{major}.{minor + 1}.0.dev1"
    if bump_type == "patch":
        if is_dev:
            return f"{major}.{minor}.{patch}.dev{dev + 1}"
        return f"{major}.{minor}.{patch + 1}.dev1"
    raise SystemExit("bump_type must be one of: patch, minor, finalize")


def set_version(current: str, target: str) -> str:
    current_version = _parse_version(current)
    target_version = _parse_version(target)
    if _version_sort_key(target_version) < _version_sort_key(current_version):
        raise SystemExit(
            f"target version {target!r} is lower than current version {current!r}"
        )
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump or set pyproject.toml version.")
    parser.add_argument("pyproject", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--bump", choices=("patch", "minor", "finalize"))
    group.add_argument("--set", dest="target_version")
    args = parser.parse_args()

    current = _read_version(args.pyproject)
    target = (
        bump_version(current, args.bump)
        if args.bump
        else set_version(current, args.target_version)
    )
    _replace_version(args.pyproject, current, target)
    print(f"{args.pyproject}: {current} -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

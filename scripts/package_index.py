"""Generate and validate the repository-wide package and layer-order index."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.package_layer_policy import load_layer_policy
except ModuleNotFoundError:
    from package_layer_policy import load_layer_policy

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.toml"
FORMAT_VERSION = "1.1.0"
_DEPENDENCY_NAME = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)")


def _normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


@dataclass(frozen=True)
class Package:
    name: str
    path: str
    layer: str
    local_dependencies: tuple[str, ...]
    same_layer_dependencies: tuple[str, ...]
    order: int


def discover() -> tuple[Package, ...]:
    raw: dict[str, tuple[str, str, tuple[str, ...]]] = {}
    for pyproject in sorted((ROOT / "pkgs").glob("*/*/pyproject.toml")):
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        project = data.get("project", {})
        declared_name = project.get("name")
        if not declared_name:
            continue
        name = _normalize(str(declared_name))
        if name in raw:
            raise ValueError(f"duplicate package name: {name}")
        dependency_names = []
        for declaration in project.get("dependencies", []):
            match = _DEPENDENCY_NAME.match(str(declaration))
            if match:
                dependency_names.append(_normalize(match.group(1)))
        relative = pyproject.parent.relative_to(ROOT).as_posix()
        raw[name] = (relative, pyproject.relative_to(ROOT).parts[1], tuple(dependency_names))

    local_dependencies = {
        name: tuple(sorted({dependency for dependency in declared if dependency in raw}))
        for name, (_, _, declared) in raw.items()
    }
    same_layer_dependencies = {
        name: tuple(
            dependency
            for dependency in local_dependencies[name]
            if raw[dependency][1] == layer
        )
        for name, (_, layer, _) in raw.items()
    }

    visiting: list[str] = []
    orders: dict[str, int] = {}

    def order_for(name: str) -> int:
        if name in orders:
            return orders[name]
        if name in visiting:
            cycle = visiting[visiting.index(name) :] + [name]
            raise ValueError("same-layer dependency cycle: " + " -> ".join(cycle))
        visiting.append(name)
        dependencies = same_layer_dependencies[name]
        order = 0 if not dependencies else 1 + max(order_for(item) for item in dependencies)
        visiting.pop()
        orders[name] = order
        return order

    for name in sorted(raw):
        order_for(name)

    return tuple(
        Package(
            name=name,
            path=raw[name][0],
            layer=raw[name][1],
            local_dependencies=local_dependencies[name],
            same_layer_dependencies=same_layer_dependencies[name],
            order=orders[name],
        )
        for name in sorted(raw, key=lambda item: (raw[item][1], orders[item], item))
    )


def render(packages: tuple[Package, ...]) -> str:
    policy = load_layer_policy()
    lines = [f"schema_version = {_quote(FORMAT_VERSION)}", ""]
    for item in policy.dependency_exceptions:
        lines.extend([
            "[[metadata.tba.dependency_exceptions]]",
            f"consumer = {_quote(item.consumer)}",
            f"target = {_quote(item.target)}",
            f"reason = {_quote(item.reason)}",
            "",
        ])
    for layer in policy.layers:
        targets = policy.rules_by_consumer[layer.id].allowed_target_layers
        same_layer = "ordered" if layer.id in targets else "forbidden"
        lines.extend([
            "[[layers]]",
            f"id = {_quote(layer.id)}",
            f"order = {layer.order}",
            f"path = {_quote('pkgs/' + layer.id)}",
            'order_strategy = "dependency_depth"',
            f"same_layer_dependencies = {_quote(same_layer)}",
            f"allowed_dependency_layers = {json.dumps(sorted(targets - {layer.id}))}",
            "[layers.metadata.tba]",
            f"category = {_quote(layer.category)}",
        ])
        if layer.terminal:
            lines.append("terminal = true")
        if layer.javascript:
            lines.append("javascript = true")
        if layer.distribution_prefix is not None:
            lines.append(f"distribution_prefix = {_quote(layer.distribution_prefix)}")
        lines.append("")
    for package in packages:
        exceptions = [
            target for target in package.local_dependencies if (package.name, target) in policy.exception_pairs
        ]
        lines.extend(
            [
                "[[packages]]",
                f"id = {_quote(package.name)}",
                f"name = {_quote(package.name)}",
                f"path = {_quote(package.path)}",
                f"layer = {_quote(package.layer)}",
                f"order = {package.order}",
                'ecosystem = "pypi"',
                f"dependencies = {json.dumps(package.local_dependencies)}",
            ]
        )
        if exceptions:
            lines.append(f"dependency_exceptions = {json.dumps(exceptions)}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    from index_toml import loads

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if index.toml is stale")
    args = parser.parse_args()
    expected = render(discover())
    loads(expected)
    if args.check:
        if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != expected:
            raise SystemExit("index.toml is stale; run uv run python scripts/package_index.py")
        return 0
    INDEX.write_text(expected, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

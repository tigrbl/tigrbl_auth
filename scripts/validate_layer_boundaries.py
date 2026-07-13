"""Validate first-party package dependency and source-layer boundaries.

The package directory is the authoritative layer declaration.  This module is
kept dependency-free so it can run before the workspace itself is installed.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 CI
    import tomli as tomllib  # type: ignore[no-redef]


ROOT = Path(__file__).resolve().parents[1]
PKGS = ROOT / "pkgs"

LAYER_ORDER = (
    "00-primitives",
    "01-storage",
    "02-contracts",
    "05-bases",
    "10-concrete",
    "20-providers",
    "30-storage-runtime",
    "40-capabilities",
    "50-protocols",
    "60-runtime",
    "70-facade",
    "80-apis",
    "deprecated",
)

# Capabilities orchestrate implemented behavior.  Contract value types and
# ports remain valid vocabulary, but capability implementations may not reach
# into primitives, storage tables, or implementation bases.  In particular,
# layer 40 never *implements* a layer-02/05 abstraction; implementation starts
# in layer 10 and concrete integrations belong in layer 20.
CAPABILITY_ALLOWED_LAYERS = frozenset(
    {
        "02-contracts",
        "10-concrete",
        "20-providers",
        "30-storage-runtime",
        "40-capabilities",
    }
)
CAPABILITY_FORBIDDEN_LAYERS = frozenset(
    {"00-primitives", "01-storage", "05-bases"}
)
CAPABILITY_FORBIDDEN_BASE_LAYERS = frozenset(
    {"00-primitives", "01-storage", "02-contracts", "05-bases"}
)

# Layer 40 is intentionally sparse and opt-in.  Each entry names the complete
# use case that would disappear if the orchestration package were removed.
CAPABILITY_PURPOSES = {
    "tigrbl-attestation-appraisal": (
        "coordinate evidence appraisal and result recording"
    ),
    "tigrbl-digital-credential-issuance": (
        "coordinate credential configuration, wallet trust, offers, and issuance"
    ),
    "tigrbl-digital-credential-presentation": (
        "coordinate holder consent, replay defense, and presentation verification"
    ),
    "tigrbl-identity-admin-control-plane": (
        "coordinate administrative resource lifecycle use cases"
    ),
    "tigrbl-replay-protection-capability": (
        "coordinate normalized replay reservations across protocol mappings, "
        "durable repositories, and replaceable providers"
    ),
    "tigrbl-security-events": (
        "coordinate security-event transmission, receipt, and recording"
    ),
    "tigrbl-workload-identity": (
        "coordinate workload credential retrieval and identity verification"
    ),
}

REQ_NAME_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+)")
DYNAMIC_IMPORT_RE = re.compile(
    r"(?:import_module|find_spec)\(\s*['\"](?P<module>[A-Za-z0-9_.]+)['\"]"
)


@dataclass(frozen=True)
class Package:
    distribution: str
    import_roots: tuple[str, ...]
    layer: str
    path: Path
    dependencies: tuple[str, ...]


@dataclass(frozen=True)
class Violation:
    kind: str
    package: str
    package_layer: str
    target: str
    target_layer: str
    path: str
    line: int | None
    detail: str


def _normalize_distribution(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def _dependency_name(requirement: object) -> str | None:
    match = REQ_NAME_RE.match(str(requirement))
    return _normalize_distribution(match.group(1)) if match else None


def _manifest_dependencies(data: dict[str, object]) -> set[str]:
    project = data.get("project", {})
    if not isinstance(project, dict):
        project = {}
    requirements: list[object] = list(project.get("dependencies", []) or [])
    optional = project.get("optional-dependencies", {}) or {}
    if isinstance(optional, dict):
        for group in optional.values():
            if isinstance(group, list):
                requirements.extend(group)

    dependency_groups = data.get("dependency-groups", {}) or {}
    if isinstance(dependency_groups, dict):
        for group in dependency_groups.values():
            if isinstance(group, list):
                requirements.extend(group)

    tool = data.get("tool", {}) or {}
    if isinstance(tool, dict):
        poetry = tool.get("poetry", {}) or {}
        if isinstance(poetry, dict):
            for table_name in ("dependencies", "dev-dependencies"):
                table = poetry.get(table_name, {}) or {}
                if isinstance(table, dict):
                    requirements.extend(table)
            groups = poetry.get("group", {}) or {}
            if isinstance(groups, dict):
                for group in groups.values():
                    if isinstance(group, dict):
                        table = group.get("dependencies", {}) or {}
                        if isinstance(table, dict):
                            requirements.extend(table)

    return {name for item in requirements if (name := _dependency_name(item))}


def discover_packages(root: Path = ROOT) -> tuple[Package, ...]:
    packages: list[Package] = []
    seen_distributions: dict[str, Path] = {}
    seen_import_roots: dict[str, Path] = {}
    pkgs = root / "pkgs"

    for manifest in sorted(pkgs.rglob("pyproject.toml")):
        relative = manifest.relative_to(pkgs)
        layer = relative.parts[0]
        if layer not in LAYER_ORDER:
            raise ValueError(f"unknown package layer {layer!r}: {manifest}")
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
        project = data.get("project", {})
        if not isinstance(project, dict) or not project.get("name"):
            raise ValueError(f"missing project.name: {manifest}")
        distribution = _normalize_distribution(str(project["name"]))
        if previous := seen_distributions.get(distribution):
            raise ValueError(
                f"duplicate distribution {distribution!r}: {previous} and {manifest}"
            )
        seen_distributions[distribution] = manifest

        src = manifest.parent / "src"
        import_roots = tuple(
            sorted(
                child.name
                for child in src.iterdir()
                if src.is_dir()
                and child.is_dir()
                and not child.name.endswith((".dist-info", ".egg-info"))
                and child.name != "__pycache__"
            )
        ) if src.is_dir() else ()
        for import_root in import_roots:
            if previous := seen_import_roots.get(import_root):
                raise ValueError(
                    f"duplicate import root {import_root!r}: {previous} and {manifest}"
                )
            seen_import_roots[import_root] = manifest

        packages.append(
            Package(
                distribution=distribution,
                import_roots=import_roots,
                layer=layer,
                path=manifest.parent,
                dependencies=tuple(sorted(_manifest_dependencies(data))),
            )
        )
    return tuple(packages)


def _base_root(base: ast.expr, imports: dict[str, str]) -> str | None:
    node = base
    while isinstance(node, (ast.Subscript, ast.Call)):
        node = node.value if isinstance(node, ast.Subscript) else node.func
    while isinstance(node, ast.Attribute):
        node = node.value
    if isinstance(node, ast.Name):
        return imports.get(node.id)
    return None


def validate(root: Path = ROOT) -> tuple[Violation, ...]:
    packages = discover_packages(root)
    by_distribution = {item.distribution: item for item in packages}
    by_import_root = {
        import_root: item
        for item in packages
        for import_root in item.import_roots
    }
    violations: list[Violation] = []

    capability_packages = {
        item.distribution for item in packages if item.layer == "40-capabilities"
    }
    for package_name in sorted(capability_packages - set(CAPABILITY_PURPOSES)):
        package = by_distribution[package_name]
        violations.append(
            Violation(
                kind="unregistered-capability",
                package=package.distribution,
                package_layer=package.layer,
                target="capability-purpose-registry",
                target_layer="architecture-policy",
                path=package.path.relative_to(root).as_posix(),
                line=None,
                detail=(
                    "layer 40 is opt-in; document the multi-component use case or "
                    "move the implementation to its owning layer"
                ),
            )
        )
    for package_name in sorted(set(CAPABILITY_PURPOSES) - capability_packages):
        violations.append(
            Violation(
                kind="stale-capability-registration",
                package=package_name,
                package_layer="40-capabilities",
                target="capability-purpose-registry",
                target_layer="architecture-policy",
                path="scripts/validate_layer_boundaries.py",
                line=None,
                detail="registered layer-40 package does not exist",
            )
        )

    for package in packages:
        if package.layer != "40-capabilities":
            continue

        manifest = package.path / "pyproject.toml"
        for dependency in package.dependencies:
            target = by_distribution.get(dependency)
            if target is None or target.layer not in CAPABILITY_FORBIDDEN_LAYERS:
                continue
            violations.append(
                Violation(
                    kind="manifest-dependency",
                    package=package.distribution,
                    package_layer=package.layer,
                    target=target.distribution,
                    target_layer=target.layer,
                    path=manifest.relative_to(root).as_posix(),
                    line=None,
                    detail=(
                        "capabilities may use contracts and layers 10, 20, 30, and 40; "
                        "primitives, storage implementations, and bases require an "
                        "implementation boundary"
                    ),
                )
            )

        for source in sorted((package.path / "src").rglob("*.py")):
            text = source.read_text(encoding="utf-8-sig")
            tree = ast.parse(text, filename=str(source))
            imports: dict[str, str] = {}
            source_imports: list[tuple[str, int]] = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root_name = alias.name.split(".")[0]
                        imports[alias.asname or root_name] = root_name
                        source_imports.append((root_name, node.lineno))
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    root_name = node.module.split(".")[0]
                    source_imports.append((root_name, node.lineno))
                    for alias in node.names:
                        imports[alias.asname or alias.name] = root_name

            for match in DYNAMIC_IMPORT_RE.finditer(text):
                source_imports.append(
                    (match.group("module").split(".")[0], text.count("\n", 0, match.start()) + 1)
                )

            relative_source = source.relative_to(root).as_posix()
            for import_root, line in sorted(set(source_imports)):
                target = by_import_root.get(import_root)
                if target is None or target.layer not in CAPABILITY_FORBIDDEN_LAYERS:
                    continue
                violations.append(
                    Violation(
                        kind="source-import",
                        package=package.distribution,
                        package_layer=package.layer,
                        target=target.distribution,
                        target_layer=target.layer,
                        path=relative_source,
                        line=line,
                        detail=f"imports first-party root {import_root!r}",
                    )
                )

            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                for base in node.bases:
                    import_root = _base_root(base, imports)
                    target = by_import_root.get(import_root or "")
                    if target is None or target.layer not in CAPABILITY_FORBIDDEN_BASE_LAYERS:
                        continue
                    violations.append(
                        Violation(
                            kind="inheritance",
                            package=package.distribution,
                            package_layer=package.layer,
                            target=target.distribution,
                            target_layer=target.layer,
                            path=relative_source,
                            line=node.lineno,
                            detail=(
                                f"class {node.name!r} inherits from "
                                f"{ast.unparse(base)!r}"
                            ),
                        )
                    )

    return tuple(
        sorted(
            violations,
            key=lambda item: (
                item.package,
                item.kind,
                item.path,
                item.line or 0,
                item.target,
            ),
        )
    )


def report(violations: tuple[Violation, ...]) -> dict[str, object]:
    return {
        "policy": {
            "consumer": "40-capabilities",
            "allowed_target_layers": sorted(CAPABILITY_ALLOWED_LAYERS),
            "forbidden_target_layers": sorted(CAPABILITY_FORBIDDEN_LAYERS),
            "forbidden_inheritance_layers": sorted(
                CAPABILITY_FORBIDDEN_BASE_LAYERS
            ),
        },
        "capability_purposes": dict(sorted(CAPABILITY_PURPOSES.items())),
        "violation_count": len(violations),
        "violations": [asdict(item) for item in violations],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    violations = validate()
    if args.json:
        print(json.dumps(report(violations), indent=2))
    elif violations:
        for item in violations:
            location = f"{item.path}:{item.line}" if item.line else item.path
            print(
                f"{location}: {item.kind}: {item.package} ({item.package_layer}) "
                f"-> {item.target} ({item.target_layer}): {item.detail}"
            )
    else:
        print("layer boundary validation passed")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())

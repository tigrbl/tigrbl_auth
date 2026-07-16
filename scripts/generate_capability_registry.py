"""Generate the machine-readable layer-40 capability ownership registry."""

from __future__ import annotations

import ast
import json
from pathlib import Path

from validate_layer_boundaries import (
    CAPABILITY_COMPATIBILITY_AGGREGATORS,
    CAPABILITY_IMPLEMENTATION_ROOTS,
    CAPABILITY_PURPOSES,
    ROOT,
    _base_root,
    discover_packages,
)


def _literal_strings(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return tuple(
            item.value
            for item in node.elts
            if isinstance(item, ast.Constant) and isinstance(item.value, str)
        )
    if isinstance(node, ast.Dict):
        return tuple(
            key.value
            for key in node.keys
            if isinstance(key, ast.Constant) and isinstance(key.value, str)
        )
    return ()


def _class_record(source: Path, node: ast.ClassDef, imports: dict[str, str]) -> dict[str, object] | None:
    if not any(_base_root(base, imports) in CAPABILITY_IMPLEMENTATION_ROOTS for base in node.bases):
        return None
    capability_id = ""
    version = ""
    operations: tuple[str, ...] = ()
    for call in (item for item in ast.walk(node) if isinstance(item, ast.Call)):
        if isinstance(call.func, ast.Name) and call.func.id == "CapabilityDefinition":
            values = [arg.value for arg in call.args if isinstance(arg, ast.Constant) and isinstance(arg.value, str)]
            capability_id = values[0] if values else capability_id
            version = values[1] if len(values) > 1 else version
            for keyword in call.keywords:
                if keyword.arg == "capability_id" and isinstance(keyword.value, ast.Constant):
                    capability_id = str(keyword.value.value)
                elif keyword.arg == "version" and isinstance(keyword.value, ast.Constant):
                    version = str(keyword.value.value)
        for keyword in call.keywords:
            if keyword.arg == "operations":
                operations = _literal_strings(keyword.value) or operations
    return {
        "class": node.name,
        "capability_id": capability_id,
        "version": version,
        "operations": sorted(operations),
        "source": source.relative_to(ROOT).as_posix(),
    }


def build_registry() -> dict[str, object]:
    packages = discover_packages(ROOT)
    by_import_root = {root: item for item in packages for root in item.import_roots}
    protocol_consumers: dict[str, set[str]] = {}
    for protocol in (item for item in packages if item.layer == "50-protocols"):
        for dependency in protocol.dependencies:
            protocol_consumers.setdefault(dependency, set()).add(protocol.distribution)
        for source in (protocol.path / "src").rglob("*.py"):
            tree = ast.parse(source.read_text(encoding="utf-8-sig"))
            for item in ast.walk(tree):
                module = item.module if isinstance(item, ast.ImportFrom) else None
                if module:
                    owner = by_import_root.get(module.split(".")[0])
                    if owner:
                        protocol_consumers.setdefault(owner.distribution, set()).add(protocol.distribution)

    records: list[dict[str, object]] = []
    for package in (item for item in packages if item.layer == "40-capabilities"):
        implementations: list[dict[str, object]] = []
        for source in sorted((package.path / "src").rglob("*.py")):
            tree = ast.parse(source.read_text(encoding="utf-8-sig"))
            imports: dict[str, str] = {}
            for item in ast.walk(tree):
                if isinstance(item, ast.ImportFrom) and item.level == 0 and item.module:
                    root = item.module.split(".")[0]
                    for alias in item.names:
                        imports[alias.asname or alias.name] = root
                elif isinstance(item, ast.Import):
                    for alias in item.names:
                        root = alias.name.split(".")[0]
                        imports[alias.asname or root] = root
            for item in tree.body:
                if isinstance(item, ast.ClassDef):
                    record = _class_record(source, item, imports)
                    if record:
                        implementations.append(record)
        ids = [str(item["capability_id"]) for item in implementations if item["capability_id"]]
        families = sorted({identifier.split(".", 1)[0] for identifier in ids})
        records.append(
            {
                "package": package.distribution,
                "purpose": CAPABILITY_PURPOSES[package.distribution],
                "families": families,
                "compatibility_aggregator": package.distribution in CAPABILITY_COMPATIBILITY_AGGREGATORS,
                "implementations": implementations,
                "dependencies": {
                    "providers": sorted(dep for dep in package.dependencies if (owner := next((candidate for candidate in packages if candidate.distribution == dep), None)) and owner.layer == "20-providers"),
                    "durability": sorted(dep for dep in package.dependencies if (owner := next((candidate for candidate in packages if candidate.distribution == dep), None)) and owner.layer == "30-storage-runtime"),
                    "capabilities": sorted(dep for dep in package.dependencies if (owner := next((candidate for candidate in packages if candidate.distribution == dep), None)) and owner.layer == "40-capabilities"),
                },
                "protocol_packages": sorted(protocol_consumers.get(package.distribution, ())),
            }
        )
    return {"schema_version": 1, "capabilities": records}


if __name__ == "__main__":
    print(json.dumps(build_registry(), indent=2, sort_keys=True))

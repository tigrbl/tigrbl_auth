from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

import yaml

PROFILE_SEQUENCE = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")
PROFILE_GROUPS = {
    "baseline": ("baseline",),
    "production": ("baseline", "production"),
    "hardening": ("baseline", "production", "hardening"),
    "fapi2-security": ("baseline", "production", "hardening", "fapi2-security"),
    "peer-claim": ("baseline", "production", "hardening"),
}
PUBLIC_ROUTE_SEARCH_ROOTS = (
    "tigrbl_auth/api/rest/routers",
    "tigrbl_auth/standards/oauth2",
    "tigrbl_auth/standards/oidc",
)
OPENAPI_TARGET_LABEL = "OpenAPI 3.1 / 3.2 compatible public contract"
OPENRPC_TARGET_LABEL = "OpenRPC 1.4.x admin/control-plane contract"
ROUTE_CONSTANTS = {"JWKS_PATH": "/.well-known/jwks.json"}
WELL_KNOWN_ENDPOINTS = {"oauth_protected_resource": "/.well-known/oauth-protected-resource"}


def write_report(report_dir: Path, stem: str, payload: dict[str, Any], title: str) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / f"{stem}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [f"# {title}", "", f"- Passed: `{payload.get('passed', False)}`", ""]
    if payload.get("summary"):
        lines.extend(["## Summary", ""])
        for key, value in payload["summary"].items():
            lines.append(f"- {key}: `{value}`")
        lines.append("")
    if payload.get("failures"):
        lines.extend(["## Failures", ""])
        lines.extend(f"- {item}" for item in payload["failures"])
        lines.append("")
    if payload.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {item}" for item in payload["warnings"])
        lines.append("")
    (report_dir / f"{stem}.md").write_text("\n".join(lines), encoding="utf-8")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _assignment_value(tree: ast.Module, name: str) -> ast.AST:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            return node.value
    raise KeyError(name)


def literal_assignment(path: Path, name: str) -> Any:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    value = _assignment_value(tree, name)
    return ast.literal_eval(value)


def load_public_capabilities(repo_root: Path) -> list[dict[str, Any]]:
    return list(literal_assignment(repo_root / "tigrbl_auth/config/surfaces.py", "PUBLIC_CAPABILITIES"))


def load_diagnostics_capabilities(repo_root: Path) -> list[dict[str, Any]]:
    return list(literal_assignment(repo_root / "tigrbl_auth/config/surfaces.py", "DIAGNOSTICS_CAPABILITIES"))


def capability_registry(repo_root: Path) -> dict[str, dict[str, Any]]:
    items = load_public_capabilities(repo_root) + load_diagnostics_capabilities(repo_root)
    return {str(item["capability"]): dict(item) for item in items}


def route_registry(repo_root: Path) -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for item in load_public_capabilities(repo_root) + load_diagnostics_capabilities(repo_root):
        for path in item.get("paths", ()):
            registry[str(path)] = {
                "capability": str(item["capability"]),
                "surface_set": str(item.get("surface_set", "")),
                "methods": tuple(str(method).lower() for method in item.get("methods", ())),
                "flags": tuple(str(flag) for flag in item.get("flags", ())),
                "kind": str(item.get("kind", "")),
                "router_ref": item.get("router_ref"),
                "publisher_ref": item.get("publisher_ref"),
                "contract_visible": bool(item.get("contract_visible", True)),
                "discovery_visible": bool(item.get("discovery_visible", False)),
            }
    return registry


def load_feature_flag_groups(repo_root: Path) -> dict[str, dict[str, Any]]:
    return dict(literal_assignment(repo_root / "tigrbl_auth/config/feature_flags.py", "FEATURE_FLAG_GROUPS"))


def active_flags_for_profile(repo_root: Path, profile: str) -> set[str]:
    groups = load_feature_flag_groups(repo_root)
    active: set[str] = set(groups.get("operations", {}).get("flags", {}).keys())
    active.update(groups.get("surface", {}).get("flags", {}).keys())
    for group_name in PROFILE_GROUPS.get(profile, ("baseline",)):
        active.update(groups.get(group_name, {}).get("flags", {}).keys())
    return active


def expected_public_paths_for_profile(repo_root: Path, profile: str) -> list[str]:
    active_flags = active_flags_for_profile(repo_root, profile)
    paths: list[str] = []
    for item in load_public_capabilities(repo_root):
        flags = tuple(str(flag) for flag in item.get("flags", ()))
        if all(flag in active_flags for flag in flags):
            for path in item.get("paths", ()):
                path_str = str(path)
                if path_str not in paths:
                    paths.append(path_str)
    return paths


def expected_discovery_paths_for_profile(repo_root: Path, profile: str) -> list[str]:
    active_flags = active_flags_for_profile(repo_root, profile)
    paths: list[str] = []
    for item in load_public_capabilities(repo_root):
        flags = tuple(str(flag) for flag in item.get("flags", ()))
        if all(flag in active_flags for flag in flags) and bool(item.get("discovery_visible", False)):
            for path in item.get("paths", ()):
                path_str = str(path)
                if path_str not in paths:
                    paths.append(path_str)
    return paths


def openapi_contract_path(repo_root: Path, profile: str) -> Path:
    return repo_root / "specs" / "openapi" / "profiles" / profile / "tigrbl_auth.public.openapi.json"


def openrpc_contract_path(repo_root: Path, profile: str) -> Path:
    return repo_root / "specs" / "openrpc" / "profiles" / profile / "tigrbl_auth.admin.openrpc.json"


def discovery_snapshot_dir(repo_root: Path, profile: str) -> Path:
    return repo_root / "specs" / "discovery" / "profiles" / profile


def load_openapi_paths(repo_root: Path, profile: str) -> list[str]:
    return list(load_json(openapi_contract_path(repo_root, profile)).get("paths", {}).keys())


def load_openrpc_method_names(repo_root: Path, profile: str) -> list[str]:
    return [str(item.get("name")) for item in load_json(openrpc_contract_path(repo_root, profile)).get("methods", [])]


def _literal_str(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _literal_route_path(node: ast.AST) -> str | None:
    literal = _literal_str(node)
    if literal is not None:
        return literal
    if isinstance(node, ast.Name):
        return ROUTE_CONSTANTS.get(node.id)
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "WELL_KNOWN_ENDPOINTS":
        key_node = node.slice
        if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
            return WELL_KNOWN_ENDPOINTS.get(key_node.value)
    return None


def _literal_methods(node: ast.AST) -> list[str]:
    if isinstance(node, (ast.Tuple, ast.List)):
        values: list[str] = []
        for item in node.elts:
            value = _literal_str(item)
            if value is not None:
                values.append(value.lower())
        return values
    return []


def extract_route_definitions(repo_root: Path) -> dict[str, dict[str, Any]]:
    extracted: dict[str, dict[str, Any]] = {}
    for rel_root in PUBLIC_ROUTE_SEARCH_ROOTS:
        base = repo_root / rel_root
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            rel = str(path.relative_to(repo_root)).replace("\\", "/")
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for decorator in node.decorator_list:
                    if not isinstance(decorator, ast.Call):
                        continue
                    func = decorator.func
                    if not isinstance(func, ast.Attribute) or func.attr != "route":
                        continue
                    route_path: str | None = None
                    methods: list[str] = []
                    if decorator.args:
                        route_path = _literal_route_path(decorator.args[0])
                    for keyword in decorator.keywords:
                        if keyword.arg == "methods":
                            methods = _literal_methods(keyword.value)
                    if route_path is None:
                        continue
                    entry = extracted.setdefault(route_path, {"methods": set(), "files": set()})
                    entry["files"].add(rel)
                    entry["methods"].update(methods)
    normalized: dict[str, dict[str, Any]] = {}
    for path, entry in extracted.items():
        normalized[path] = {
            "methods": sorted(entry["methods"]),
            "files": sorted(entry["files"]),
        }
    return normalized


def _call_keyword_map(call: ast.Call) -> dict[str, ast.AST]:
    return {keyword.arg: keyword.value for keyword in call.keywords if keyword.arg}


def _extract_rpc_methods_from_methods_tuple(node: ast.AST) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not isinstance(node, (ast.Tuple, ast.List)):
        return items
    for elt in node.elts:
        if not isinstance(elt, ast.Call):
            continue
        func = elt.func
        func_name = None
        if isinstance(func, ast.Name):
            func_name = func.id
        elif isinstance(func, ast.Attribute):
            func_name = func.attr
        if func_name != "RpcMethodDefinition":
            continue
        keywords = _call_keyword_map(elt)
        name = _literal_str(keywords.get("name")) if keywords.get("name") is not None else None
        owner = _literal_str(keywords.get("owner_module")) if keywords.get("owner_module") is not None else None
        surface_set = _literal_str(keywords.get("surface_set")) if keywords.get("surface_set") is not None else "admin-rpc"
        required_flags = tuple(_literal_methods(keywords.get("required_flags"))) if keywords.get("required_flags") is not None else ()
        if not name:
            continue
        items.append({
            "name": name,
            "owner_module": owner,
            "surface_set": surface_set,
            "required_flags": required_flags,
        })
    return items


def extract_rpc_method_definitions(repo_root: Path) -> dict[str, dict[str, Any]]:
    extracted: dict[str, dict[str, Any]] = {}
    base = repo_root / "tigrbl_auth/api/rpc/methods"
    for path in sorted(base.glob("*.py")):
        if path.name.startswith("_") or path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.Assign):
                if any(isinstance(target, ast.Name) and target.id == "METHODS" for target in node.targets):
                    for item in _extract_rpc_methods_from_methods_tuple(node.value):
                        extracted[item["name"]] = item
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "METHODS":
                for item in _extract_rpc_methods_from_methods_tuple(node.value):
                    extracted[item["name"]] = item
    return dict(sorted(extracted.items()))


def expected_openrpc_methods_for_profile(repo_root: Path, profile: str) -> list[str]:
    active_flags = active_flags_for_profile(repo_root, profile)
    expected: list[str] = []
    for name, meta in extract_rpc_method_definitions(repo_root).items():
        required_flags = tuple(str(flag) for flag in meta.get("required_flags", ()))
        if all(flag in active_flags for flag in required_flags):
            expected.append(name)
    return expected


def in_scope_targets(repo_root: Path) -> list[dict[str, Any]]:
    scope = load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml") or {}
    targets: list[dict[str, Any]] = []
    for item in scope.get("targets", []):
        if str(item.get("scope_bucket")) == "out-of-scope/deferred":
            continue
        targets.append(item)
    return targets


def target_index(repo_root: Path) -> dict[str, dict[str, Any]]:
    return {str(item.get("label")): item for item in in_scope_targets(repo_root)}


def target_route_mappings(repo_root: Path) -> dict[str, Any]:
    return load_yaml(repo_root / "compliance" / "mappings" / "target-to-endpoint.yaml") or {}


def target_module_mappings(repo_root: Path) -> dict[str, Any]:
    return load_yaml(repo_root / "compliance" / "mappings" / "target-to-module.yaml") or {}


def target_test_mappings(repo_root: Path) -> dict[str, Any]:
    return load_yaml(repo_root / "compliance" / "mappings" / "target-to-test.yaml") or {}


def target_evidence_mappings(repo_root: Path) -> dict[str, Any]:
    return load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml") or {}


ALLOWED_TEST_CATEGORIES = (
    "unit",
    "integration",
    "conformance",
    "interop",
    "e2e",
    "security",
    "negative",
    "security-negative",
    "migration-portability",
    "peer",
    "perf",
)
_AUXILIARY_TEST_CATEGORY_BY_PREFIX = {
    "tests/examples/": "e2e",
    "tests/uix/": "e2e",
}


def resolve_test_classification_path(repo_root: Path) -> Path:
    preferred = repo_root / "compliance" / "mappings" / "test_classification.yaml"
    legacy = repo_root / "compliance" / "mappings" / "test-classification.yaml"
    return preferred if preferred.exists() else legacy


def load_test_classification(repo_root: Path) -> dict[str, Any]:
    path = resolve_test_classification_path(repo_root)
    return load_yaml(path) or {}


def categorized_tests(repo_root: Path) -> dict[str, list[str]]:
    mapping = load_test_classification(repo_root)
    return {str(category): [str(rel).replace("\\", "/") for rel in files] for category, files in (mapping.get("categories") or {}).items()}


def classified_tests(repo_root: Path) -> set[str]:
    classified: set[str] = set()
    for files in categorized_tests(repo_root).values():
        for rel in files:
            classified.add(str(rel).replace("\\", "/"))
    return classified


def collect_test_files(repo_root: Path) -> set[str]:
    discovered: set[str] = set()
    for path in sorted((repo_root / "tests").glob("**/test_*.py")):
        discovered.add(str(path.relative_to(repo_root)).replace("\\", "/"))
    return discovered


def infer_test_category(rel_path: str) -> str | None:
    normalized = rel_path.replace("\\", "/")
    prefixes = {
        "tests/unit/": "unit",
        "tests/integration/": "integration",
        "tests/runtime/": "integration",
        "tests/conformance/": "conformance",
        "tests/interop/": "interop",
        "tests/e2e/": "e2e",
        "tests/security/": "security",
        "tests/negative/": "negative",
        "tests/perf/": "perf",
    }
    for prefix, category in prefixes.items():
        if normalized.startswith(prefix):
            return category
    for prefix, category in _AUXILIARY_TEST_CATEGORY_BY_PREFIX.items():
        if normalized.startswith(prefix):
            return category
    return None


def verify_test_classification_manifest(repo_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    mapping_path = resolve_test_classification_path(repo_root)
    mapping = load_test_classification(repo_root)
    categories = mapping.get("categories") or {}
    if not categories:
        failures.append("Missing test classification categories")
    if not (repo_root / "compliance" / "mappings" / "test_classification.yaml").exists():
        failures.append("Missing canonical test classification manifest: compliance/mappings/test_classification.yaml")
    unknown_categories = sorted(set(categories) - set(ALLOWED_TEST_CATEGORIES))
    for category in unknown_categories:
        failures.append(f"Unknown test classification category: {category}")
    duplicates: dict[str, list[str]] = {}
    for category, files in categories.items():
        if category in ALLOWED_TEST_CATEGORIES and not (repo_root / "tests" / category).exists() and category != "conformance":
            warnings.append(f"Category directory missing for {category}: tests/{category}")
        for rel in files:
            normalized = str(rel).replace("\\", "/")
            duplicates.setdefault(normalized, []).append(str(category))
            if not path_exists(repo_root, normalized):
                failures.append(f"Missing classified test file: {normalized}")
            inferred = infer_test_category(normalized)
            if inferred is None:
                failures.append(f"Classified test path is outside supported test roots: {normalized}")
            elif inferred != category:
                failures.append(f"Classified test path category mismatch: {normalized} mapped={category} inferred={inferred}")
    for rel, cats in sorted(duplicates.items()):
        if len(cats) > 1:
            failures.append(f"Classified test file appears in multiple categories: {rel} -> {', '.join(sorted(cats))}")
    discovered = collect_test_files(repo_root)
    classified = classified_tests(repo_root)
    unclassified = sorted(discovered - classified)
    if unclassified:
        failures.append(f"Unclassified test files present: {', '.join(unclassified)}")
    legacy_i9n = sorted(str(path.relative_to(repo_root)).replace("\\", "/") for path in (repo_root / "tests" / "i9n").glob("test_*.py")) if (repo_root / "tests" / "i9n").exists() else []
    if legacy_i9n:
        failures.append(f"Legacy tests/i9n migration incomplete: {', '.join(legacy_i9n)}")
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "mapping_path": str(mapping_path.relative_to(repo_root)) if mapping_path.exists() else None,
            "category_count": len(categories),
            "classified_test_count": len(classified),
            "discovered_test_count": len(discovered),
        },
    }


def path_exists(repo_root: Path, rel_path: str) -> bool:
    path = repo_root / rel_path
    if path.is_file():
        return True
    if path.is_dir():
        return any(path.iterdir())
    return False


def verify_target_module_mapping(repo_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    targets = target_index(repo_root)
    mappings = target_module_mappings(repo_root)
    for label, item in targets.items():
        mapped = list((mappings.get(label) or {}).get("modules", []))
        scope_modules = [str(value) for value in item.get("owner_modules", [])]
        if not mapped:
            failures.append(f"{label}: missing target-to-module mapping")
            continue
        missing = [rel for rel in mapped if not path_exists(repo_root, str(rel))]
        for rel in missing:
            failures.append(f"{label}: mapped module path missing: {rel}")
        if sorted(str(rel) for rel in mapped) != sorted(scope_modules):
            warnings.append(f"{label}: certification_scope owner_modules differ from target-to-module mapping")
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "in_scope_target_count": len(targets),
            "mapped_target_count": sum(1 for label in targets if label in mappings),
        },
    }


def verify_target_route_mapping(repo_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    targets = target_index(repo_root)
    mappings = target_route_mappings(repo_root)
    route_defs = extract_route_definitions(repo_root)
    capability_routes = route_registry(repo_root)
    contract_paths_by_profile = {profile: set(load_openapi_paths(repo_root, profile)) for profile in PROFILE_SEQUENCE if profile != "peer-claim"}
    for label, item in targets.items():
        if label in {OPENAPI_TARGET_LABEL, OPENRPC_TARGET_LABEL}:
            continue
        mapping = mappings.get(label) or {}
        current_paths = [str(path) for path in mapping.get("current", [])]
        if not current_paths:
            continue
        for path in current_paths:
            if path not in capability_routes:
                failures.append(f"{label}: mapped current route not present in capability registry: {path}")
            if path not in route_defs:
                failures.append(f"{label}: mapped current route has no decorated implementation: {path}")
            if not any(path in paths for paths in contract_paths_by_profile.values()):
                failures.append(f"{label}: mapped current route not present in any profile OpenAPI snapshot: {path}")
        profile_reality = item.get("profile_reality", {})
        for profile in ("baseline", "production", "hardening"):
            reality = profile_reality.get(profile) or {}
            present_paths = set(str(path) for path in reality.get("openapi_paths_present", []))
            missing_paths = present_paths - contract_paths_by_profile.get(profile, set())
            if missing_paths:
                failures.append(
                    f"{label}: profile_reality for {profile} references OpenAPI paths missing from the committed contract: {', '.join(sorted(missing_paths))}"
                )
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "mapped_target_count": sum(1 for label in targets if (mappings.get(label) or {}).get("current")),
            "route_definition_count": len(route_defs),
            "capability_route_count": len(capability_routes),
        },
    }


def verify_target_contract_mapping(repo_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    capability_routes = route_registry(repo_root)
    source_routes = extract_route_definitions(repo_root)
    for profile in ("baseline", "production", "hardening"):
        expected_paths = expected_public_paths_for_profile(repo_root, profile)
        actual_paths = load_openapi_paths(repo_root, profile)
        if expected_paths != actual_paths:
            failures.append(
                f"{profile}: OpenAPI paths drift from executable capability wiring: expected={expected_paths} actual={actual_paths}"
            )
        for path in actual_paths:
            if path not in capability_routes:
                failures.append(f"{profile}: OpenAPI publishes path without capability entry: {path}")
            if path not in source_routes:
                failures.append(f"{profile}: OpenAPI publishes path without decorated implementation: {path}")
        discovery_dir = discovery_snapshot_dir(repo_root, profile)
        for name in ("openid-configuration.json", "oauth-authorization-server.json", "jwks.json"):
            if not (discovery_dir / name).exists():
                failures.append(f"{profile}: missing discovery snapshot {name}")
        expected_discovery = set(expected_discovery_paths_for_profile(repo_root, profile))
        if "/.well-known/oauth-protected-resource" in expected_discovery and not (discovery_dir / "oauth-protected-resource.json").exists():
            failures.append(f"{profile}: missing discovery snapshot oauth-protected-resource.json")
        if "/.well-known/oauth-protected-resource" not in expected_discovery and (discovery_dir / "oauth-protected-resource.json").exists():
            warnings.append(f"{profile}: protected-resource snapshot exists even though the profile does not publish that surface")
    rpc_defs = extract_rpc_method_definitions(repo_root)
    for profile in ("baseline", "production", "hardening", "peer-claim"):
        expected_methods = expected_openrpc_methods_for_profile(repo_root, profile)
        actual_methods = load_openrpc_method_names(repo_root, profile)
        if expected_methods != actual_methods:
            failures.append(
                f"{profile}: OpenRPC methods drift from implementation-backed method modules: expected={expected_methods} actual={actual_methods}"
            )
    for name, meta in rpc_defs.items():
        owner = str(meta.get("owner_module") or "")
        if not owner:
            failures.append(f"RPC method {name} is missing owner_module metadata")
        elif not path_exists(repo_root, owner):
            failures.append(f"RPC method {name} owner_module path missing: {owner}")
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "capability_public_path_count": len([path for path, meta in capability_routes.items() if meta.get("surface_set") == "public-rest"]),
            "rpc_method_definition_count": len(rpc_defs),
        },
    }


def verify_target_test_mapping(repo_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    targets = target_index(repo_root)
    mappings = target_test_mappings(repo_root)
    classification_report = verify_test_classification_manifest(repo_root)
    failures.extend(classification_report["failures"])
    warnings.extend(classification_report["warnings"])
    classified = classified_tests(repo_root)
    for label in targets:
        refs = [str(value).replace("\\", "/") for value in (mappings.get(label) or [])]
        if not refs:
            failures.append(f"{label}: missing target-to-test mapping")
            continue
        for rel in refs:
            if not path_exists(repo_root, rel):
                failures.append(f"{label}: mapped test path missing: {rel}")
            if rel not in classified:
                failures.append(f"{label}: mapped test path is not present in the canonical test classification manifest: {rel}")
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "in_scope_target_count": len(targets),
            "classified_test_count": len(classified),
            "discovered_test_count": len(collect_test_files(repo_root)),
        },
    }


def verify_target_evidence_mapping(repo_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    targets = target_index(repo_root)
    mappings = target_evidence_mappings(repo_root)
    for label in targets:
        refs = [str(value) for value in (mappings.get(label) or [])]
        if not refs:
            failures.append(f"{label}: missing target-to-evidence mapping")
            continue
        for rel in refs:
            normalized = rel.replace("\\", "/")
            if not path_exists(repo_root, normalized):
                failures.append(f"{label}: mapped evidence ref missing: {normalized}")
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "in_scope_target_count": len(targets),
            "mapped_target_count": sum(1 for label in targets if mappings.get(label)),
        },
    }


def verify_feature_surface_modularity(repo_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    capability_map = capability_registry(repo_root)
    route_map = route_registry(repo_root)
    surface_yaml = load_yaml(repo_root / "compliance" / "targets" / "public-operator-surface.yaml") or {}
    current_routes = list((((surface_yaml.get("surfaces") or {}).get("public_auth_plane") or {}).get("checkpoint_current") or {}).get("routes", []))
    expected_routes = [path for path, meta in route_map.items() if meta.get("surface_set") == "public-rest" and meta.get("contract_visible")]
    if set(current_routes) != set(expected_routes):
        failures.append(f"public-operator-surface current routes drift from capability registry: expected={expected_routes} actual={current_routes}")
    if "attach_runtime_surfaces(" not in (repo_root / "tigrbl_auth/plugin.py").read_text(encoding="utf-8"):
        failures.append("plugin.py does not install surfaces through attach_runtime_surfaces")
    if "attach_runtime_surfaces(" not in (repo_root / "tigrbl_auth/api/app.py").read_text(encoding="utf-8"):
        failures.append("api/app.py does not install surfaces through attach_runtime_surfaces")
    source_routes = extract_route_definitions(repo_root)
    for capability, meta in capability_map.items():
        paths = tuple(str(path) for path in meta.get("paths", ()))
        if meta.get("surface_set") == "public-rest" and bool(meta.get("contract_visible", True)):
            if not paths:
                failures.append(f"{capability}: public capability is missing route paths")
        ref = meta.get("router_ref") or meta.get("publisher_ref")
        if meta.get("surface_set") == "public-rest" and not ref:
            failures.append(f"{capability}: public capability is missing router_ref/publisher_ref")
        if meta.get("surface_set") != "public-rest":
            continue
        for path in paths:
            if path not in source_routes:
                failures.append(f"{capability}: capability path has no decorated implementation: {path}")
    module_report = verify_target_module_mapping(repo_root)
    route_report = verify_target_route_mapping(repo_root)
    test_report = verify_target_test_mapping(repo_root)
    evidence_report = verify_target_evidence_mapping(repo_root)
    for report in (module_report, route_report, test_report, evidence_report):
        failures.extend(report["failures"])
        warnings.extend(report["warnings"])
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "capability_count": len(capability_map),
            "public_route_count": len(expected_routes),
            "module_mapping_failures": len(module_report["failures"]),
            "route_mapping_failures": len(route_report["failures"]),
            "test_mapping_failures": len(test_report["failures"]),
            "evidence_mapping_failures": len(evidence_report["failures"]),
        },
    }


def verify_contract_sync(repo_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    contract_report = verify_target_contract_mapping(repo_root)
    failures.extend(contract_report["failures"])
    warnings.extend(contract_report["warnings"])
    route_report = verify_target_route_mapping(repo_root)
    failures.extend(route_report["failures"])
    warnings.extend(route_report["warnings"])
    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "contract_mapping_failures": len(contract_report["failures"]),
            "route_mapping_failures": len(route_report["failures"]),
            "baseline_path_count": len(load_openapi_paths(repo_root, "baseline")),
            "production_path_count": len(load_openapi_paths(repo_root, "production")),
            "hardening_path_count": len(load_openapi_paths(repo_root, "hardening")),
        },
    }

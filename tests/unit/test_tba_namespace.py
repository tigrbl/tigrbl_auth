"""Guard the downstream namespace without renaming the upstream framework."""
from pathlib import Path
import ast
import json
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
import subprocess
import io

ROOT = Path(__file__).resolve().parents[2]


def test_workspace_package_names_and_sources_use_tba():
    root = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    manifests = list((ROOT / "pkgs").rglob("pyproject.toml"))
    names = [tomllib.loads(p.read_text(encoding="utf-8"))["project"]["name"] for p in manifests if "deprecated" not in p.parts]
    assert len(names) == len(set(names))
    assert all(name.startswith("tba-") or name in {"tba", "tbauth"} for name in names)
    assert root["project"]["name"] == "tba-workspace"
    for name, source in root["tool"]["uv"]["sources"].items():
        if "path" in source:
            target = ROOT / source["path"] / "pyproject.toml"
            assert target.is_file(), source
            assert tomllib.loads(target.read_text(encoding="utf-8"))["project"]["name"] == name
    assert "tigrbl==0.4.5.dev4" in root["project"]["dependencies"]
    assert "tigrbl-runtime==0.4.5.dev4" in root["project"]["dependencies"]


def test_npm_manifests_and_local_dependencies_use_tba():
    for path in (ROOT / "pkgs").rglob("package.json"):
        if "node_modules" in path.parts:
            continue
        manifest = json.loads(path.read_text(encoding="utf-8"))
        assert manifest["name"].startswith("@tba/"), path
        for group in ("dependencies", "devDependencies", "peerDependencies"):
            assert not any(name.startswith("@tigrbl" + "-auth/") for name in manifest.get(group, {})), path
            for name, requirement in manifest.get(group, {}).items():
                if requirement.startswith("file:"):
                    target = (path.parent / requirement.removeprefix("file:")).resolve()
                    assert (target / "package.json").is_file(), (path, requirement)
                    assert json.loads((target / "package.json").read_text())["name"] == name


def test_local_python_imports_do_not_use_the_old_suite_namespace():
    old_prefixes = tuple("tigrbl" + suffix for suffix in ("_auth", "_identity", "_claim", "_security", "_workload"))
    for path in (ROOT / "pkgs").rglob("*.py"):
        if any(part in {"node_modules", "build", "dist", "__pycache__", "deprecated"} for part in path.parts):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        for node in ast.walk(tree):
            imports = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
            assert not any(name.startswith(old_prefixes) for name in imports), path


def test_deprecated_packages_remain_byte_for_byte_legacy():
    paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "pkgs/deprecated"], cwd=ROOT
    ).decode().splitlines()
    refs = "".join(f"HEAD:{path}\n" for path in paths).encode()
    stream = io.BytesIO(subprocess.run(
        ["git", "cat-file", "--batch"], input=refs, stdout=subprocess.PIPE, check=True, cwd=ROOT
    ).stdout)
    for path in paths:
        size = int(stream.readline().split()[2])
        assert (ROOT / path).read_bytes() == stream.read(size), path
        assert stream.read(1) == b"\n"


def test_active_package_directories_have_suite_prefixes():
    for filename in ("pyproject.toml", "package.json"):
        for path in (ROOT / "pkgs").glob(f"*/*/{filename}"):
            if "deprecated" not in path.parts:
                assert path.parent.name.startswith("tba-") or path.parent.name in {"tba", "tbauth"}, path


def test_layer_75_contains_only_explicit_client_names():
    layer = ROOT / "pkgs/75-clients"
    expected = {
        "tba-client-authorization-admin",
        "tba-client-policy-decision",
        "tba-client-relying-party-session",
        "tba-typescript-client-oidc-relying-party",
        "tba-typescript-client-relying-party-session",
        "tba-typescript-client-policy-decision",
        "tba-typescript-client-platform-admin",
        "tba-typescript-client-tenant-admin",
    }
    actual = {p.parent.name for name in ("pyproject.toml", "package.json") for p in layer.glob(f"*/{name}")}
    assert actual == expected


def test_protocol_and_profile_roles_are_prefixes_in_separate_layers():
    for layer, role in (("50-protocols", "protocol"), ("55-profiles", "profile")):
        paths = list((ROOT / "pkgs" / layer).glob("*/pyproject.toml"))
        assert paths
        for path in paths:
            name = tomllib.loads(path.read_text(encoding="utf-8"))["project"]["name"]
            assert name.startswith(f"tba-{role}-"), name
    from scripts.package_layer_policy import dependency_allowed, load_layer_policy
    policy = load_layer_policy(ROOT / "pkgs/layers.toml")
    assert policy.by_id["55-profiles"].category == "index"
    assert dependency_allowed("55-profiles", "50-protocols", policy)
    assert not dependency_allowed("50-protocols", "55-profiles", policy)


def test_approved_role_first_matrix_matches_live_packages():
    rows = json.loads((ROOT / "docs/packaging/role-first-renaming.json").read_text())
    roles = {"primitives", "storage", "contracts", "bases", "concrete", "provider", "durability", "capability", "protocol", "profile", "runtime", "server", "operator", "cli", "plugin", "certification", "client", "router", "middleware", "app", "ui", "example", "testkit"}
    seen = set()
    for row in rows:
        directory = ROOT / row["new_path"]
        if row["registry"] == "Python":
            metadata = tomllib.loads((directory / "pyproject.toml").read_text(encoding="utf-8"))
            name = metadata["project"]["name"]
        else:
            name = json.loads((directory / "package.json").read_text())["name"]
        assert name == row["proposed_name"]
        assert (row["registry"], name) not in seen
        seen.add((row["registry"], name))
        if row["current_layer"] == "70-facade":
            assert name == row["current_name"]
        else:
            stem = name.removeprefix("@tba/").removeprefix("tba-")
            role, separator, subject = stem.partition("-")
            assert role in roles and separator and subject, name


def test_middleware_is_above_clients_with_narrow_dependencies():
    from scripts.package_layer_policy import dependency_allowed, load_layer_policy

    policy = load_layer_policy(ROOT / "pkgs/layers.toml")
    assert policy.by_id["75-clients"].order < policy.by_id["80-routers"].order < policy.by_id["85-middleware"].order < policy.by_id["90-backend-apps"].order
    assert dependency_allowed("85-middleware", "02-contracts", policy)
    assert dependency_allowed("85-middleware", "75-clients", policy)
    assert dependency_allowed("90-backend-apps", "85-middleware", policy)
    assert not dependency_allowed("85-middleware", "80-routers", policy)
    assert not dependency_allowed("85-middleware", "90-backend-apps", policy)
    assert not dependency_allowed("75-clients", "85-middleware", policy)
    assert not dependency_allowed("80-routers", "85-middleware", policy)
    assert (ROOT / "pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/pyproject.toml").is_file()
    assert not (ROOT / "pkgs/75-clients/tba-middleware-policy-enforcement-asgi").exists()

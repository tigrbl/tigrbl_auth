"""Guard the separate OAuth and GNAP distribution and import boundaries."""

import ast
from pathlib import Path

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

try:
    from tomllib import loads
except ModuleNotFoundError:
    from tomli import loads


ROOT = Path(__file__).resolve().parents[5]
PROTOCOLS = ROOT / "pkgs/050-protocols"


def dependency_closure(project: str) -> set[str]:
    lock = loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    graph: dict[str, set[str]] = {}
    for package in lock["package"]:
        graph.setdefault(package["name"], set()).update(
            dep["name"] for dep in package.get("dependencies", ())
        )
    pending = list(graph[project])
    seen: set[str] = set()
    while pending:
        name = pending.pop()
        if name not in seen:
            seen.add(name)
            pending.extend(graph.get(name, ()))
    return seen


@pytest.mark.parametrize(("protocol", "peer"), [("oauth", "gnap"), ("gnap", "oauth")])
def test_protocol_distribution_is_independent(protocol: str, peer: str) -> None:
    name = f"tba-protocol-{protocol}"
    manifest = loads((PROTOCOLS / name / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    requirements = list(manifest.get("dependencies", ()))
    for extra in manifest.get("optional-dependencies", {}).values():
        requirements.extend(extra)
    forbidden = {f"tba-protocol-{peer}", f"tigrbl-identity-{peer}"}

    assert forbidden.isdisjoint(canonicalize_name(Requirement(item).name) for item in requirements)
    assert forbidden.isdisjoint(dependency_closure(name))


@pytest.mark.parametrize(("protocol", "peer"), [("oauth", "gnap"), ("gnap", "oauth")])
def test_protocol_source_avoids_peer_imports(protocol: str, peer: str) -> None:
    source = PROTOCOLS / f"tba-protocol-{protocol}" / "src" / f"tba_protocol_{protocol}"
    modules = list(source.rglob("*.py"))
    assert modules, source
    forbidden = {f"tba_protocol_{peer}", f"tigrbl_identity_{peer}"}
    for path in modules:
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=str(path))):
            if isinstance(node, ast.Import):
                assert forbidden.isdisjoint(alias.name.partition(".")[0] for alias in node.names), path
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                assert node.module.partition(".")[0] not in forbidden, path

from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


USER_PLANE_ROOT = (
    ROOT
    / "pkgs"
    / "00-core"
    / "tigrbl-user-plane-contracts"
    / "src"
    / "tigrbl_user_plane_contracts"
)


ALLOWED_PUBLIC_FUNCTIONS = {
    "authz/authority_graph.py": {"authority_matches"},
}


FORBIDDEN_BEHAVIOR_CLASSES = {
    "AuthorityDerivationGraph",
    "AuthorizationSafetyPropertyEvaluator",
    "CredentialLedger",
    "InvariantRegistry",
    "IntrospectionClient",
    "JWKSCache",
    "PolicyDecisionEngine",
    "ResourceServerVerifier",
}


def test_user_plane_contracts_do_not_define_runtime_behavior_functions() -> None:
    offenders: list[str] = []
    for path in USER_PLANE_ROOT.rglob("*.py"):
        rel = path.relative_to(USER_PLANE_ROOT).as_posix()
        allowed = ALLOWED_PUBLIC_FUNCTIONS.get(rel, set())
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_") or node.name in allowed:
                    continue
                offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}:{node.name}")

    assert offenders == []


def test_user_plane_contracts_do_not_define_runtime_behavior_classes() -> None:
    offenders: list[str] = []
    for path in USER_PLANE_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in FORBIDDEN_BEHAVIOR_CLASSES:
                offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}:{node.name}")

    assert offenders == []


def test_moved_runtime_behavior_imports_from_capability_packages() -> None:
    from tigrbl_authn_credentials import CredentialLedger, hash_secret
    from tigrbl_authz_policy import (
        AuthorityDerivationGraph,
        InvariantRegistry,
        PolicyDecisionEngine,
        evaluate_liveness_convergence,
        replay_policy_determinism,
    )
    from tigrbl_authz_resource_server import JWKSCache, ResourceServerVerifier

    assert CredentialLedger.__module__.startswith("tigrbl_authn_credentials")
    assert hash_secret.__module__.startswith("tigrbl_authn_credentials")
    assert AuthorityDerivationGraph.__module__.startswith("tigrbl_authz_policy")
    assert InvariantRegistry.__module__.startswith("tigrbl_authz_policy")
    assert PolicyDecisionEngine.__module__.startswith("tigrbl_authz_policy")
    assert evaluate_liveness_convergence.__module__.startswith("tigrbl_authz_policy")
    assert replay_policy_determinism.__module__.startswith("tigrbl_authz_policy")
    assert JWKSCache.__module__.startswith("tigrbl_authz_resource_server")
    assert ResourceServerVerifier.__module__.startswith("tigrbl_authz_resource_server")

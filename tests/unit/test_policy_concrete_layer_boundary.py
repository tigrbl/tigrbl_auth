from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_ROOT = (
    ROOT
    / "pkgs"
    / "01-contracts"
    / "tigrbl-identity-contracts"
    / "src"
    / "tigrbl_identity_contracts"
)
CONCRETE_ROOT = (
    ROOT
    / "pkgs"
    / "10-concrete"
    / "tigrbl-authz-policy-concrete"
    / "src"
    / "tigrbl_authz_policy_concrete"
)


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_contracts_do_not_own_concrete_policy_rule_variants() -> None:
    import tigrbl_identity_contracts.policy.rules as rules

    concrete_names = {
        "AdminPolicy",
        "AttributePolicy",
        "DelegationPolicy",
        "PermissionPolicy",
        "RolePolicy",
    }

    assert rules.PolicyRule.__module__ == "tigrbl_identity_contracts.policy.rules"
    assert not (concrete_names & set(dir(rules)))


def test_policy_variants_subclass_contract_dataclass() -> None:
    import tigrbl_authz_policy_concrete as concrete
    from tigrbl_identity_contracts.policy.rules import PolicyRule

    for name in (
        "AdminPolicy",
        "AttributePolicy",
        "DelegationPolicy",
        "PermissionPolicy",
        "RolePolicy",
    ):
        assert issubclass(getattr(concrete, name), PolicyRule), name


def test_policy_concrete_layer_only_imports_lower_contract_surfaces() -> None:
    allowed = {
        "__future__",
        "dataclasses",
        "typing",
        "tigrbl_identity_contracts",
    }

    offenders = {
        str(path.relative_to(ROOT)): sorted(_imports(path) - allowed)
        for path in CONCRETE_ROOT.rglob("*.py")
        if _imports(path) - allowed
    }

    assert offenders == {}

from __future__ import annotations

import ast
import importlib
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "pkgs" / "02-contracts" / "tigrbl-security-trust-contracts"
BASES = ROOT / "pkgs" / "05-bases" / "tigrbl-security-trust-domain-bases"


def _absolute_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def test_security_trust_contracts_are_dependency_free_protocols() -> None:
    metadata = tomllib.loads((CONTRACTS / "pyproject.toml").read_text(encoding="utf-8"))

    assert metadata["project"]["dependencies"] == []
    for path in sorted((CONTRACTS / "src").rglob("*.py")):
        imports = _absolute_import_roots(path)
        assert imports <= {
            "__future__",
            "dataclasses",
            "typing",
            "tigrbl_security_trust_contracts",
        }, path


def test_security_trust_domain_bases_depend_only_on_contracts() -> None:
    metadata = tomllib.loads((BASES / "pyproject.toml").read_text(encoding="utf-8"))

    assert metadata["project"]["dependencies"] == [
        "tigrbl-security-trust-contracts==0.1.0"
    ]
    for path in sorted((BASES / "src").rglob("*.py")):
        imports = _absolute_import_roots(path)
        assert imports <= {
            "__future__",
            "abc",
            "typing",
            "tigrbl_security_trust_contracts",
            "tigrbl_security_trust_domain_bases",
        }, path


def test_security_trust_contract_and_base_packages_export_expected_surfaces() -> None:
    contracts = importlib.import_module("tigrbl_security_trust_contracts")
    bases = importlib.import_module("tigrbl_security_trust_domain_bases")

    assert contracts.ICapabilityProvider.__name__ == "ICapabilityProvider"
    assert contracts.Artifact.__name__ == "Artifact"
    assert contracts.JWTPayload.__module__ == "tigrbl_security_trust_contracts.types"
    assert contracts.ProofBinding("dpop", {"jkt": "thumb"}).method == "dpop"
    assert contracts.DPoPBinding(jwk_thumbprint="thumb", htm="get", htu="https://api.example.test", jti="jti").confirmation_claim == {"jkt": "thumb"}
    assert contracts.MTLSBinding(certificate_thumbprint="thumb").confirmation_claim == {"x5t#S256": "thumb"}
    assert bases.SigningDomainBase.__name__ == "SigningDomainBase"
    assert bases.KeyProviderDomainBase.__name__ == "KeyProviderDomainBase"

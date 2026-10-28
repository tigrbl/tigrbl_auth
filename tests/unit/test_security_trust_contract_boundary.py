from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "pkgs" / "02-contracts" / "tba-contracts-security-trust"
BASES = ROOT / "pkgs" / "05-bases" / "tba-bases-security-trust-domain"


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
        "datetime",
            "enum",
            "typing",
            "tba_contracts_security_trust",
        }, path


def test_security_trust_domain_bases_depend_only_on_contracts_and_peer_bases() -> None:
    metadata = tomllib.loads((BASES / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = metadata["project"]["dependencies"]
    assert {
        "tba-bases-certificate==0.4.0.dev2",
        "tba-bases-capability==0.4.0.dev2",
        "tba-bases-claim==0.4.0.dev2",
        "tba-bases-did==0.4.0.dev2",
        "tba-bases-encryption==0.4.0.dev2",
        "tba-bases-key==0.4.0.dev2",
        "tba-bases-identity==0.4.0.dev2",
        "tba-bases-proof-of-possession==0.4.0.dev2",
        "tba-bases-protected-artifact==0.4.0.dev2",
        "tba-bases-signing==0.4.0.dev2",
        "tba-bases-token-introspection==0.4.0.dev2",
        "tba-bases-trust==0.4.0.dev2",
        "tba-bases-workload-identity==0.4.0.dev2",
    } <= set(dependencies)
    for path in sorted((BASES / "src").rglob("*.py")):
        imports = _absolute_import_roots(path)
        assert imports <= {
            "__future__",
            "abc",
            "typing",
            "tba_bases_capability",
            "tba_bases_claim",
            "tba_bases_identity_claims",
            "tba_bases_identity",
            "tba_contracts_identity",
            "tba_bases_identity_model",
            "tba_bases_authentication_context",
            "tba_bases_certificate",
            "tba_bases_did",
            "tba_bases_encryption",
            "tba_bases_key",
            "tba_bases_proof_of_possession",
            "tba_bases_protected_artifact",
            "tba_bases_signing",
            "tba_bases_token_introspection",
            "tba_bases_trust",
            "tba_bases_workload_identity",
            "tba_bases_security_artifact",
            "tba_contracts_security_trust",
            "tba_bases_security_trust_domain",
        }, path


def test_security_trust_contract_and_base_packages_export_expected_surfaces() -> None:
    contracts = importlib.import_module("tba_contracts_security_trust")
    bases = importlib.import_module("tba_bases_security_trust_domain")

    assert contracts.ICapabilityProvider.__name__ == "ICapabilityProvider"
    assert contracts.Artifact.__name__ == "Artifact"
    assert contracts.JWTPayload.__module__ == "tba_contracts_security_trust.types"
    assert contracts.ProofBinding("dpop", {"jkt": "thumb"}).method == "dpop"
    assert contracts.DPoPBinding(
        jwk_thumbprint="thumb",
        htm="get",
        htu="https://api.example.test",
        jti="jti",
    ).confirmation_claim == {"jkt": "thumb"}
    assert contracts.MTLSBinding(certificate_thumbprint="thumb").confirmation_claim == {"x5t#S256": "thumb"}
    assert not hasattr(contracts, "KeyProfile")
    assert contracts.KeyUsage.KEK.value == "kek"
    assert contracts.KeyUsage.DEK.value == "dek"
    assert contracts.KEY_USAGE_SPECS[contracts.KeyUsage.KEK].default_ops == (
        contracts.KeyOperation.WRAP_KEY,
        contracts.KeyOperation.UNWRAP_KEY,
    )
    assert contracts.resolve_key_allowed_operations(
        kind=contracts.KeyKind.SYMMETRIC,
        usages=(contracts.KeyUsage.KEK,),
        allowed_ops=(contracts.KeyOperation.WRAP_KEY,),
    ) == (contracts.KeyOperation.WRAP_KEY,)
    assert contracts.KeyOperation.ENCAPSULATE.value == "encapsulate"
    assert contracts.KeyOperation.DECAPSULATE.value == "decapsulate"
    assert contracts.EncapsulateRequest(public_key="pub").public_key == "pub"
    assert bases.SigningDomainBase.__name__ == "SigningDomainBase"
    assert bases.SigningProviderBase.__name__ == "SigningProviderBase"
    assert bases.KeyWrappingProviderBase.__name__ == "KeyWrappingProviderBase"
    assert bases.KeyEncapsulationProviderBase.__name__ == "KeyEncapsulationProviderBase"
    assert bases.KeyProviderDomainBase.__name__ == "KeyProviderDomainBase"


def test_key_usage_specs_default_narrow_and_reject_expanded_operations() -> None:
    contracts = importlib.import_module("tba_contracts_security_trust")

    assert contracts.resolve_key_allowed_operations(
        kind="symmetric",
        usages=("dek",),
        allowed_ops=None,
    ) == (contracts.KeyOperation.ENCRYPT, contracts.KeyOperation.DECRYPT)
    assert contracts.resolve_key_allowed_operations(
        kind="symmetric",
        usages=("dek",),
        allowed_ops=("encrypt",),
    ) == (contracts.KeyOperation.ENCRYPT,)

    with pytest.raises(ValueError):
        contracts.resolve_key_allowed_operations(
            kind="symmetric",
            usages=("dek",),
            allowed_ops=("encrypt", "sign"),
        )

    with pytest.raises(ValueError):
        contracts.resolve_key_allowed_operations(
            kind="asymmetric",
            usages=("dek",),
        )

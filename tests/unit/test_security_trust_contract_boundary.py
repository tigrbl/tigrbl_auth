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
        "datetime",
            "enum",
            "typing",
            "tigrbl_security_trust_contracts",
        }, path


def test_security_trust_domain_bases_depend_only_on_contracts_and_peer_bases() -> None:
    metadata = tomllib.loads((BASES / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = metadata["project"]["dependencies"]
    assert {
        "tigrbl-certificate-bases==0.4.0.dev2",
        "tigrbl-capability-bases==0.4.0.dev2",
        "tigrbl-claim-bases==0.4.0.dev2",
        "tigrbl-did-bases==0.4.0.dev2",
        "tigrbl-encryption-bases==0.4.0.dev2",
        "tigrbl-key-bases==0.4.0.dev2",
        "tigrbl-identity-bases==0.4.0.dev2",
        "tigrbl-proof-of-possession-bases==0.4.0.dev2",
        "tigrbl-protected-artifact-bases==0.4.0.dev2",
        "tigrbl-signing-bases==0.4.0.dev2",
        "tigrbl-token-introspection-bases==0.4.0.dev2",
        "tigrbl-trust-bases==0.4.0.dev2",
        "tigrbl-workload-identity-bases==0.4.0.dev2",
    } <= set(dependencies)
    for path in sorted((BASES / "src").rglob("*.py")):
        imports = _absolute_import_roots(path)
        assert imports <= {
            "__future__",
            "abc",
            "typing",
            "tigrbl_capability_bases",
            "tigrbl_claim_bases",
            "tigrbl_identity_claims_bases",
            "tigrbl_identity_bases",
            "tigrbl_identity_contracts",
            "tigrbl_identity_model_bases",
            "tigrbl_authentication_context_bases",
            "tigrbl_certificate_bases",
            "tigrbl_did_bases",
            "tigrbl_encryption_bases",
            "tigrbl_key_bases",
            "tigrbl_proof_of_possession_bases",
            "tigrbl_protected_artifact_bases",
            "tigrbl_signing_bases",
            "tigrbl_token_introspection_bases",
            "tigrbl_trust_bases",
            "tigrbl_workload_identity_bases",
            "tigrbl_security_artifact_bases",
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
    contracts = importlib.import_module("tigrbl_security_trust_contracts")

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

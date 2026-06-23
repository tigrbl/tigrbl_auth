from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_ROOT = (
    ROOT
    / "pkgs"
    / "02-contracts"
    / "tigrbl-identity-contracts"
    / "src"
    / "tigrbl_identity_contracts"
)
CONCRETE_ROOT = (
    ROOT
    / "pkgs"
    / "10-concrete"
    / "tigrbl-identity-concrete"
    / "src"
    / "tigrbl_identity_concrete"
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


def test_contracts_do_not_own_concrete_identity_or_credential_variants() -> None:
    import tigrbl_identity_contracts as contracts

    concrete_names = {
        "ApiKeyCredential",
        "DeviceIdentity",
        "DpopKeyCredential",
        "MachineIdentity",
        "MfaFactor",
        "MtlsCertificateCredential",
        "PasswordlessCredential",
        "ServiceCredential",
        "ServiceIdentity",
        "WebAuthnCredential",
        "WorkloadIdentity",
    }

    assert not (concrete_names & set(dir(contracts)))
    assert not (CONTRACTS_ROOT / "credentials" / "services.py").exists()
    assert not (CONTRACTS_ROOT / "credentials" / "webauthn.py").exists()
    assert not (CONTRACTS_ROOT / "credentials" / "passwordless.py").exists()
    assert not (CONTRACTS_ROOT / "credentials" / "factors.py").exists()
    assert not (CONTRACTS_ROOT / "principals" / "services.py").exists()
    assert not (CONTRACTS_ROOT / "principals" / "workloads.py").exists()
    assert not (CONTRACTS_ROOT / "principals" / "devices.py").exists()


def test_concrete_variants_subclass_contract_dataclasses() -> None:
    import tigrbl_identity_concrete as concrete
    import tigrbl_identity_contracts as contracts

    for name in (
        "AdminIdentity",
        "ClientIdentity",
        "DeviceIdentity",
        "MachineIdentity",
        "ServiceIdentity",
        "UserIdentity",
        "WorkloadIdentity",
    ):
        assert issubclass(getattr(concrete, name), contracts.Identity), name

    for name in (
        "ApiKeyCredential",
        "ClientSecretCredential",
        "DpopKeyCredential",
        "MfaCredential",
        "MfaFactor",
        "MtlsCertificateCredential",
        "PasskeyCredential",
        "PasswordCredential",
        "PasswordResetCredential",
        "PasswordlessCredential",
        "ServiceCredential",
        "ServiceKeyCredential",
        "WebAuthnCredential",
    ):
        assert issubclass(getattr(concrete, name), contracts.Credential), name


def test_concrete_layer_only_imports_lower_contract_surfaces() -> None:
    allowed = {
        "__future__",
        "dataclasses",
        "datetime",
        "typing",
        "uuid",
        "tigrbl_identity_contracts",
    }

    offenders = {
        str(path.relative_to(ROOT)): sorted(_imports(path) - allowed)
        for path in CONCRETE_ROOT.rglob("*.py")
        if _imports(path) - allowed
    }

    assert offenders == {}

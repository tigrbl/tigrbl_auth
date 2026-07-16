from __future__ import annotations

from importlib import import_module
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
OWNERSHIP = ROOT / "architecture" / "contract-ownership.yaml"


def _resolve(qualified_name: str) -> object:
    module_name, _, attribute = qualified_name.rpartition(".")
    return getattr(import_module(module_name), attribute)


def test_contract_ownership_manifest_names_importable_canonical_objects() -> None:
    document = yaml.safe_load(OWNERSHIP.read_text(encoding="utf-8"))
    assert document["version"] == 1
    assert document["layer"] == "02-contracts"
    for name, declaration in document["owners"].items():
        canonical = _resolve(declaration["canonical"])
        assert getattr(canonical, "__name__", name), name


def test_equivalent_compatibility_exports_preserve_class_identity() -> None:
    document = yaml.safe_load(OWNERSHIP.read_text(encoding="utf-8"))
    for name, declaration in document["owners"].items():
        canonical = _resolve(declaration["canonical"])
        for compatibility_name in declaration.get("compatibility", ()):
            assert _resolve(compatibility_name) is canonical, (name, compatibility_name)


def test_renamed_contract_families_are_unambiguous() -> None:
    from tigrbl_identity_contracts.adaptive_access import AdaptiveTrustDomain
    from tigrbl_identity_contracts.credentials.errors import CredentialVerificationError
    from tigrbl_identity_contracts.public_key_authentication.errors import (
        PublicKeyCredentialVerificationError,
    )
    from tigrbl_identity_contracts.workloads import TrustDomain
    from tigrbl_security_trust_contracts import KeyAttestationEvidence

    assert AdaptiveTrustDomain is not TrustDomain
    assert issubclass(PublicKeyCredentialVerificationError, RuntimeError)
    assert PublicKeyCredentialVerificationError is not CredentialVerificationError
    assert KeyAttestationEvidence.__name__ == "KeyAttestationEvidence"


def test_semantic_contracts_do_not_advertise_storage_implementations() -> None:
    oauth = import_module("tigrbl_identity_contracts.oauth")
    oidc = import_module("tigrbl_identity_contracts.oidc")

    assert not hasattr(oauth, "OAuthRepositoryPort")
    assert not hasattr(oidc, "BackchannelReplayStorePort")


def test_neutral_contract_packages_are_the_canonical_authority() -> None:
    token_facade = import_module("tigrbl_identity_contracts.tokens")
    token_contracts = import_module("tigrbl_token_contracts")
    assurance_facade = import_module("tigrbl_identity_contracts.assurance")
    assurance_contracts = import_module("tigrbl_identity_assurance_contracts")

    assert token_facade.TokenProfile is token_contracts.TokenProfile
    assert (
        token_facade.TokenVerificationRequest
        is token_contracts.TokenVerificationRequest
    )
    assert assurance_facade.VerifiedClaims is assurance_contracts.VerifiedClaims

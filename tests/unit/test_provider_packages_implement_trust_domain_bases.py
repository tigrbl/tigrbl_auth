from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDERS = ROOT / "pkgs" / "20-providers"

TRUST_BASE_PROVIDER_PACKAGES = {
    "tigrbl-security-certificate-mtls",
    "tigrbl-security-dpop-cnf-binding-validator",
    "tigrbl-security-mtls-cnf-binding-validator",
    "tigrbl-security-proof-dpop",
    "tigrbl-security-proof-pkce",
    "tigrbl-security-sender-constraint-validator",
    "tigrbl-security-signing-pqc",
    "tigrbl-security-token-introspection-client",
    "tigrbl-security-token-jwks-cache",
}

COMPOSITION_PROVIDER_PACKAGES = {
    "tigrbl-authz-resource-server-verifier",
    "tigrbl-identity-jose",
}


def test_pqc_provider_inherits_signing_domain_base() -> None:
    from tigrbl_security_signing_pqc import PQCSigningProvider
    from tigrbl_security_trust_domain_bases import SigningDomainBase

    assert issubclass(PQCSigningProvider, SigningDomainBase)
    assert "ML-DSA-65" in PQCSigningProvider().supports().algs


def test_pkce_provider_inherits_proof_of_possession_domain_base() -> None:
    from tigrbl_security_proof_pkce import PkceProofProvider
    from tigrbl_security_trust_domain_bases import ProofOfPossessionDomainBase

    assert issubclass(PkceProofProvider, ProofOfPossessionDomainBase)
    assert "S256" in PkceProofProvider().supports().algs


def test_provider_packages_have_explicit_trust_boundary_kind() -> None:
    packages = {path.name for path in PROVIDERS.iterdir() if (path / "pyproject.toml").exists()}
    assert packages
    assert packages == TRUST_BASE_PROVIDER_PACKAGES | COMPOSITION_PROVIDER_PACKAGES


def test_trust_base_provider_packages_expose_base_implementers() -> None:
    packages = [path for path in PROVIDERS.iterdir() if (path / "pyproject.toml").exists()]
    assert packages

    offenders: list[str] = []
    for package in packages:
        if package.name in COMPOSITION_PROVIDER_PACKAGES:
            continue
        implementers: list[str] = []
        for path in (package / "src").rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                base_names = {
                    getattr(base, "id", getattr(base, "attr", ""))
                        for base in node.bases
                    }
                if any(name.endswith("Base") for name in base_names):
                    implementers.append(f"{path.relative_to(package)}::{node.name}")
        if not implementers:
            offenders.append(package.name)

    assert offenders == []

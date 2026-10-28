from __future__ import annotations

import ast
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROVIDERS = ROOT / "pkgs" / "20-providers"
PROVIDER_TAXONOMY = ROOT / "architecture" / "provider-package-taxonomy.yaml"

TRUST_BASE_PROVIDER_PACKAGES = {
    "tba-provider-authenticator-api-key-local",
    "tba-provider-authenticator-client-secret-local",
    "tba-provider-authenticator-dpop-proof",
    "tba-provider-authenticator-federated-oidc",
    "tba-provider-authenticator-mtls-client-cert",
    "tba-provider-authenticator-otp-local",
    "tba-provider-authenticator-password-local",
    "tba-provider-authenticator-recovery-code-local",
    "tba-provider-authenticator-remote-introspection",
    "tba-provider-authenticator-service-key-local",
    "tba-provider-authenticator-session-local",
    "tba-provider-authorization-resource-server-verifier",
    "tba-provider-identity-jose",
    "tba-provider-authentication-context-acr-basic",
    "tba-provider-authentication-context-amr-basic",
    "tba-provider-security-authorization-provenance-builder",
    "tba-provider-security-certificate-mtls",
    "tba-provider-claims-local",
    "tba-provider-security-dpop-cnf-binding-validator",
    "tba-provider-security-mtls-cnf-binding-validator",
    "tba-provider-security-proof-dpop",
    "tba-provider-security-proof-pkce",
    "tba-provider-security-signing-pqc",
    "tba-provider-security-subject-pairwise",
    "tba-provider-token-introspection",
    "tba-provider-security-token-jwks-cache",
}

COMPOSITION_PROVIDER_PACKAGES = {
    "tba-runtime-authorization-policy",
    "tba-provider-authorization-policy-decision-engine",
    "tba-provider-access-governance-memory",
    "tba-provider-certificate-status",
    "tba-provider-corim-reference-memory",
    "tba-provider-did-controller",
    "tba-provider-digital-credential-trust",
    "tba-provider-authentication-anomaly-detector",
    "tba-provider-identity-administration-relationship-graph",
    "tba-provider-key-attestation-verifier",
    "tba-provider-platform-attestation",
    "tba-provider-security-cose",
    "tba-provider-trust-anchor",
}

DIRECT_CONTRACT_PROVIDER_PACKAGES = {
    # Bcrypt is the sole implementation of the shared-secret hashing contract;
    # a layer-05 behavior base would add no shared implementation seam.
    "tba-provider-secret-hashing-bcrypt",
    # These protocol-specific providers implement their layer-02 ports directly;
    # their versioned protocol mapping belongs in layer 50, not a general trust base.
    "tba-provider-security-oidc-federation",
    "tba-provider-security-webfinger",
    "tba-provider-cose-cryptography",
    "tba-provider-jose-swarmauri",
}


def test_pqc_provider_inherits_signing_domain_base() -> None:
    from tba_provider_security_signing_pqc import PQCSigningProvider
    from tba_bases_security_trust_domain import (
        SigningDomainBase,
        SigningProviderBase,
    )

    assert issubclass(PQCSigningProvider, SigningDomainBase)
    assert issubclass(PQCSigningProvider, SigningProviderBase)
    assert "ML-DSA-65" in PQCSigningProvider().supports().algs


def test_pkce_provider_inherits_proof_of_possession_domain_base() -> None:
    from tba_provider_security_proof_pkce import PkceProofProvider
    from tba_bases_security_trust_domain import ProofOfPossessionDomainBase

    assert issubclass(PkceProofProvider, ProofOfPossessionDomainBase)
    assert "S256" in PkceProofProvider().supports().algs


def test_provider_packages_have_explicit_trust_boundary_kind() -> None:
    packages = {
        path.name for path in PROVIDERS.iterdir() if (path / "pyproject.toml").exists()
    }
    assert packages
    classified = (
        TRUST_BASE_PROVIDER_PACKAGES
        | COMPOSITION_PROVIDER_PACKAGES
        | DIRECT_CONTRACT_PROVIDER_PACKAGES
    )
    assert classified <= packages
    assert not (TRUST_BASE_PROVIDER_PACKAGES & COMPOSITION_PROVIDER_PACKAGES)
    assert (
        not (classified - DIRECT_CONTRACT_PROVIDER_PACKAGES)
        & DIRECT_CONTRACT_PROVIDER_PACKAGES
    )


def test_trust_base_provider_packages_expose_base_implementers() -> None:
    taxonomy = yaml.safe_load(PROVIDER_TAXONOMY.read_text(encoding="utf-8"))
    migrating = set(taxonomy["compatibility_or_migration_packages"])
    packages = [
        path for path in PROVIDERS.iterdir() if (path / "pyproject.toml").exists()
    ]
    assert packages

    offenders: list[str] = []
    for package in packages:
        if (
            package.name
            in COMPOSITION_PROVIDER_PACKAGES
            | DIRECT_CONTRACT_PROVIDER_PACKAGES
            | migrating
        ):
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

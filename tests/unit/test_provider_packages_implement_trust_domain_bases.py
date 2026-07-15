from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROVIDERS = ROOT / "pkgs" / "20-providers"

TRUST_BASE_PROVIDER_PACKAGES = {
    "tigrbl-authenticator-api-key-local",
    "tigrbl-authenticator-client-secret-local",
    "tigrbl-authenticator-dpop-proof",
    "tigrbl-authenticator-federated-oidc",
    "tigrbl-authenticator-mtls-client-cert",
    "tigrbl-authenticator-otp-local",
    "tigrbl-authenticator-password-local",
    "tigrbl-authenticator-recovery-code-local",
    "tigrbl-authenticator-remote-introspection",
    "tigrbl-authenticator-service-key-local",
    "tigrbl-authenticator-session-local",
    "tigrbl-authz-resource-server-verifier",
    "tigrbl-identity-jose",
    "tigrbl-security-auth-context-acr-basic",
    "tigrbl-security-auth-context-amr-basic",
    "tigrbl-security-authorization-provenance-builder",
    "tigrbl-security-certificate-mtls",
    "tigrbl-security-claims-provider-local",
    "tigrbl-security-dpop-cnf-binding-validator",
    "tigrbl-security-mtls-cnf-binding-validator",
    "tigrbl-security-oidc-federation-provider",
    "tigrbl-security-proof-dpop",
    "tigrbl-security-proof-pkce",
    "tigrbl-security-sender-constraint-validator",
    "tigrbl-security-signing-pqc",
    "tigrbl-security-subject-pairwise-provider",
    "tigrbl-security-token-introspection-client",
    "tigrbl-security-token-jwks-cache",
    "tigrbl-security-webfinger-provider",
}

COMPOSITION_PROVIDER_PACKAGES = {
    "tigrbl-authn-credentials",
    "tigrbl-authz-policy",
    "tigrbl-authz-policy-admin-gate",
    "tigrbl-authz-policy-decision-engine",
    "tigrbl-certificate-status-provider",
    "tigrbl-corim-reference-memory-provider",
    "tigrbl-did-controller-provider",
    "tigrbl-digital-credential-trust-provider",
    "tigrbl-identity-admin",
    "tigrbl-identity-admin-auth-anomaly-detector",
    "tigrbl-identity-admin-relationship-graph",
    "tigrbl-key-attestation-verifier",
    "tigrbl-platform-attestation-provider",
    "tigrbl-security-cose",
    "tigrbl-trust-anchor-provider",
}

DIRECT_CONTRACT_PROVIDER_PACKAGES = {
    # Bcrypt is the sole implementation of the shared-secret hashing contract;
    # a layer-05 behavior base would add no shared implementation seam.
    "tigrbl-secret-hashing-bcrypt-provider",
}


def test_pqc_provider_inherits_signing_domain_base() -> None:
    from tigrbl_security_signing_pqc import PQCSigningProvider
    from tigrbl_security_trust_domain_bases import (
        SigningDomainBase,
        SigningProviderBase,
    )

    assert issubclass(PQCSigningProvider, SigningDomainBase)
    assert issubclass(PQCSigningProvider, SigningProviderBase)
    assert "ML-DSA-65" in PQCSigningProvider().supports().algs


def test_pkce_provider_inherits_proof_of_possession_domain_base() -> None:
    from tigrbl_security_proof_pkce import PkceProofProvider
    from tigrbl_security_trust_domain_bases import ProofOfPossessionDomainBase

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
    packages = [
        path for path in PROVIDERS.iterdir() if (path / "pyproject.toml").exists()
    ]
    assert packages

    offenders: list[str] = []
    for package in packages:
        if (
            package.name
            in COMPOSITION_PROVIDER_PACKAGES | DIRECT_CONTRACT_PROVIDER_PACKAGES
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

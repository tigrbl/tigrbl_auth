"""Release authoring and provenance helpers for the Tigrbl identity package suite."""

from __future__ import annotations

from .release_signing import (
    DEFAULT_SIGNER_ID,
    LoadedSigner,
    SignerIdentity,
    VerificationResult,
    build_contract_set_manifest,
    load_signer,
    sha256_bytes,
    sha256_file,
    verify_bundle_attestations,
    verify_statement,
    write_artifact_attestation,
    write_attestation,
    write_bundle_attestation,
    write_public_key_artifacts,
)

__all__ = [
    "DEFAULT_SIGNER_ID",
    "LoadedSigner",
    "SignerIdentity",
    "VerificationResult",
    "build_contract_set_manifest",
    "load_signer",
    "sha256_bytes",
    "sha256_file",
    "verify_bundle_attestations",
    "verify_statement",
    "write_artifact_attestation",
    "write_attestation",
    "write_bundle_attestation",
    "write_public_key_artifacts",
]

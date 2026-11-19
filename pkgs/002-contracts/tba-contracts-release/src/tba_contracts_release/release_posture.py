from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "docs").is_dir() and (parent / ".github").is_dir():
            return parent
    return Path(__file__).resolve().parents[2]


REPO_ROOT = _repo_root()


PRIVATE_JWK_FIELDS: tuple[str, ...] = (
    "d",
    "dp",
    "dq",
    "k",
    "oth",
    "p",
    "q",
    "qi",
)


SECRET_FIELD_TOKENS: tuple[str, ...] = (
    "assertion",
    "client_secret",
    "encrypted",
    "password",
    "private",
    "refresh_token",
    "secret",
    "signature",
    "token",
)


@dataclass(frozen=True, slots=True)
class TransportPosture:
    protocol: str
    backend_runtime_support: str
    runtime_enablement: str
    contract_visibility: str
    uix_dependency: str
    certification_claimable: bool
    supported_runners: tuple[str, ...]
    enablement_flags: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DisclosureRule:
    artifact_kind: str
    admin_rendering: str
    public_rendering: str
    redacted_fields: tuple[str, ...]
    implementation_only_fields: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ProvenanceRequirement:
    standard: str
    required_artifact_paths: tuple[str, ...]
    generated_projection_paths: tuple[str, ...]
    release_gate_obligations: tuple[str, ...]
    disclosure_paths: tuple[str, ...]
    satisfied: bool
    missing_paths: tuple[str, ...]


TRANSPORT_REQUIREMENTS: dict[str, dict[str, Any]] = {
    "http11": {
        "capabilities": ("http",),
        "flag_names": (),
        "runtime_enablement": "baseline runner transport",
        "contract_visibility": "indirect via deployment and runtime profile",
        "uix_dependency": "required browser transport baseline",
    },
    "http2": {
        "capabilities": ("http2",),
        "flag_names": ("hypercorn_http2",),
        "runtime_enablement": "opt-in runner flag where the adapter exposes HTTP/2",
        "contract_visibility": "indirect via runtime profile and operator configuration",
        "uix_dependency": "optional browser transport upgrade",
    },
    "http3": {
        "capabilities": (),
        "flag_names": (),
        "runtime_enablement": "not implemented in the current runner registry",
        "contract_visibility": "not declared in current OpenAPI or OpenRPC contracts",
        "uix_dependency": "no current UIX dependency",
    },
    "quic": {
        "capabilities": (),
        "flag_names": (),
        "runtime_enablement": "not implemented in the current runner registry",
        "contract_visibility": "not declared in current OpenAPI or OpenRPC contracts",
        "uix_dependency": "no current UIX dependency",
    },
}


DISCLOSURE_RULES: dict[str, DisclosureRule] = {
    "json-schema": DisclosureRule(
        artifact_kind="json-schema",
        admin_rendering="schema field summary with sensitive examples removed",
        public_rendering="field list and requirement summary only",
        redacted_fields=("default", "examples", "$comment"),
        implementation_only_fields=("$defs", "unevaluatedProperties", "x-internal"),
    ),
    "jws": DisclosureRule(
        artifact_kind="jws",
        admin_rendering="header and redacted claims with signature presence only",
        public_rendering="algorithm and claim-name summary without token material",
        redacted_fields=("signature", "client_secret", "assertion"),
        implementation_only_fields=("compact_token", "raw_signature_bytes"),
    ),
    "jwe": DisclosureRule(
        artifact_kind="jwe",
        admin_rendering="protected header and encrypted payload placeholder only",
        public_rendering="encryption status and header summary only",
        redacted_fields=("ciphertext", "encrypted_key", "iv", "tag"),
        implementation_only_fields=("decrypted_payload", "cek"),
    ),
    "jwt": DisclosureRule(
        artifact_kind="jwt",
        admin_rendering="registered claims with secret-bearing values redacted",
        public_rendering="claim-name summary and bounded identity hints only",
        redacted_fields=("access_token", "authorization_details", "refresh_token"),
        implementation_only_fields=("raw_token", "signature_material"),
    ),
    "jwks": DisclosureRule(
        artifact_kind="jwks",
        admin_rendering="public key metadata only",
        public_rendering="key identifiers and public key-type summary only",
        redacted_fields=PRIVATE_JWK_FIELDS,
        implementation_only_fields=("private_jwk_material", "rotation_private_cache"),
    ),
}


PROVENANCE_REQUIREMENTS: dict[str, dict[str, tuple[str, ...]]] = {
    "ssdf": {
        "required": (
            "docs/runbooks/CLEAN_CHECKOUT_REPRO.md",
            ".github/workflows/ci-install-profiles.yml",
            "scripts/verify_clean_room_install_substrate.py",
        ),
        "generated": ("docs/compliance/validated_execution_report.json",),
        "gates": ("gate-21-repro-clean-room", "gate-24-ci-install-profiles"),
        "disclosure": ("docs/compliance/validated_execution_report.md",),
    },
    "slsa": {
        "required": (
            "pyproject.toml",
            "uv.lock",
            ".github/workflows/ci-release-gates.yml",
            "docs/compliance/release_gate_report.json",
        ),
        "generated": ("docs/compliance/final_release_gate_report.json",),
        "gates": ("gate-90-release",),
        "disclosure": ("docs/compliance/final_release_gate_report.md",),
    },
    "in-toto": {
        "required": (
            "docs/compliance/release_signing_report.json",
            "scripts/materialize_tier4_peer_evidence.py",
        ),
        "generated": ("docs/compliance/release_signing_report.md",),
        "gates": ("gate-87-peer-bundle-completeness",),
        "disclosure": ("docs/compliance/release_signing_report.md",),
    },
    "sigstore": {
        "required": (
            "docs/compliance/release_signing_report.json",
            ".github/workflows/ci-release-gates.yml",
        ),
        "generated": ("docs/compliance/release_signing_report.md",),
        "gates": ("gate-90-release",),
        "disclosure": ("docs/compliance/release_signing_report.md",),
    },
    "spdx": {
        "required": (
            "pyproject.toml",
            "uv.lock",
            "docs/compliance/current_state_report.json",
        ),
        "generated": ("docs/compliance/current_state_report.md",),
        "gates": ("gate-truth-current-state",),
        "disclosure": ("docs/compliance/current_state_report.md",),
    },
    "cyclonedx": {
        "required": (
            "pyproject.toml",
            "uv.lock",
            "docs/compliance/certification_state_report.json",
        ),
        "generated": ("docs/compliance/certification_state_report.md",),
        "gates": ("gate-truth-release-decision",),
        "disclosure": ("docs/compliance/certification_state_report.md",),
    },
}

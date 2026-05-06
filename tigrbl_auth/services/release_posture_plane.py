from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from tigrbl_auth.runtime import runner_registry_manifest

REPO_ROOT = Path(__file__).resolve().parents[2]

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
            "constraints/dependency-lock.json",
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
            "constraints/dependency-lock.json",
            "docs/compliance/current_state_report.json",
        ),
        "generated": ("docs/compliance/current_state_report.md",),
        "gates": ("gate-truth-current-state",),
        "disclosure": ("docs/compliance/current_state_report.md",),
    },
    "cyclonedx": {
        "required": (
            "constraints/dependency-lock.json",
            "docs/compliance/certification_state_report.json",
        ),
        "generated": ("docs/compliance/certification_state_report.md",),
        "gates": ("gate-truth-release-decision",),
        "disclosure": ("docs/compliance/certification_state_report.md",),
    },
}


def build_transport_postures() -> dict[str, TransportPosture]:
    runners = runner_registry_manifest()
    postures: dict[str, TransportPosture] = {}
    for protocol, requirement in TRANSPORT_REQUIREMENTS.items():
        capabilities = set(requirement["capabilities"])
        supported_runners = tuple(
            sorted(
                runner["name"]
                for runner in runners
                if capabilities
                and capabilities
                <= {item["name"] for item in runner.get("capabilities", [])}
            )
        )
        implemented = bool(supported_runners) if capabilities else False
        postures[protocol] = TransportPosture(
            protocol=protocol,
            backend_runtime_support="implemented" if implemented else "absent",
            runtime_enablement=str(requirement["runtime_enablement"]),
            contract_visibility=str(requirement["contract_visibility"]),
            uix_dependency=str(requirement["uix_dependency"]),
            certification_claimable=implemented,
            supported_runners=supported_runners,
            enablement_flags=tuple(requirement["flag_names"]),
        )
    return postures


def build_disclosure_rules() -> dict[str, DisclosureRule]:
    return dict(DISCLOSURE_RULES)


def redact_schema_for_admin(schema: Mapping[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    summarized_properties = {
        str(name): {
            key: value
            for key, value in dict(spec).items()
            if key in {"description", "enum", "format", "items", "type"}
        }
        for name, spec in dict(properties).items()
        if isinstance(spec, Mapping)
    }
    return {
        "kind": "json-schema",
        "$schema": schema.get("$schema"),
        "title": schema.get("title"),
        "type": schema.get("type"),
        "required": list(schema.get("required", [])),
        "properties": summarized_properties,
    }


def explain_schema_publicly(schema: Mapping[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    return {
        "kind": "json-schema",
        "title": schema.get("title"),
        "field_names": sorted(str(name) for name in dict(properties)),
        "required": list(schema.get("required", [])),
    }


def disclose_jws_admin(token_summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "kind": "jws",
        "header": _redact_sensitive_mapping(token_summary.get("header", {})),
        "payload": _redact_sensitive_mapping(token_summary.get("payload", {})),
        "signature": "[REDACTED]" if token_summary.get("signature") else None,
    }


def disclose_jws_public(token_summary: Mapping[str, Any]) -> dict[str, Any]:
    header = dict(token_summary.get("header", {}))
    payload = dict(token_summary.get("payload", {}))
    return {
        "kind": "jws",
        "alg": header.get("alg"),
        "typ": header.get("typ"),
        "claim_names": sorted(str(key) for key in payload),
        "signature_present": bool(token_summary.get("signature")),
    }


def disclose_jwe_admin(envelope: Mapping[str, Any]) -> dict[str, Any]:
    header = envelope.get("protected_header", envelope.get("header", {}))
    return {
        "kind": "jwe",
        "protected_header": _redact_sensitive_mapping(header),
        "ciphertext": "[REDACTED]" if envelope.get("ciphertext") else None,
        "tag": "[REDACTED]" if envelope.get("tag") else None,
    }


def disclose_jwe_public(envelope: Mapping[str, Any]) -> dict[str, Any]:
    header = dict(envelope.get("protected_header", envelope.get("header", {})))
    return {
        "kind": "jwe",
        "alg": header.get("alg"),
        "enc": header.get("enc"),
        "encrypted": bool(envelope.get("ciphertext")),
    }


def disclose_jwt_admin(claims: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "kind": "jwt",
        "claims": _redact_sensitive_mapping(claims),
    }


def disclose_jwt_public(claims: Mapping[str, Any]) -> dict[str, Any]:
    values = dict(claims)
    return {
        "kind": "jwt",
        "claim_names": sorted(str(key) for key in values),
        "issuer": values.get("iss"),
        "audience_present": "aud" in values,
        "subject_present": "sub" in values,
    }


def disclose_jwks_admin(jwks: Mapping[str, Any]) -> dict[str, Any]:
    keys = jwks.get("keys", [])
    return {
        "kind": "jwks",
        "keys": [
            {key: value for key, value in dict(item).items() if key not in PRIVATE_JWK_FIELDS}
            for item in keys
            if isinstance(item, Mapping)
        ],
    }


def disclose_jwks_public(jwks: Mapping[str, Any]) -> dict[str, Any]:
    keys = [
        dict(item)
        for item in jwks.get("keys", [])
        if isinstance(item, Mapping)
    ]
    return {
        "kind": "jwks",
        "key_count": len(keys),
        "kids": sorted(str(item.get("kid")) for item in keys if item.get("kid")),
        "key_types": sorted({str(item.get("kty")) for item in keys if item.get("kty")}),
    }


def build_release_provenance_requirements(repo_root: Path | None = None) -> dict[str, ProvenanceRequirement]:
    root = (repo_root or REPO_ROOT).resolve()
    requirements: dict[str, ProvenanceRequirement] = {}
    for standard, requirement in PROVENANCE_REQUIREMENTS.items():
        expected_paths = tuple(
            dict.fromkeys(
                (
                    *requirement["required"],
                    *requirement["generated"],
                    *requirement["disclosure"],
                )
            )
        )
        missing_paths = tuple(path for path in expected_paths if not (root / path).exists())
        requirements[standard] = ProvenanceRequirement(
            standard=standard,
            required_artifact_paths=requirement["required"],
            generated_projection_paths=requirement["generated"],
            release_gate_obligations=requirement["gates"],
            disclosure_paths=requirement["disclosure"],
            satisfied=not missing_paths,
            missing_paths=missing_paths,
        )
    return requirements


def build_phase6_delivery_summary(*, repo_root: Path | None = None) -> dict[str, Any]:
    transport = build_transport_postures()
    disclosure = build_disclosure_rules()
    provenance = build_release_provenance_requirements(repo_root=repo_root)
    return {
        "transport": {
            "implemented_protocols": sorted(
                protocol
                for protocol, posture in transport.items()
                if posture.backend_runtime_support == "implemented"
            ),
            "claimable_protocols": sorted(
                protocol
                for protocol, posture in transport.items()
                if posture.certification_claimable
            ),
            "upgrade_protocols": sorted(
                protocol
                for protocol, posture in transport.items()
                if posture.enablement_flags
            ),
            "missing_protocols": sorted(
                protocol
                for protocol, posture in transport.items()
                if posture.backend_runtime_support != "implemented"
            ),
        },
        "uix_disclosure": {
            "artifact_kinds": sorted(disclosure),
            "admin_renderings": sorted(rule.admin_rendering for rule in disclosure.values()),
            "public_renderings": sorted(rule.public_rendering for rule in disclosure.values()),
            "redacted_field_count": sum(len(rule.redacted_fields) for rule in disclosure.values()),
        },
        "release_provenance": {
            "standards": sorted(provenance),
            "satisfied_standards": sorted(
                standard
                for standard, requirement in provenance.items()
                if requirement.satisfied
            ),
            "release_gate_obligations": sorted(
                {
                    gate
                    for requirement in provenance.values()
                    for gate in requirement.release_gate_obligations
                }
            ),
            "missing_path_count": sum(len(requirement.missing_paths) for requirement in provenance.values()),
        },
    }


def _redact_sensitive_mapping(values: Mapping[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_text = str(key)
        lower = key_text.lower()
        if key_text in PRIVATE_JWK_FIELDS or any(token in lower for token in SECRET_FIELD_TOKENS):
            redacted[key_text] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_text] = _redact_sensitive_mapping(value)
        elif isinstance(value, list):
            redacted[key_text] = [
                _redact_sensitive_mapping(item) if isinstance(item, Mapping) else item
                for item in value
            ]
        else:
            redacted[key_text] = value
    return redacted


__all__ = [
    "DisclosureRule",
    "ProvenanceRequirement",
    "TransportPosture",
    "build_disclosure_rules",
    "build_phase6_delivery_summary",
    "build_release_provenance_requirements",
    "build_transport_postures",
    "disclose_jwe_admin",
    "disclose_jwe_public",
    "disclose_jws_admin",
    "disclose_jws_public",
    "disclose_jwks_admin",
    "disclose_jwks_public",
    "disclose_jwt_admin",
    "disclose_jwt_public",
    "explain_schema_publicly",
    "redact_schema_for_admin",
]

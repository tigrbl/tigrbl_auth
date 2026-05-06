from __future__ import annotations

from tigrbl_auth.services.release_posture_plane import (
    build_disclosure_rules,
    build_phase6_delivery_summary,
    build_release_provenance_requirements,
    build_transport_postures,
    disclose_jwe_admin,
    disclose_jwe_public,
    disclose_jws_admin,
    disclose_jws_public,
    disclose_jwks_admin,
    disclose_jwks_public,
    disclose_jwt_admin,
    disclose_jwt_public,
    explain_schema_publicly,
    redact_schema_for_admin,
)


def test_transport_postures_distinguish_support_enablement_and_claimability():
    postures = build_transport_postures()

    assert postures["http11"].backend_runtime_support == "implemented"
    assert set(postures["http11"].supported_runners) == {"hypercorn", "tigrcorn", "uvicorn"}
    assert postures["http11"].certification_claimable is True

    assert postures["http2"].backend_runtime_support == "implemented"
    assert postures["http2"].supported_runners == ("hypercorn",)
    assert postures["http2"].enablement_flags == ("hypercorn_http2",)

    assert postures["http3"].backend_runtime_support == "absent"
    assert postures["http3"].certification_claimable is False
    assert postures["quic"].backend_runtime_support == "absent"
    assert postures["quic"].contract_visibility.startswith("not declared")


def test_disclosure_rules_cover_all_phase6_artifacts():
    rules = build_disclosure_rules()

    assert sorted(rules) == ["json-schema", "jwe", "jwks", "jws", "jwt"]
    assert "signature" in rules["jws"].redacted_fields
    assert "ciphertext" in rules["jwe"].redacted_fields
    assert "private_jwk_material" in rules["jwks"].implementation_only_fields


def test_schema_jose_and_jwks_disclosure_redacts_secret_or_private_material():
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Client Registration",
        "type": "object",
        "required": ["client_id"],
        "properties": {
            "client_id": {"type": "string", "format": "uuid", "description": "Stable identifier"},
            "client_secret": {"type": "string", "examples": ["do-not-render"]},
        },
    }
    jws = {
        "header": {"alg": "ES256", "kid": "kid-1"},
        "payload": {"sub": "alice", "client_secret": "top-secret"},
        "signature": "abc123",
    }
    jwe = {
        "protected_header": {"alg": "ECDH-ES", "enc": "A256GCM"},
        "ciphertext": "deadbeef",
        "tag": "signed",
    }
    jwt = {"iss": "https://issuer.example", "sub": "alice", "refresh_token": "rt-secret", "aud": ["api://default"]}
    jwks = {
        "keys": [
            {"kid": "rsa-1", "kty": "RSA", "n": "abc", "e": "AQAB", "d": "private"},
            {"kid": "oct-1", "kty": "oct", "k": "secret"},
        ]
    }

    admin_schema = redact_schema_for_admin(schema)
    public_schema = explain_schema_publicly(schema)
    admin_jws = disclose_jws_admin(jws)
    public_jws = disclose_jws_public(jws)
    admin_jwe = disclose_jwe_admin(jwe)
    public_jwe = disclose_jwe_public(jwe)
    admin_jwt = disclose_jwt_admin(jwt)
    public_jwt = disclose_jwt_public(jwt)
    admin_jwks = disclose_jwks_admin(jwks)
    public_jwks = disclose_jwks_public(jwks)

    assert admin_schema["properties"]["client_secret"]["type"] == "string"
    assert public_schema["field_names"] == ["client_id", "client_secret"]

    assert admin_jws["payload"]["client_secret"] == "[REDACTED]"
    assert admin_jws["signature"] == "[REDACTED]"
    assert public_jws["claim_names"] == ["client_secret", "sub"]

    assert admin_jwe["ciphertext"] == "[REDACTED]"
    assert admin_jwe["tag"] == "[REDACTED]"
    assert public_jwe == {"kind": "jwe", "alg": "ECDH-ES", "enc": "A256GCM", "encrypted": True}

    assert admin_jwt["claims"]["refresh_token"] == "[REDACTED]"
    assert public_jwt["subject_present"] is True
    assert public_jwt["audience_present"] is True

    assert "d" not in admin_jwks["keys"][0]
    assert "k" not in admin_jwks["keys"][1]
    assert public_jwks["kids"] == ["oct-1", "rsa-1"]


def test_release_provenance_requirements_point_to_real_repo_artifacts():
    requirements = build_release_provenance_requirements()

    assert sorted(requirements) == ["cyclonedx", "in-toto", "sigstore", "slsa", "spdx", "ssdf"]
    assert all(requirement.satisfied for requirement in requirements.values())
    assert requirements["ssdf"].release_gate_obligations == (
        "gate-21-repro-clean-room",
        "gate-24-ci-install-profiles",
    )
    assert "docs/compliance/release_signing_report.md" in requirements["sigstore"].generated_projection_paths
    assert requirements["cyclonedx"].missing_paths == ()


def test_phase6_delivery_summary_aggregates_transport_disclosure_and_provenance_state():
    summary = build_phase6_delivery_summary()

    assert summary["transport"]["implemented_protocols"] == ["http11", "http2"]
    assert summary["transport"]["missing_protocols"] == ["http3", "quic"]
    assert summary["uix_disclosure"]["artifact_kinds"] == ["json-schema", "jwe", "jwks", "jws", "jwt"]
    assert summary["release_provenance"]["missing_path_count"] == 0
    assert summary["release_provenance"]["satisfied_standards"] == [
        "cyclonedx",
        "in-toto",
        "sigstore",
        "slsa",
        "spdx",
        "ssdf",
    ]

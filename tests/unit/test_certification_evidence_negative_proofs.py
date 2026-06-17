from __future__ import annotations

from tigrbl_identity_cli.cli.reports._execution_status import _negative_tests_for_claim


PARTITIONED_TESTS = {
    "security-negative": [
        "tests/negative/test_certification_attack_paths.py",
        "tests/negative/test_hardening_runtime_enforcement.py",
        "tests/security/test_issuer_confusion_resistance.py",
    ],
    "conformance": [
        "tests/conformance/baseline/test_rfc6750_bearer_token.py",
        "tests/conformance/hardening/test_rfc9126_par.py",
        "tests/conformance/hardening/test_rfc9207_issuer_identification.py",
    ],
    "unit": [
        "tests/unit/test_resource_server_consumer_boundary.py",
        "tests/unit/test_hardening_cluster_c.py",
    ],
    "interop": [
        "tests/interop/test_peer_counterpart_catalog.py",
        "tests/interop/test_tier4_promotion_fail_closed.py",
    ],
}


def test_negative_proof_classifier_matches_real_attack_path_files() -> None:
    claim = {
        "id": "fapi2-security.par-required",
        "title": "FAPI 2.0 Security profile requires PAR",
        "targets": ["RFC 9126", "RFC 9700"],
    }

    selected = _negative_tests_for_claim(claim, PARTITIONED_TESTS)

    assert "tests/negative/test_certification_attack_paths.py" in selected
    assert "tests/conformance/hardening/test_rfc9126_par.py" in selected


def test_negative_proof_classifier_matches_issuer_confusion_files() -> None:
    claim = {
        "id": "cli-flag:issuer",
        "title": "--issuer",
        "description": "Issuer override for discovery and contract generation.",
        "targets": ["CLI operator surface"],
    }

    selected = _negative_tests_for_claim(claim, PARTITIONED_TESTS)

    assert "tests/security/test_issuer_confusion_resistance.py" in selected


def test_negative_proof_classifier_matches_bearer_form_query_files() -> None:
    claim = {
        "id": "flag:enable_rfc6750_query",
        "title": "enable_rfc6750_query",
        "targets": ["RFC 6750", "RFC 9700"],
    }

    selected = _negative_tests_for_claim(claim, PARTITIONED_TESTS)

    assert "tests/conformance/baseline/test_rfc6750_bearer_token.py" in selected


def test_negative_proof_classifier_matches_external_profile_fail_closed_files() -> None:
    claim = {
        "id": "profile:camara-security-interoperability",
        "title": "camara-security-interoperability",
        "description": "External tracked profile for CAMARA Security and Interoperability.",
        "targets": ["CAMARA Security and Interoperability profile"],
    }

    selected = _negative_tests_for_claim(claim, PARTITIONED_TESTS)

    assert "tests/interop/test_peer_counterpart_catalog.py" in selected
    assert "tests/interop/test_tier4_promotion_fail_closed.py" in selected

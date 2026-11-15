from __future__ import annotations

from tba_cli_identity.cli.reports._execution_status import _clean_check_ignored, _negative_tests_for_claim


PARTITIONED_TESTS = {
    "security-negative": [
        "pkgs/120-tests/tba-tests-oauth/tests/negative/test_oauth_security_policy_rejections.py",
        "pkgs/120-tests/tba-tests-oauth/tests/negative/test_hardening_runtime_enforcement.py",
        "pkgs/120-tests/tba-tests-oauth/tests/security/test_issuer_confusion_resistance.py",
    ],
    "conformance": [
        "pkgs/120-tests/tba-tests-oauth/tests/conformance/baseline/test_rfc6750_bearer_token.py",
        "pkgs/120-tests/tba-tests-oauth/tests/conformance/hardening/test_rfc9126_par.py",
        "pkgs/120-tests/tba-tests-oauth/tests/conformance/hardening/test_rfc9207_issuer_identification.py",
    ],
    "unit": [
        "pkgs/120-tests/tba-tests-oauth/tests/unit/test_resource_server_consumer_boundary.py",
        "pkgs/120-tests/tba-tests-oauth/tests/unit/test_hardening_sender_constraints.py",
        "pkgs/120-tests/tba-tests-oidc/tests/unit/test_hardening_logout.py",
        "pkgs/120-tests/tba-tests-api-contracts/tests/unit/test_hardening_discovery_contract.py",
    ],
    "interop": [
        "pkgs/120-tests/tba-tests-governance-release-certification/tests/interop/test_peer_counterpart_catalog.py",
        "pkgs/120-tests/tba-tests-governance-release-certification/tests/interop/test_tier4_promotion_fail_closed.py",
    ],
}


def test_negative_proof_classifier_matches_real_attack_path_files() -> None:
    claim = {
        "id": "fapi2-security.par-required",
        "title": "FAPI 2.0 Security profile requires PAR",
        "targets": ["RFC 9126", "RFC 9700"],
    }

    selected = _negative_tests_for_claim(claim, PARTITIONED_TESTS)

    assert "pkgs/120-tests/tba-tests-oauth/tests/negative/test_oauth_security_policy_rejections.py" in selected
    assert "pkgs/120-tests/tba-tests-oauth/tests/conformance/hardening/test_rfc9126_par.py" in selected


def test_negative_proof_classifier_matches_issuer_confusion_files() -> None:
    claim = {
        "id": "cli-flag:issuer",
        "title": "--issuer",
        "description": "Issuer override for discovery and contract generation.",
        "targets": ["CLI operator surface"],
    }

    selected = _negative_tests_for_claim(claim, PARTITIONED_TESTS)

    assert "pkgs/120-tests/tba-tests-oauth/tests/security/test_issuer_confusion_resistance.py" in selected


def test_negative_proof_classifier_matches_bearer_form_query_files() -> None:
    claim = {
        "id": "flag:enable_rfc6750_query",
        "title": "enable_rfc6750_query",
        "targets": ["RFC 6750", "RFC 9700"],
    }

    selected = _negative_tests_for_claim(claim, PARTITIONED_TESTS)

    assert "pkgs/120-tests/tba-tests-oauth/tests/conformance/baseline/test_rfc6750_bearer_token.py" in selected


def test_negative_proof_classifier_matches_external_profile_fail_closed_files() -> None:
    claim = {
        "id": "profile:camara-security-interoperability",
        "title": "camara-security-interoperability",
        "description": "External tracked profile for CAMARA Security and Interoperability.",
        "targets": ["CAMARA Security and Interoperability profile"],
    }

    selected = _negative_tests_for_claim(claim, PARTITIONED_TESTS)

    assert "pkgs/120-tests/tba-tests-governance-release-certification/tests/interop/test_peer_counterpart_catalog.py" in selected
    assert "pkgs/120-tests/tba-tests-governance-release-certification/tests/interop/test_tier4_promotion_fail_closed.py" in selected


def test_generated_issue_registry_is_not_release_signing_source_dirtiness() -> None:
    assert _clean_check_ignored("compliance/claims/issue-registry.yaml") is True

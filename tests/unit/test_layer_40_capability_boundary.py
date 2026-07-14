from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_layer_boundaries import CAPABILITY_PURPOSES, validate


def test_layer_40_contains_only_registered_multi_component_use_cases() -> None:
    assert CAPABILITY_PURPOSES == {
        "tigrbl-attestation-appraisal": (
            "coordinate evidence appraisal and result recording"
        ),
        "tigrbl-client-registration-capability": (
            "coordinate client and registration metadata lifecycle with optional "
            "audit recording"
        ),
        "tigrbl-digital-credential-issuance": (
            "coordinate credential configuration, wallet trust, offers, and issuance"
        ),
        "tigrbl-digital-credential-presentation": (
            "coordinate holder consent, replay defense, and presentation verification"
        ),
        "tigrbl-identity-admin-control-plane": (
            "coordinate administrative resource lifecycle use cases"
        ),
        "tigrbl-protocol-artifact-processing": (
            "coordinate protocol-neutral artifact decoding, validation, encoding, "
            "and error normalization through replaceable processors"
        ),
        "tigrbl-principal-authentication": (
            "coordinate durable principal lookup with replaceable credential verifiers"
        ),
        "tigrbl-pushed-authorization-capability": (
            "coordinate durable pushed-request creation with optional audit recording"
        ),
        "tigrbl-replay-protection-capability": (
            "coordinate normalized replay reservations across protocol mappings, "
            "durable repositories, and replaceable providers"
        ),
        "tigrbl-security-events": (
            "coordinate security-event transmission, receipt, and recording"
        ),
        "tigrbl-token-introspection-capability": (
            "coordinate protocol-neutral token-state lookup and profile validation"
        ),
        "tigrbl-token-revocation-capability": (
            "coordinate durable token revocation with optional audit recording"
        ),
        "tigrbl-workload-identity": (
            "coordinate workload credential retrieval and identity verification"
        ),
    }


def test_layer_40_dependency_import_and_inheritance_boundaries() -> None:
    assert validate() == ()

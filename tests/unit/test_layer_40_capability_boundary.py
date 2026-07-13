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
        "tigrbl-digital-credential-issuance": (
            "coordinate credential configuration, wallet trust, offers, and issuance"
        ),
        "tigrbl-digital-credential-presentation": (
            "coordinate holder consent, replay defense, and presentation verification"
        ),
        "tigrbl-identity-admin-control-plane": (
            "coordinate administrative resource lifecycle use cases"
        ),
        "tigrbl-security-events": (
            "coordinate security-event transmission, receipt, and recording"
        ),
        "tigrbl-workload-identity": (
            "coordinate workload credential retrieval and identity verification"
        ),
    }


def test_layer_40_dependency_import_and_inheritance_boundaries() -> None:
    assert validate() == ()

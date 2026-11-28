from __future__ import annotations

from pathlib import Path

from tba_auth.config.profile_loader import load_profile_reference


ROOT = Path(__file__).resolve().parents[5]
EXTERNAL_PROFILE = (
    ROOT
    / "pkgs/120-tests/tba-tests-runtime/tests/fixtures/profiles/external-production.yaml"
)


def test_profile_reference_discovery_contract_alignment() -> None:
    deployment = load_profile_reference(str(EXTERNAL_PROFILE)).resolve()

    assert "/.well-known/openid-configuration" in deployment.active_contract_routes
    assert deployment.profile == "production"

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
OPERATOR_SRC = ROOT / "pkgs" / "tigrbl-identity-operator" / "src"
if str(OPERATOR_SRC) not in sys.path:
    sys.path.append(str(OPERATOR_SRC))

import tigrbl_identity_operator.uix as operator_uix  # noqa: E402

from tigrbl_auth.uix import (  # noqa: E402
    ADMINISTRATIVE_SAFE_MUTATION_FEATURES,
    SAFE_MUTATION_METHODS,
    SafeMutationRequest,
    administrative_safe_mutations_boundary_integrity,
    administrative_safe_mutations_boundary_manifest,
    execute_safe_mutation,
)


BOUNDARY_FEATURE_IDS = {
    "feat:uix-safe-mutation-revoke-session",
    "feat:uix-safe-mutation-revoke-token",
    "feat:uix-safe-mutation-revoke-consent",
    "feat:uix-safe-mutation-lock-identity",
    "feat:uix-safe-mutation-toggle-tenant",
    "feat:uix-safe-mutation-toggle-client",
    "feat:uix-safe-mutation-rotate-key",
    "feat:uix-safe-mutation-publish-jwks",
    "feat:uix-safe-mutation-update-client-registration",
}


def test_priority1_administrative_safe_mutations_boundary_t0_inventory_tracks_all_features():
    manifest = administrative_safe_mutations_boundary_manifest()
    integrity = administrative_safe_mutations_boundary_integrity()
    operator_manifest = operator_uix.administrative_safe_mutations_boundary_manifest()
    operator_integrity = operator_uix.administrative_safe_mutations_boundary_integrity()

    assert set(manifest) == BOUNDARY_FEATURE_IDS
    assert set(ADMINISTRATIVE_SAFE_MUTATION_FEATURES) == BOUNDARY_FEATURE_IDS
    assert manifest == operator_manifest
    assert integrity["passed"] is True
    assert operator_integrity["passed"] is True
    assert integrity["feature_count"] == 9
    assert set(integrity["actions"]) == set(SAFE_MUTATION_METHODS)


def test_priority1_administrative_safe_mutations_boundary_t1_executes_confirmed_mutations_with_audit():
    executed: list[str] = []

    for action, required_method in SAFE_MUTATION_METHODS.items():
        result = execute_safe_mutation(
            SafeMutationRequest(
                action=action,
                target_id="target-1",
                confirmed=True,
                confirmation_text=f"{action}:target-1",
            ),
            executor=lambda request: executed.append(request.action) or {"ok": True},
        )

        assert result.status == "executed"
        assert result.required_method == required_method
        assert result.audit_event == {
            "action": action,
            "target_id": "target-1",
            "required_method": required_method,
            "outcome": "executed",
        }

    assert executed == list(SAFE_MUTATION_METHODS)


def test_priority1_administrative_safe_mutations_boundary_t2_fails_closed_for_missing_confirmation_and_failures():
    for action, required_method in SAFE_MUTATION_METHODS.items():
        blocked = execute_safe_mutation(SafeMutationRequest(action=action, target_id="target-1"))
        wrong_confirmation = execute_safe_mutation(
            SafeMutationRequest(
                action=action,
                target_id="target-1",
                confirmed=True,
                confirmation_text=f"{action}:other-target",
            )
        )

        assert blocked.status == "confirmation_required"
        assert blocked.required_method == required_method
        assert blocked.audit_event["outcome"] == "blocked"
        assert wrong_confirmation.status == "confirmation_required"
        assert wrong_confirmation.audit_event["outcome"] == "blocked"

    failed = execute_safe_mutation(
        SafeMutationRequest(
            action="rotate-key",
            target_id="kid-1",
            confirmed=True,
            confirmation_text="rotate-key:kid-1",
        ),
        executor=lambda _request: {"ok": False, "error": "upstream unavailable"},
    )

    assert failed.status == "failed"
    assert failed.error == "upstream unavailable"
    assert failed.audit_event["outcome"] == "failed"

    with pytest.raises(ValueError, match="unknown safe mutation action"):
        execute_safe_mutation(SafeMutationRequest(action="unknown-action", target_id="target-1"))

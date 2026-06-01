from datetime import datetime, timedelta, timezone

import pytest

from tigrbl_auth.security.certification import (
    CertificationError,
    MachineIdentity,
    assert_machine_identity_governed,
)


def _identity(**overrides: object) -> MachineIdentity:
    data: dict[str, object] = {
        "subject_id": "svc-1",
        "owner_id": "team-platform",
        "tenant_id": "tenant-a",
        "credential_id": "cred-1",
        "credential_rotates_at": datetime.now(timezone.utc) + timedelta(days=10),
        "allowed_audiences": frozenset({"api://notes"}),
        "human": False,
    }
    data.update(overrides)
    return MachineIdentity(**data)


def test_machine_identity_t0_contract_exports_governance_check() -> None:
    assert callable(assert_machine_identity_governed)


def test_machine_identity_t1_accepts_owned_scoped_rotating_identity() -> None:
    assert_machine_identity_governed(_identity())


@pytest.mark.parametrize(
    "overrides,match",
    [
        ({"human": True}, "human"),
        ({"owner_id": ""}, "owner"),
        ({"credential_rotates_at": datetime.now(timezone.utc) - timedelta(days=1)}, "rotation"),
        ({"allowed_audiences": frozenset()}, "audiences"),
    ],
)
def test_machine_identity_t2_rejects_ungoverned_machine_identities(
    overrides: dict[str, object],
    match: str,
) -> None:
    with pytest.raises(CertificationError, match=match):
        assert_machine_identity_governed(_identity(**overrides))

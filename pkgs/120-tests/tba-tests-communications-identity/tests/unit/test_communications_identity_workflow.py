from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

pytest.importorskip("tba_capability_communications_identity")

from tba_capability_communications_identity import (
    DomainCheck,
    DomainOutcome,
    recheck_domain,
)


@pytest.mark.asyncio
async def test_workflow_uses_same_contract_for_a_different_profile():
    checker = Mock(profile="example-channel")
    checker.check.return_value = DomainCheck("example.test", DomainOutcome.NOT_READY)
    audit = AsyncMock()
    tenant_id = uuid4()
    db = object()

    result = await recheck_domain(
        "example.test",
        checker=checker,
        audit=audit,
        db=db,
        tenant_id=tenant_id,
    )

    assert result.outcome is DomainOutcome.NOT_READY
    audit.assert_awaited_once_with(
        db=db,
        tenant_id=tenant_id,
        event_type="communications_identity.domain.rechecked",
        target_type="sending_domain",
        target_id="example.test",
        outcome="not_ready",
        details={"profile": "example-channel"},
    )


@pytest.mark.asyncio
async def test_workflow_requires_explicit_tenant_before_checking_or_auditing():
    checker = Mock()
    audit = AsyncMock()
    with pytest.raises(ValueError, match="explicit tenant"):
        await recheck_domain(
            "example.test", checker=checker, audit=audit, db=None, tenant_id=None
        )
    checker.check.assert_not_called()
    audit.assert_not_awaited()

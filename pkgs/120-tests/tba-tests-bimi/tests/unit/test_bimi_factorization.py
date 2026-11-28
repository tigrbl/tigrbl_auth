from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

pytest.importorskip("tba_capability_communications_identity")
pytest.importorskip("tba_profile_communications_identity_bimi")

from tba_capability_communications_identity import (
    DomainOutcome,
    assess_domain_onboarding,
    recheck_domain,
)
from tba_contracts_dns import TxtResult, TxtStatus
from tba_profile_communications_identity_bimi import (
    BimiProfile,
    CertificateOutcome,
    CheckOutcome,
    MarkType,
    MarkVerification,
)
from tba_profile_communications_identity_bimi.capability_adapter import (
    BimiDomainChecker,
)
from tba_protocol_bimi import AssertionStatus, discover_assertion
from tba_protocol_dmarc import (
    PolicyStatus,
    discover_policy,
    effective_policy,
    parse_policy_record,
)


def _dns(records):
    dns = Mock()
    dns.lookup_txt.side_effect = lambda name: (
        TxtResult(TxtStatus.FOUND, (records[name],))
        if name in records
        else TxtResult(TxtStatus.ABSENT)
    )
    return dns


def test_protocol_discovers_psd_policy_but_profile_requires_organizational_enforcement():
    dns = _dns({"_dmarc.test": b"v=DMARC1; p=reject; sp=quarantine; np=reject; psd=y"})
    policy = discover_policy(dns, "news.example.test", author_exists=False)
    assert policy.status is PolicyStatus.FOUND
    assert policy.policy_source == "_dmarc.test"
    assert policy.organizational_domain == "example.test"
    assert policy.organizational_record is None
    assert policy.effective_policy == "reject"

    profile = BimiProfile(dns=dns, validator=Mock())
    assert (
        profile.check_readiness("news.example.test").dmarc.outcome
        is CheckOutcome.MISSING
    )

    record = parse_policy_record(b"v=DMARC1; p=none; sp=quarantine; t=y; pct=25")
    assert effective_policy(record, inherited=True) == "quarantine"
    assert record.testing
    assert record.legacy_percentage == 25


def test_bimi_protocol_discovers_assertions_independently_of_dmarc():
    dns = _dns(
        {
            "spring.sales._bimi.example.test": b"v=BIMI1; l=https://example.test/logo.svg",
        }
    )
    result = discover_assertion(
        dns, "mail.example.test", "spring.sales", "example.test"
    )
    assert result.status is AssertionStatus.FOUND
    assert result.assertion.name == "spring.sales._bimi.example.test"
    assert result.assertion.evidence_url is None
    with pytest.raises(ValueError, match="must contain"):
        discover_assertion(dns, "mail.example.test", organizational_domain="other.test")


@pytest.mark.asyncio
async def test_bimi_workflow_uses_discovered_owner_and_audits_recheck():
    dns = _dns(
        {
            "_dmarc.example.test": b"v=DMARC1; p=reject",
            "default._bimi.example.test": b"v=BIMI1; l=https://example.test/logo.svg; a=https://example.test/mark.pem",
        }
    )
    profile = BimiProfile(dns=dns, validator=Mock())
    profile.verify_certificate = Mock(
        return_value=MarkVerification(
            CertificateOutcome.VALID,
            MarkType.CMC,
            sha256="fixture-digest",
        )
    )
    evidence = Mock(side_effect=[b"fixture certificate", None])
    checker = BimiDomainChecker(profile, evidence=evidence)
    tenant_id = uuid4()
    audit = AsyncMock()

    initial = await assess_domain_onboarding(
        "News.Example.test",
        checker=checker,
        audit=audit,
        db=None,
        tenant_id=tenant_id,
    )
    later = await recheck_domain(
        "News.Example.test",
        checker=checker,
        audit=audit,
        db=None,
        tenant_id=tenant_id,
    )

    assert initial.outcome is DomainOutcome.READY
    assert later.outcome is DomainOutcome.INDETERMINATE
    profile.verify_certificate.assert_called_once_with(
        b"fixture certificate",
        assertion_name="default._bimi.example.test",
    )
    initial_event, later_event = (call.kwargs for call in audit.await_args_list)
    assert initial_event["tenant_id"] == later_event["tenant_id"] == tenant_id
    assert (
        initial_event["event_type"]
        == "communications_identity.domain.onboarding_assessed"
    )
    assert initial_event["details"]["mark_type"] == "cmc"
    assert later_event["details"]["certificate"] == "unavailable"

import asyncio

import pytest
from tigrbl_identity_contracts.policy import (
    PolicyDecision,
    PolicyEntity,
    PolicyEntityChain,
    PolicyEntitySearchRequest,
    PolicyEntitySearchResult,
    PolicyEntitySearchTarget,
    PolicyEvaluationRequest,
    PolicyEvaluationResult,
    PolicyServiceCapabilities,
)
from tigrbl_policy_evaluation_capability import PolicyEvaluationCapability


def _request(identifier: str = "alice") -> PolicyEvaluationRequest:
    return PolicyEvaluationRequest(
        PolicyEntityChain((PolicyEntity("user", identifier),)),
        PolicyEntityChain((PolicyEntity("action", "read"),)),
        PolicyEntityChain((PolicyEntity("document", "document-1"),)),
    )


def test_policy_capability_requires_evaluation_and_reports_optional_bindings() -> None:
    with pytest.raises(NotImplementedError):
        PolicyEvaluationCapability(None)

    capability = PolicyEvaluationCapability(
        lambda request: PolicyEvaluationResult(PolicyDecision(True, "allowed")),
        describe=lambda: PolicyServiceCapabilities(search=False),
    )

    assert capability.state().ready
    assert set(capability.callables()) == {"describe", "evaluate", "evaluate_many"}


def test_policy_capability_preserves_batch_order_and_typed_search() -> None:
    capability = PolicyEvaluationCapability(
        lambda request: PolicyEvaluationResult(
            PolicyDecision(
                request.subject.entities[0].identifier != "blocked",
                request.subject.entities[0].identifier,
            )
        ),
        search_entities=lambda request: PolicyEntitySearchResult(
            (PolicyEntity(request.target.value, "result-1"),)
        ),
    )

    batch = capability.evaluate_many((_request("alice"), _request("blocked")))
    assert [result.decision.allowed for result in batch] == [True, False]

    search = capability.search_entities(
        PolicyEntitySearchRequest(PolicyEntitySearchTarget.RESOURCE)
    )
    assert search.entities[0].identifier == "result-1"

    result = asyncio.run(capability.call("evaluate", _request()))
    assert result.capability_id == "policy.evaluation"
    assert result.operation == "evaluate"

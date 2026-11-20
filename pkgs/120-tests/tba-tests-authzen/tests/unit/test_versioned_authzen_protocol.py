from tba_protocol_authzen import (
    CAPABILITY_REQUIREMENTS as AUTHZEN_REQUIREMENTS,
    AuthzenProtocol,
    CURRENT_VERSION as AUTHZEN_CURRENT,
    capability_report as authzen_capability_report,
    compatibility as authzen_compatibility,
    migrate_evaluation,
    supports as authzen_supports,
)
from tba_contracts_identity.policy import (
    PolicyDecision,
    PolicyEntity,
    PolicyEntitySearchResult,
    PolicyEvaluationResult,
)
from tba_capability_policy_evaluation import PolicyEvaluationCapability


def test_authzen_pins_final_version_and_features():
    assert AUTHZEN_CURRENT.identifier == "1.0"
    assert AUTHZEN_CURRENT.published == "2026-01-11"
    assert authzen_supports("search-resource")


def test_authzen_migrates_a_legacy_evaluation_with_explicit_context():
    assert migrate_evaluation({"subject": {}}, "draft-00")["context"] == {}


class _Evaluator:
    def evaluate(self, request):
        self.request = request
        return PolicyEvaluationResult(PolicyDecision(True, "policy matched"))


def test_authzen_maps_wire_entities_to_neutral_policy_contracts():
    evaluator = _Evaluator()
    response = AuthzenProtocol(evaluator).access_evaluation(
        {
            "subject": {"type": "user", "id": "alice"},
            "action": {"name": "read"},
            "resource": {"type": "document", "id": "document-1"},
            "context": {"time": "day"},
        }
    )
    assert response == {
        "decision": True,
        "context": {"reason": "policy matched"},
    }
    assert evaluator.request.subject.entities[0].identifier == "alice"
    assert evaluator.request.action.entities[0].identifier == "read"


def test_authzen_maps_batch_search_and_discovery_capabilities():
    capability = PolicyEvaluationCapability(
        lambda request: PolicyEvaluationResult(PolicyDecision(True, "allowed")),
        search_entities=lambda request: PolicyEntitySearchResult(
            (PolicyEntity(request.target.value, "result-1"),)
        ),
    )
    protocol = AuthzenProtocol(capability)

    batch = protocol.access_evaluations(
        {
            "subject": {"type": "user", "id": "alice"},
            "action": {"name": "read"},
            "evaluations": [
                {"resource": {"type": "document", "id": "one"}},
                {"resource": {"type": "document", "id": "two"}},
            ],
        }
    )
    assert [item["decision"] for item in batch["evaluations"]] == [True, True]

    search = protocol.search_resource(
        {
            "subject": {"type": "user", "id": "alice"},
            "action": {"name": "read"},
            "resource": {"type": "document"},
        }
    )
    assert search == {"results": [{"type": "resource", "id": "result-1"}]}

    assert authzen_compatibility("draft-03").migration_required
    assert {requirement.operation for requirement in AUTHZEN_REQUIREMENTS} == {
        "describe",
        "evaluate",
        "evaluate_many",
        "search_entities",
        "validate",
    }
    assert authzen_capability_report()["required_capabilities"] == (
        "artifact.processing",
        "policy.evaluation",
    )

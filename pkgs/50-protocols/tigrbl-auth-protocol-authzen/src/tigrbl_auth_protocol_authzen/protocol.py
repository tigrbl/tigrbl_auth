from collections.abc import Mapping

from tigrbl_identity_contracts.policy import (
    PolicyEntity,
    PolicyEntityChain,
    PolicyEvaluationPort,
    PolicyEvaluationRequest,
)


def _entity(value: object, expected_type: str) -> PolicyEntityChain:
    if not isinstance(value, Mapping):
        raise ValueError(f"AuthZEN {expected_type} must be an object")
    entity_type, identifier = value.get("type"), value.get("id")
    if not isinstance(entity_type, str) or not isinstance(identifier, str):
        raise ValueError(f"AuthZEN {expected_type} requires type and id")
    properties = value.get("properties", {})
    if not isinstance(properties, Mapping):
        raise ValueError("AuthZEN entity properties must be an object")
    return PolicyEntityChain((PolicyEntity(entity_type, identifier, dict(properties)),))


class AuthzenProtocol:
    version = "1.0"

    def __init__(self, evaluator: PolicyEvaluationPort):
        self._evaluator = evaluator

    def access_evaluation(self, payload: Mapping[str, object]) -> dict[str, object]:
        context = payload.get("context", {})
        if not isinstance(context, Mapping):
            raise ValueError("AuthZEN context must be an object")
        result = self._evaluator.evaluate(
            PolicyEvaluationRequest(
                _entity(payload.get("subject"), "subject"),
                _entity(payload.get("action"), "action"),
                _entity(payload.get("resource"), "resource"),
                dict(context),
            )
        )
        response = {"decision": result.decision.allowed}
        if result.decision.reason:
            response["reason"] = result.decision.reason
        if result.obligations:
            response["obligations"] = list(result.obligations)
        return response


__all__ = ["AuthzenProtocol"]

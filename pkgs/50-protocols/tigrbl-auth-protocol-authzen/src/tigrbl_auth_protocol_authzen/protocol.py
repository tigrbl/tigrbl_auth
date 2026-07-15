"""Authorization API 1.0 mapping to neutral policy operations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Protocol

from tigrbl_identity_contracts.policy import (
    PolicyEntitySearchRequest,
    PolicyEntitySearchResult,
    PolicyEntitySearchTarget,
    PolicyEvaluationRequest,
    PolicyEvaluationResult,
)

from .errors import AuthzenOperationUnavailableError, AuthzenSchemaError
from .schemas import (
    parse_evaluation_request,
    parse_search_request,
    serialize_evaluation_result,
    serialize_search_result,
)


class _PolicyOperations(Protocol):
    def evaluate(self, request: PolicyEvaluationRequest) -> PolicyEvaluationResult: ...


def _merged_evaluations(
    payload: Mapping[str, object],
) -> tuple[Mapping[str, object], ...]:
    evaluations = payload.get("evaluations")
    if evaluations is None or evaluations == []:
        return (payload,)
    if not isinstance(evaluations, Sequence) or isinstance(evaluations, (str, bytes)):
        raise AuthzenSchemaError("AuthZEN evaluations must be an array")
    defaults = {
        name: payload[name]
        for name in ("subject", "action", "resource", "context")
        if name in payload
    }
    merged = []
    for item in evaluations:
        if not isinstance(item, Mapping):
            raise AuthzenSchemaError("each AuthZEN evaluation must be an object")
        merged.append({**defaults, **item})
    return tuple(merged)


class AuthzenProtocol:
    version = "1.0"

    def __init__(self, capability: _PolicyOperations):
        self._capability = capability

    def access_evaluation(self, payload: Mapping[str, object]) -> dict[str, object]:
        return serialize_evaluation_result(
            self._capability.evaluate(parse_evaluation_request(payload))
        )

    def access_evaluations(self, payload: Mapping[str, object]) -> dict[str, object]:
        merged = _merged_evaluations(payload)
        if len(merged) == 1 and not payload.get("evaluations"):
            return self.access_evaluation(merged[0])

        requests = tuple(parse_evaluation_request(item) for item in merged)
        evaluate_many = getattr(self._capability, "evaluate_many", None)
        results = (
            evaluate_many(requests)
            if callable(evaluate_many)
            else tuple(self._capability.evaluate(request) for request in requests)
        )
        return {
            "evaluations": [serialize_evaluation_result(result) for result in results]
        }

    def _search(
        self,
        payload: Mapping[str, object],
        target: PolicyEntitySearchTarget,
    ) -> dict[str, object]:
        search = getattr(self._capability, "search_entities", None)
        if not callable(search):
            raise AuthzenOperationUnavailableError(
                f"AuthZEN {target.value} search is not configured"
            )
        request: PolicyEntitySearchRequest = parse_search_request(payload, target)
        result = search(request)
        if not isinstance(result, PolicyEntitySearchResult):
            raise TypeError("policy search must return PolicyEntitySearchResult")
        return serialize_search_result(result)

    def search_subject(self, payload: Mapping[str, object]) -> dict[str, object]:
        return self._search(payload, PolicyEntitySearchTarget.SUBJECT)

    def search_resource(self, payload: Mapping[str, object]) -> dict[str, object]:
        return self._search(payload, PolicyEntitySearchTarget.RESOURCE)

    def search_action(self, payload: Mapping[str, object]) -> dict[str, object]:
        return self._search(payload, PolicyEntitySearchTarget.ACTION)


__all__ = ["AuthzenProtocol"]

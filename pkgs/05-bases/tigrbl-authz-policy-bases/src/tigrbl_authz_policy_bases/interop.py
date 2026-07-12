from abc import ABC

from tigrbl_identity_contracts.policy import (
    PolicyEvaluationPort,
    PolicyEvaluationRequest,
    PolicyEvaluationResult,
    PolicySearchPort,
    PolicySearchRequest,
    PolicySearchResult,
)


class AuthzenEvaluationAdapterBase(PolicyEvaluationPort, ABC):
    def evaluate(self, request: PolicyEvaluationRequest, /) -> PolicyEvaluationResult:
        raise NotImplementedError


class AuthzenSearchAdapterBase(PolicySearchPort, ABC):
    def search(self, request: PolicySearchRequest, /) -> PolicySearchResult:
        raise NotImplementedError


class XacmlRequestMapperBase(ABC):
    def map_request(self, request: object, /) -> PolicyEvaluationRequest:
        raise NotImplementedError


class XacmlResponseMapperBase(ABC):
    def map_response(self, result: PolicyEvaluationResult, /) -> object:
        raise NotImplementedError


__all__ = [
    "AuthzenEvaluationAdapterBase",
    "AuthzenSearchAdapterBase",
    "XacmlRequestMapperBase",
    "XacmlResponseMapperBase",
]

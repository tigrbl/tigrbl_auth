"""Authorization API 1.0 wire-schema normalization."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from tigrbl_identity_contracts.policy import (
    PolicyEntity,
    PolicyEntityChain,
    PolicyEntitySearchRequest,
    PolicyEntitySearchResult,
    PolicyEntitySearchTarget,
    PolicyEvaluationRequest,
    PolicyEvaluationResult,
)

from .errors import AuthzenSchemaError


@dataclass(frozen=True, slots=True)
class AuthzenPdpMetadata:
    policy_decision_point: str
    access_evaluation_endpoint: str
    access_evaluations_endpoint: str | None = None
    search_subject_endpoint: str | None = None
    search_resource_endpoint: str | None = None
    search_action_endpoint: str | None = None
    capabilities: tuple[str, ...] = ()
    signed_metadata: str | None = None

    def to_payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "policy_decision_point": self.policy_decision_point,
            "access_evaluation_endpoint": self.access_evaluation_endpoint,
        }
        for name in (
            "access_evaluations_endpoint",
            "search_subject_endpoint",
            "search_resource_endpoint",
            "search_action_endpoint",
            "signed_metadata",
        ):
            if (value := getattr(self, name)) is not None:
                payload[name] = value
        if self.capabilities:
            payload["capabilities"] = list(self.capabilities)
        return payload


def _object(value: object, name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise AuthzenSchemaError(f"AuthZEN {name} must be an object")
    return value


def _properties(value: Mapping[str, object], name: str) -> Mapping[str, object]:
    properties = value.get("properties", {})
    if not isinstance(properties, Mapping):
        raise AuthzenSchemaError(f"AuthZEN {name} properties must be an object")
    return dict(properties)


def _entity(
    value: object,
    name: str,
    *,
    identifier_required: bool = True,
) -> PolicyEntity:
    item = _object(value, name)
    if name == "action":
        identifier = item.get("name")
        if identifier_required and not isinstance(identifier, str):
            raise AuthzenSchemaError("AuthZEN action requires name")
        return PolicyEntity(
            "action",
            identifier if isinstance(identifier, str) else "",
            _properties(item, name),
        )

    entity_type = item.get("type")
    identifier = item.get("id")
    if not isinstance(entity_type, str):
        raise AuthzenSchemaError(f"AuthZEN {name} requires type")
    if identifier_required and not isinstance(identifier, str):
        raise AuthzenSchemaError(f"AuthZEN {name} requires id")
    return PolicyEntity(
        entity_type,
        identifier if isinstance(identifier, str) else "",
        _properties(item, name),
    )


def parse_evaluation_request(
    payload: Mapping[str, object],
) -> PolicyEvaluationRequest:
    context = payload.get("context", {})
    if not isinstance(context, Mapping):
        raise AuthzenSchemaError("AuthZEN context must be an object")
    return PolicyEvaluationRequest(
        PolicyEntityChain((_entity(payload.get("subject"), "subject"),)),
        PolicyEntityChain((_entity(payload.get("action"), "action"),)),
        PolicyEntityChain((_entity(payload.get("resource"), "resource"),)),
        dict(context),
    )


def parse_search_request(
    payload: Mapping[str, object],
    target: PolicyEntitySearchTarget,
) -> PolicyEntitySearchRequest:
    context = payload.get("context", {})
    if not isinstance(context, Mapping):
        raise AuthzenSchemaError("AuthZEN context must be an object")
    page = payload.get("page", {})
    if not isinstance(page, Mapping):
        raise AuthzenSchemaError("AuthZEN page must be an object")
    token = page.get("token")
    if token is not None and not isinstance(token, str):
        raise AuthzenSchemaError("AuthZEN page token must be a string")

    subject = _entity(
        payload.get("subject"),
        "subject",
        identifier_required=target is not PolicyEntitySearchTarget.SUBJECT,
    )
    resource = _entity(
        payload.get("resource"),
        "resource",
        identifier_required=target is not PolicyEntitySearchTarget.RESOURCE,
    )
    action = (
        None
        if target is PolicyEntitySearchTarget.ACTION
        else _entity(payload.get("action"), "action")
    )
    return PolicyEntitySearchRequest(
        target=target,
        subject=subject,
        action=action,
        resource=resource,
        context=dict(context),
        page_token=token,
    )


def serialize_evaluation_result(result: PolicyEvaluationResult) -> dict[str, object]:
    payload: dict[str, object] = {"decision": result.decision.allowed}
    context: dict[str, object] = {}
    if result.decision.reason:
        context["reason"] = result.decision.reason
    if result.obligations:
        context["obligations"] = list(result.obligations)
    if result.advice:
        context["advice"] = list(result.advice)
    if context:
        payload["context"] = context
    return payload


def serialize_search_result(result: PolicyEntitySearchResult) -> dict[str, object]:
    entities = []
    for entity in result.entities:
        item: dict[str, object]
        if entity.entity_type == "action":
            item = {"name": entity.identifier}
        else:
            item = {"type": entity.entity_type, "id": entity.identifier}
        if entity.properties:
            item["properties"] = dict(entity.properties)
        entities.append(item)
    payload: dict[str, object] = {"results": entities}
    page: dict[str, object] = {}
    if result.next_page_token is not None:
        page["next_token"] = result.next_page_token
    if result.total is not None:
        page["total"] = result.total
    if page:
        payload["page"] = page
    if result.context:
        payload["context"] = dict(result.context)
    return payload


__all__ = [
    "AuthzenPdpMetadata",
    "parse_evaluation_request",
    "parse_search_request",
    "serialize_evaluation_result",
    "serialize_search_result",
]

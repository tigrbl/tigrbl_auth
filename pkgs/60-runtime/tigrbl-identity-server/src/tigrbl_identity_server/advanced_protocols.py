from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from typing import Any

from tigrbl import TigrblApp, TigrblRouter
from tigrbl_identity_contracts.attestation import AttestationEvidence
from tigrbl_identity_storage.framework import HTTPException, Request, status

api = TigrblRouter()


def _components(request: Request) -> Mapping[str, object]:
    app = getattr(request, "app", None)
    state = getattr(app, "state", None)
    components = getattr(state, "tigrbl_auth_protocol_components", None)
    return components if isinstance(components, Mapping) else {}


def _component(request: Request, name: str) -> object:
    component = _components(request).get(name)
    if component is None:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            f"{name} protocol component is not configured",
        )
    return component


async def _payload(request: Request) -> Mapping[str, Any]:
    value = await request.json()
    if not isinstance(value, Mapping):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "request body must be an object"
        )
    return value


def _jsonable(value: object) -> object:
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.hex()
    return value


@api.route("/credential", methods=["POST"], include_in_schema=True, tags=["oid4vci"])
async def issue_credential(request: Request) -> object:
    payload = await _payload(request)
    protocol = _component(request, "oid4vci")
    try:
        result = protocol.credential(
            payload,
            wallet_attestation=request.headers.get("OAuth-Client-Attestation"),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return _jsonable(result)


@api.route(
    "/presentation/verify", methods=["POST"], include_in_schema=True, tags=["oid4vp"]
)
async def verify_presentation(request: Request) -> object:
    payload = await _payload(request)
    holder, vp_token, authorization_request = (
        payload.get("holder"),
        payload.get("vp_token"),
        payload.get("authorization_request"),
    )
    if (
        not isinstance(holder, str)
        or not isinstance(vp_token, (str, bytes))
        or not isinstance(authorization_request, Mapping)
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "holder, vp_token, and authorization_request are required",
        )
    try:
        result = _component(request, "oid4vp").verify(
            holder, vp_token, authorization_request
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return _jsonable(result)


@api.route(
    "/access/v1/evaluation", methods=["POST"], include_in_schema=True, tags=["authzen"]
)
async def evaluate_access(request: Request) -> object:
    try:
        return _component(request, "authzen").access_evaluation(await _payload(request))
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc


@api.route("/gnap/tx", methods=["POST"], include_in_schema=True, tags=["gnap"])
async def process_gnap(request: Request) -> object:
    handler = _component(request, "gnap")
    from tigrbl_auth_protocol_gnap import parse_gnap_request

    try:
        parsed = parse_gnap_request(await _payload(request))
        result = handler(parsed)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return _jsonable(result)


@api.route(
    "/security-events/receive", methods=["POST"], include_in_schema=True, tags=["set"]
)
async def receive_security_event(request: Request) -> object:
    payload = await _payload(request)
    token = payload.get("set")
    if not isinstance(token, str):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "set token is required")
    try:
        event = _component(request, "security_events").receive(token)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return _jsonable(event)


@api.route(
    "/attestations/appraise",
    methods=["POST"],
    include_in_schema=True,
    tags=["attestation"],
)
async def appraise_attestation(request: Request) -> object:
    payload = await _payload(request)
    profile, claims, raw = (
        payload.get("profile"),
        payload.get("claims"),
        payload.get("raw"),
    )
    if (
        not isinstance(profile, str)
        or not isinstance(claims, Mapping)
        or (raw is not None and not isinstance(raw, str))
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "profile and claims are required"
        )
    evidence = AttestationEvidence(profile, dict(claims), raw)
    return _jsonable(_component(request, "attestation").appraise(evidence))


def include_advanced_protocols(app: TigrblApp) -> None:
    existing = {
        getattr(route, "path", None) or getattr(route, "path_template", None)
        for route in getattr(getattr(app, "router", app), "routes", ())
    }
    if "/credential" not in existing:
        app.include_router(api)


__all__ = ["api", "include_advanced_protocols"]

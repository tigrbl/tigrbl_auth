"""Runtime-owned OAuth/OIDC authorization endpoint."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlencode
from uuid import UUID, uuid4

from tigrbl import (
    Depends,
    HTMLResponse,
    RedirectResponse,
    Request,
    TigrblRouter,
)
from tigrbl.engine import HybridSession as AsyncSession
from tigrbl.runtime.status import HTTPException, status
from tigrbl_identity_storage.tables.auth_code import AuthCode
from .engine import get_db

router = TigrblRouter()


def _coerce_multi_value(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item)]
    return [str(value)] if str(value) else []


async def _resolve_pushed_authorization_request(db: Any, params: dict[str, Any]) -> tuple[dict[str, Any], Any | None]:
    from tigrbl_auth_protocol_oauth.standards.pushed_authorization_requests import (
        RFC9126_SPEC_URL,
        validate_pushed_authorization_request_row,
    )
    from tigrbl_identity_server.security.handler_records import first_handler_record
    from tigrbl_identity_storage.tables.pushed_authorization_request import PushedAuthorizationRequest

    request_uri = params.get("request_uri")
    if not request_uri:
        return params, None
    row = await first_handler_record(PushedAuthorizationRequest, db, {"request_uri": str(request_uri)})
    if row is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {"error": "invalid_request_uri", "error_description": RFC9126_SPEC_URL},
        )
    try:
        result = validate_pushed_authorization_request_row(
            row,
            client_id=str(params.get("client_id") or "") or None,
            request_uri=str(request_uri),
        )
    except Exception as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            {"error": "invalid_request_uri", "error_description": RFC9126_SPEC_URL},
        ) from exc

    merged = dict(result.params or {})
    for key, value in params.items():
        if value in (None, "", [], (), {}):
            continue
        if key not in {"request_uri", "client_id"}:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                {"error": "invalid_request", "error_description": RFC9126_SPEC_URL},
            )
        existing = merged.get(key)
        if existing not in (None, "", [], (), {}) and existing != value:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                {"error": "invalid_request_uri", "error_description": RFC9126_SPEC_URL},
            )
        merged[key] = value
    return merged, row


async def _resolve_request_object(params: dict[str, Any], deployment: Any) -> dict[str, Any]:
    from tigrbl_auth_protocol_oauth.standards.authorization_server_metadata import ISSUER
    from tigrbl_auth_protocol_oauth.standards.jwt_secured_authorization_requests import (
        merge_request_object_params,
        parse_request_object,
    )
    from tigrbl_identity_runtime.settings import settings

    request_object = params.get("request")
    if not request_object:
        return params
    if not deployment.flag_enabled("enable_rfc9101"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request_object"})
    try:
        parsed = await parse_request_object(
            str(request_object),
            secret=settings.jwt_secret,
            algorithms=("HS256", "HS384", "HS512"),
            expected_client_id=str(params.get("client_id") or "") or None,
            expected_audience=str(deployment.issuer or ISSUER),
        )
        merged = merge_request_object_params(parsed, params)
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {"error": "invalid_request_object"}) from exc
    return merged



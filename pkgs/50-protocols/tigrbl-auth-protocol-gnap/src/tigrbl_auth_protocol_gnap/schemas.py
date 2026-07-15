"""RFC 9635 request and response schema normalization."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from tigrbl_identity_contracts.gnap import (
    GrantAccessRequest,
    GrantNegotiationRequest,
    GrantNegotiationResult,
)

from .errors import GnapSchemaError


@dataclass(frozen=True, slots=True)
class GnapRequest:
    access_token: tuple[Mapping[str, Any], ...]
    client: Mapping[str, Any] | str
    interact: Mapping[str, Any] | None = None
    subject: Mapping[str, Any] | None = None

    def to_contract(self) -> GrantNegotiationRequest:
        requests = tuple(
            GrantAccessRequest(
                tuple(item["access"]),
                label=item.get("label"),
                flags=tuple(item.get("flags", ())),
            )
            for item in self.access_token
        )
        return GrantNegotiationRequest(
            requests,
            self.client,
            dict(self.interact) if self.interact is not None else None,
            dict(self.subject) if self.subject is not None else None,
        )


def _access_requests(value: object) -> tuple[Mapping[str, Any], ...]:
    if value is None:
        return ()
    items = (value,) if isinstance(value, Mapping) else value
    if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
        raise GnapSchemaError("GNAP access_token must be an object or array")
    requests = []
    for item in items:
        if not isinstance(item, Mapping):
            raise GnapSchemaError("GNAP access_token entries must be objects")
        access = item.get("access")
        if (
            not isinstance(access, Sequence)
            or isinstance(access, (str, bytes))
            or not access
        ):
            raise GnapSchemaError("GNAP access token request requires access")
        label = item.get("label")
        if label is not None and not isinstance(label, str):
            raise GnapSchemaError("GNAP access token label must be a string")
        flags = item.get("flags", ())
        if (
            not isinstance(flags, Sequence)
            or isinstance(flags, (str, bytes))
            or any(not isinstance(flag, str) for flag in flags)
            or len(set(flags)) != len(flags)
        ):
            raise GnapSchemaError("GNAP access token flags must be unique strings")
        requests.append(dict(item))
    labels = [item.get("label") for item in requests if item.get("label") is not None]
    if len(requests) > 1 and len(labels) != len(requests):
        raise GnapSchemaError("multiple GNAP access token requests require labels")
    if len(set(labels)) != len(labels):
        raise GnapSchemaError("GNAP access token labels must be unique")
    return tuple(requests)


def parse_gnap_request(value: Mapping[str, Any]) -> GnapRequest:
    access = _access_requests(value.get("access_token"))
    subject = value.get("subject")
    if subject is not None and not isinstance(subject, Mapping):
        raise GnapSchemaError("GNAP subject must be an object")
    if not access and subject is None:
        raise GnapSchemaError("GNAP request requires access_token or subject")
    client = value.get("client")
    if not isinstance(client, (Mapping, str)):
        raise GnapSchemaError("GNAP request requires a client instance")
    interact = value.get("interact")
    if interact is not None and not isinstance(interact, Mapping):
        raise GnapSchemaError("GNAP interact must be an object")
    return GnapRequest(
        access,
        dict(client) if isinstance(client, Mapping) else client,
        dict(interact) if isinstance(interact, Mapping) else None,
        dict(subject) if isinstance(subject, Mapping) else None,
    )


def serialize_gnap_result(result: GrantNegotiationResult) -> dict[str, object]:
    payload: dict[str, object] = {}
    if result.continuation is not None:
        payload["continue"] = dict(result.continuation)
    if result.access_tokens:
        payload["access_token"] = (
            dict(result.access_tokens[0])
            if len(result.access_tokens) == 1
            else [dict(token) for token in result.access_tokens]
        )
    if result.interaction is not None:
        payload["interact"] = dict(result.interaction)
    if result.subject is not None:
        payload["subject"] = dict(result.subject)
    if result.metadata:
        payload.update(result.metadata)
    return payload


__all__ = ["GnapRequest", "parse_gnap_request", "serialize_gnap_result"]

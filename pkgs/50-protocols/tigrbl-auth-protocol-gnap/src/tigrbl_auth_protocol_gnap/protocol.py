from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class GnapRequest:
    access_token: tuple[Mapping[str, Any], ...]
    client: Mapping[str, Any] | str
    interact: Mapping[str, Any] | None = None


def parse_gnap_request(value: Mapping[str, Any]) -> GnapRequest:
    access = value.get("access_token")
    client = value.get("client")
    if isinstance(access, Mapping):
        access = [access]
    if (
        not isinstance(access, list)
        or not access
        or not all(isinstance(item, Mapping) for item in access)
    ):
        raise ValueError("GNAP access_token must contain one or more requests")
    if not isinstance(client, (Mapping, str)):
        raise ValueError("GNAP request requires a client instance or key reference")
    interact = value.get("interact")
    if interact is not None and not isinstance(interact, Mapping):
        raise ValueError("interact must be an object")
    return GnapRequest(tuple(dict(item) for item in access), client, interact)


__all__ = ["GnapRequest", "parse_gnap_request"]

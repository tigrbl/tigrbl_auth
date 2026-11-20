from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class EatSubmodule:
    name: str
    claims_set: Mapping[str | int, object] | None = None
    nested_token: bytes | str | None = None


def parse_submodules(value: object) -> tuple[EatSubmodule, ...]:
    if value is None:
        return ()
    if not isinstance(value, Mapping):
        raise ValueError("submods must be an object")
    modules = []
    for name, content in value.items():
        if not isinstance(name, str) or not name:
            raise ValueError("submodule names must be non-empty strings")
        if isinstance(content, Mapping):
            modules.append(EatSubmodule(name, dict(content)))
        elif isinstance(content, (bytes, str)) and content:
            modules.append(EatSubmodule(name, nested_token=content))
        else:
            raise ValueError("submodule must be a claims set or nested token")
    return tuple(modules)


__all__ = ["EatSubmodule", "parse_submodules"]

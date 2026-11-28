"""Canonical DID identifier contracts."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Did:
    method: str
    method_specific_id: str

    @classmethod
    def parse(cls, value: str) -> "Did":
        parts = value.split(":", 2)
        if len(parts) != 3 or parts[0] != "did" or not all(parts[1:]):
            raise ValueError("invalid DID")
        return cls(parts[1], parts[2])

    def __str__(self) -> str:
        return f"did:{self.method}:{self.method_specific_id}"


@dataclass(frozen=True, slots=True)
class DidUrl:
    did: Did
    path: str = ""
    query: str = ""
    fragment: str = ""


__all__ = ["Did", "DidUrl"]

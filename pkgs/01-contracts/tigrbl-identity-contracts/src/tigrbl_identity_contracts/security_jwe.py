from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JWEPolicy:
    alg: str = "dir"
    enc: str = "A256GCM"
    key_type: str = "oct"
    key_size_bytes: int = 32

    def as_header(self, *, typ: str | None = None, cty: str | None = None) -> dict[str, str]:
        header = {"alg": self.alg, "enc": self.enc}
        if typ:
            header["typ"] = typ
        if cty:
            header["cty"] = cty
        return header


__all__ = ["JWEPolicy"]

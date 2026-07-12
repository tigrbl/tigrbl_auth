"""SPIFFE workload identity contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class SvidFormat(StrEnum):
    X509 = "x509-svid"
    JWT = "jwt-svid"


@dataclass(frozen=True, slots=True)
class SpiffeId:
    trust_domain: str
    path: str

    @classmethod
    def parse(cls, value: str) -> "SpiffeId":
        if not value.startswith("spiffe://"):
            raise ValueError("SPIFFE ID must use the spiffe URI scheme")
        rest = value[len("spiffe://"):]
        domain, separator, path = rest.partition("/")
        if not domain or not separator or not path or ".." in path.split("/"):
            raise ValueError("SPIFFE ID requires a trust domain and normalized workload path")
        return cls(domain.lower(), "/" + path)

    def __str__(self) -> str:
        return f"spiffe://{self.trust_domain}{self.path}"


@dataclass(frozen=True, slots=True)
class Svid:
    spiffe_id: SpiffeId
    format: SvidFormat
    credential: bytes | str
    bundle_hint: str | None = None


class WorkloadIdentityProvider(Protocol):
    def fetch_svid(self, audience: str | None = None, /) -> Svid: ...


__all__ = ["SpiffeId", "Svid", "SvidFormat", "WorkloadIdentityProvider"]

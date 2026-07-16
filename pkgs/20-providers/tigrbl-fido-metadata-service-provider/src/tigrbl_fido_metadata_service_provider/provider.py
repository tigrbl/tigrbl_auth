"""FIDO Metadata Service BLOB orchestration with injected trust and I/O."""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Mapping, MutableMapping
from dataclasses import dataclass
from datetime import date

from tigrbl_identity_contracts.public_key_authentication import (
    AuthenticatorMetadataResult,
)
from tigrbl_public_key_authentication_bases import AuthenticatorMetadataProviderBase


@dataclass(frozen=True, slots=True)
class StatusReport:
    status: str
    effective_date: str | None = None
    certificate: str | None = None
    url: str | None = None


@dataclass(frozen=True, slots=True)
class MetadataEntry:
    aaguid: str
    statement: Mapping[str, object] | None
    status_reports: tuple[StatusReport, ...]
    time_of_last_status_change: str | None = None


@dataclass(frozen=True, slots=True)
class MetadataBlob:
    number: int
    next_update: str
    entries: tuple[MetadataEntry, ...]


def _aaguid(value: bytes | str) -> str:
    if isinstance(value, bytes):
        if len(value) != 16:
            raise ValueError("AAGUID must contain 16 bytes")
        hexed = value.hex()
        return f"{hexed[:8]}-{hexed[8:12]}-{hexed[12:16]}-{hexed[16:20]}-{hexed[20:]}"
    return value.lower()


def _parse_blob(claims: Mapping[str, object]) -> MetadataBlob:
    number, next_update, entries = (
        claims.get("no"),
        claims.get("nextUpdate"),
        claims.get("entries"),
    )
    if (
        not isinstance(number, int)
        or number < 0
        or not isinstance(next_update, str)
        or not isinstance(entries, list)
    ):
        raise ValueError("verified metadata BLOB payload is invalid")
    date.fromisoformat(next_update)
    parsed = []
    for item in entries:
        if not isinstance(item, Mapping) or not isinstance(item.get("aaguid"), str):
            continue
        reports = tuple(
            StatusReport(
                report["status"],
                report.get("effectiveDate"),
                report.get("certificate"),
                report.get("url"),
            )
            for report in item.get("statusReports", [])
            if isinstance(report, Mapping) and isinstance(report.get("status"), str)
        )
        statement = item.get("metadataStatement")
        parsed.append(
            MetadataEntry(
                _aaguid(item["aaguid"]),
                statement if isinstance(statement, Mapping) else None,
                reports,
                item.get("timeOfLastStatusChange"),
            )
        )
    return MetadataBlob(number, next_update, tuple(parsed))


class FidoMetadataServiceProvider(AuthenticatorMetadataProviderBase):
    def __init__(
        self,
        *,
        fetch_blob: Callable[[], bytes | str | Awaitable[bytes | str]],
        verify_signed_blob: Callable[
            [bytes | str], Mapping[str, object] | Awaitable[Mapping[str, object]]
        ],
        cache: MutableMapping[str, object] | None = None,
    ) -> None:
        self._fetch_blob, self._verify_signed_blob = fetch_blob, verify_signed_blob
        self._cache = cache if cache is not None else {}

    async def refresh(self) -> MetadataBlob:
        encoded = self._fetch_blob()
        encoded = await encoded if inspect.isawaitable(encoded) else encoded
        claims = self._verify_signed_blob(encoded)
        claims = await claims if inspect.isawaitable(claims) else claims
        blob = _parse_blob(claims)
        previous = self._cache.get("blob")
        if isinstance(previous, MetadataBlob) and blob.number < previous.number:
            raise ValueError("metadata BLOB rollback detected")
        self._cache["blob"] = blob
        return blob

    async def resolve(self, aaguid: bytes | str) -> AuthenticatorMetadataResult:
        blob = self._cache.get("blob")
        if (
            not isinstance(blob, MetadataBlob)
            or date.fromisoformat(blob.next_update) < date.today()
        ):
            blob = await self.refresh()
        identifier = _aaguid(aaguid)
        entry = next((item for item in blob.entries if item.aaguid == identifier), None)
        raw = bytes.fromhex(identifier.replace("-", ""))
        if entry is None:
            return AuthenticatorMetadataResult(raw, False)
        status = entry.status_reports[-1].status if entry.status_reports else None
        return AuthenticatorMetadataResult(
            raw,
            True,
            status,
            {
                "statement": entry.statement or {},
                "status_reports": entry.status_reports,
                "blob_number": blob.number,
            },
        )


__all__ = [
    "FidoMetadataServiceProvider",
    "MetadataBlob",
    "MetadataEntry",
    "StatusReport",
]

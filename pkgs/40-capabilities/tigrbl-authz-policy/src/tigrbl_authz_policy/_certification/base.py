from __future__ import annotations

import re
from urllib.parse import urlparse

from tigrbl_release_contracts import CertificationError


_SLUG_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


_SECRET_KEYS = {"password", "secret", "token", "access_token", "refresh_token"}


def _require_slug(value: str, label: str) -> str:
    if not _SLUG_RE.fullmatch(value):
        raise CertificationError(f"invalid {label}: {value!r}")
    return value


def _require_https_url(value: str, label: str, *, allow_http_localhost: bool = False) -> str:
    parsed = urlparse(value)
    if parsed.scheme == "https" and parsed.netloc:
        return value.rstrip("/")
    if (
        allow_http_localhost
        and parsed.scheme == "http"
        and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        and parsed.netloc
    ):
        return value.rstrip("/")
    raise CertificationError(f"{label} must be an absolute https issuer URL")


def deterministic_issuer(
    base_issuer: str,
    *,
    realm_slug: str | None = None,
    tenant_slug: str | None = None,
    allow_http_localhost: bool = False,
) -> str:
    """Derive an issuer without consulting request host/proxy headers."""

    issuer = _require_https_url(
        base_issuer,
        "base_issuer",
        allow_http_localhost=allow_http_localhost,
    )
    if realm_slug is not None:
        issuer = f"{issuer}/realms/{_require_slug(realm_slug, 'realm_slug')}"
    if tenant_slug is not None:
        if realm_slug is None:
            raise CertificationError("tenant issuer derivation requires a realm slug")
        issuer = f"{issuer}/tenants/{_require_slug(tenant_slug, 'tenant_slug')}"
    return issuer

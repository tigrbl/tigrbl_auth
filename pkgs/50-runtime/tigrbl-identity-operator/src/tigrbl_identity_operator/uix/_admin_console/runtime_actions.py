from __future__ import annotations

from .shell_state import *
from .resource_views import *

def build_tenant_jwks_publication_view(
    *,
    root_issuer: str,
    tenant_slug: str,
    jwks: Mapping[str, Any],
    key_records: tuple[Mapping[str, Any], ...] | list[Mapping[str, Any]] = (),
    tenant_enabled: bool = True,
) -> TenantJwksPublicationView:
    issuer = f"{root_issuer.rstrip('/')}/tenants/{tenant_slug}"
    jwks_uri = f"{root_issuer.rstrip('/')}/tenants/{tenant_slug}/.well-known/jwks.json"
    public_keys = {
        str(key.get("kid")): key
        for key in jwks.get("keys", [])
        if isinstance(key, Mapping) and key.get("kid") not in {None, ""}
    }
    rows: dict[str, TenantJwksPublicationKey] = {}

    for kid, key in public_keys.items():
        lifecycle = str(key.get("status") or "active").lower()
        rows[kid] = TenantJwksPublicationKey(
            kid=kid,
            alg=str(key.get("alg") or ""),
            kty=str(key.get("kty") or ""),
            use=str(key.get("use") or ""),
            crv=str(key.get("crv")) if key.get("crv") not in {None, ""} else None,
            lifecycle=lifecycle,
            public=True,
        )

    for record in key_records:
        data = record.get("data") or record.get("metadata") or {}
        if not isinstance(data, Mapping):
            data = {}
        kid = str(data.get("kid") or record.get("kid") or record.get("id") or "")
        if not kid:
            continue
        record_tenant = record.get("tenant") or record.get("tenant_slug") or data.get("tenant") or data.get("tenant_slug")
        if record_tenant not in {None, ""} and str(record_tenant) != tenant_slug:
            continue
        if record_tenant in {None, ""} and kid not in public_keys:
            continue
        lifecycle = str(data.get("publication_status") or record.get("status") or data.get("status") or "active").lower()
        if lifecycle not in {"active", "next", "retired"}:
            lifecycle = "active" if rows.get(kid, None) and rows[kid].public else lifecycle
        if lifecycle == "retired" or kid not in rows:
            rows[kid] = TenantJwksPublicationKey(
                kid=kid,
                alg=str(data.get("alg") or record.get("alg") or ""),
                kty=str(data.get("kty") or record.get("kty") or ""),
                use=str(data.get("use") or record.get("use") or ""),
                crv=str(data.get("crv") or data.get("curve")) if (data.get("crv") or data.get("curve")) else None,
                lifecycle=lifecycle,
                public=kid in public_keys,
                created_at=str(record.get("created_at")) if record.get("created_at") else None,
                updated_at=str(record.get("updated_at")) if record.get("updated_at") else None,
                rotated_at=str(data.get("rotated_at")) if data.get("rotated_at") else None,
                retired_at=str(data.get("retired_at")) if data.get("retired_at") else None,
            )

    ordered = tuple(sorted(rows.values(), key=lambda key: ({"active": 0, "next": 1, "retired": 2}.get(key.lifecycle, 3), key.kid)))
    status = "published" if tenant_enabled and public_keys else "not_published"
    return TenantJwksPublicationView(
        tenant_slug=tenant_slug,
        issuer=issuer,
        jwks_uri=jwks_uri,
        publication_status=status,
        keys=ordered,
        parity_indicator=f"Matches GET /tenants/{tenant_slug}/.well-known/jwks.json",
    )


def build_readiness_dashboard(
    readiness: Mapping[str, bool],
    diagnostics: Mapping[str, Any] | None = None,
) -> ReadinessDashboard:
    warnings = tuple(_warnings_for(readiness))
    if not warnings:
        status = "healthy"
    elif any(warning.code in {"admin_authorized", "contracts_valid", "migrations_current"} for warning in warnings):
        status = "blocked"
    else:
        status = "degraded"

    section_keys = {
        "runtime": "readiness_healthy",
        "database": "migrations_current",
        "issuer": "contracts_valid",
        "key_material": "openrpc_available",
        "admin_gate": "admin_authorized",
        "cookie_tls": "cookies_secure",
    }
    sections = {
        name: "ready" if bool(readiness.get(key, False)) else "blocked"
        for name, key in section_keys.items()
    }
    return ReadinessDashboard(
        status=status,
        sections=sections,
        warnings=warnings,
        diagnostics=redact_sensitive_values(diagnostics or {}),
    )


def execute_safe_mutation(
    request: SafeMutationRequest,
    *,
    executor: Callable[[SafeMutationRequest], Mapping[str, Any]] | None = None,
) -> SafeMutationResult:
    required_method = SAFE_MUTATION_METHODS.get(request.action)
    if required_method is None:
        raise ValueError(f"unknown safe mutation action {request.action!r}")
    expected_confirmation = f"{request.action}:{request.target_id}"
    audit_event = {
        "action": request.action,
        "target_id": request.target_id,
        "required_method": required_method,
    }
    if not request.confirmed or request.confirmation_text != expected_confirmation:
        return SafeMutationResult(
            action=request.action,
            target_id=request.target_id,
            status="confirmation_required",
            required_method=required_method,
            audit_event={**audit_event, "outcome": "blocked"},
            error="explicit confirmation required",
        )
    try:
        payload = dict(executor(request) if executor else {"ok": True})
    except Exception as exc:  # pragma: no cover - exception type is caller-owned.
        return SafeMutationResult(
            action=request.action,
            target_id=request.target_id,
            status="failed",
            required_method=required_method,
            audit_event={**audit_event, "outcome": "failed"},
            error=str(exc),
        )
    if payload.get("ok") is False:
        return SafeMutationResult(
            action=request.action,
            target_id=request.target_id,
            status="failed",
            required_method=required_method,
            audit_event={**audit_event, "outcome": "failed"},
            error=str(payload.get("error") or "mutation failed"),
        )
    return SafeMutationResult(
        action=request.action,
        target_id=request.target_id,
        status="executed",
        required_method=required_method,
        audit_event={**audit_event, "outcome": "executed"},
    )


def redact_sensitive_values(values: Mapping[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in values.items():
        key_text = str(key)
        if _is_sensitive_key(key_text):
            redacted[key_text] = "[REDACTED]"
        elif isinstance(value, Mapping):
            redacted[key_text] = redact_sensitive_values(value)
        else:
            redacted[key_text] = value
    return redacted


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    if normalized.startswith(("not_", "non_")):
        return False
    return any(normalized == token or normalized.endswith(f"_{token}") for token in SECRET_TOKENS)


def _warnings_for(readiness: Mapping[str, bool]) -> list[UnsafeStateWarning]:
    warning_messages = {
        "admin_authorized": "Administrator authorization is not active.",
        "readiness_healthy": "Readiness checks are degraded.",
        "contracts_valid": "Contract checks are failing.",
        "migrations_current": "Database migrations are not current.",
        "cookies_secure": "Cookie or TLS posture is unsafe.",
        "openrpc_available": "Required OpenRPC methods are unavailable.",
    }
    warnings: list[UnsafeStateWarning] = []
    for key, message in warning_messages.items():
        if not bool(readiness.get(key, False)):
            warnings.append(UnsafeStateWarning(code=key, message=message))
    return warnings

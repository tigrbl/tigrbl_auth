from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from typing import Callable, Iterable

from tigrbl_identity_contracts.oauth import (
    DPoPProof,
    DeviceAuthorization,
    OAuthClient,
    OAuthRepositoryPort,
    TokenExchangeResult,
)
from tigrbl_identity_contracts.protocols import OAuthGrantStatus


class OAuthError(RuntimeError):
    def __init__(self, code: str, description: str) -> None:
        super().__init__(description)
        self.code = code
        self.description = description


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _code(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(24)}"


def _normalize_scope(scopes: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({scope.strip() for scope in scopes if scope and scope.strip()}))


class InMemoryOAuthRepository:
    def __init__(self) -> None:
        self.clients: dict[str, OAuthClient] = {}
        self.device_authorizations: dict[str, DeviceAuthorization] = {}
        self.dpop_jtis: set[tuple[str, str]] = set()

    def save_client(self, client: OAuthClient) -> None:
        self.clients[client.client_id] = client

    def get_client(self, client_id: str) -> OAuthClient | None:
        return self.clients.get(client_id)

    def save_device_authorization(self, grant: DeviceAuthorization) -> None:
        self.device_authorizations[grant.device_code] = grant

    def get_device_authorization(self, device_code: str) -> DeviceAuthorization | None:
        return self.device_authorizations.get(device_code)

    def remember_dpop_jti(self, client_id: str, jti: str) -> bool:
        key = (client_id, jti)
        if key in self.dpop_jtis:
            return False
        self.dpop_jtis.add(key)
        return True


class OAuthProtocolService:
    def __init__(
        self,
        repository: OAuthRepositoryPort,
        now: Callable[[], datetime] = _utc_now,
    ) -> None:
        self.repository = repository
        self.now = now

    def register_client(self, client: OAuthClient) -> OAuthClient:
        if not client.client_id or not client.tenant_id:
            raise OAuthError("invalid_client_metadata", "client_id and tenant_id are required")
        if not client.allowed_scopes:
            raise OAuthError("invalid_client_metadata", "at least one allowed scope is required")
        self.repository.save_client(client)
        return client

    def start_device_authorization(
        self,
        *,
        client_id: str,
        scopes: Iterable[str],
        expires_in_seconds: int = 600,
        interval_seconds: int = 5,
    ) -> DeviceAuthorization:
        client = self._require_client(client_id)
        requested = _normalize_scope(scopes)
        self._require_scopes(client, requested)
        if expires_in_seconds <= 0 or interval_seconds <= 0:
            raise OAuthError("invalid_request", "device code expiry and polling interval must be positive")
        grant = DeviceAuthorization(
            device_code=_code("dc"),
            user_code=_code("uc")[:16],
            client_id=client.client_id,
            tenant_id=client.tenant_id,
            scopes=requested,
            expires_at=self.now() + timedelta(seconds=expires_in_seconds),
            interval_seconds=interval_seconds,
        )
        self.repository.save_device_authorization(grant)
        return grant

    def approve_device_authorization(self, device_code: str, *, subject: str) -> DeviceAuthorization:
        grant = self._require_device_authorization(device_code)
        self._require_pending_not_expired(grant)
        approved = replace(grant, status=OAuthGrantStatus.APPROVED, subject=subject)
        self.repository.save_device_authorization(approved)
        return approved

    def poll_device_authorization(self, device_code: str) -> TokenExchangeResult:
        grant = self._require_device_authorization(device_code)
        if self.now() >= grant.expires_at:
            expired = replace(grant, status=OAuthGrantStatus.EXPIRED)
            self.repository.save_device_authorization(expired)
            raise OAuthError("expired_token", "device code expired")
        if grant.status == OAuthGrantStatus.PENDING:
            polled = replace(grant, poll_count=grant.poll_count + 1)
            self.repository.save_device_authorization(polled)
            code = "slow_down" if polled.poll_count > 1 else "authorization_pending"
            raise OAuthError(code, "authorization is still pending")
        if grant.status == OAuthGrantStatus.DENIED:
            raise OAuthError("access_denied", "device authorization was denied")
        if grant.status == OAuthGrantStatus.CONSUMED:
            raise OAuthError("invalid_grant", "device code was already consumed")
        if not grant.subject:
            raise OAuthError("server_error", "approved device grant has no subject")
        consumed = replace(grant, status=OAuthGrantStatus.CONSUMED)
        self.repository.save_device_authorization(consumed)
        return TokenExchangeResult(
            issued_token=_code("at"),
            subject=grant.subject,
            actor=grant.client_id,
            audience=grant.tenant_id,
            scopes=grant.scopes,
        )

    def exchange_token(
        self,
        *,
        client_id: str,
        subject_token_subject: str,
        requested_subject: str,
        audience: str,
        scopes: Iterable[str],
        actor: str,
    ) -> TokenExchangeResult:
        client = self._require_client(client_id)
        requested = _normalize_scope(scopes)
        self._require_scopes(client, requested)
        if not audience:
            raise OAuthError("invalid_target", "audience is required")
        if subject_token_subject != requested_subject and actor != subject_token_subject:
            raise OAuthError("invalid_request", "token exchange actor must match the subject token")
        return TokenExchangeResult(
            issued_token=_code("tx"),
            subject=requested_subject,
            actor=actor,
            audience=audience,
            scopes=requested,
        )

    def validate_dpop(
        self,
        *,
        client_id: str,
        proof: DPoPProof,
        method: str,
        url: str,
        max_age_seconds: int = 300,
    ) -> None:
        client = self._require_client(client_id)
        if client.jwk_thumbprint and proof.jwk_thumbprint != client.jwk_thumbprint:
            raise OAuthError("invalid_dpop_proof", "DPoP key thumbprint does not match client binding")
        if proof.htm.upper() != method.upper() or proof.htu != url:
            raise OAuthError("invalid_dpop_proof", "DPoP proof method or URL mismatch")
        now_seconds = int(self.now().timestamp())
        if abs(now_seconds - int(proof.iat)) > max_age_seconds:
            raise OAuthError("invalid_dpop_proof", "DPoP proof is outside the accepted time window")
        if not self.repository.remember_dpop_jti(client_id, proof.jti):
            raise OAuthError("use_dpop_nonce", "DPoP proof replay detected")

    def validate_mtls_client(self, *, client_id: str, certificate_thumbprint: str) -> None:
        client = self._require_client(client_id)
        if not client.mtls_thumbprint:
            raise OAuthError("invalid_client", "client is not configured for mTLS")
        if not hmac.compare_digest(client.mtls_thumbprint, certificate_thumbprint):
            raise OAuthError("invalid_client", "mTLS certificate thumbprint mismatch")

    def _require_client(self, client_id: str) -> OAuthClient:
        client = self.repository.get_client(client_id)
        if client is None or not client.enabled:
            raise OAuthError("invalid_client", "client is unknown or disabled")
        return client

    def _require_device_authorization(self, device_code: str) -> DeviceAuthorization:
        grant = self.repository.get_device_authorization(device_code)
        if grant is None:
            raise OAuthError("invalid_grant", "unknown device code")
        return grant

    def _require_pending_not_expired(self, grant: DeviceAuthorization) -> None:
        if grant.status != OAuthGrantStatus.PENDING:
            raise OAuthError("invalid_grant", "device authorization is not pending")
        if self.now() >= grant.expires_at:
            raise OAuthError("expired_token", "device code expired")

    @staticmethod
    def _require_scopes(client: OAuthClient, scopes: tuple[str, ...]) -> None:
        allowed = set(client.allowed_scopes)
        if not scopes or not set(scopes).issubset(allowed):
            raise OAuthError("invalid_scope", "requested scopes are not allowed for client")


def sha256_thumbprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


__all__ = [
    "DPoPProof",
    "DeviceAuthorization",
    "InMemoryOAuthRepository",
    "OAuthClient",
    "OAuthError",
    "OAuthGrantStatus",
    "OAuthProtocolService",
    "OAuthRepositoryPort",
    "TokenExchangeResult",
    "sha256_thumbprint",
]

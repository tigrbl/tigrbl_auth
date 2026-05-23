from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Mapping
from urllib.parse import parse_qs, urlencode, urlparse


class RPError(RuntimeError):
    pass


class BrowserStoragePolicy(str, Enum):
    MEMORY_ONLY = "memory_only"
    SESSION_STORAGE = "session_storage"
    LOCAL_STORAGE = "local_storage"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def make_pkce_verifier() -> str:
    return secrets.token_urlsafe(48)


def pkce_s256_challenge(verifier: str) -> str:
    if not verifier:
        raise ValueError("PKCE verifier is required")
    return _b64url(hashlib.sha256(verifier.encode("ascii")).digest())


@dataclass(frozen=True, slots=True)
class RPConfiguration:
    issuer: str
    client_id: str
    redirect_uri: str
    scopes: tuple[str, ...] = ("openid",)
    client_secret: str | None = None
    post_logout_redirect_uri: str | None = None

    def __post_init__(self) -> None:
        if not self.issuer or not self.client_id or not self.redirect_uri:
            raise ValueError("issuer, client_id, and redirect_uri are required")
        object.__setattr__(self, "issuer", self.issuer.rstrip("/"))
        object.__setattr__(self, "scopes", tuple(sorted(set(self.scopes))))


@dataclass(frozen=True, slots=True)
class LoginRequest:
    state: str
    nonce: str
    code_verifier: str
    redirect_uri: str
    scope: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CallbackResult:
    code: str
    state: str
    iss: str | None = None


@dataclass(frozen=True, slots=True)
class RPSession:
    subject: str
    id_token: str
    access_token: str
    refresh_token: str | None = None


class StateNonceStore:
    def __init__(self) -> None:
        self._items: dict[str, LoginRequest] = {}
        self._consumed: set[str] = set()

    def create(self, *, redirect_uri: str, scope: tuple[str, ...]) -> LoginRequest:
        request = LoginRequest(
            state=secrets.token_urlsafe(24),
            nonce=secrets.token_urlsafe(24),
            code_verifier=make_pkce_verifier(),
            redirect_uri=redirect_uri,
            scope=tuple(scope),
        )
        self._items[request.state] = request
        return request

    def consume(self, state: str) -> LoginRequest:
        if state in self._consumed:
            raise RPError("callback state was already consumed")
        try:
            request = self._items.pop(state)
        except KeyError as exc:
            raise RPError("unknown callback state") from exc
        self._consumed.add(state)
        return request


class BrowserMemorySession:
    def __init__(self, *, policy: BrowserStoragePolicy = BrowserStoragePolicy.MEMORY_ONLY, client_secret: str | None = None) -> None:
        if client_secret is not None:
            raise RPError("browser RP sessions must not contain a client secret")
        self.policy = BrowserStoragePolicy(policy)
        self._session: RPSession | None = None

    def set(self, session: RPSession) -> None:
        self._session = session

    def get(self) -> RPSession | None:
        return self._session

    def clear(self) -> None:
        self._session = None


def assert_browser_no_client_secret(config: RPConfiguration) -> None:
    if config.client_secret is not None:
        raise RPError("browser RP configuration must not include a client secret")


def validate_browser_storage_policy(policy: BrowserStoragePolicy | str) -> BrowserStoragePolicy:
    selected = BrowserStoragePolicy(policy)
    if selected is BrowserStoragePolicy.LOCAL_STORAGE:
        raise RPError("browser RP tokens must not be persisted in localStorage")
    return selected


class JwksCache:
    def __init__(self) -> None:
        self._keys: dict[str, Mapping[str, Any]] = {}

    def put(self, jwks: Mapping[str, Any]) -> None:
        for key in jwks.get("keys", []):
            kid = key.get("kid")
            if kid:
                self._keys[str(kid)] = dict(key)

    def get(self, kid: str) -> Mapping[str, Any]:
        try:
            return self._keys[kid]
        except KeyError as exc:
            raise RPError("unknown JWKS key") from exc


class DiscoveryClient:
    def __init__(self, fetch: Callable[[str], Mapping[str, Any]]) -> None:
        self.fetch = fetch

    def discover(self, issuer: str) -> Mapping[str, Any]:
        metadata = dict(self.fetch(issuer.rstrip("/") + "/.well-known/openid-configuration"))
        if metadata.get("issuer", "").rstrip("/") != issuer.rstrip("/"):
            raise RPError("issuer metadata mismatch")
        required = (
            "authorization_endpoint",
            "token_endpoint",
            "jwks_uri",
            "userinfo_endpoint",
        )
        missing = [name for name in required if not metadata.get(name)]
        if missing:
            raise RPError(f"issuer metadata missing required endpoints: {', '.join(missing)}")
        return metadata


class UserInfoClient:
    def __init__(self, fetch: Callable[[str, str], Mapping[str, Any]]) -> None:
        self.fetch = fetch

    def get(self, endpoint: str, access_token: str) -> Mapping[str, Any]:
        if not access_token:
            raise RPError("access token is required for UserInfo")
        return dict(self.fetch(endpoint, access_token))


class TokenStore:
    def __init__(self) -> None:
        self._sessions: dict[str, RPSession] = {}

    def save(self, session_id: str, session: RPSession) -> None:
        self._sessions[session_id] = session

    def get(self, session_id: str) -> RPSession:
        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise RPError("unknown RP session") from exc


class RelyingParty:
    def __init__(self, config: RPConfiguration, *, state_store: StateNonceStore | None = None) -> None:
        self.config = config
        self.state_store = state_store or StateNonceStore()
        self.token_store = TokenStore()

    def build_authorization_url(self, authorization_endpoint: str) -> tuple[str, LoginRequest]:
        login = self.state_store.create(redirect_uri=self.config.redirect_uri, scope=self.config.scopes)
        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": login.redirect_uri,
            "scope": " ".join(login.scope),
            "state": login.state,
            "nonce": login.nonce,
            "code_challenge": pkce_s256_challenge(login.code_verifier),
            "code_challenge_method": "S256",
        }
        return f"{authorization_endpoint}?{urlencode(params)}", login

    def parse_callback(self, callback_url: str) -> CallbackResult:
        parsed = urlparse(callback_url)
        values = parse_qs(parsed.query, keep_blank_values=True)
        if "error" in values:
            raise RPError(values["error"][0] or "authorization error")
        code = (values.get("code") or [""])[0]
        state = (values.get("state") or [""])[0]
        if not code or not state:
            raise RPError("callback requires code and state")
        return CallbackResult(code=code, state=state, iss=(values.get("iss") or [None])[0])

    def validate_callback(self, callback: CallbackResult) -> LoginRequest:
        return self.state_store.consume(callback.state)

    def build_logout_url(self, end_session_endpoint: str, *, id_token_hint: str, state: str | None = None) -> str:
        params = {
            "client_id": self.config.client_id,
            "id_token_hint": id_token_hint,
        }
        if self.config.post_logout_redirect_uri:
            params["post_logout_redirect_uri"] = self.config.post_logout_redirect_uri
        if state:
            params["state"] = state
        return f"{end_session_endpoint}?{urlencode(params)}"

    def exchange_code_confidential(
        self,
        exchange: Callable[[Mapping[str, str]], Mapping[str, str]],
        callback: CallbackResult,
    ) -> RPSession:
        if self.config.client_secret is None:
            raise RPError("confidential token exchange requires a client secret")
        login = self.validate_callback(callback)
        token_response = dict(
            exchange(
                {
                    "grant_type": "authorization_code",
                    "code": callback.code,
                    "redirect_uri": login.redirect_uri,
                    "client_id": self.config.client_id,
                    "client_secret": self.config.client_secret,
                    "code_verifier": login.code_verifier,
                }
            )
        )
        session = RPSession(
            subject=token_response.get("sub", ""),
            id_token=token_response["id_token"],
            access_token=token_response["access_token"],
            refresh_token=token_response.get("refresh_token"),
        )
        self.token_store.save(login.state, session)
        return session

    def refresh(self, refresh: Callable[[str], Mapping[str, str]], session_id: str) -> RPSession:
        current = self.token_store.get(session_id)
        if not current.refresh_token:
            raise RPError("refresh token is not available")
        response = dict(refresh(current.refresh_token))
        updated = RPSession(
            subject=current.subject,
            id_token=response.get("id_token", current.id_token),
            access_token=response["access_token"],
            refresh_token=response.get("refresh_token", current.refresh_token),
        )
        self.token_store.save(session_id, updated)
        return updated


def validate_id_token_claims(claims: Mapping[str, Any], *, issuer: str, audience: str, nonce: str) -> Mapping[str, Any]:
    if str(claims.get("iss", "")).rstrip("/") != issuer.rstrip("/"):
        raise RPError("ID token issuer mismatch")
    aud = claims.get("aud", ())
    audiences = {aud} if isinstance(aud, str) else set(aud)
    if audience not in audiences:
        raise RPError("ID token audience mismatch")
    if claims.get("nonce") != nonce:
        raise RPError("ID token nonce mismatch")
    if int(claims.get("exp", 0)) <= 0:
        raise RPError("ID token expiry is required")
    return dict(claims)


def shared_vector_manifest() -> Mapping[str, str]:
    return {
        "pkce_s256_empty": pkce_s256_challenge("vector-verifier"),
        "browser_storage_policy": BrowserStoragePolicy.MEMORY_ONLY.value,
        "callback_required_params": "code,state",
    }


def framework_login_adapter(rp: RelyingParty, authorization_endpoint: str) -> Mapping[str, Any]:
    url, login = rp.build_authorization_url(authorization_endpoint)
    return {
        "status": 302,
        "headers": {"location": url},
        "state": login.state,
        "nonce": login.nonce,
    }


def framework_callback_adapter(rp: RelyingParty, request_url: str) -> CallbackResult:
    return rp.parse_callback(request_url)


def example_app_manifest() -> Mapping[str, Any]:
    return {
        "python_server_rp": {
            "login_route": "/login",
            "callback_route": "/callback",
            "session_cookie": "rp_session",
        },
        "browser_rp": {
            "storage_policy": BrowserStoragePolicy.MEMORY_ONLY.value,
            "client_secret": False,
        },
    }


__all__ = [
    "BrowserMemorySession",
    "BrowserStoragePolicy",
    "CallbackResult",
    "DiscoveryClient",
    "JwksCache",
    "LoginRequest",
    "RPConfiguration",
    "RPError",
    "RPSession",
    "RelyingParty",
    "StateNonceStore",
    "TokenStore",
    "UserInfoClient",
    "assert_browser_no_client_secret",
    "example_app_manifest",
    "framework_login_adapter",
    "framework_callback_adapter",
    "make_pkce_verifier",
    "pkce_s256_challenge",
    "shared_vector_manifest",
    "validate_browser_storage_policy",
    "validate_id_token_claims",
]

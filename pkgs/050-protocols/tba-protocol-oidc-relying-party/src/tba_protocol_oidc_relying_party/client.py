from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from hmac import compare_digest
from time import time
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

from tba_contracts_identity.protocols import BrowserStoragePolicy
from tba_contracts_identity.rp import (
    CallbackResult,
    LoginRequest,
    RPConfiguration,
    RPSession,
    RPSessionPort,
    RPStatePort,
)

from .errors import RPError
from .pkce import PkceVerifier, make_pkce_verifier, pkce_s256_challenge
from .public_client import check_callback, check_discovery, https_url, token_claims


def authorization_options(
    intent: str = "ordinary", acr_values: str | None = None
) -> dict[str, str]:
    """Translate a login intent into controlled authorization parameters."""
    if intent not in ("ordinary", "interactive", "step_up"):
        raise RPError("invalid login intent")
    if intent == "step_up":
        if (
            not isinstance(acr_values, str)
            or not acr_values.split()
            or len(acr_values) > 512
        ):
            raise RPError("step-up requires requested assurance values")
        return {"prompt": "login", "acr_values": acr_values}
    if acr_values is not None:
        raise RPError("requested assurance values require step-up")
    return {"prompt": "login"} if intent == "interactive" else {}


def resolve_end_session_endpoint(
    metadata: Mapping[str, Any], issuer: str
) -> str | None:
    """Resolve an advertised end-session endpoint on the configured issuer origin."""
    expected = urlparse(https_url(issuer, "issuer"))
    if "?" in issuer or metadata.get("issuer") != issuer:
        raise RPError("issuer metadata mismatch")
    value = metadata.get("end_session_endpoint")
    if value is None:
        return None
    endpoint = https_url(value, "end_session_endpoint")
    actual = urlparse(endpoint)
    actual_port = 443 if actual.port is None else actual.port
    expected_port = 443 if expected.port is None else expected.port
    if "?" in endpoint or (actual.hostname, actual_port) != (
        expected.hostname,
        expected_port,
    ):
        raise RPError(
            "end_session_endpoint must belong to the configured issuer origin"
        )
    return endpoint


def validate_logout_return(url: str, registered: str, expected_state: str) -> bool:
    """Validate a return before the host atomically consumes browser-bound state."""
    if not expected_state or not expected_state.isascii() or len(expected_state) > 512:
        return False
    try:
        actual = urlparse(https_url(url, "logout return"))
        expected = urlparse(https_url(registered, "post-logout redirect URI"))
        query = parse_qs(actual.query, keep_blank_values=True, max_num_fields=64)
        fixed = parse_qs(expected.query, keep_blank_values=True, max_num_fields=64)
    except (RPError, ValueError):
        return False
    state = query.pop("state", [])
    return (
        url.partition("?")[0] == registered.partition("?")[0]
        and query == fixed
        and len(state) == 1
        and state[0].isascii()
        and compare_digest(state[0], expected_state)
    )


JsonGetter = Callable[[str], Awaitable[Mapping[str, Any]]]
FormPoster = Callable[[str, Mapping[str, str]], Awaitable[Mapping[str, Any]]]


class BrowserMemorySession:
    def __init__(
        self,
        *,
        policy: BrowserStoragePolicy = BrowserStoragePolicy.MEMORY_ONLY,
        client_secret: str | None = None,
    ) -> None:
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


def validate_browser_storage_policy(
    policy: BrowserStoragePolicy | str,
) -> BrowserStoragePolicy:
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
        metadata = dict(
            self.fetch(issuer.rstrip("/") + "/.well-known/openid-configuration")
        )
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
            raise RPError(
                f"issuer metadata missing required endpoints: {', '.join(missing)}"
            )
        return metadata


class UserInfoClient:
    def __init__(self, fetch: Callable[[str, str], Mapping[str, Any]]) -> None:
        self.fetch = fetch

    def get(self, endpoint: str, access_token: str) -> Mapping[str, Any]:
        if not access_token:
            raise RPError("access token is required for UserInfo")
        return dict(self.fetch(endpoint, access_token))


class RelyingParty:
    def __init__(
        self,
        config: RPConfiguration,
        *,
        state_store: RPStatePort,
        session_store: RPSessionPort | None = None,
    ) -> None:
        self.config = config
        self.state_store = state_store
        self.token_store = session_store

    def build_authorization_url(
        self,
        authorization_endpoint: str,
        *,
        intent: str = "ordinary",
        acr_values: str | None = None,
    ) -> tuple[str, LoginRequest]:
        options = authorization_options(intent, acr_values)
        query = parse_qs(urlparse(authorization_endpoint).query, keep_blank_values=True)
        if options.keys() & query.keys() or (options and "acr_values" in query):
            raise RPError(
                "authorization endpoint already contains login intent parameters"
            )
        login = self.state_store.create(
            redirect_uri=self.config.redirect_uri, scope=self.config.scopes
        )
        pkce = PkceVerifier(login.code_verifier)
        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": login.redirect_uri,
            "scope": " ".join(login.scope),
            "state": login.state,
            "nonce": login.nonce,
            **pkce.authorization_params(),
            **options,
        }
        separator = "&" if "?" in authorization_endpoint else "?"
        return f"{authorization_endpoint}{separator}{urlencode(params)}", login

    def parse_callback(self, callback_url: str) -> CallbackResult:
        parsed = urlparse(callback_url)
        values = parse_qs(parsed.query, keep_blank_values=True)
        if "error" in values:
            raise RPError(values["error"][0] or "authorization error")
        code = (values.get("code") or [""])[0]
        state = (values.get("state") or [""])[0]
        if not code or not state:
            raise RPError("callback requires code and state")
        return CallbackResult(
            code=code, state=state, iss=(values.get("iss") or [None])[0]
        )

    def validate_callback(self, callback: CallbackResult) -> LoginRequest:
        try:
            return self.state_store.consume(callback.state)
        except (KeyError, ValueError) as exc:
            raise RPError(str(exc)) from exc

    async def _public_metadata(self, get_json: JsonGetter) -> Mapping[str, Any]:
        assert_browser_no_client_secret(self.config)
        issuer = https_url(self.config.issuer, "issuer")
        if urlparse(issuer).query or "?" in issuer:
            raise RPError("invalid issuer URL")
        https_url(self.config.redirect_uri, "redirect URI")
        if "openid" not in self.config.scopes:
            raise RPError("public OIDC login requires the openid scope")
        metadata = await get_json(issuer + "/.well-known/openid-configuration")
        check_discovery(metadata, issuer)
        return metadata

    async def begin_public_login(
        self,
        get_json: JsonGetter,
        *,
        intent: str = "ordinary",
        acr_values: str | None = None,
    ) -> tuple[str, LoginRequest]:
        """Discover the issuer and start a public S256 login via the configured state store."""
        metadata = await self._public_metadata(get_json)
        return self.build_authorization_url(
            metadata["authorization_endpoint"],
            intent=intent,
            acr_values=acr_values,
        )

    async def complete_public_callback(
        self,
        callback_url: str,
        *,
        expected_state: str,
        get_json: JsonGetter,
        post_form: FormPoster,
        expected_subject: str | None = None,
    ) -> VerifiedCallback:
        """Redeem a browser-bound callback and save tokens only after ID-token verification.

        Pass expected_state from the app's browser session. The state store must
        atomically consume unexpired requests scoped to this issuer and client.
        The transport must enforce HTTPS certificate verification and reject redirects.
        """
        assert_browser_no_client_secret(self.config)
        if self.token_store is None:
            raise RPError("public callback requires a token store")
        check_callback(callback_url, self.config.redirect_uri)
        if "error" in parse_qs(urlparse(callback_url).query, keep_blank_values=True):
            raise RPError("authorization was not completed")
        callback = self.parse_callback(callback_url)
        if not expected_state or callback.state != expected_state:
            raise RPError("callback state mismatch")
        if callback.iss is not None and callback.iss != self.config.issuer:
            raise RPError("callback issuer mismatch")
        login = self.validate_callback(callback)
        if (
            login.state != callback.state
            or login.redirect_uri != self.config.redirect_uri
            or not login.nonce
        ):
            raise RPError("callback does not match the stored login request")
        verifier = PkceVerifier(login.code_verifier)
        metadata = await self._public_metadata(get_json)
        tokens = await post_form(
            metadata["token_endpoint"],
            {
                "grant_type": "authorization_code",
                "client_id": self.config.client_id,
                "redirect_uri": login.redirect_uri,
                "code": callback.code,
                "code_verifier": verifier.value,
            },
        )
        if not isinstance(tokens, Mapping) or tokens.get("error"):
            raise RPError("token exchange was rejected")
        access_token = tokens.get("access_token")
        id_token = tokens.get("id_token")
        refresh_token = tokens.get("refresh_token")
        token_type = tokens.get("token_type")
        if (
            not isinstance(access_token, str)
            or not access_token
            or not isinstance(id_token, str)
            or not id_token
            or not isinstance(token_type, str)
            or token_type.lower() != "bearer"
            or (
                "refresh_token" in tokens
                and (not isinstance(refresh_token, str) or not refresh_token)
            )
        ):
            raise RPError("token response is missing valid OIDC tokens")
        jwks = await get_json(metadata["jwks_uri"])
        claims = token_claims(id_token, jwks)
        if claims.get("iss") != self.config.issuer:
            raise RPError("ID token issuer mismatch")
        if claims["aud"] not in (self.config.client_id, [self.config.client_id]):
            raise RPError("ID token audience mismatch")
        if "azp" in claims and claims["azp"] != self.config.client_id:
            raise RPError("ID token authorized party mismatch")
        identity = verify_id_token(
            id_token,
            verifier=lambda _: claims,
            issuer=self.config.issuer,
            audience=self.config.client_id,
            nonce=login.nonce,
            now=int(time()),
        )
        if expected_subject is not None and identity.subject != expected_subject:
            raise RPError("callback subject does not match the expected account")
        session = RPSession(identity.subject, id_token, access_token, refresh_token)
        self.token_store.save(login.state, session)
        return VerifiedCallback(identity, session)

    def build_logout_url(
        self, end_session_endpoint: str, *, id_token_hint: str, state: str | None = None
    ) -> str:
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
        if self.token_store is None:
            raise RPError("this exchange requires a token store")
        secret = self.config.client_secret
        if secret is None:
            raise RPError("confidential token exchange requires a client secret")
        login = self.validate_callback(callback)
        token_response = dict(
            self._exchange_confidential(exchange, callback, login, secret)
        )
        session = RPSession(
            subject=token_response.get("sub", ""),
            id_token=token_response["id_token"],
            access_token=token_response["access_token"],
            refresh_token=token_response.get("refresh_token"),
        )
        self.token_store.save(login.state, session)
        return session

    def complete_confidential_callback(
        self,
        exchange: Callable[[Mapping[str, str]], Mapping[str, str]],
        callback: CallbackResult,
        *,
        browser_state: str,
        verifier: Callable[[str], Mapping[str, Any]],
        now: int,
    ) -> VerifiedExternalIdentity:
        """Verify a browser-bound login before the app establishes a session.

        Supply browser_state from the initiating browser's transaction cookie
        and a verifier that checks the configured issuer's signing keys.
        Provider tokens are discarded after verifying the identity.
        """
        secret = self.config.client_secret
        if not secret:
            raise RPError("confidential token exchange requires a client secret")
        if not browser_state or not compare_digest(
            browser_state.encode("utf-8"), callback.state.encode("utf-8")
        ):
            raise RPError("callback does not match the browser transaction")
        if callback.iss is not None and callback.iss != self.config.issuer:
            raise RPError("callback issuer mismatch")
        login = self.validate_callback(callback)
        if (
            login.state != callback.state
            or login.redirect_uri != self.config.redirect_uri
            or not login.nonce
        ):
            raise RPError("callback does not match the stored login request")
        PkceVerifier(login.code_verifier)
        response = self._exchange_confidential(exchange, callback, login, secret)
        token = response.get("id_token")
        if not isinstance(token, str) or not token:
            raise RPError("token response must include an ID token")
        return verify_id_token(
            token,
            verifier=verifier,
            issuer=self.config.issuer,
            audience=self.config.client_id,
            nonce=login.nonce,
            now=now,
        )

    def _exchange_confidential(
        self,
        exchange: Callable[[Mapping[str, str]], Mapping[str, str]],
        callback: CallbackResult,
        login: LoginRequest,
        secret: str,
    ) -> Mapping[str, str]:
        return exchange(
            {
                "grant_type": "authorization_code",
                "code": callback.code,
                "redirect_uri": login.redirect_uri,
                "client_id": self.config.client_id,
                "client_secret": secret,
                "code_verifier": login.code_verifier,
            }
        )

    def refresh(
        self, refresh: Callable[[str], Mapping[str, str]], session_id: str
    ) -> RPSession:
        if self.token_store is None:
            raise RPError("refresh requires a token store")
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


def validate_id_token_claims(
    claims: Mapping[str, Any], *, issuer: str, audience: str, nonce: str
) -> Mapping[str, Any]:
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


@dataclass(frozen=True, slots=True)
class VerifiedExternalIdentity:
    subject: str
    issuer: str
    claims: Mapping[str, Any]
    userinfo: Mapping[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class VerifiedCallback:
    identity: VerifiedExternalIdentity
    session: RPSession


def verify_id_token(
    token: str,
    *,
    verifier: Callable[[str], Mapping[str, Any]],
    issuer: str,
    audience: str,
    nonce: str,
    now: int,
    userinfo: Mapping[str, Any] | None = None,
    maximum_age: int | None = None,
) -> VerifiedExternalIdentity:
    """Verify signature through the injected JOSE boundary, then enforce OIDC claims."""
    claims = dict(verifier(token))
    validate_id_token_claims(claims, issuer=issuer, audience=audience, nonce=nonce)
    if not claims.get("sub"):
        raise RPError("ID token subject is required")
    if int(claims.get("exp", 0)) <= now:
        raise RPError("ID token has expired")
    if int(claims.get("iat", now)) > now:
        raise RPError("ID token was issued in the future")
    if int(claims.get("nbf", now)) > now:
        raise RPError("ID token is not active yet")
    if maximum_age is not None:
        if "auth_time" not in claims:
            raise RPError("ID token authentication time is required")
        if now - int(claims["auth_time"]) > maximum_age:
            raise RPError("ID token authentication is too old")
    audiences = claims.get("aud", ())
    if (
        not isinstance(audiences, str)
        and len(tuple(audiences)) > 1
        and claims.get("azp") != audience
    ):
        raise RPError("ID token authorized party mismatch")
    if userinfo is not None and userinfo.get("sub") != claims["sub"]:
        raise RPError("UserInfo subject does not match ID token subject")
    return VerifiedExternalIdentity(
        str(claims["sub"]),
        str(claims["iss"]),
        claims,
        dict(userinfo) if userinfo is not None else None,
    )


def shared_vector_manifest() -> Mapping[str, str]:
    return {
        "pkce_s256_empty": pkce_s256_challenge("vector-verifier"),
        "browser_storage_policy": BrowserStoragePolicy.MEMORY_ONLY.value,
        "callback_required_params": "code,state",
    }


def framework_login_adapter(
    rp: RelyingParty, authorization_endpoint: str
) -> Mapping[str, Any]:
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
    "PkceVerifier",
    "RPConfiguration",
    "RPError",
    "RPSession",
    "RelyingParty",
    "UserInfoClient",
    "VerifiedCallback",
    "VerifiedExternalIdentity",
    "assert_browser_no_client_secret",
    "example_app_manifest",
    "framework_callback_adapter",
    "framework_login_adapter",
    "make_pkce_verifier",
    "pkce_s256_challenge",
    "shared_vector_manifest",
    "validate_browser_storage_policy",
    "validate_id_token_claims",
    "verify_id_token",
]

"""Server-side Google Workspace relying-party routes."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from http.client import HTTPException, HTTPSConnection
from http.cookies import CookieError, SimpleCookie
from threading import Lock
from urllib.parse import parse_qs, urlencode, urlsplit

from tba_concrete_jws import parse_jws_compact
from tba_protocol_oidc_relying_party import RelyingParty, RPConfiguration, RPError
from tba_provider_jose_cryptography.public_jws import verify_public_jws
from tba_runtime_relying_party_session.sqlite import SQLiteRPStore

_LOGGER = logging.getLogger(__name__)
_ISSUER = "https://accounts.google.com"
_AUTHORIZE = f"{_ISSUER}/o/oauth2/v2/auth"
_STATE_COOKIE = "__Host-tba-workspace-state"
_RETURN_COOKIE = "__Host-tba-workspace-return"
_SESSION_COOKIE = "__Host-tba-workspace"
_LOGIN = "/auth/login"
_LOGOUT = "/auth/logout"
_AUTHORIZE_SESSION = "/auth/session"


def _google_json(host, path, *, form=None):
    connection = HTTPSConnection(host, timeout=5)
    try:
        if form is None:
            connection.request("GET", path)
        else:
            connection.request(
                "POST", path, urlencode(form),
                {"Content-Type": "application/x-www-form-urlencoded"},
            )
        response = connection.getresponse()
        payload = response.read(131073)
        if response.status != 200 or len(payload) > 131072:
            raise ValueError("Google Workspace OIDC endpoint rejected the request")
        result = json.loads(payload)
        if not isinstance(result, dict):
            raise TypeError("Google Workspace OIDC endpoint returned an invalid object")
        return result
    finally:
        connection.close()


class GoogleWorkspace:
    def __init__(self):
        self._keys = {}
        self._next_refresh = 0.0
        self._last_refresh = float("-inf")
        self._lock = Lock()

    def exchange(self, form):
        return _google_json("oauth2.googleapis.com", "/token", form=form)

    def verify(self, token):
        jws = parse_jws_compact(token)
        header = jws.protected_headers
        kid = header.get("kid")
        if header.get("alg") != "RS256" or not isinstance(kid, str) or not kid:
            raise ValueError("Google Workspace requires a signed RS256 token with a key ID")
        now = time.monotonic()
        with self._lock:
            if now >= self._next_refresh or (kid not in self._keys and now - self._last_refresh >= 30):
                self._last_refresh = now
                keys = _google_json("www.googleapis.com", "/oauth2/v3/certs").get("keys", ())
                self._keys = {key["kid"]: key for key in keys}
                self._next_refresh = now + 300
            key = self._keys.get(kid)
        if key is None:
            raise ValueError("Google Workspace signing key is unavailable")
        verify_public_jws(token, key)
        claims = json.loads(jws.payload)
        if not isinstance(claims, dict):
            raise TypeError("Google Workspace returned invalid ID token claims")
        if claims.get("iss") == "accounts.google.com":
            claims["iss"] = _ISSUER
        return claims


def _cookie_header(name, value, *, max_age):
    cookie = SimpleCookie()
    cookie[name] = value
    cookie[name]["secure"] = True
    cookie[name]["httponly"] = True
    cookie[name]["samesite"] = "Lax"
    cookie[name]["path"] = "/"
    cookie[name]["max-age"] = max_age
    return (b"set-cookie", cookie[name].OutputString().encode("ascii"))


def _read_cookies(scope):
    result = SimpleCookie()
    try:
        for name, value in scope.get("headers", ()):
            if name.lower() == b"cookie":
                result.load(value.decode("latin-1"))
    except CookieError:
        return {}
    return {name: morsel.value for name, morsel in result.items()}


def _safe_return(value, application_path):
    if (
        not value.startswith(application_path) or not value.isascii()
        or any(ord(c) < 33 for c in value) or "\\" in value
    ):
        return application_path
    parsed = urlsplit(value)
    if not parsed.netloc and not parsed.scheme and (
        parsed.path == application_path or parsed.path.startswith(application_path + "/")
    ):
        return value
    return application_path


async def _respond(send, status, *, location=None, cookies=(), body=b""):
    headers = [
        (b"cache-control", b"no-store"),
        (b"referrer-policy", b"no-referrer"),
        (b"content-type", b"text/plain; charset=utf-8"),
        *cookies,
    ]
    if location is not None:
        headers.append((b"location", location.encode("ascii")))
    await send({"type": "http.response.start", "status": status, "headers": headers})
    await send({"type": "http.response.body", "body": body})


class WorkspaceLogin:
    """Authenticate Workspace identities and let the app enforce its own grants."""

    def __init__(
        self, *, client_id, client_secret, redirect_uri, database, authorize,
        application_path, signed_out_path, google=None,
    ):
        redirect = urlsplit(redirect_uri)
        if (
            redirect.scheme != "https" or not redirect.hostname or redirect.username is not None
            or redirect.query or redirect.fragment or not redirect.path
        ):
            raise ValueError("Workspace requires a fixed HTTPS callback")
        if not client_id or not client_secret:
            raise ValueError("Workspace requires confidential client credentials")
        if (
            not application_path.startswith("/") or application_path.startswith("//")
            or application_path.endswith("/") or urlsplit(application_path).path != application_path
            or not signed_out_path.startswith(f"{application_path}/")
            or _safe_return(signed_out_path, application_path) != signed_out_path
        ):
            raise ValueError("Workspace requires local application and signed-out paths")
        self.origin = f"{redirect.scheme}://{redirect.netloc}"
        self.callback = redirect.path
        self.application_path = application_path
        self.signed_out_path = signed_out_path
        self.authorize = authorize
        self.google = google if google is not None else GoogleWorkspace()
        self.store = SQLiteRPStore(database, realm=f"{_ISSUER}\n{client_id}\n{self.origin}")
        self.rp = RelyingParty(
            RPConfiguration(
                issuer=_ISSUER, client_id=client_id, client_secret=client_secret,
                redirect_uri=redirect_uri, scopes=("openid", "email"),
            ),
            state_store=self.store,
        )

    def resolve(self, scope):
        if scope["method"] not in {"GET", "HEAD", "OPTIONS"} and not self._same_origin(scope):
            raise PermissionError("Workspace session origin denied")
        session = _read_cookies(scope).get(_SESSION_COOKIE)
        identity = self.store.get_session(session) if session else None
        if identity is None:
            raise PermissionError("Workspace sign-in required")
        return self.authorize(identity)

    def _same_origin(self, scope):
        origins = [value for name, value in scope["headers"] if name.lower() == b"origin"]
        return origins == [self.origin.encode("ascii")]

    def _finish(self, scope, cookies):
        query = scope["query_string"].decode("ascii")
        callback = self.rp.parse_callback(f"{self.rp.config.redirect_uri}?{query}")
        now = int(time.time())
        verified = self.rp.complete_confidential_callback(
            self.google.exchange, callback, browser_state=cookies.get(_STATE_COOKIE, ""),
            verifier=self.google.verify, now=now,
        )
        claims = verified.claims
        email, domain = claims.get("email"), claims.get("hd")
        if (
            not isinstance(email, str) or not isinstance(domain, str) or not domain
            or email.rpartition("@")[2].lower() != domain.lower()
            or claims.get("email_verified") is not True
            or claims["aud"] != self.rp.config.client_id
            or claims.get("azp", self.rp.config.client_id) != self.rp.config.client_id
            or not isinstance(claims.get("iat"), int)
        ):
            raise PermissionError("Verified Workspace account required")
        identity = {"iss": verified.issuer, "sub": verified.subject, "email": email.lower(),
                    "hd": domain.lower()}
        self.authorize(identity)
        old_session = cookies.get(_SESSION_COOKIE)
        if old_session:
            self.store.revoke_session(old_session)
        expires = min(int(claims["exp"]), now + 50 * 60)
        return self.store.start_session(identity, expires=expires), expires - now

    def wrap(self, app):
        async def workspace_routes(scope, receive, send):
            if scope["type"] != "http" or scope["path"] not in {
                _LOGIN, _LOGOUT, _AUTHORIZE_SESSION, self.callback,
            }:
                await app(scope, receive, send)
                return
            path = scope["path"]
            method = scope["method"]
            if method != ("POST" if path == _LOGOUT else "GET"):
                await _respond(send, 405)
                return
            cookies = _read_cookies(scope)
            if path == _LOGIN:
                params = parse_qs(scope["query_string"].decode("ascii", errors="replace"))
                destination = _safe_return(params.get("return", [""])[0], self.application_path)
                location, transaction = await asyncio.to_thread(
                    self.rp.build_authorization_url, _AUTHORIZE
                )
                await _respond(send, 302, location=location, cookies=(
                    _cookie_header(_STATE_COOKIE, transaction.state, max_age=300),
                    _cookie_header(_RETURN_COOKIE, destination, max_age=300),
                ))
            elif path == _LOGOUT:
                if not self._same_origin(scope):
                    await _respond(send, 403)
                    return
                session = cookies.get(_SESSION_COOKIE)
                if session:
                    await asyncio.to_thread(self.store.revoke_session, session)
                await _respond(send, 303, location=self.signed_out_path, cookies=(
                    _cookie_header(_SESSION_COOKIE, "", max_age=0),
                    _cookie_header(_STATE_COOKIE, "", max_age=0),
                    _cookie_header(_RETURN_COOKIE, "", max_age=0),
                ))
            elif path == _AUTHORIZE_SESSION:
                try:
                    await asyncio.to_thread(self.resolve, scope)
                except PermissionError:
                    await _respond(send, 401)
                else:
                    await _respond(send, 204)
            else:
                clear_state = (
                    _cookie_header(_STATE_COOKIE, "", max_age=0),
                    _cookie_header(_RETURN_COOKIE, "", max_age=0),
                )
                try:
                    session, max_age = await asyncio.to_thread(self._finish, scope, cookies)
                except (PermissionError, TypeError, ValueError, KeyError, RPError) as error:
                    _LOGGER.info("Workspace login failed (%s)", type(error).__name__)
                    await _respond(send, 403, cookies=clear_state, body=b"Workspace sign-in could not be completed.")
                except (OSError, HTTPException) as error:
                    _LOGGER.warning("Workspace provider unavailable (%s)", type(error).__name__)
                    await _respond(send, 503, cookies=clear_state, body=b"Workspace sign-in is temporarily unavailable.")
                else:
                    destination = _safe_return(cookies.get(_RETURN_COOKIE, ""), self.application_path)
                    await _respond(send, 303, location=destination, cookies=(
                        *clear_state, _cookie_header(_SESSION_COOKIE, session, max_age=max_age),
                    ))
        return workspace_routes

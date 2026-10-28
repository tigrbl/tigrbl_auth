from __future__ import annotations

import base64
import hashlib
import secrets
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping
from urllib.parse import parse_qs, urlencode, urlparse


class TestkitError(RuntimeError):
    pass


TestkitError.__test__ = False


class MatrixCellStatus(str, Enum):
    PLANNED = "planned"
    PASSING = "passing"
    FAILING = "failing"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def pkce_s256(verifier: str) -> str:
    if not verifier:
        raise TestkitError("PKCE verifier is required")
    return _b64url(hashlib.sha256(verifier.encode("ascii")).digest())


@dataclass(frozen=True, slots=True)
class SeededTenant:
    tenant_id: str
    issuer: str


@dataclass(frozen=True, slots=True)
class SeededClient:
    client_id: str
    tenant_id: str
    redirect_uri: str
    scopes: tuple[str, ...] = ("openid",)

    def __post_init__(self) -> None:
        object.__setattr__(self, "scopes", tuple(sorted(set(self.scopes))))


@dataclass(frozen=True, slots=True)
class SeededUser:
    subject: str
    tenant_id: str
    username: str


@dataclass(frozen=True, slots=True)
class TestkitSeedSet:
    tenant: SeededTenant
    clients: tuple[SeededClient, ...]
    users: tuple[SeededUser, ...]

    def client(self, client_id: str) -> SeededClient:
        for client in self.clients:
            if client.client_id == client_id:
                return client
        raise TestkitError("seeded client is not configured")

    def user(self, subject: str) -> SeededUser:
        for user in self.users:
            if user.subject == subject:
                return user
        raise TestkitError("seeded user is not configured")


@dataclass(frozen=True, slots=True)
class TestkitProviderRuntimeProfile:
    name: str = "testkit-provider-runtime"
    tenant_id: str = "test"
    routes: tuple[str, ...] = (
        "/authorize",
        "/token",
        "/userinfo",
        "/.well-known/openid-configuration",
        "/.well-known/jwks.json",
        "/rpc",
        "/device_authorization",
        "/tenants",
        "/users",
    )
    feature_flags: Mapping[str, bool] = field(
        default_factory=lambda: {
            "public_oauth": True,
            "public_oidc": True,
            "admin_crud": True,
            "json_rpc": True,
            "device_flow": True,
            "token_exchange": True,
            "dpop": True,
            "tenant_discovery": True,
            "seeded_identities": True,
        }
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "routes", tuple(dict.fromkeys(self.routes)))
        object.__setattr__(self, "feature_flags", dict(self.feature_flags))

    def require_route(self, route: str) -> None:
        if route not in self.routes:
            raise TestkitError(f"testkit provider route is not enabled: {route}")

    def require_feature(self, feature: str) -> None:
        if not self.feature_flags.get(feature, False):
            raise TestkitError(f"testkit provider feature is not enabled: {feature}")


@dataclass(frozen=True, slots=True)
class AuthorizationCode:
    code: str
    client_id: str
    redirect_uri: str
    subject: str
    scope: tuple[str, ...]
    code_challenge: str
    nonce: str


@dataclass(frozen=True, slots=True)
class TokenResponse:
    access_token: str
    id_token: str
    token_type: str
    subject: str
    scope: tuple[str, ...]


class FakeIdentityProvider:
    def __init__(
        self,
        *,
        seeds: TestkitSeedSet,
        profile: TestkitProviderRuntimeProfile | None = None,
    ) -> None:
        self.seeds = seeds
        self.profile = profile or TestkitProviderRuntimeProfile(tenant_id=seeds.tenant.tenant_id)
        self._codes: dict[str, AuthorizationCode] = {}
        self._tokens: dict[str, TokenResponse] = {}

    def discovery_document(self) -> Mapping[str, str]:
        issuer = self.seeds.tenant.issuer.rstrip("/")
        return {
            "issuer": issuer,
            "authorization_endpoint": f"{issuer}/authorize",
            "token_endpoint": f"{issuer}/token",
            "userinfo_endpoint": f"{issuer}/userinfo",
            "jwks_uri": f"{issuer}/.well-known/jwks.json",
            "device_authorization_endpoint": f"{issuer}/device_authorization",
        }

    def jwks(self) -> Mapping[str, object]:
        return {"keys": [{"kid": f"{self.seeds.tenant.tenant_id}-sig-1", "kty": "OKP", "use": "sig"}]}

    def authorize(
        self,
        *,
        client_id: str,
        redirect_uri: str,
        subject: str,
        scope: Iterable[str],
        code_challenge: str,
        nonce: str,
    ) -> AuthorizationCode:
        self.profile.require_route("/authorize")
        client = self.seeds.client(client_id)
        self.seeds.user(subject)
        if redirect_uri != client.redirect_uri:
            raise TestkitError("redirect URI is not registered for seeded client")
        requested_scopes = tuple(sorted(set(scope)))
        if not set(requested_scopes).issubset(set(client.scopes)):
            raise TestkitError("requested scope is not allowed for seeded client")
        code = AuthorizationCode(
            code=f"code_{secrets.token_urlsafe(12)}",
            client_id=client_id,
            redirect_uri=redirect_uri,
            subject=subject,
            scope=requested_scopes,
            code_challenge=code_challenge,
            nonce=nonce,
        )
        self._codes[code.code] = code
        return code

    def token(self, *, code: str, code_verifier: str, client_id: str) -> TokenResponse:
        self.profile.require_route("/token")
        try:
            grant = self._codes[code]
        except KeyError as exc:
            raise TestkitError("authorization code is unknown or already used") from exc
        if grant.client_id != client_id:
            raise TestkitError("authorization code client mismatch")
        if pkce_s256(code_verifier) != grant.code_challenge:
            raise TestkitError("PKCE verifier does not match authorization code")
        self._codes.pop(code)
        token = TokenResponse(
            access_token=f"at_{secrets.token_urlsafe(16)}",
            id_token=f"id_{grant.subject}_{grant.nonce}",
            token_type="Bearer",
            subject=grant.subject,
            scope=grant.scope,
        )
        self._tokens[token.access_token] = token
        return token

    def introspect(self, access_token: str) -> Mapping[str, object]:
        token = self._tokens.get(access_token)
        if token is None:
            return {"active": False}
        return {
            "active": True,
            "iss": self.seeds.tenant.issuer,
            "sub": token.subject,
            "aud": "api://test",
            "scope": " ".join(token.scope),
            "token_type": token.token_type,
        }

    def userinfo(self, access_token: str) -> Mapping[str, str]:
        self.profile.require_route("/userinfo")
        payload = self.introspect(access_token)
        if not payload.get("active"):
            raise TestkitError("userinfo requires an active access token")
        user = self.seeds.user(str(payload["sub"]))
        return {"sub": user.subject, "preferred_username": user.username, "tenant_id": user.tenant_id}


@dataclass(slots=True)
class FakeRelyingParty:
    client: SeededClient
    issuer: str
    code_verifier: str = "testkit-vector-verifier"
    state: str = "testkit-state"
    nonce: str = "testkit-nonce"

    def authorization_url(self) -> str:
        return f"{self.issuer.rstrip('/')}/authorize?{urlencode(self.authorization_params())}"

    def authorization_params(self) -> Mapping[str, str]:
        return {
            "response_type": "code",
            "client_id": self.client.client_id,
            "redirect_uri": self.client.redirect_uri,
            "scope": " ".join(self.client.scopes),
            "state": self.state,
            "nonce": self.nonce,
            "code_challenge": pkce_s256(self.code_verifier),
            "code_challenge_method": "S256",
        }

    def parse_callback(self, callback_url: str) -> Mapping[str, str]:
        parsed = parse_qs(urlparse(callback_url).query)
        code = (parsed.get("code") or [""])[0]
        state = (parsed.get("state") or [""])[0]
        if not code or state != self.state:
            raise TestkitError("RP callback is missing code or has invalid state")
        return {"code": code, "state": state}


@dataclass(slots=True)
class FakeResourceServer:
    idp: FakeIdentityProvider
    audience: str = "api://test"
    required_scopes: tuple[str, ...] = ("openid",)

    def verify(self, authorization: str | None) -> Mapping[str, object]:
        if not authorization:
            raise TestkitError("resource server request is missing authorization")
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise TestkitError("resource server request must use bearer authorization")
        payload = self.idp.introspect(token)
        if not payload.get("active"):
            raise TestkitError("resource server token is inactive")
        scopes = set(str(payload.get("scope", "")).split())
        missing = set(self.required_scopes) - scopes
        if missing:
            raise TestkitError(f"resource server token is missing scopes: {', '.join(sorted(missing))}")
        if payload.get("aud") != self.audience:
            raise TestkitError("resource server audience mismatch")
        return payload


@dataclass(frozen=True, slots=True)
class PackageMatrixCell:
    package: str
    python_version: str
    test_paths: tuple[str, ...]
    cross_cutting: bool = False
    status: MatrixCellStatus = MatrixCellStatus.PLANNED

    def __post_init__(self) -> None:
        object.__setattr__(self, "test_paths", tuple(self.test_paths))
        object.__setattr__(self, "status", MatrixCellStatus(self.status))


class PackageMatrixHarness:
    def __init__(self, *, python_versions: Iterable[str] = ("3.10", "3.11", "3.12", "3.13", "3.14")) -> None:
        self.python_versions = tuple(python_versions)

    def cells_for(self, package: str, *, test_paths: Iterable[str], cross_cutting: bool = False) -> tuple[PackageMatrixCell, ...]:
        paths = tuple(test_paths)
        if not package or not paths:
            raise TestkitError("package matrix cells require package and test paths")
        return tuple(
            PackageMatrixCell(package=package, python_version=version, test_paths=paths, cross_cutting=cross_cutting)
            for version in self.python_versions
        )

    def assert_complete(self, cells: Iterable[PackageMatrixCell], *, package: str) -> None:
        present = {cell.python_version for cell in cells if cell.package == package}
        missing = set(self.python_versions) - present
        if missing:
            raise TestkitError(f"package matrix is missing Python versions: {', '.join(sorted(missing))}")


def default_seed_set() -> TestkitSeedSet:
    return TestkitSeedSet(
        tenant=SeededTenant(tenant_id="test", issuer="https://issuer.example.test"),
        clients=(
            SeededClient(
                client_id="test-rp",
                tenant_id="test",
                redirect_uri="https://rp.example.test/callback",
                scopes=("openid", "profile", "api.read"),
            ),
        ),
        users=(SeededUser(subject="user:123", tenant_id="test", username="alice"),),
    )


def provider_runtime_profile() -> TestkitProviderRuntimeProfile:
    return TestkitProviderRuntimeProfile()


def cross_language_vectors() -> Mapping[str, object]:
    verifier = "testkit-vector-verifier"
    return {
        "pkce_verifier": verifier,
        "pkce_s256": pkce_s256(verifier),
        "state": "testkit-state",
        "nonce": "testkit-nonce",
        "authorization_required_params": (
            "client_id",
            "code_challenge",
            "code_challenge_method",
            "nonce",
            "redirect_uri",
            "response_type",
            "scope",
            "state",
        ),
    }


def build_fake_flow() -> tuple[FakeIdentityProvider, FakeRelyingParty, FakeResourceServer]:
    seeds = default_seed_set()
    idp = FakeIdentityProvider(seeds=seeds)
    rp = FakeRelyingParty(client=seeds.client("test-rp"), issuer=seeds.tenant.issuer)
    rs = FakeResourceServer(idp=idp)
    return idp, rp, rs


__all__ = [
    "AuthorizationCode",
    "FakeIdentityProvider",
    "FakeRelyingParty",
    "FakeResourceServer",
    "MatrixCellStatus",
    "PackageMatrixCell",
    "PackageMatrixHarness",
    "SeededClient",
    "SeededTenant",
    "SeededUser",
    "TestkitError",
    "TestkitProviderRuntimeProfile",
    "TestkitSeedSet",
    "TokenResponse",
    "build_fake_flow",
    "cross_language_vectors",
    "default_seed_set",
    "pkce_s256",
    "provider_runtime_profile",
]

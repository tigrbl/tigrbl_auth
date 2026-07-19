# settings.py

from __future__ import annotations

import os
from typing import Optional

from tigrbl_identity_jose.configuration import configure_jose_provider

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency for clean-room/checkpoint tooling
    def load_dotenv(*_args, **_kwargs):
        return False

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except Exception:  # pragma: no cover - fallback for dependency-light checkpoint tooling
    from pydantic import BaseModel as _BaseModel

    class BaseSettings(_BaseModel):
        model_config = {}

        def model_dump(self, *args, **kwargs):  # pragma: no cover - v1/v2 compatibility shim
            if hasattr(super(), "model_dump"):
                return super().model_dump(*args, **kwargs)
            return self.dict(*args, **kwargs)

    def SettingsConfigDict(**kwargs):
        return kwargs

try:
    from tigrbl.types import Field
except Exception:  # pragma: no cover - dependency-light fallback for governance/checkpoint tooling
    from pydantic import Field

load_dotenv()


def _env_bool(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    text = str(raw).strip()
    if not text:
        return default
    try:
        return int(text)
    except (TypeError, ValueError):
        return default


class Settings(BaseSettings):
    # ------------------------------------------------------------------
    # Storage and runtime infrastructure
    # ------------------------------------------------------------------
    redis_url_env: Optional[str] = Field(default=os.environ.get("REDIS_URL"))
    redis_host: Optional[str] = Field(default=os.environ.get("REDIS_HOST"))
    redis_port: int = Field(default=_env_int("REDIS_PORT", 6379))
    redis_db: int = Field(default=_env_int("REDIS_DB", 0))
    redis_password: Optional[str] = Field(default=os.environ.get("REDIS_PASSWORD"))

    pg_dsn_env: Optional[str] = Field(
        default=os.environ.get("POSTGRES_URL") or os.environ.get("PG_DSN")
    )
    pg_host: Optional[str] = Field(default=os.environ.get("PG_HOST"))
    pg_port: int = Field(default=_env_int("PG_PORT", 5432))
    pg_db: Optional[str] = Field(default=os.environ.get("PG_DB"))
    pg_user: Optional[str] = Field(default=os.environ.get("PG_USER"))
    pg_pass: Optional[str] = Field(default=os.environ.get("PG_PASS"))
    async_fallback_db: Optional[str] = Field(default=os.environ.get("ASYNC_FALLBACK_DB"))

    @property
    def redis_url(self) -> str:
        if self.redis_url_env:
            return self.redis_url_env
        host = self.redis_host or "localhost"
        cred = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{cred}{host}:{self.redis_port}/{self.redis_db}"

    @property
    def pg_dsn(self) -> str:
        if self.pg_dsn_env:
            return self.pg_dsn_env
        if self.pg_host and self.pg_db and self.pg_user:
            return (
                f"postgresql://{self.pg_user}:{self.pg_pass}"
                f"@{self.pg_host}:{self.pg_port}/{self.pg_db}"
            )
        return ""

    @property
    def apg_dsn(self) -> str:
        dsn = self.pg_dsn
        if dsn.startswith("postgresql://"):
            return dsn.replace("postgresql://", "postgresql+asyncpg://", 1)
        if not dsn and self.async_fallback_db:
            return self.async_fallback_db
        return dsn

    # ------------------------------------------------------------------
    # Deployment and operator profile
    # ------------------------------------------------------------------
    deployment_profile: str = Field(
        default=os.environ.get("TIGRBL_AUTH_PROFILE", "baseline"),
        description="Deployment profile: baseline, production, hardening, or fapi2-security.",
    )
    issuer: str = Field(
        default=os.environ.get("AUTHN_ISSUER", "https://authn.example.com"),
        description="Canonical issuer URL for discovery, token, and metadata documents.",
    )
    protected_resource_identifier: str = Field(
        default=os.environ.get(
            "TIGRBL_AUTH_PROTECTED_RESOURCE_IDENTIFIER",
            "https://authn.example.com/resource",
        ),
        description="Protected resource identifier exposed via RFC 9728 metadata.",
    )
    strict_boundary_enforcement: bool = Field(
        default=_env_bool("TIGRBL_AUTH_STRICT_BOUNDARY_ENFORCEMENT", "true"),
        description="Fail closed on boundary, governance, and claims hygiene regressions.",
    )

    # ------------------------------------------------------------------
    # Surface enablement
    # ------------------------------------------------------------------
    surface_public_enabled: bool = Field(
        default=_env_bool("TIGRBL_AUTH_SURFACE_PUBLIC", "true"),
        description="Enable the public auth plane.",
    )
    surface_admin_enabled: bool = Field(
        default=_env_bool("TIGRBL_AUTH_SURFACE_ADMIN", "false"),
        description="Enable table-backed admin/control-plane resources.",
    )
    surface_operator_enabled: bool = Field(
        default=_env_bool("TIGRBL_AUTH_SURFACE_OPERATOR", "true"),
        description="Enable operator CLI and governance surfaces.",
    )
    surface_diagnostics_enabled: bool = Field(
        default=_env_bool("TIGRBL_AUTH_SURFACE_DIAGNOSTICS", "false"),
        description="Enable diagnostics attachment on the composed Tigrbl surface.",
    )
    surface_plugin_mode: str = Field(
        default=os.environ.get("TIGRBL_AUTH_PLUGIN_MODE", "public-only"),
        description="Install profile: public-only, admin-only, mixed, or diagnostics-only.",
    )
    runtime_style: str = Field(
        default=os.environ.get("TIGRBL_AUTH_RUNTIME_STYLE", "standalone"),
        description="Composition mode: plugin installation into an existing Tigrbl app or standalone gateway assembly.",
    )
    active_surface_sets: str = Field(
        default=os.environ.get("TIGRBL_AUTH_ACTIVE_SURFACES", ""),
        description=(
            "Comma-separated installable surface sets: public-rest, admin-rest, "
            "diagnostics."
        ),
    )
    active_protocol_slices: str = Field(
        default=os.environ.get("TIGRBL_AUTH_ACTIVE_PROTOCOL_SLICES", ""),
        description="Comma-separated protocol slices: device, token-exchange, par, jar, rar, dpop, mtls.",
    )
    active_extensions: str = Field(
        default=os.environ.get("TIGRBL_AUTH_ACTIVE_EXTENSIONS", ""),
        description="Comma-separated quarantined extension features: webauthn-passkeys, set, webpush, dns-privacy.",
    )

    # ------------------------------------------------------------------
    # Operational and security controls
    # ------------------------------------------------------------------
    jwt_secret: str = Field(default=os.environ.get("JWT_SECRET", "insecure-dev-secret"))
    admin_api_key: Optional[str] = Field(
        default=os.environ.get("TIGRBL_AUTH_ADMIN_API_KEY"),
        description="Local control-plane API key for generated admin and diagnostics surfaces.",
    )
    admin_api_key_dir: str = Field(
        default=os.environ.get("TIGRBL_AUTH_ADMIN_API_KEY_DIR", "runtime_secrets"),
        description="Directory used for the generated local bootstrap admin API key digest.",
    )
    bootstrap_admin_username: str = Field(
        default=os.environ.get("TIGRBL_AUTH_BOOTSTRAP_ADMIN_USERNAME", "admin"),
        description="Bootstrap super-admin username for first-run initialization.",
    )
    bootstrap_admin_email: str = Field(
        default=os.environ.get("TIGRBL_AUTH_BOOTSTRAP_ADMIN_EMAIL", "admin@example.com"),
        description="Bootstrap super-admin email for first-run initialization.",
    )
    bootstrap_admin_password: Optional[str] = Field(
        default=os.environ.get("TIGRBL_AUTH_BOOTSTRAP_ADMIN_PASSWORD"),
        description="Optional bootstrap super-admin password. If omitted, a local-only password is generated.",
    )
    bootstrap_admin_tenant_slug: str = Field(
        default=os.environ.get("TIGRBL_AUTH_BOOTSTRAP_ADMIN_TENANT_SLUG", "public"),
        description="Tenant slug that owns the bootstrap super-admin identity.",
    )
    bootstrap_admin_force_password_change: bool = Field(
        default=_env_bool("TIGRBL_AUTH_BOOTSTRAP_ADMIN_FORCE_PASSWORD_CHANGE", "true"),
        description="Require the bootstrap super-admin to change their password after first login.",
    )
    admin_password_reset_debug_disclosure: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ADMIN_PASSWORD_RESET_DEBUG_DISCLOSURE", "true"),
        description="Allow local development reset flows to disclose a one-time reset token in the response when no mail channel exists.",
    )
    log_level: str = Field(default=os.environ.get("LOG_LEVEL", "INFO"))
    id_token_encryption_key: str = Field(
        default=os.environ.get("TIGRBL_AUTH_ID_TOKEN_ENC_KEY", "0" * 32),
        description="Symmetric key for ID Token encryption",
    )
    enable_id_token_encryption: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_ID_TOKEN_ENCRYPTION"),
        description="Encrypt ID Tokens using JWE when enabled",
    )
    require_tls: bool = Field(
        default=_env_bool("TIGRBL_AUTH_REQUIRE_TLS", "true"),
        description="Require HTTPS for all incoming requests",
    )
    jwt_signing_alg: str = Field(
        default=os.environ.get("TIGRBL_AUTH_JWT_SIGNING_ALG", "EdDSA"),
        description="JWT signing algorithm selector. EdDSA is the default; ML-DSA-65 opts into the PQC JOSE profile.",
    )
    enable_pqc_jose: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_PQC_JOSE"),
        description="Advertise and accept the ML-DSA-65 post-quantum JOSE profile when enabled.",
    )

    # ------------------------------------------------------------------
    # Baseline RFC / OIDC flags
    # ------------------------------------------------------------------
    enable_rfc6749: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC6749", "true"))
    enable_rfc6750: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC6750", "true"))
    enable_rfc6750_query: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_RFC6750_QUERY"),
        description="Allow access_token as URI query parameter per RFC 6750 §2.3",
    )
    enable_rfc6750_form: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_RFC6750_FORM"),
        description="Allow access_token in form bodies per RFC 6750 §2.2",
    )
    enable_rfc7636: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7636", "true"))
    enable_rfc8414: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8414", "true"))
    enable_rfc8615: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8615", "true"))
    enable_rfc7515: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7515", "true"))
    enable_rfc7516: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7516", "true"))
    enable_rfc7517: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7517", "true"))
    enable_rfc7518: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7518", "true"))
    enable_rfc7519: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7519", "true"))
    enable_rfc7520: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7520", "true"))
    enable_rfc7638: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7638", "true"))
    enable_rfc8037: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8037", "true"))
    enable_rfc8176: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8176", "true"))
    enable_rfc8725: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8725", "true"))

    # ------------------------------------------------------------------
    # Production target flags
    # ------------------------------------------------------------------
    enable_rfc7009: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7009", "true"))
    enable_rfc7521: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7521", "true"))
    enable_rfc7523: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7523", "true"))
    enable_rfc7591: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7591", "true"))
    enable_rfc7592: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7592", "true"))
    enable_rfc7662: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7662", "true"))
    enforce_rfc8252: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENFORCE_RFC8252", "true"),
        description="Validate redirect URIs according to RFC 8252",
    )
    enable_rfc8252: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8252", "true"),
        description="Track RFC 8252 native-app support in the flag registry.",
    )
    enable_rfc9068: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC9068", "false"))
    enable_rfc9207: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC9207", "true"))
    enable_rfc9728: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_RFC9728", "true"),
        description="Expose protected resource metadata per RFC 9728.",
    )
    enable_oidc_core: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_OIDC_CORE", "true"))
    enable_oidc_discovery: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_OIDC_DISCOVERY", "true"))
    enable_oidc_userinfo: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_OIDC_USERINFO", "true"))
    enable_oidc_session_management: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_OIDC_SESSION_MANAGEMENT", "true"),
        description="Enable the browser-session plane and OIDC session-state semantics.",
    )
    enable_oidc_rp_initiated_logout: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_OIDC_RP_INITIATED_LOGOUT", "true"))

    # ------------------------------------------------------------------
    # Hardening / advanced target flags
    # ------------------------------------------------------------------
    enable_rfc8628: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8628", "true"))
    enable_rfc8693: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8693", "true"))
    rfc8707_enabled: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8707", "true"))
    enable_rfc8705: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8705", "false"))
    enable_rfc8707: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8707", "true"))
    enable_rfc9101: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC9101", "true"))
    enable_rfc9126: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC9126", "true"))
    enable_rfc9396: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC9396", "true"))
    enable_rfc9449: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC9449", "true"))
    enable_rfc9700: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_RFC9700", "true"),
        description="Track RFC 9700 security BCP alignment posture.",
    )
    enable_oidc_frontchannel_logout: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_OIDC_FRONTCHANNEL_LOGOUT", "true"),
        description="Enable front-channel logout planning and discovery metadata.",
    )
    enable_oidc_backchannel_logout: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_OIDC_BACKCHANNEL_LOGOUT", "true"),
        description="Enable back-channel logout planning and token fanout semantics.",
    )

    # ------------------------------------------------------------------
    # Browser session and cookie controls
    # ------------------------------------------------------------------
    session_cookie_name: str = Field(
        default=os.environ.get("TIGRBL_AUTH_SESSION_COOKIE_NAME", "sid"),
        description="Opaque browser-session cookie name.",
    )
    session_cookie_path: str = Field(
        default=os.environ.get("TIGRBL_AUTH_SESSION_COOKIE_PATH", "/"),
        description="Cookie path for the browser-session cookie.",
    )
    session_cookie_domain: Optional[str] = Field(
        default=os.environ.get("TIGRBL_AUTH_SESSION_COOKIE_DOMAIN"),
        description="Optional cookie domain override for browser-session cookies.",
    )
    session_cookie_samesite: str = Field(
        default=os.environ.get("TIGRBL_AUTH_SESSION_COOKIE_SAMESITE", "lax"),
        description="Default SameSite policy when cross-site browser flows are not enabled.",
    )
    session_cookie_max_age_seconds: int = Field(
        default=int(os.environ.get("TIGRBL_AUTH_SESSION_COOKIE_MAX_AGE_SECONDS", "3600")),
        description="Maximum age for the opaque browser-session cookie.",
    )
    session_cookie_renewal_seconds: int = Field(
        default=int(os.environ.get("TIGRBL_AUTH_SESSION_COOKIE_RENEWAL_SECONDS", "900")),
        description="Rotate browser-session cookie secrets when the session cookie is older than this threshold.",
    )
    session_cookie_cross_site: bool = Field(
        default=_env_bool("TIGRBL_AUTH_SESSION_COOKIE_CROSS_SITE"),
        description="Force SameSite=None for browser-session cookies to support cross-site logout interoperability.",
    )
    session_cookie_force_secure: bool = Field(
        default=_env_bool("TIGRBL_AUTH_SESSION_COOKIE_FORCE_SECURE", "true"),
        description="Always set Secure on the browser-session cookie regardless of inferred scheme.",
    )

    # ------------------------------------------------------------------
    # Alignment only
    # ------------------------------------------------------------------
    oauth21_alignment_mode: str = Field(
        default=os.environ.get("TIGRBL_AUTH_OAUTH21_ALIGNMENT_MODE", "tracked"),
        description="OAuth 2.1 alignment profile mode. This is never an RFC compliance claim.",
    )

    # ------------------------------------------------------------------
    # Extension and quarantined flags
    # ------------------------------------------------------------------
    enable_rfc7800: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC7800"))
    enable_rfc8417: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8417"))
    enable_rfc8291: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8291"))
    enable_rfc8812: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8812"))
    enable_webauthn: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_WEBAUTHN"))
    webauthn_version: str = Field(default=os.environ.get("TIGRBL_AUTH_WEBAUTHN_VERSION", "level-2"))
    webauthn_rp_id: str | None = Field(default=os.environ.get("TIGRBL_AUTH_WEBAUTHN_RP_ID"))
    webauthn_allowed_origins: str = Field(default=os.environ.get("TIGRBL_AUTH_WEBAUTHN_ALLOWED_ORIGINS", ""))
    webauthn_user_verification: str = Field(default=os.environ.get("TIGRBL_AUTH_WEBAUTHN_USER_VERIFICATION", "preferred"))
    webauthn_resident_key: str = Field(default=os.environ.get("TIGRBL_AUTH_WEBAUTHN_RESIDENT_KEY", "preferred"))
    webauthn_attestation: str = Field(default=os.environ.get("TIGRBL_AUTH_WEBAUTHN_ATTESTATION", "none"))
    webauthn_allowed_algorithms: str = Field(default=os.environ.get("TIGRBL_AUTH_WEBAUTHN_ALLOWED_ALGORITHMS", "-7,-257"))
    enable_fido2_server_profile: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_FIDO2_SERVER_PROFILE"))
    enable_fido_metadata_service: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_FIDO_METADATA_SERVICE"))
    enable_spiffe_x509_svid: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_SPIFFE_X509_SVID"))
    enable_spiffe_jwt_svid: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_SPIFFE_JWT_SVID"))
    enable_spiffe_workload_api: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_SPIFFE_WORKLOAD_API"))
    enable_spiffe_broker_api: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_SPIFFE_BROKER_API"))
    enable_wimse_wit: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_WIMSE_WIT"))
    enable_wimse_wpt: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_WIMSE_WPT"))
    enable_spiffe_wit_svid: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_SPIFFE_WIT_SVID"))
    enable_cwt_svid_extension: bool = Field(default=_env_bool("TIGRBL_AUTH_ENABLE_CWT_SVID_EXTENSION"))
    spiffe_workload_api_version: str = Field(default=os.environ.get("TIGRBL_AUTH_SPIFFE_WORKLOAD_API_VERSION", "SPIFFE-Workload-API-1.0"))
    spiffe_broker_api_version: str = Field(default=os.environ.get("TIGRBL_AUTH_SPIFFE_BROKER_API_VERSION", "SPIFFE-v1.15.1-Broker-API"))
    wimse_wit_version: str = Field(default=os.environ.get("TIGRBL_AUTH_WIMSE_WIT_VERSION", "draft-ietf-wimse-workload-creds-02"))
    wimse_wpt_version: str = Field(default=os.environ.get("TIGRBL_AUTH_WIMSE_WPT_VERSION", "draft-ietf-wimse-wpt-01"))
    spiffe_wit_svid_version: str = Field(default=os.environ.get("TIGRBL_AUTH_SPIFFE_WIT_SVID_VERSION", "SPIFFE-v1.15.1-WIT-SVID"))
    cwt_svid_extension_version: str = Field(default=os.environ.get("TIGRBL_AUTH_CWT_SVID_EXTENSION_VERSION", "TIGRBL-CWT-SVID-EXPERIMENT-1"))
    spiffe_workload_endpoint: str | None = Field(default=os.environ.get("TIGRBL_AUTH_SPIFFE_WORKLOAD_ENDPOINT"))
    spiffe_broker_endpoint: str | None = Field(default=os.environ.get("TIGRBL_AUTH_SPIFFE_BROKER_ENDPOINT"))
    spiffe_broker_authorized_principals: str = Field(default=os.environ.get("TIGRBL_AUTH_SPIFFE_BROKER_AUTHORIZED_PRINCIPALS", ""))
    enable_rfc8932: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8932"),
        description="Quarantined extension flag for RFC 8932 DNS privacy work; not part of the certified auth-core boundary.",
    )

    # ------------------------------------------------------------------
    # Legacy migration history only
    # ------------------------------------------------------------------
    enable_rfc8523: bool = Field(
        default=_env_bool("TIGRBL_AUTH_ENABLE_RFC8523"),
        description="Legacy mislabeled migration flag retained for history only. Certification claims map JWT client authentication to RFC 7523.",
    )

    @property
    def enable_dpop(self) -> bool:
        return self.enable_rfc9449

    model_config = SettingsConfigDict(env_file=None, env_ignore_empty=True)


_existing = globals().get("settings")
if _existing is None:
    settings = Settings()
else:
    _new = Settings()
    for field, value in _new.model_dump().items():
        setattr(_existing, field, value)
    settings = _existing

configure_jose_provider(settings)

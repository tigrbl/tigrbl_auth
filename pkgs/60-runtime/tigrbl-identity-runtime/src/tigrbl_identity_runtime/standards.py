from dataclasses import asdict, dataclass
from importlib import import_module


@dataclass(frozen=True, slots=True)
class RuntimeStandard:
    family: str
    version: str
    status: str
    published: str


def _entry(family: str, module_name: str) -> RuntimeStandard:
    version = getattr(import_module(module_name), "CURRENT_VERSION")
    return RuntimeStandard(
        family,
        str(getattr(version, "identifier")),
        str(getattr(version, "status")),
        str(getattr(version, "published")),
    )


STANDARD_OWNER_MODULES = (
    ("jwt", "tigrbl_auth_protocol_jwt"),
    ("oauth", "tigrbl_auth_protocol_oauth"),
    ("oidc", "tigrbl_auth_protocol_oidc"),
    ("oid4vci", "tigrbl_auth_protocol_oid4vci"),
    ("oid4vp", "tigrbl_auth_protocol_oid4vp"),
    ("haip", "tigrbl_auth_profile_haip"),
    ("authzen", "tigrbl_auth_protocol_authzen"),
    ("gnap", "tigrbl_auth_protocol_gnap"),
    ("set", "tigrbl_security_event_protocol_set"),
    ("eat", "tigrbl_attestation_protocol_eat"),
    ("sd-jwt-vc", "tigrbl_credential_profile_sd_jwt_vc"),
)


def standards_manifest() -> tuple[dict[str, str], ...]:
    return tuple(
        asdict(_entry(family, module)) for family, module in STANDARD_OWNER_MODULES
    )


def standard_version(family: str) -> RuntimeStandard:
    for registered_family, module in STANDARD_OWNER_MODULES:
        if registered_family == family:
            return _entry(family, module)
    raise KeyError(family)


__all__ = [
    "STANDARD_OWNER_MODULES",
    "RuntimeStandard",
    "standard_version",
    "standards_manifest",
]

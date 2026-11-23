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
    ("jwt", "tba_protocol_jwt"),
    ("oauth", "tba_protocol_oauth"),
    ("oidc", "tba_protocol_oidc"),
    ("oid4vci", "tba_protocol_oid4vci"),
    ("oid4vp", "tba_protocol_oid4vp"),
    ("haip", "tba_profile_haip"),
    ("authzen", "tba_protocol_authzen"),
    ("gnap", "tba_protocol_gnap"),
    ("set", "tba_protocol_security_event_set"),
    ("eat", "tba_protocol_attestation_eat"),
    ("sd-jwt-vc", "tba_profile_credential_sd_jwt_vc"),
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

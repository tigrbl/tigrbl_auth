from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_configuration
from .profile import HAIP_CREDENTIAL_FORMATS, HaipConfiguration, configure_haip
from .versions import CURRENT_VERSION, VERSION_HISTORY, HaipVersion, select_version

__all__ = [
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "HAIP_CREDENTIAL_FORMATS",
    "VERSION_HISTORY",
    "HaipConfiguration",
    "HaipVersion",
    "configure_haip",
    "migrate_configuration",
    "select_version",
    "supports",
]


from tigrbl_identity_contracts.protocol_processing import build_protocol_capability_report as _build_protocol_capability_report

def capability_report() -> dict[str, object]:
    return _build_protocol_capability_report(
        protocol='haip',
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=('tests/unit/test_versioned_haip_profile.py',),
        extra_requirements=tuple(globals().get('CAPABILITY_REQUIREMENTS', ())),
    )

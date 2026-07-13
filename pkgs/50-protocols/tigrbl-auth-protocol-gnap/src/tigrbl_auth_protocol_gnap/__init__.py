from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_request
from .protocol import GnapRequest, parse_gnap_request
from .versions import CURRENT_VERSION, VERSION_HISTORY, GnapVersion, select_version

__all__ = [
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "VERSION_HISTORY",
    "GnapRequest",
    "GnapVersion",
    "migrate_request",
    "parse_gnap_request",
    "select_version",
    "supports",
]


from tigrbl_identity_contracts.protocol_processing import build_protocol_capability_report as _build_protocol_capability_report

def capability_report() -> dict[str, object]:
    return _build_protocol_capability_report(
        protocol='gnap',
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=('tests/unit/test_versioned_gnap_protocol.py',),
        extra_requirements=tuple(globals().get('CAPABILITY_REQUIREMENTS', ())),
    )

from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_request
from .protocol import Oid4vpProtocol
from .versions import CURRENT_VERSION, VERSION_HISTORY, Oid4vpVersion, select_version
from .capability_requirements import CAPABILITY_REQUIREMENTS

__all__ = [
    "CURRENT_VERSION",
    "CAPABILITY_REQUIREMENTS",
    "FEATURES_BY_VERSION",
    "VERSION_HISTORY",
    "Oid4vpProtocol",
    "Oid4vpVersion",
    "migrate_request",
    "select_version",
    "supports",
]


from tigrbl_identity_contracts.protocol_processing import build_protocol_capability_report as _build_protocol_capability_report

def capability_report() -> dict[str, object]:
    return _build_protocol_capability_report(
        protocol='oid4vp',
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=('tests/unit/test_versioned_oid4vc_authzen_protocols.py',),
        extra_requirements=tuple(globals().get('CAPABILITY_REQUIREMENTS', ())),
    )

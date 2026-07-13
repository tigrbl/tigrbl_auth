from .features import FEATURES_BY_VERSION, supports
from .migrations import migrate_evaluation
from .protocol import AuthzenProtocol
from .versions import AuthzenVersion, CURRENT_VERSION, VERSION_HISTORY, select_version

__all__ = [
    "AuthzenProtocol",
    "AuthzenVersion",
    "CURRENT_VERSION",
    "FEATURES_BY_VERSION",
    "VERSION_HISTORY",
    "migrate_evaluation",
    "select_version",
    "supports",
]


from tigrbl_identity_contracts.protocol_processing import build_protocol_capability_report as _build_protocol_capability_report

def capability_report() -> dict[str, object]:
    return _build_protocol_capability_report(
        protocol='authzen',
        revision=CURRENT_VERSION.identifier,
        features=tuple(FEATURES_BY_VERSION[CURRENT_VERSION.identifier]),
        evidence_links=('tests/unit/test_versioned_oid4vc_authzen_protocols.py',),
        extra_requirements=tuple(globals().get('CAPABILITY_REQUIREMENTS', ())),
    )

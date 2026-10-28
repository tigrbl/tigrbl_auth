"""Owned mapped-table inventory."""

from .authz_verification_report import AuthzVerificationReport
from .control_correctness_report import ControlCorrectnessReport
from .plugin_descriptor import PluginDescriptorRecord
from .plugin_lifecycle_event import PluginLifecycleEventRecord
from .release_attestation_event import ReleaseAttestationEvent
from .release_authorization_state import ReleaseAuthorizationState
from .release_capability_record import ReleaseCapabilityRecord
from .release_posture import ReleasePosture
from .release_security_posture import ReleaseSecurityPosture
from .resource_server_contract import ResourceServerContract
from .runtime_qualification import RuntimeQualificationRecord
from .sdk_package import SDKPackageRecord

TABLE_MODELS = (
    SDKPackageRecord,
    PluginDescriptorRecord,
    PluginLifecycleEventRecord,
    ReleaseCapabilityRecord,
    ReleaseAuthorizationState,
    RuntimeQualificationRecord,
    ReleaseSecurityPosture,
    ReleasePosture,
    ReleaseAttestationEvent,
    ControlCorrectnessReport,
    AuthzVerificationReport,
    ResourceServerContract,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]

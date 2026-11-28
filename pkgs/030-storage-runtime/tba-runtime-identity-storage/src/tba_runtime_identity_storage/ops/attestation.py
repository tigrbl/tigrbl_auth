"""Compatibility facade for tba_durability_attestation operations."""

from tba_durability_attestation.operations.attestation import *
from tba_durability_attestation.operations.attestation import (
    make_attestation_appraisal_recorder as _make_attestation_appraisal_recorder,
)


def make_attestation_appraisal_recorder(**kwargs):
    """Preserve patchable legacy recorder bindings during migration."""

    return _make_attestation_appraisal_recorder(
        evidence_recorder=record_attestation_evidence,
        result_recorder=record_attestation_result,
        **kwargs,
    )

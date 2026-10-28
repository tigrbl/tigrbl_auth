BASELINE_ATTESTATION_FORMATS = ("none", "packed", "fido-u2f")
CERTIFICATION_ATTESTATION_FORMATS = BASELINE_ATTESTATION_FORMATS + (
    "tpm",
    "android-key",
    "android-safetynet",
    "apple",
)

__all__ = ["BASELINE_ATTESTATION_FORMATS", "CERTIFICATION_ATTESTATION_FORMATS"]

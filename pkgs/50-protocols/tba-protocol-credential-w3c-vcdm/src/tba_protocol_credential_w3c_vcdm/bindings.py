"""Capability bindings required by the W3C VCDM protocol owner."""

CAPABILITY_REQUIREMENTS = (
    "credential.issue.verifiable-credential",
    "credential.verify.verifiable-credential",
    "presentation.verify.verifiable-presentation",
)

__all__ = ["CAPABILITY_REQUIREMENTS"]

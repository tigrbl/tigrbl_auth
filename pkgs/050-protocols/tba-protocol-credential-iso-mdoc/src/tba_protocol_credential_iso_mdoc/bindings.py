"""Capability bindings required by the ISO mdoc protocol owner."""

CAPABILITY_REQUIREMENTS = (
    "credential.issue.mdoc",
    "credential.verify.mdoc",
    "presentation.verify.mdoc",
)

__all__ = ["CAPABILITY_REQUIREMENTS"]

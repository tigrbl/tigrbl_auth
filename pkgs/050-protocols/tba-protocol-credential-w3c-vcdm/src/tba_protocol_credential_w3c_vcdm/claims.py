"""W3C VCDM credential-subject claim material."""

from collections.abc import Mapping


def credential_subject_claims(value: Mapping[str, object]) -> dict[str, object]:
    """Normalize credential-subject claims without assigning assurance."""

    return {str(name): claim for name, claim in value.items()}


__all__ = ["credential_subject_claims"]

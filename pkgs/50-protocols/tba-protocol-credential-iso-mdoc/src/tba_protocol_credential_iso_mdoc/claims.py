"""ISO mdoc namespace claim material."""

from collections.abc import Mapping


def namespace_claims(value: Mapping[str, object]) -> dict[str, object]:
    """Normalize one namespace without assigning issuer trust."""

    return {str(name): claim for name, claim in value.items()}


__all__ = ["namespace_claims"]

from .versions import CURRENT_VERSION, Fido2ServerRevision


def compatible_revisions(
    source: Fido2ServerRevision, target: Fido2ServerRevision = CURRENT_VERSION
) -> bool:
    return source.webauthn_revision == target.webauthn_revision


__all__ = ["compatible_revisions"]

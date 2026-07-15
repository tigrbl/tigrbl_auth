"""COSE algorithm identifiers used by detached public-key signatures."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CoseAlgorithm:
    identifier: int
    name: str
    key_type: str
    hash_name: str | None = None


COSE_ALGORITHMS = {
    -7: CoseAlgorithm(-7, "ES256", "EC2", "sha256"),
    -35: CoseAlgorithm(-35, "ES384", "EC2", "sha384"),
    -36: CoseAlgorithm(-36, "ES512", "EC2", "sha512"),
    -47: CoseAlgorithm(-47, "ES256K", "EC2", "sha256"),
    -8: CoseAlgorithm(-8, "EdDSA", "OKP"),
    -37: CoseAlgorithm(-37, "PS256", "RSA", "sha256"),
    -38: CoseAlgorithm(-38, "PS384", "RSA", "sha384"),
    -39: CoseAlgorithm(-39, "PS512", "RSA", "sha512"),
    -257: CoseAlgorithm(-257, "RS256", "RSA", "sha256"),
    -258: CoseAlgorithm(-258, "RS384", "RSA", "sha384"),
    -259: CoseAlgorithm(-259, "RS512", "RSA", "sha512"),
}


def resolve_cose_algorithm(identifier: int) -> CoseAlgorithm:
    if isinstance(identifier, bool) or not isinstance(identifier, int):
        raise TypeError("COSE algorithm identifier must be an integer")
    try:
        return COSE_ALGORITHMS[identifier]
    except KeyError as exc:
        raise ValueError(f"unsupported COSE algorithm: {identifier}") from exc


__all__ = ["COSE_ALGORITHMS", "CoseAlgorithm", "resolve_cose_algorithm"]

"""Deterministic COSE algorithm registry."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CoseAlgorithm:
    identifier: int
    name: str
    key_type: str
    hash_name: str | None


COSE_ALGORITHMS = {
    -7: CoseAlgorithm(-7, "ES256", "EC2", "sha256"),
    -8: CoseAlgorithm(-8, "EdDSA", "OKP", None),
    -35: CoseAlgorithm(-35, "ES384", "EC2", "sha384"),
    -36: CoseAlgorithm(-36, "ES512", "EC2", "sha512"),
    -37: CoseAlgorithm(-37, "PS256", "RSA", "sha256"),
    -38: CoseAlgorithm(-38, "PS384", "RSA", "sha384"),
    -39: CoseAlgorithm(-39, "PS512", "RSA", "sha512"),
    -257: CoseAlgorithm(-257, "RS256", "RSA", "sha256"),
    -258: CoseAlgorithm(-258, "RS384", "RSA", "sha384"),
    -259: CoseAlgorithm(-259, "RS512", "RSA", "sha512"),
}


def resolve_cose_algorithm(identifier: int) -> CoseAlgorithm:
    try:
        return COSE_ALGORITHMS[int(identifier)]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"unsupported COSE algorithm: {identifier!r}") from exc

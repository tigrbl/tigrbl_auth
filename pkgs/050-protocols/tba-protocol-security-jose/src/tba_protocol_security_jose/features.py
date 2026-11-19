"""Versioned JOSE feature selection."""

from dataclasses import dataclass

from .versions import CURRENT_VERSION


@dataclass(frozen=True, slots=True)
class JoseFeatures:
    jws: bool = True
    jwe: bool = True
    jwk: bool = True
    jwt: bool = True
    proof_of_possession: bool = True
    webauthn_algorithms: bool = True


FEATURES_BY_VERSION = {
    "jose-suite-2015": frozenset({"jws", "jwe", "jwk", "jwt"}),
    "jose-suite-2020-bcp": frozenset(
        {
            "jws",
            "jwe",
            "jwk",
            "jwt",
            "proof-of-possession",
            "jwk-thumbprints",
            "unencoded-jws-payload",
            "cfrg-elliptic-curves",
            "jwt-bcp",
            "webauthn-algorithms",
        }
    ),
}


def supports(feature: str, version: str = CURRENT_VERSION.identifier) -> bool:
    try:
        return feature in FEATURES_BY_VERSION[version]
    except KeyError as exc:
        raise ValueError(f"unsupported JOSE suite revision: {version}") from exc


__all__ = ["FEATURES_BY_VERSION", "JoseFeatures", "supports"]

"""Versioned JOSE feature selection."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JoseFeatures:
    jws: bool = True
    jwe: bool = True
    jwk: bool = True
    jwt: bool = True
    proof_of_possession: bool = True
    webauthn_algorithms: bool = True

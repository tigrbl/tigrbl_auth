"""Published specifications composing the JOSE protocol family."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JoseSpecification:
    identifier: str
    title: str
    status: str = "rfc"


JOSE_SPECIFICATIONS = (
    JoseSpecification("RFC7515", "JSON Web Signature"),
    JoseSpecification("RFC7516", "JSON Web Encryption"),
    JoseSpecification("RFC7517", "JSON Web Key"),
    JoseSpecification("RFC7518", "JSON Web Algorithms"),
    JoseSpecification("RFC7519", "JSON Web Token"),
    JoseSpecification("RFC7520", "JOSE Cookbook"),
    JoseSpecification("RFC7638", "JSON Web Key Thumbprint"),
    JoseSpecification("RFC7797", "JWS Unencoded Payload Option"),
    JoseSpecification("RFC7800", "Proof-of-Possession Key Semantics"),
    JoseSpecification("RFC8037", "CFRG Elliptic Curve Algorithms"),
    JoseSpecification("RFC8176", "Authentication Method Reference Values"),
    JoseSpecification("RFC8725", "JSON Web Token Best Current Practices"),
    JoseSpecification(
        "RFC8812", "CBOR Object Signing and Encryption Algorithms for WebAuthn"
    ),
)

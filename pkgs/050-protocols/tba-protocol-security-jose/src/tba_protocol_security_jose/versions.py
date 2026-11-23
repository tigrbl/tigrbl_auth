"""Published specifications and suite revisions composing JOSE."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JoseSpecification:
    identifier: str
    title: str
    status: str = "rfc"
    published: str = ""


JOSE_SPECIFICATIONS = (
    JoseSpecification("RFC7515", "JSON Web Signature", published="2015-05"),
    JoseSpecification("RFC7516", "JSON Web Encryption", published="2015-05"),
    JoseSpecification("RFC7517", "JSON Web Key", published="2015-05"),
    JoseSpecification("RFC7518", "JSON Web Algorithms", published="2015-05"),
    JoseSpecification("RFC7519", "JSON Web Token", published="2015-05"),
    JoseSpecification("RFC7520", "JOSE Cookbook", published="2015-05"),
    JoseSpecification("RFC7638", "JSON Web Key Thumbprint", published="2015-09"),
    JoseSpecification("RFC7797", "JWS Unencoded Payload Option", published="2016-02"),
    JoseSpecification(
        "RFC7800", "Proof-of-Possession Key Semantics", published="2016-04"
    ),
    JoseSpecification("RFC8037", "CFRG Elliptic Curve Algorithms", published="2017-01"),
    JoseSpecification(
        "RFC8176", "Authentication Method Reference Values", published="2017-06"
    ),
    JoseSpecification(
        "RFC8725", "JSON Web Token Best Current Practices", published="2020-02"
    ),
    JoseSpecification(
        "RFC8812",
        "CBOR Object Signing and Encryption Algorithms for WebAuthn",
        published="2020-01",
    ),
)


@dataclass(frozen=True, slots=True)
class JoseVersion:
    """A versioned Tigrbl composition of published JOSE specifications."""

    identifier: str
    status: str
    published: str
    specification_ids: tuple[str, ...]


VERSION_HISTORY = (
    JoseVersion(
        "jose-suite-2015",
        "superseded-suite-profile",
        "2015-05",
        ("RFC7515", "RFC7516", "RFC7517", "RFC7518", "RFC7519"),
    ),
    JoseVersion(
        "jose-suite-2020-bcp",
        "current-suite-profile",
        "2020-02",
        tuple(spec.identifier for spec in JOSE_SPECIFICATIONS),
    ),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = CURRENT_VERSION.identifier) -> JoseVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported JOSE suite revision: {identifier}")


__all__ = [
    "CURRENT_VERSION",
    "JOSE_SPECIFICATIONS",
    "VERSION_HISTORY",
    "JoseSpecification",
    "JoseVersion",
    "select_version",
]

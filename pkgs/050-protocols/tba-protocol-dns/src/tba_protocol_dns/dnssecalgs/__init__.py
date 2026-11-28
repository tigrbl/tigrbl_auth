"""Registry of DNSSEC signing algorithms, including private-use algorithms."""

from tba_primitives_dns_name.name import Name, from_text, from_wire

from . import dsa, ecdsa, eddsa, mldsa, rsa
from .base import (
    GenericPrivateKey as GenericPrivateKey,
    GenericPublicKey as GenericPublicKey,
)

AlgorithmPrefix = bytes | Name | None
algorithms: dict[tuple[int, AlgorithmPrefix], type[GenericPrivateKey]] = {
    (cls.public_cls.algorithm, None): cls
    for module in (rsa, dsa, ecdsa, eddsa, mldsa)
    for name, cls in vars(module).items()
    if name.startswith("Private")
}


def get_algorithm_cls(algorithm, prefix=None):
    """Return the registered private key class for an algorithm and prefix."""
    from ..dnssec import UnsupportedAlgorithm, algorithm_from_text

    number = algorithm_from_text(algorithm)
    try:
        return algorithms[number, prefix]
    except KeyError as exc:
        raise UnsupportedAlgorithm(
            f"unsupported DNSSEC key algorithm {algorithm}"
        ) from exc


def get_algorithm_cls_from_dnskey(dnskey):
    """Look up the algorithm implementation identified by a DNSKEY."""
    from ..dnssec import Algorithm, UnsupportedAlgorithm

    prefix = None
    if dnskey.algorithm == Algorithm.PRIVATEDNS:
        prefix, _ = from_wire(dnskey.key)
    elif dnskey.algorithm == Algorithm.PRIVATEOID:
        if not dnskey.key or len(dnskey.key) <= dnskey.key[0]:
            raise UnsupportedAlgorithm("invalid PRIVATEOID DNSKEY prefix")
        prefix = dnskey.key[: dnskey.key[0] + 1]
    return get_algorithm_cls(dnskey.algorithm, prefix)


def register_algorithm_cls(algorithm, algorithm_cls, name=None, oid=None):
    """Register a private key implementation and its optional private-use prefix."""
    from ..dnssec import Algorithm, algorithm_from_text

    if not issubclass(algorithm_cls, GenericPrivateKey):
        raise TypeError("invalid DNSSEC algorithm class")
    number = algorithm_from_text(algorithm)
    prefix = None
    if number == Algorithm.PRIVATEDNS:
        if name is None:
            raise ValueError("PRIVATEDNS requires a name")
        prefix = from_text(name) if isinstance(name, str) else name
    elif number == Algorithm.PRIVATEOID:
        if oid is None:
            raise ValueError("PRIVATEOID requires an OID")
        prefix = bytes((len(oid),)) + oid
    elif name or oid:
        raise ValueError("DNS names and OIDs require a private-use algorithm")
    algorithms[number, prefix] = algorithm_cls

from datetime import datetime, timezone
from math import isfinite

from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_concrete_jwt import decode_jwt_unverified
from tba_contracts_security_trust import (
    CertificateArtifact,
    CertificatePathValidationRequest,
)
from tba_provider_jose_cryptography.public_jws import verify_public_jws


from .spiffe_id import validate_spiffe_id
from .x509_svid import validate_x509_svid


_SVID_ALGORITHMS = frozenset(
    {f"{kind}{bits}" for kind in ("ES", "RS", "PS") for bits in (256, 384, 512)}
)


def verify_x509_svid(chain, *, validators_by_domain, expected_identity=None, now=None):
    leaf, *intermediates = chain
    certificate = parse_x509_certificate(leaf)
    usage = certificate.key_usage
    constraints = certificate.basic_constraints
    if usage is None or constraints is None or usage.key_cert_sign or usage.crl_sign:
        raise ValueError("invalid X.509-SVID leaf extensions")
    subject = validate_x509_svid(
        uri_sans=certificate.uri_sans,
        dns_sans=(),
        key_usage_digital_signature=usage.digital_signature,
        basic_constraints_ca=constraints.ca,
    )
    domain, path = validate_spiffe_id(subject)
    if not path or (expected_identity is not None and subject != expected_identity):
        raise ValueError("unexpected X.509-SVID workload identity")
    now = datetime.now(timezone.utc) if now is None else now
    if not certificate.not_before <= now <= certificate.not_after:
        raise ValueError("X.509-SVID certificate is outside its validity period")
    validator = validators_by_domain.get(domain)
    if validator is None:
        raise ValueError("no X.509-SVID path validator for the trust domain")
    result = validator.validate(
        CertificatePathValidationRequest(
            CertificateArtifact(certificate.der, "x509-svid"),
            tuple(intermediates),
            now,
        )
    )
    if not result.valid or result.indeterminate or result.profile != "x509-svid":
        raise ValueError("X.509-SVID certificate path was not verified")
    return subject


def verify_jwt_svid(serialized, *, expected_audience, keys_by_domain, now):
    token = decode_jwt_unverified(serialized)
    headers = token.jws.protected_headers
    if headers.keys() - {"alg", "kid", "typ"} or headers.get("typ", "JWT") not in (
        "JWT",
        "JOSE",
    ):
        raise ValueError("invalid JWT-SVID protected headers")
    audience = token.claims.get("aud")
    values = [audience] if isinstance(audience, str) else audience
    if (
        not isinstance(values, list)
        or not all(isinstance(value, str) and value for value in values)
        or expected_audience not in values
    ):
        raise ValueError("JWT-SVID audience mismatch")
    if "exp" not in token.claims:
        raise ValueError("JWT-SVID expiry is required")
    if headers["alg"] not in _SVID_ALGORITHMS:
        raise ValueError("unsupported JWT-SVID signing algorithm")
    for field in ("exp", "iat", "nbf"):
        if field in token.claims and (
            type(token.claims[field]) not in (int, float)
            or not isfinite(token.claims[field])
        ):
            raise ValueError("invalid JWT-SVID NumericDate")
    if "nbf" in token.claims and token.claims["nbf"] > now:
        raise ValueError("JWT-SVID is not yet valid")
    domain, path = validate_spiffe_id(token.claims["sub"])
    if not path or not now < token.claims["exp"]:
        raise ValueError("JWT-SVID has an invalid workload identity or expiry")
    kid = headers.get("kid")
    if "kid" in headers and (not isinstance(kid, str) or not kid):
        raise ValueError("invalid JWT-SVID signing key ID")
    keys = [
        key
        for key in keys_by_domain.get(domain, ())
        if (kid is None or key.get("kid") == kid) and key.get("use") == "jwt-svid"
    ]
    if not keys or (kid is not None and len(keys) != 1):
        raise ValueError("JWT-SVID signing key must resolve within its trust bundle")
    for key in keys:
        try:
            verify_public_jws(serialized, key)
        except ValueError:
            continue
        return token.claims["sub"]
    raise ValueError("JWT-SVID signature verification failed")

from collections.abc import Callable, Mapping

from tigrbl_identity_contracts.workloads import (
    SpiffeId,
    SpiffeTrustBundle,
    Svid,
    SvidFormat,
    TrustBundleProviderPort,
)
from tigrbl_workload_identity_bases import SvidVerifierBase
from tigrbl_svid_concrete import (
    X509SvidStructure,
    parse_jwt_svid_claims,
    validate_x509_svid_structure,
)

JwtSvidTokenVerifier = Callable[[str, str, SpiffeTrustBundle], Mapping[str, object]]
X509SvidPathVerifier = Callable[[bytes, SpiffeTrustBundle], X509SvidStructure]


class ProfiledSvidVerifier(SvidVerifierBase):
    def __init__(
        self,
        bundles: TrustBundleProviderPort,
        jwt_verifier: JwtSvidTokenVerifier | None = None,
        x509_verifier: X509SvidPathVerifier | None = None,
    ):
        self._bundles = bundles
        self._jwt_verifier = jwt_verifier
        self._x509_verifier = x509_verifier

    def verify_svid(self, svid: Svid, audience: str | None = None, /) -> SpiffeId:
        bundle = self._bundles.bundle_for(svid.spiffe_id.trust_domain)
        if svid.format is SvidFormat.JWT:
            if audience is None:
                raise ValueError("JWT-SVID verification requires audience")
            if not isinstance(svid.credential, str) or self._jwt_verifier is None:
                raise ValueError("JWT-SVID token verifier is not configured")
            claims = parse_jwt_svid_claims(
                self._jwt_verifier(svid.credential, audience, bundle)
            )
            verified = SpiffeId.parse(claims.subject)
            if audience not in claims.audience:
                raise ValueError("JWT-SVID audience mismatch")
        elif svid.format is SvidFormat.X509:
            if not isinstance(svid.credential, bytes) or self._x509_verifier is None:
                raise ValueError("X.509-SVID path verifier is not configured")
            verified = validate_x509_svid_structure(
                self._x509_verifier(svid.credential, bundle)
            )
        else:  # pragma: no cover - enum exhaustiveness
            raise ValueError("unsupported SVID format")
        if verified != svid.spiffe_id:
            raise ValueError("verified SVID identity does not match declared SPIFFE ID")
        return verified


__all__ = ["JwtSvidTokenVerifier", "ProfiledSvidVerifier", "X509SvidPathVerifier"]

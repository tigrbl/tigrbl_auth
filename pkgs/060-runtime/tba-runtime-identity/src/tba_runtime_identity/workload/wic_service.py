"""Authorized issuance of native WIMSE workload certificates."""

from collections.abc import Callable
from time import time

from cryptography import x509
from cryptography.x509.oid import ExtendedKeyUsageOID

from tba_bases_certificate import CertificateServiceBase
from tba_concrete_certificate_x509 import parse_x509_certificate
from tba_contracts_security_trust import CertificateRequest
from tba_profile_workload_credential_wimse_wic import validate_wic

from .enrollment import ResolveWorkloadIdentity, resolve_enrolled_identity


class WicIssuanceService:
    def __init__(
        self,
        issuer: CertificateServiceBase,
        *,
        trust_domain: str,
        resolve_identity: ResolveWorkloadIdentity,
        lifetime_seconds: int = 3600,
        clock: Callable[[], float] = time,
    ) -> None:
        if (
            not trust_domain
            or type(lifetime_seconds) is not int
            or lifetime_seconds <= 0
        ):
            raise ValueError(
                "WIC issuance requires a trust domain and positive lifetime"
            )
        self._issuer = issuer
        self._trust_domain = trust_domain
        self._resolve_identity = resolve_identity
        self._lifetime_seconds = lifetime_seconds
        self._clock = clock

    async def issue(self, principal: str, csr: bytes) -> bytes:
        identity = await resolve_enrolled_identity(
            principal, self._trust_domain, self._resolve_identity
        )
        now = int(self._clock())
        usage = x509.ExtendedKeyUsage(
            [ExtendedKeyUsageOID.CLIENT_AUTH, ExtendedKeyUsageOID.SERVER_AUTH]
        )
        key_usage = x509.KeyUsage(
            digital_signature=True,
            content_commitment=False,
            key_encipherment=False,
            data_encipherment=False,
            key_agreement=False,
            key_cert_sign=False,
            crl_sign=False,
            encipher_only=False,
            decipher_only=False,
        )
        artifact = await self._issuer.issue_certificate(
            CertificateRequest(
                op="issue_certificate",
                csr=csr,
                san={"uri": (str(identity),)},
                not_before=now,
                not_after=now + self._lifetime_seconds,
                extensions={
                    usage.oid.dotted_string: (usage, False),
                    key_usage.oid.dotted_string: (key_usage, True),
                },
            )
        )
        pem = artifact.bytes_value
        if artifact.format != "x509-pem" or not pem:
            raise RuntimeError("certificate issuer did not return a PEM certificate")
        try:
            credential = validate_wic(parse_x509_certificate(pem))
        except ValueError as exc:
            raise RuntimeError("certificate issuer did not return a valid WIC") from exc
        if credential.workload_identifier != str(identity):
            raise RuntimeError(
                "certificate issuer returned an unauthorized workload identity"
            )
        return pem

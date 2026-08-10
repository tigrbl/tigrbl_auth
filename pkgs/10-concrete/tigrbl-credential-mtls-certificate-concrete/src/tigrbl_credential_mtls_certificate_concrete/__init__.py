from dataclasses import dataclass, field
from tigrbl_identity_contracts.credentials import Credential, CredentialKind
from tigrbl_authentication_credential_bases import CredentialBase
from tigrbl_identity_core import clean_tuple, new_model_id, required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class MtlsCertificateCredential(CredentialBase):
    id: str = field(default_factory=new_model_id)
    kind: CredentialKind = field(default=CredentialKind.MTLS_CERTIFICATE, init=False)
    certificate_thumbprint: str
    subject_dn: str | None = None
    san_dns: tuple[str, ...] = ()
    san_uri: tuple[str, ...] = ()
    san_ip: tuple[str, ...] = ()
    san_email: tuple[str, ...] = ()

    def __post_init__(self):
        thumb = required_text(self.certificate_thumbprint, "certificate thumbprint")
        object.__setattr__(self, "certificate_thumbprint", thumb)
        object.__setattr__(
            self,
            "subject_dn",
            str(self.subject_dn).strip() or None
            if self.subject_dn is not None
            else None,
        )
        object.__setattr__(self, "public_id", self.public_id or thumb)
        for name in ("san_dns", "san_uri", "san_ip", "san_email"):
            object.__setattr__(self, name, clean_tuple(getattr(self, name)))
        object.__setattr__(
            self,
            "metadata",
            {
                **dict(self.metadata),
                "subject_dn": self.subject_dn,
                "san_dns": list(self.san_dns),
                "san_uri": list(self.san_uri),
                "san_ip": list(self.san_ip),
                "san_email": list(self.san_email),
            },
        )
        CredentialBase.__post_init__(self)

    @property
    def confirmation_claim(self):
        return {"x5t#S256": self.certificate_thumbprint}

    def to_credential(self):
        return Credential(
            id=self.id,
            principal_id=self.principal_id,
            kind=CredentialKind.MTLS_CERTIFICATE,
            public_id=self.certificate_thumbprint,
            status=self.status,
            metadata=self.metadata,
        )


__all__ = ["MtlsCertificateCredential"]

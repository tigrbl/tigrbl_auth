from dataclasses import dataclass, field

from cryptography import x509


@dataclass(frozen=True, slots=True)
class X509Certificate:
    der: bytes
    _certificate: x509.Certificate = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        object.__setattr__(
            self, "_certificate", x509.load_der_x509_certificate(self.der)
        )

    def _extension(self, kind):
        try:
            return self._certificate.extensions.get_extension_for_class(kind).value
        except x509.ExtensionNotFound:
            return None

    @property
    def uri_sans(self) -> tuple[str, ...]:
        names = self._extension(x509.SubjectAlternativeName)
        return (
            tuple(names.get_values_for_type(x509.UniformResourceIdentifier))
            if names
            else ()
        )

    @property
    def dns_sans(self) -> tuple[str, ...]:
        names = self._extension(x509.SubjectAlternativeName)
        return tuple(names.get_values_for_type(x509.DNSName)) if names else ()

    @property
    def key_usage(self):
        return self._extension(x509.KeyUsage)

    @property
    def basic_constraints(self):
        return self._extension(x509.BasicConstraints)

    @property
    def not_before(self):
        return self._certificate.not_valid_before_utc

    @property
    def not_after(self):
        return self._certificate.not_valid_after_utc

    def public_key(self):
        return self._certificate.public_key()

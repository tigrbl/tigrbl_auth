"""Adapt exportable SSLContext verification policy to the QUIC TLS engine."""

import re
import ssl
from dataclasses import dataclass
from pathlib import Path

from tba_codec_dns.wire import WireError

_CRL_PEM = re.compile(rb"-----BEGIN X509 CRL-----.*?-----END X509 CRL-----", re.S)


def configure_http3_crls(context: ssl.SSLContext, *sources) -> None:
    """Attach CRLs from PEM bundles or DER data to a QUIC client context.

    Python exposes CA certificates but does not expose CRLs already loaded
    into an SSLContext. Pass the same CRL material here for HTTP/3.
    Set SSLContext.verify_flags to select leaf or full-chain checking.
    """
    from cryptography import x509

    crls = []
    for source in sources:
        data = source if isinstance(source, bytes) else Path(source).read_bytes()
        blocks = _CRL_PEM.findall(data)
        if blocks:
            crls.extend(x509.load_pem_x509_crl(block) for block in blocks)
        else:
            crls.append(x509.load_der_x509_crl(data))
    context._tba_http3_crls = tuple(crls)


@dataclass(frozen=True, repr=False)
class ClientIdentity:
    chain: tuple
    private_key: object


def configure_http3_client_identity(
    context: ssl.SSLContext,
    certfile,
    keyfile=None,
    password=None,
) -> None:
    """Load a client PEM chain and private key for native HTTP/3.

    Use a separate key file or append the private key to the PEM chain.
    An encrypted key accepts a password as text, bytes, or a callback.
    """
    if context.protocol == ssl.PROTOCOL_TLS_SERVER:
        raise ValueError("HTTP/3 requires a client SSLContext")
    identity, _ = _load_client_identity(certfile, keyfile, password)
    context._tba_http3_client_identity = identity


class HTTP3SSLContext(ssl.SSLContext):
    """A client SSLContext that registers loaded identities for QUIC as well."""

    def __new__(cls):
        return super().__new__(cls, ssl.PROTOCOL_TLS_CLIENT)

    def load_cert_chain(self, certfile, keyfile=None, password=None):
        # Validate the QUIC identity first. A failed reload must not replace it.
        identity, resolved_password = _load_client_identity(certfile, keyfile, password)
        super().load_cert_chain(certfile, keyfile, resolved_password)
        self._tba_http3_client_identity = identity


def _load_client_identity(certfile, keyfile, password):
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization

    with open(certfile, "rb") as pem:
        cert_data = pem.read()
    cert_blocks = re.findall(
        rb"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----",
        cert_data,
        re.S,
    )
    if not cert_blocks:
        raise ValueError("HTTP/3 client identity requires a PEM certificate")
    certificates = tuple(x509.load_pem_x509_certificate(block) for block in cert_blocks)
    if keyfile is None:
        key_data = cert_data
    else:
        with open(keyfile, "rb") as pem:
            key_data = pem.read()
    encrypted = (
        b"-----BEGIN ENCRYPTED PRIVATE KEY-----" in key_data
        or b"Proc-Type: 4,ENCRYPTED" in key_data
    )
    resolved = (
        password()
        if encrypted and callable(password)
        else password
        if encrypted
        else None
    )
    if isinstance(resolved, str):
        resolved = resolved.encode("utf-8")
    private_key = serialization.load_pem_private_key(key_data, resolved)
    if certificates[0].public_key() != private_key.public_key():
        raise ValueError("HTTP/3 client certificate and private key do not match")
    return ClientIdentity(certificates, private_key), resolved


def client_identity(context):
    identity = getattr(context, "_tba_http3_client_identity", None)
    if identity is not None and context.verify_mode != ssl.CERT_REQUIRED:
        raise ValueError(
            "HTTP/3 client authentication requires server certificate verification"
        )
    return identity


@dataclass(frozen=True)
class PeerPolicy:
    anchors: tuple[bytes, ...]
    flags: int
    crls: tuple

    def __call__(self, chain):
        from OpenSSL import crypto

        if not chain:
            raise WireError("HTTP/3 did not provide its peer certificate chain")
        store = crypto.X509Store()
        for anchor in self.anchors:
            store.add_cert(crypto.load_certificate(crypto.FILETYPE_ASN1, anchor))
        for crl in self.crls:
            store.add_crl(crl)
        store.set_flags(self.flags)
        leaf, *issuers = map(crypto.X509.from_cryptography, chain)
        try:
            crypto.X509StoreContext(store, leaf, issuers).verify_certificate()
        except crypto.X509StoreContextError as exc:
            raise WireError(f"HTTP/3 certificate verification failed: {exc}") from exc


def _cipher_suites(context):
    from aioquic.tls import CipherSuite

    supported = {suite.value: suite for suite in CipherSuite}
    suites = [
        supported[item["id"] & 0xFFFF]
        for item in context.get_ciphers()
        if item["protocol"] == "TLSv1.3" and item["id"] & 0xFFFF in supported
    ]
    if not suites:
        raise ValueError("HTTP/3 SSLContext has no supported TLS 1.3 ciphers")
    return suites


def context_trust(context):
    if context.protocol == ssl.PROTOCOL_TLS_SERVER:
        raise ValueError("HTTP/3 requires a client SSLContext")
    if (
        context.maximum_version
        not in (ssl.TLSVersion.MAXIMUM_SUPPORTED, ssl.TLSVersion.TLSv1_3)
        or context.minimum_version == ssl.TLSVersion.MAXIMUM_SUPPORTED
        or context.options & getattr(ssl, "OP_NO_TLSv1_3", 0)
    ):
        raise ValueError("HTTP/3 requires TLS 1.3")
    suites = _cipher_suites(context)
    if context.verify_mode == ssl.CERT_NONE:
        return False, None, None, suites
    if context.verify_mode != ssl.CERT_REQUIRED:
        raise ValueError("verified HTTP/3 requires CERT_REQUIRED")
    anchors = tuple(context.get_ca_certs(binary_form=True))
    if not anchors:
        raise ValueError("HTTP/3 SSLContext has no exportable CA certificates")
    crls = getattr(context, "_tba_http3_crls", ())
    if context.verify_flags & ssl.VERIFY_CRL_CHECK_LEAF and not crls:
        raise ValueError("configure HTTP/3 CRLs explicitly with configure_http3_crls()")
    pem = "".join(ssl.DER_cert_to_PEM_cert(cert) for cert in anchors).encode("ascii")
    return (
        context.check_hostname,
        pem,
        PeerPolicy(anchors, int(context.verify_flags), crls),
        suites,
    )

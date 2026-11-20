"""Verified Discovery of Designated Resolvers (RFC 9462)."""

import asyncio
import ipaddress
import ssl
from importlib.util import find_spec
from struct import unpack

from tba_codec_dns.rdata import decoded
from tba_codec_dns.wire import WireError
from tba_provider_dns_resolver.async_transport import run_blocking
from tba_provider_dns_resolver.client import (
    NXDOMAIN,
    HttpsNameserver,
    NoAnswer,
    NoNameservers,
    QuicNameserver,
    Resolver,
    TlsNameserver,
)
from tba_provider_dns_resolver.transport import (
    deadline_after,
    remaining,
    stream,
    verify_quic_resolver,
)


def discover(
    resolver: Resolver, *, lifetime: float = 3, context: ssl.SSLContext | None = None
) -> tuple[HttpsNameserver | TlsNameserver | QuicNameserver, ...]:
    """Return encrypted endpoints whose certificate also covers the original resolver IP."""
    if not resolver.nameservers or not isinstance(resolver.nameservers[0], str):
        return ()
    original = ipaddress.ip_address(resolver.nameservers[0])
    deadline = deadline_after(lifetime)
    trust = ssl.create_default_context() if context is None else context
    if trust.verify_mode != ssl.CERT_REQUIRED or not trust.check_hostname:
        raise ValueError("DDR requires certificate chain and hostname verification")
    try:
        source = (
            resolver
            if len(resolver.nameservers) == 1
            else Resolver(
                [str(original)],
                port=resolver.nameserver_ports.get(str(original), resolver.port),
                timeout=resolver.timeout,
            )
        )
        records = Resolver.resolve(
            source, "_dns.resolver.arpa.", "SVCB", lifetime=remaining(deadline)
        )
        bindings = sorted(
            (decoded(rr)[0] for rr in records), key=lambda binding: binding.priority
        )
    except (NoAnswer, NXDOMAIN, NoNameservers, TimeoutError, WireError):
        return ()
    output = []
    quic_available = find_spec("aioquic") is not None
    quic_ca_data = None
    for binding in bindings:
        if not binding.priority or not binding.target:
            continue
        params = dict(binding.params)
        if 0 in params and any(
            key not in {1, 2, 3, 4, 6, 7}
            for key in unpack(f"!{len(params[0]) // 2}H", params[0])
        ):
            continue
        alpn = params.get(1, b"")
        protocols = set()
        offset = 0
        while offset < len(alpn):
            end = offset + 1 + alpn[offset]
            protocols.add(alpn[offset + 1 : end])
            offset = end
        try:
            target = b".".join(binding.target).decode("ascii")
            alternatives = []
            if b"dot" in protocols:
                port = int.from_bytes(params.get(3, b"\x03\x55"), "big")
                alternatives.append(
                    (
                        TlsNameserver(
                            str(original), target, port, trust, str(original)
                        ),
                        port,
                        None,
                    )
                )
            if (
                quic_available
                and protocols.intersection((b"doq", b"h3"))
                and quic_ca_data is None
            ):
                quic_ca_data = "".join(
                    ssl.DER_cert_to_PEM_cert(cert)
                    for cert in trust.get_ca_certs(binary_form=True)
                ).encode("ascii")
            if b"doq" in protocols and quic_ca_data:
                port = int.from_bytes(params.get(3, b"\x03\x55"), "big")
                alternatives.append(
                    (
                        QuicNameserver(
                            str(original),
                            target,
                            port,
                            ca_data=quic_ca_data,
                            certificate_ip=str(original),
                        ),
                        port,
                        "doq",
                    )
                )
            if 7 in params and protocols.intersection((b"h2", b"h3")):
                path = params[7].decode("ascii").removesuffix("{?dns}")
                if path.startswith("/") and not any(ch in path for ch in "{}#\r\n"):
                    port = int.from_bytes(params.get(3, b"\x01\xbb"), "big")
                    url = f"https://{target}:{port}{path}"
                    if b"h3" in protocols and quic_ca_data:
                        alternatives.append(
                            (
                                HttpsNameserver(
                                    url,
                                    http_version=3,
                                    ca_data=quic_ca_data,
                                    bootstrap_address=str(original),
                                    certificate_ip=str(original),
                                ),
                                port,
                                "h3",
                            )
                        )
                    if b"h2" in protocols and find_spec("httpx") and find_spec("h2"):
                        alternatives.append(
                            (
                                HttpsNameserver(
                                    url,
                                    context=trust,
                                    http_version=2,
                                    bootstrap_address=str(original),
                                    certificate_ip=str(original),
                                ),
                                port,
                                None,
                            )
                        )
            for endpoint, port, quic_alpn in alternatives:
                if not port:
                    continue
                try:
                    if quic_alpn is not None:
                        asyncio.run(
                            verify_quic_resolver(
                                str(original),
                                port,
                                target,
                                quic_alpn,
                                timeout=remaining(deadline),
                                ca_data=quic_ca_data,
                            )
                        )
                        output.append(endpoint)
                        continue
                    with stream(
                        str(original),
                        port,
                        deadline,
                        server_name=target,
                        context=trust,
                        certificate_ip=str(original),
                    ):
                        output.append(endpoint)
                except (OSError, ValueError):
                    continue
        except (UnicodeError, ValueError):
            continue
    return tuple(dict.fromkeys(output))


def try_ddr(
    resolver: Resolver, *, lifetime: float = 3, context: ssl.SSLContext | None = None
) -> bool:
    """Set verified encrypted endpoints on the resolver when discovery succeeds."""
    endpoints = discover(resolver, lifetime=lifetime, context=context)
    if not endpoints:
        return False
    resolver.nameservers = endpoints
    return True


async def try_ddr_async(
    resolver: Resolver, *, lifetime: float = 3, context: ssl.SSLContext | None = None
) -> bool:
    """Run verified resolver discovery without blocking the async runtime."""
    return await run_blocking(try_ddr, resolver, lifetime=lifetime, context=context)

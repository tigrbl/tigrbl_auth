"""Opt-in interception of Python's socket resolution functions."""

import ipaddress
import socket
from collections.abc import Iterator
from contextlib import contextmanager
from threading import RLock

from tba_codec_dns.wire import WireError
from tba_primitives_dns_name.names import name_text

from .client import NXDOMAIN, NoAnswer, Resolver, get_default_resolver

_LOCK = RLock()


@contextmanager
def override_system_resolver(resolver: Resolver | None = None) -> Iterator[Resolver]:
    """Use a DNS resolver for socket name lookups for the lifetime of this context."""
    resolver = get_default_resolver() if resolver is None else resolver
    with _LOCK:
        addrinfo = socket.getaddrinfo
        hostbyaddr = socket.gethostbyaddr
        hostname = socket.gethostbyname
        hostname_ex = socket.gethostbyname_ex
        nameinfo = socket.getnameinfo

        def _addresses(host, family=0):
            host = host.decode("ascii") if isinstance(host, bytes) else host
            try:
                answers = resolver.resolve_name(host, family=family, search=True)
                return tuple(
                    ipaddress.ip_address(address) for address in answers.addresses()
                )
            except (NoAnswer, NXDOMAIN) as exc:
                raise socket.gaierror(
                    socket.EAI_NONAME, "name does not have a DNS address"
                ) from exc
            except (OSError, WireError) as exc:
                raise socket.gaierror(
                    socket.EAI_AGAIN, "DNS server could not answer"
                ) from exc

        def getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
            if (
                host is None
                or flags & socket.AI_NUMERICHOST
                or family
                not in (
                    socket.AF_UNSPEC,
                    socket.AF_INET,
                    socket.AF_INET6,
                )
            ):
                return addrinfo(host, port, family, type, proto, flags)
            try:
                numeric = host.decode("ascii") if isinstance(host, bytes) else host
                ipaddress.ip_address(numeric)
                return addrinfo(host, port, family, type, proto, flags)
            except ValueError:
                pass
            wanted = {socket.AF_UNSPEC: 0, socket.AF_INET: 4, socket.AF_INET6: 6}[
                family
            ]
            if wanted == 6 and flags & socket.AI_V4MAPPED:
                try:
                    found = _addresses(host, 6)
                except socket.gaierror as exc:
                    if exc.errno != socket.EAI_NONAME:
                        raise
                    found = ()
                if not found or flags & socket.AI_ALL:
                    found = (*found, *_addresses(host, 4))
            else:
                found = _addresses(host, wanted)
            results = []
            for address in found:
                results.extend(
                    addrinfo(
                        str(address),
                        port,
                        family,
                        type,
                        proto,
                        (flags & ~socket.AI_CANONNAME) | socket.AI_NUMERICHOST,
                    )
                )
            if results and flags & socket.AI_CANONNAME:
                identity = host.decode("ascii") if isinstance(host, bytes) else host
                canonical = name_text(resolver.canonical_name(identity)).removesuffix(
                    "."
                )
                first = results[0]
                results[0] = (*first[:3], canonical, first[4])
            return results

        def gethostbyname(host):
            label = host.decode("ascii") if isinstance(host, bytes) else host
            try:
                ipaddress.IPv4Address(label)
            except (TypeError, ValueError):
                return str(_addresses(label, 4)[0])
            return hostname(host)

        def gethostbyname_ex(host):
            label = host.decode("ascii") if isinstance(host, bytes) else host
            try:
                ipaddress.IPv4Address(label)
                return hostname_ex(host)
            except (TypeError, ValueError):
                addresses = _addresses(label, 4)
                canonical = name_text(resolver.canonical_name(label)).removesuffix(".")
                return canonical, [], list(map(str, addresses))

        def gethostbyaddr(host):
            label = host.decode("ascii") if isinstance(host, bytes) else host
            try:
                address = ipaddress.ip_address(label)
            except ValueError:
                address = _addresses(label)[0]
            try:
                pointers = resolver.resolve_address(str(address))
            except (NoAnswer, NXDOMAIN, OSError, WireError) as exc:
                raise socket.herror(1, "DNS address has no PTR record") from exc
            names = tuple(
                dict.fromkeys(rr.target.to_text().removesuffix(".") for rr in pointers)
            )
            return names[0], list(names[1:]), [str(address)]

        def getnameinfo(sockaddr, flags):
            numeric, service = nameinfo(sockaddr, flags | socket.NI_NUMERICHOST)
            if flags & socket.NI_NUMERICHOST:
                return numeric, service
            try:
                resolved = gethostbyaddr(numeric)[0]
            except socket.herror as exc:
                if flags & socket.NI_NAMEREQD:
                    raise socket.gaierror(
                        socket.EAI_NONAME, "address has no DNS name"
                    ) from exc
                resolved = numeric
            return resolved, service

        socket.getaddrinfo = getaddrinfo
        socket.gethostbyname = gethostbyname
        socket.gethostbyname_ex = gethostbyname_ex
        socket.gethostbyaddr = gethostbyaddr
        socket.getnameinfo = getnameinfo
        try:
            yield resolver
        finally:
            socket.getaddrinfo = addrinfo
            socket.gethostbyname = hostname
            socket.gethostbyname_ex = hostname_ex
            socket.gethostbyaddr = hostbyaddr
            socket.getnameinfo = nameinfo

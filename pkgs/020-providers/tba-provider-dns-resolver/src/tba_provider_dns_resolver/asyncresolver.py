"""Asynchronous stub-resolver functions and default resolver."""

import socket
from threading import RLock

from tba_codec_dns.wire import RecordClass, RecordType
from tba_primitives_dns_name.name import Name

from .client import (
    NXDOMAIN as NXDOMAIN,
    Answer as Answer,
    AsyncResolver as Resolver,
    NoAnswer as NoAnswer,
    NoNameservers as NoNameservers,
    NoRootSOA as NoRootSOA,
    NotAbsolute as NotAbsolute,
)
from .nameserver import Do53Nameserver
from .resolver import _address_literal

_default: Resolver | None = None
_default_lock = RLock()


def get_default_resolver() -> Resolver:
    global _default
    with _default_lock:
        if _default is None:
            _default = Resolver()
        return _default


def reset_default_resolver() -> None:
    global _default
    with _default_lock:
        _default = Resolver()


async def resolve(
    qname,
    rdtype=RecordType.A,
    rdclass=RecordClass.IN,
    tcp=False,
    source=None,
    raise_on_no_answer=True,
    source_port=0,
    lifetime=None,
    search=None,
    backend=None,
) -> Answer:
    return await get_default_resolver().resolve(
        qname,
        rdtype,
        rdclass,
        tcp,
        source,
        raise_on_no_answer,
        source_port,
        lifetime,
        search,
        backend,
    )


async def resolve_address(ipaddr, **kwargs):
    return await get_default_resolver().resolve_address(ipaddr, **kwargs)


async def resolve_name(name, family=socket.AF_UNSPEC, **kwargs):
    return await get_default_resolver().resolve_name(name, family, **kwargs)


async def canonical_name(name, backend=None):
    owner = await get_default_resolver().canonical_name(name, backend=backend)
    return Name((*owner, b""))


async def try_ddr(lifetime=5.0):
    await get_default_resolver().try_ddr(lifetime)


async def zone_for_name(
    name,
    rdclass=RecordClass.IN,
    tcp=False,
    resolver=None,
    lifetime=None,
    backend=None,
):
    if resolver is None:
        resolver = get_default_resolver()
    owner = await resolver.zone_for_name(
        name,
        rdclass=rdclass,
        tcp=tcp,
        backend=backend,
        lifetime=resolver.lifetime if lifetime is None else lifetime,
    )
    return Name((*owner, b""))


async def make_resolver_at(
    where, port=53, family=socket.AF_UNSPEC, resolver=None
) -> Resolver:
    address = _address_literal(where)
    if address is None:
        if resolver is None:
            resolver = get_default_resolver()
        answer = await resolver.resolve_name(where, family)
        addresses = answer.addresses()
    else:
        addresses = (address,)
    return Resolver(
        (Do53Nameserver(address, port) for address in addresses), configure=False
    )


async def resolve_at(
    where,
    qname,
    rdtype=RecordType.A,
    rdclass=RecordClass.IN,
    tcp=False,
    source=None,
    raise_on_no_answer=True,
    source_port=0,
    lifetime=None,
    search=None,
    backend=None,
    port=53,
    family=socket.AF_UNSPEC,
    resolver=None,
) -> Answer:
    server = await make_resolver_at(where, port, family, resolver)
    return await server.resolve(
        qname,
        rdtype,
        rdclass,
        tcp,
        source,
        raise_on_no_answer,
        source_port,
        lifetime,
        search,
        backend,
    )

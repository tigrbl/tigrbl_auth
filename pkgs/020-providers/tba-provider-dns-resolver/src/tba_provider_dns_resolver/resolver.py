"""Synchronous stub-resolver functions and default resolver."""

import ipaddress
import socket

from tba_codec_dns.wire import RecordClass, RecordType
from tba_primitives_dns_name.name import Name

from . import client
from .client import (
    NXDOMAIN as NXDOMAIN,
    Answer as Answer,
    Cache as Cache,
    HostAnswers as HostAnswers,
    LRUCache as LRUCache,
    NoAnswer as NoAnswer,
    NoNameservers as NoNameservers,
    NoRootSOA as NoRootSOA,
    NotAbsolute as NotAbsolute,
    Resolver as Resolver,
    get_default_resolver as get_default_resolver,
)
from .nameserver import Do53Nameserver
from .system_resolver import override_system_resolver as override_system_resolver


def reset_default_resolver() -> None:
    client.reset_default_resolver()


def resolve(
    qname,
    rdtype=RecordType.A,
    rdclass=RecordClass.IN,
    tcp=False,
    source=None,
    raise_on_no_answer=True,
    source_port=0,
    lifetime=None,
    search=None,
) -> Answer:
    return get_default_resolver().resolve(
        qname,
        rdtype,
        rdclass,
        tcp,
        source,
        raise_on_no_answer,
        source_port,
        lifetime,
        search,
    )


def query(qname, *args, **kwargs):
    return resolve(qname, *args, search=True, **kwargs)


def resolve_address(ipaddr, **kwargs):
    return get_default_resolver().resolve_address(ipaddr, **kwargs)


def resolve_name(name, family=socket.AF_UNSPEC, **kwargs):
    return get_default_resolver().resolve_name(name, family, **kwargs)


def canonical_name(name):
    return Name((*get_default_resolver().canonical_name(name), b""))


def try_ddr(lifetime=5.0):
    get_default_resolver().try_ddr(lifetime)


def zone_for_name(
    name, rdclass=RecordClass.IN, tcp=False, resolver=None, lifetime=None
):
    if resolver is None:
        resolver = get_default_resolver()
    owner = resolver.zone_for_name(
        name,
        rdclass=rdclass,
        tcp=tcp,
        lifetime=resolver.lifetime if lifetime is None else lifetime,
    )
    return Name((*owner, b""))


def _address_literal(where):
    if isinstance(where, str):
        try:
            return str(ipaddress.ip_address(where))
        except ValueError:
            pass
    return None


def make_resolver_at(
    where, port=53, family=socket.AF_UNSPEC, resolver=None
) -> Resolver:
    address = _address_literal(where)
    if address is None:
        if resolver is None:
            resolver = get_default_resolver()
        addresses = resolver.resolve_name(where, family).addresses()
    else:
        addresses = (address,)
    return Resolver(
        (Do53Nameserver(address, port) for address in addresses), configure=False
    )


def resolve_at(
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
    port=53,
    family=socket.AF_UNSPEC,
    resolver=None,
) -> Answer:
    server = make_resolver_at(where, port, family, resolver)
    return server.resolve(
        qname,
        rdtype,
        rdclass,
        tcp,
        source,
        raise_on_no_answer,
        source_port,
        lifetime,
        search,
    )

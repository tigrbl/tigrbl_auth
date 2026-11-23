"""Convert IPv4 and IPv6 addresses between text and DNS reverse names."""

import ipaddress

from .name import Name, from_text

ipv4_reverse_domain = from_text("in-addr.arpa.")
ipv6_reverse_domain = from_text("ip6.arpa.")


def from_address(
    text: str,
    v4_origin: Name = ipv4_reverse_domain,
    v6_origin: Name = ipv6_reverse_domain,
) -> Name:
    address = ipaddress.ip_address(text)
    standard, origin = (
        (ipv4_reverse_domain, v4_origin)
        if address.version == 4
        else (ipv6_reverse_domain, v6_origin)
    )
    return (
        from_text(address.reverse_pointer + ".")
        .relativize(standard)
        .concatenate(origin)
    )


def to_address(
    name: Name,
    v4_origin: Name = ipv4_reverse_domain,
    v6_origin: Name = ipv6_reverse_domain,
) -> str:
    if name.is_subdomain(v4_origin):
        labels = name.relativize(v4_origin).labels
        return str(ipaddress.IPv4Address(b".".join(reversed(labels)).decode("ascii")))
    if name.is_subdomain(v6_origin):
        labels = name.relativize(v6_origin).labels
        if len(labels) != 32 or any(len(label) != 1 for label in labels):
            raise ValueError("invalid IPv6 reverse name")
        return str(ipaddress.IPv6Address(int(b"".join(reversed(labels)), 16)))
    raise ValueError("DNS name is outside the configured reverse zones")

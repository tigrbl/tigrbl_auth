"""Public DNS transport APIs."""

from tba_codec_dns.wire import Truncated

from ._doh import https3_query, https_query
from ._quic import QuicSession, quic_query, quic_session, verify_quic_resolver
from ._socket_transport import (
    DnsStream,
    UnexpectedSource,
    check_response,
    deadline_after,
    exchange_udp_packet,
    receive_tcp,
    receive_udp,
    remaining,
    send_tcp,
    send_udp,
    stream,
    tcp_query,
    tls_query,
    udp_query,
    udp_with_fallback,
)

__all__ = [
    "DnsStream",
    "QuicSession",
    "Truncated",
    "UnexpectedSource",
    "check_response",
    "deadline_after",
    "exchange_udp_packet",
    "https3_query",
    "https_query",
    "quic_query",
    "quic_session",
    "receive_tcp",
    "receive_udp",
    "remaining",
    "send_tcp",
    "send_udp",
    "stream",
    "tcp_query",
    "tls_query",
    "udp_query",
    "udp_with_fallback",
    "verify_quic_resolver",
]

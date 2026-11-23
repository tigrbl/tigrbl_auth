"""Verified DNS over QUIC connections and reusable DoQ sessions."""

import asyncio
import ipaddress
import os
import socket
import ssl
from collections.abc import Callable
from contextlib import AsyncExitStack, asynccontextmanager
from copy import copy
from dataclasses import replace

from tba_codec_dns.wire import Message, RecordType, WireError

from ._http3_tls import client_identity, context_trust
from ._socket_transport import check_response, deadline_after, remaining


class UnexpectedEOF(WireError):
    """The peer closed a QUIC stream before its message was complete."""


def _client_configuration(conf, verify_mode, server_name, h3):
    from aioquic.quic.configuration import QuicConfiguration

    if conf is not None:
        return copy(conf), None
    alpn = ["doq"]
    if h3:
        from aioquic.h3.connection import H3_ALPN

        alpn = H3_ALPN
    options = {}
    policy = None
    if isinstance(verify_mode, (str, os.PathLike)):
        options["cafile"] = os.fspath(verify_mode)
        verify_mode = ssl.CERT_REQUIRED
    elif h3 and isinstance(verify_mode, ssl.SSLContext):
        verify, ca_data, policy, cipher_suites = context_trust(verify_mode)
        identity = client_identity(verify_mode)
        options.update(cadata=ca_data, cipher_suites=cipher_suites)
        if identity is not None:
            options.update(
                certificate=identity.chain[0],
                certificate_chain=list(identity.chain[1:]),
                private_key=identity.private_key,
            )
        verify_mode = ssl.CERT_REQUIRED if verify else ssl.CERT_NONE
    elif isinstance(verify_mode, bool):
        verify_mode = ssl.CERT_REQUIRED if verify_mode else ssl.CERT_NONE
    return QuicConfiguration(
        is_client=True,
        alpn_protocols=alpn,
        server_name=server_name,
        verify_mode=verify_mode,
        **options,
    ), policy


def _has_tsig(message: Message) -> bool:
    return any(rr.type == RecordType.TSIG for rr in message.additional)


def _zero_id_request(query: Message) -> Message:
    if query._sign_on_wire and not _has_tsig(query):
        return replace(query, id=0, _original_id=0)
    if query.id == 0:
        return query
    if _has_tsig(query):
        raise WireError("sign the DNS message with ID zero for this transport")
    return replace(query, id=0)


def _restore_id(response: Message, identifier: int) -> Message:
    if response.id == identifier or _has_tsig(response):
        return response
    return replace(response, id=identifier)


def _check_certificate_ip(certificates, address):
    from cryptography.x509 import ExtensionNotFound, IPAddress, SubjectAlternativeName

    expected = ipaddress.ip_address(address)
    if certificates:
        try:
            san = certificates[0].extensions.get_extension_for_class(
                SubjectAlternativeName
            )
            if expected in san.value.get_values_for_type(IPAddress):
                return
        except ExtensionNotFound:
            pass
    raise WireError("QUIC certificate does not cover the original DNS resolver address")


def _deadline(timeout):
    return None if timeout is None else deadline_after(timeout)


def _remaining(deadline):
    return None if deadline is None else remaining(deadline)


async def quic_query(
    query: Message,
    server: str,
    *,
    port: int = 853,
    timeout: float = 3,
    server_name: str | None = None,
    ca_file: str | None = None,
    ca_data: bytes | None = None,
    certificate_ip: str | None = None,
    token: bytes = b"",
    token_handler: Callable[[bytes], None] | None = None,
    local_port: int = 0,
    local_address: str | None = None,
    verify: bool = True,
    one_rr_per_rrset: bool = False,
    ignore_trailing: bool = False,
) -> Message:
    """Send one RFC 9250 DNS transaction over a verified QUIC stream."""
    deadline = _deadline(timeout)
    request = _doq_request(query)
    async with quic_session(
        server,
        port=port,
        timeout=_remaining(deadline),
        server_name=server_name,
        ca_file=ca_file,
        ca_data=ca_data,
        certificate_ip=certificate_ip,
        token=token,
        token_handler=token_handler,
        local_port=local_port,
        local_address=local_address,
        verify=verify,
    ) as session:
        return await session._query(
            request, query.id, deadline, one_rr_per_rrset, ignore_trailing
        )


def _doq_request(query: Message) -> Message:
    if query.get_options(11):
        raise ValueError("EDNS TCP keepalive is prohibited over QUIC")
    return _zero_id_request(query)


class QuicSession:
    """A verified DoQ connection that can open a stream for each DNS question."""

    def __init__(self, connection):
        self._connection = connection

    async def query(
        self,
        query: Message,
        *,
        timeout=3,
        one_rr_per_rrset=False,
        ignore_trailing=False,
    ) -> Message:
        return await self._query(
            _doq_request(query),
            query.id,
            _deadline(timeout),
            one_rr_per_rrset,
            ignore_trailing,
        )

    async def _query(
        self,
        request: Message,
        identifier: int,
        deadline,
        one_rr_per_rrset=False,
        ignore_trailing=False,
    ) -> Message:
        packet = request.to_wire()
        authentication = {}
        if request.tsig_key is not None:
            sent = Message.from_wire(packet)
            authentication = {"keyring": request.tsig_key, "request_mac": sent.mac}

        async def exchange() -> Message:
            reader, writer = await self._connection.create_stream()
            writer.write(len(packet).to_bytes(2, "big") + packet)
            writer.write_eof()
            try:
                length = int.from_bytes(await reader.readexactly(2), "big")
                response = Message.from_wire(
                    await reader.readexactly(length),
                    one_rr_per_rrset=one_rr_per_rrset,
                    ignore_trailing=ignore_trailing,
                    **authentication,
                )
                if await reader.read(1):
                    raise WireError("extra data after DNS QUIC response")
            except asyncio.IncompleteReadError as exc:
                raise WireError("truncated DNS QUIC response") from exc
            check_response(request, response)
            return _restore_id(response, identifier)

        return await asyncio.wait_for(exchange(), timeout=_remaining(deadline))


@asynccontextmanager
async def quic_session(
    server: str,
    *,
    port: int = 853,
    timeout: float = 3,
    server_name: str | None = None,
    ca_file: str | None = None,
    ca_data: bytes | None = None,
    certificate_ip: str | None = None,
    token: bytes = b"",
    token_handler: Callable[[bytes], None] | None = None,
    local_port: int = 0,
    local_address: str | None = None,
    verify: bool = True,
):
    """Open one certificate-verified DoQ connection on asyncio."""
    deadline = _deadline(timeout)
    connection = _verified_quic_connection(
        server,
        port,
        ["doq"],
        server_name=server_name or server,
        ca_file=ca_file,
        ca_data=ca_data,
        certificate_ip=certificate_ip,
        token=token,
        token_handler=token_handler,
        local_port=local_port,
        local_address=local_address,
        verify=verify,
    )
    async with AsyncExitStack() as cleanup:
        peer = await asyncio.wait_for(
            cleanup.enter_async_context(connection), timeout=_remaining(deadline)
        )
        yield QuicSession(peer)


@asynccontextmanager
async def _verified_quic_connection(
    server: str,
    port: int,
    alpn: list[str],
    *,
    server_name: str,
    ca_file: str | None = None,
    ca_data: bytes | None = None,
    certificate_ip: str | None = None,
    protocol=None,
    token: bytes = b"",
    token_handler: Callable[[bytes], None] | None = None,
    local_port: int = 0,
    local_address: str | None = None,
    verify: bool = True,
    peer_policy=None,
    client_identity=None,
    cipher_suites=None,
):
    from aioquic.asyncio import QuicConnectionProtocol, connect
    from aioquic.quic.configuration import QuicConfiguration
    from aioquic.quic.events import HandshakeCompleted

    if certificate_ip is not None and not verify and peer_policy is None:
        raise ValueError("certificate IP checking requires QUIC verification")

    base_protocol = QuicConnectionProtocol if protocol is None else protocol

    class AuthenticatedPeer(base_protocol):
        certificates = ()

        def quic_event_received(self, event):
            if (certificate_ip is not None or peer_policy is not None) and isinstance(
                event, HandshakeCompleted
            ):
                chain = getattr(event, "peer_certificates", None)
                if chain is None:
                    # aioquic 1.3 predates public certificate metadata on this event.
                    tls = getattr(self._quic, "tls", None)
                    leaf = getattr(tls, "_peer_certificate", None)
                    chain = (
                        ()
                        if leaf is None
                        else (leaf, *getattr(tls, "_peer_certificate_chain", ()))
                    )
                self.certificates = tuple(chain)
            super().quic_event_received(event)

    configuration = QuicConfiguration(
        is_client=True,
        alpn_protocols=alpn,
        cipher_suites=cipher_suites,
        server_name=server_name,
        cafile=ca_file,
        cadata=ca_data,
        token=token,
        verify_mode=ssl.CERT_REQUIRED if verify else ssl.CERT_NONE,
    )
    if client_identity is not None:
        configuration.certificate = client_identity.chain[0]
        configuration.certificate_chain = list(client_identity.chain[1:])
        configuration.private_key = client_identity.private_key

    def validate_peer(certificates):
        if peer_policy is not None:
            peer_policy(certificates)
        if certificate_ip is not None:
            _check_certificate_ip(certificates, certificate_ip)

    options = dict(
        configuration=configuration,
        create_protocol=AuthenticatedPeer,
        token_handler=token_handler,
        local_port=local_port,
    )
    if local_address is None and client_identity is None:
        connection = connect(server, port, **options)
    else:
        connection = _connect_from(
            server,
            port,
            local_address,
            validate_peer=validate_peer if client_identity is not None else None,
            **options,
        )
    async with connection as peer:
        if client_identity is None:
            validate_peer(peer.certificates)
        yield peer


def _new_connection(
    configuration, validate_peer, session_ticket_handler, token_handler
):
    from aioquic import tls
    from aioquic.quic.connection import QuicConnection

    class AuthenticatedConnection(QuicConnection):
        def _initialize(self, peer_cid):
            super()._initialize(peer_cid)
            context = self.tls
            original = context._client_handle_certificate_verify

            def verify_before_client_identity(input_buf):
                original(input_buf)
                try:
                    validate_peer(
                        (context._peer_certificate, *context._peer_certificate_chain)
                    )
                except (WireError, ValueError) as exc:
                    self._dns_peer_error = exc
                    raise tls.AlertBadCertificate(str(exc)) from exc

            # aioquic has no public per-connection certificate validation hook.
            # Running this before Finished prevents sending a client certificate
            # to a server that fails CRL, chain, or identity policy.
            context._client_handle_certificate_verify = verify_before_client_identity

    cls = QuicConnection if validate_peer is None else AuthenticatedConnection
    return cls(
        configuration=configuration,
        token_handler=token_handler,
        session_ticket_handler=session_ticket_handler,
    )


@asynccontextmanager
async def _connect_from(
    server,
    port,
    local_address,
    *,
    configuration,
    create_protocol,
    token_handler,
    local_port,
    validate_peer=None,
    session_ticket_handler=None,
    socket_factory=socket.socket,
):
    loop = asyncio.get_running_loop()
    local = None
    family = socket.AF_UNSPEC
    if local_address is not None:
        family, _, _, _, local = (
            await loop.getaddrinfo(
                local_address,
                local_port,
                type=socket.SOCK_DGRAM,
                flags=socket.AI_NUMERICHOST,
            )
        )[0]
    family, kind, _, _, peer_address = (
        await loop.getaddrinfo(server, port, family=family, type=socket.SOCK_DGRAM)
    )[0]
    if local is None:
        local = (
            ("::", local_port, 0, 0)
            if family == socket.AF_INET6
            else ("0.0.0.0", local_port)
        )

    connection = _new_connection(
        configuration, validate_peer, session_ticket_handler, token_handler
    )
    sock = socket_factory(family, kind, 0)
    try:
        sock.bind(local)
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: create_protocol(connection),
            sock=sock,
        )
    except BaseException:
        sock.close()
        raise
    try:
        protocol.connect(peer_address)
        await protocol.wait_connected()
        yield protocol
    finally:
        protocol.close()
        try:
            await protocol.wait_closed()
        finally:
            transport.close()


async def verify_quic_resolver(
    address: str,
    port: int,
    server_name: str,
    alpn: str,
    *,
    timeout: float,
    ca_data: bytes,
) -> None:
    async def probe() -> None:
        async with _verified_quic_connection(
            address,
            port,
            [alpn],
            server_name=server_name,
            ca_data=ca_data,
            certificate_ip=address,
        ):
            pass

    if alpn not in ("doq", "h3"):
        raise ValueError("unsupported QUIC DNS discovery ALPN")
    await asyncio.wait_for(probe(), timeout=remaining(deadline_after(timeout)))

import asyncio
import hmac
import ipaddress
import socket
import ssl
import struct
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Event

import pytest

pytest.importorskip("tba_provider_dns_txt")

from tba_codec_dns.edns import (
    ClientSubnet,
    Cookie,
    ExtendedError,
    decoded_option,
)
from tba_codec_dns.rdata import decoded, from_tokens
from tba_codec_dns.wire import (
    EdnsOption,
    Message,
    Question,
    RecordClass,
    RecordType,
    WireError,
    make_query,
    make_response,
)
from tba_concrete_dns_zone.btreezone import Zone as BTreeZone
from tba_concrete_dns_zone.zone import VersionedZone, Zone, read_rrsets
from tba_primitives_dns_name.names import (
    common_ancestor,
    concatenate,
    encode_idna2008,
    is_absolute_text,
    name_text,
    parent,
    parse_name,
    relativize,
)
from tba_protocol_dns.ddr import try_ddr, try_ddr_async
from tba_protocol_dns.dnssec import (
    Policy,
    ValidationError,
    key_tag,
    make_dnskey,
    make_ds,
    nsec3_hash,
    sign_rrset,
    validate_rrsig,
)
from tba_protocol_dns.update import Update, send_update
from tba_protocol_dns.xfr import transfer
from tba_protocol_dns.zonemd import make_zonemd, verify_zonemd
from tba_provider_dns_resolver import async_transport
from tba_provider_dns_resolver.client import (
    AsyncResolver,
    Cache,
    Resolver,
)
from tba_provider_dns_resolver.transport import (
    DnsStream,
    deadline_after,
    https_query,
    quic_query,
    quic_session,
    receive_tcp,
    receive_udp,
    send_tcp,
    send_udp,
    tcp_query,
    tls_query,
    udp_query,
)
from tba_provider_dns_resolver.tsig import GssTsigKey, TsigError, TsigKey, sign, verify
from tba_provider_dns_txt import DnsTxtResolver, TxtResult, TxtStatus


def _response(query, *, flags=0x8180, answers=()):
    return (
        query[:2]
        + struct.pack("!5H", flags, 1, len(answers), 0, 0)
        + query[12:]
        + b"".join(answers)
    )


def _record(rdtype, data, *, name=b"\xc0\x0c"):
    return name + struct.pack("!HHIH", rdtype, 1, 60, len(data)) + data


def test_dns_tcp_fallback_preserves_txt_segments_and_aliases(monkeypatch):
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp,
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        tcp.bind(("127.0.0.1", 0))
        tcp.listen()
        tcp.settimeout(3)
        udp.bind(("127.0.0.1", 0))
        udp.settimeout(3)
        udp_address = udp.getsockname()
        connect = socket.create_connection

        def connect_tcp(address, *, timeout):
            assert address == udp_address
            # Windows can reserve ephemeral ports independently for UDP and TCP.
            return connect(tcp.getsockname(), timeout=timeout)

        monkeypatch.setattr(socket, "create_connection", connect_tcp)

        def serve():
            request, peer = udp.recvfrom(512)
            udp.sendto(_response(request, flags=0x8380), peer)
            connection, _ = tcp.accept()
            with connection, connection.makefile("rb") as stream:
                connection.settimeout(3)
                query = stream.read(int.from_bytes(stream.read(2), "big"))
                target = b"\x05alias\xc0\x0c"
                response = _response(
                    query,
                    answers=(
                        _record(5, target),
                        _record(16, b"\x01a\x01b", name=target),
                        _record(16, b"\x01c", name=target),
                    ),
                )
                connection.sendall(len(response).to_bytes(2, "big") + response)

        server = worker.submit(serve)
        resolver = DnsTxtResolver(
            resolver=Resolver(["127.0.0.1"], port=udp_address[1], timeout=3)
        )
        assert resolver.lookup_txt("example.com") == TxtResult(
            TxtStatus.FOUND, (b"ab", b"c")
        )
        server.result(timeout=3)


@pytest.mark.parametrize("native", [False, True])
def test_dns_async_query_ignores_nonmatching_udp_reply(native):
    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        udp.bind(("127.0.0.1", 0))
        udp.settimeout(3)

        def serve():
            query, peer = udp.recvfrom(512)
            answers = (_record(1, b"\xc0\x00\x02\x01"),)
            wrong_question = query[:-4] + struct.pack("!HH", 28, 1)
            udp.sendto(_response(wrong_question, answers=answers), peer)
            udp.sendto(_response(query, answers=answers), peer)

        server = worker.submit(serve)
        question = Question.from_text("example.com", "A")
        port = udp.getsockname()[1]
        if native:
            message = asyncio.run(
                async_transport.udp_query(
                    question.query_message(44), "127.0.0.1", port=port
                )
            )
        else:
            resolver = AsyncResolver(["127.0.0.1"], port=port)
            message = asyncio.run(resolver.query(question))
        assert message.answers[0].data == b"\xc0\x00\x02\x01"
        server.result(timeout=3)


_ZONE = r"""
$ORIGIN example.
$TTL 1h
@ IN SOA ns hostmaster ( 1 2h 15m 4w 60 )
  NS ns
ns A 192.0.2.53
@ MX 10 mail
@ TXT "a;b" "x\046y"
unknown TYPE65400 \# 2 AABB
$GENERATE 1-2 item$ IN A 192.0.2.$
"""


def test_master_file_round_trip_and_atomic_zone_changes():
    zone = Zone.from_text(_ZONE)
    assert zone.get("@", "SOA").ttl == 3600
    assert decoded(zone.get("@", "TXT").records[0]) == ((b"a;b", b"x.y"),)
    assert decoded(zone.get("item2", "A").records[0]) == (
        ipaddress.IPv4Address("192.0.2.2"),
    )
    assert zone.get("unknown", 65400).records[0].data == b"\xaa\xbb"
    assert Zone.from_text(zone.to_text(), "example.").to_text() == zone.to_text()
    with pytest.raises(RuntimeError, match="changed during transaction"):
        with zone.transaction() as first:
            first.delete(zone.origin, "MX")
            with zone.transaction() as second:
                second.delete(zone.origin, "TXT")
    assert zone.get("@", "MX") is not None
    assert zone.get("@", "TXT") is None
    parsed = parse_name(r"\@.a\.b.\200.")
    assert parse_name(name_text(parsed)) == parsed


def test_edns_options_and_compressed_record_serialization():
    question = Question.from_text("example.", "MX")
    packet = question.query_wire(
        42, want_dnssec=True, edns_options=(EdnsOption(12, b"\0\0"),)
    )
    query = Message.from_wire(packet)
    assert query.edns.flags == 0x8000
    assert query.edns.options == (EdnsOption(12, b"\0\0"),)
    assert query.to_wire() == packet
    response = Message.from_wire(
        _response(question.query_wire(42), answers=(_record(15, b"\0\x0a\xc0\x0c"),))
    )
    assert decoded(response.answers[0]) == (10, (b"example",))
    expanded = Message.from_wire(response.to_wire())
    assert expanded.answers[0].data == b"\0\x0a\x07example\0"
    with pytest.raises(WireError, match="compression pointer"):
        Message.from_wire(
            _response(
                question.query_wire(42), answers=(_record(1, b"", name=b"\xc0\xff"),)
            )
        )


def _tcp_fixture(listener, reply):
    connection, _ = listener.accept()
    with connection:
        channel = DnsStream(connection, deadline_after(5))
        query = channel.receive()
        for packet in reply(query):
            channel.send(packet)


def test_tsig_and_update_round_trip():
    key = TsigKey((b"key", b"example"), b"fixture test secret")
    update = Update("example.")
    owner = parse_name("host.example.")
    address = from_tokens(owner, 300, "IN", "A", ["192.0.2.44"])
    update.absent("other", "A")
    update.replace(address)
    update.delete_values(replace(address, data=b"\xc0\x00\x02\x20"))
    unsigned = update.message(123).to_wire()
    signed, mac = sign(unsigned, key, now=100)
    assert verify(signed, key, now=101).mac == mac
    with pytest.raises(TsigError):
        verify(signed, key, now=401)
    tampered = signed.replace(b"\xc0\x00\x02\x2c", b"\xc0\x00\x02\x2d", 1)
    assert tampered != signed
    with pytest.raises(TsigError, match="digest"):
        verify(tampered, key, now=101)

    def reply(packet):
        incoming = Message.from_wire(packet)
        request_mac = verify(packet, key).mac
        assert incoming.opcode == 5
        assert incoming.answers[0].rdclass == RecordClass.NONE
        assert [rr.rdclass for rr in incoming.authority] == [
            RecordClass.ANY,
            RecordClass.IN,
            RecordClass.NONE,
        ]
        response = Message(incoming.id, incoming.flags | 0x8000, incoming.questions)
        yield sign(response.to_wire(), key, request_mac=request_mac)[0]

    with socket.socket() as sock, ThreadPoolExecutor(max_workers=1) as worker:
        sock.bind(("127.0.0.1", 0))
        sock.listen()
        sock.settimeout(5)
        server = worker.submit(_tcp_fixture, sock, reply)
        assert (
            send_update(update, "127.0.0.1", port=sock.getsockname()[1], key=key).rcode
            == 0
        )
        server.result(timeout=5)


@pytest.mark.parametrize("incremental", [False, True])
@pytest.mark.parametrize("zone_type", [Zone, BTreeZone])
def test_zone_transfers_commit_verified_snapshot(incremental, zone_type):
    base = zone_type.from_text(_ZONE)
    previous = base.get("@", "SOA").records[0]
    current = from_tokens(
        base.origin,
        3600,
        "IN",
        "SOA",
        ["ns", "hostmaster", "2", "7200", "900", "2419200", "60"],
        origin=base.origin,
    )
    old = base.get("ns", "A").records[0]
    new = replace(old, data=b"\xc0\x00\x02\x36")

    def reply(packet):
        query = Message.from_wire(packet)
        assert query.questions[0].type == (
            RecordType.IXFR if incremental else RecordType.AXFR
        )
        first = (
            (current, previous, old)
            if incremental
            else (current, *base.get("@", "NS").records)
        )
        second = (current, new, current) if incremental else (new, current)
        yield Message(query.id, 0x8400, query.questions, first).to_wire()
        yield Message(query.id, 0x8400, answers=second).to_wire()

    with socket.socket() as sock, ThreadPoolExecutor(max_workers=1) as worker:
        sock.bind(("127.0.0.1", 0))
        sock.listen()
        sock.settimeout(5)
        server = worker.submit(_tcp_fixture, sock, reply)
        received = transfer(
            "example.",
            "127.0.0.1",
            port=sock.getsockname()[1],
            base_soa=previous if incremental else None,
        )
        server.result(timeout=5)
    result = received.apply(base if incremental else None)
    assert result.get("ns", "A").records[0].data == new.data
    assert decoded(result.get("@", "SOA").records[0])[2] == 2
    assert base.get("ns", "A").records[0].data == old.data
    with base.reader() as original:
        received.apply_to(base)
        assert original.get("ns", "A")[0].data == old.data
        assert base.get("ns", "A").records[0].data == new.data
    if incremental:
        with pytest.raises(ValueError, match="IXFR baseline"):
            received.apply_to(base)


def test_dnssec_signing_verification_and_rfc_nsec3_vector():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    private = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
    key = make_dnskey("example.", private.public_key(), 15)
    address = from_tokens(parse_name("WwW.example."), 300, "IN", "A", ["192.0.2.42"])
    signature = sign_rrset((address,), key, private, inception=100, expiration=300)
    validate_rrsig((address,), signature, (key,), now=200)
    with pytest.raises(ValidationError, match="validity period"):
        validate_rrsig((address,), signature, (key,), now=400)
    with pytest.raises(ValidationError, match="no DNSKEY"):
        validate_rrsig(
            (replace(address, data=b"\xc0\x00\x02\x11"),), signature, (key,), now=200
        )
    assert decoded(make_ds(key))[0:3] == (key_tag(key), 15, 2)
    assert nsec3_hash("example.", "AABBCCDD", 12) == "0P9MHAVEQVM6T7VBL5LOP2U3T2RP3TOM"


def test_dns_search_and_cache_over_udp(monkeypatch):
    from tba_provider_dns_resolver import _cache, client

    clock = [1000.0]
    monkeypatch.setattr(_cache, "monotonic", lambda: clock[0])
    monkeypatch.setattr(client, "remaining", lambda _: 2)
    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        udp.bind(("127.0.0.1", 0))
        udp.settimeout(5)

        def serve():
            for _ in range(2):
                packet, peer = udp.recvfrom(512)
                assert Message.from_wire(packet).questions[0].name == parse_name(
                    "local.example."
                )
                udp.sendto(
                    _response(packet, answers=(_record(1, b"\xc0\x00\x02\x01"),)), peer
                )

        server = worker.submit(serve)
        resolver = Resolver(
            ["127.0.0.1"],
            port=udp.getsockname()[1],
            search=["example."],
            cache=Cache(2),
        )
        assert resolver.resolve("local", search=True).ttl == 60
        clock[0] += 5
        assert resolver.resolve("local", search=True).ttl == 55
        clock[0] += 60
        assert resolver.resolve("local", search=True).ttl == 60
        server.result(timeout=5)


@pytest.fixture
def dns_tls_identity(tmp_path):
    return _make_dns_tls_identity(tmp_path)


def _make_dns_tls_identity(tmp_path, *, include_ip=True):
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric.ec import (
        SECP256R1,
        generate_private_key,
    )
    from cryptography.x509.oid import NameOID

    private = generate_private_key(SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    now = datetime.now(timezone.utc)
    identities = [x509.DNSName("localhost")]
    if include_ip:
        identities.append(x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")))
    certificate = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=1))
        .add_extension(x509.SubjectAlternativeName(identities), critical=False)
        .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
        .sign(private, hashes.SHA256())
    )
    cert_file = tmp_path / "loopback.crt"
    key_file = tmp_path / "loopback.key"
    cert_file.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    key_file.write_bytes(
        private.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    return str(cert_file), str(key_file)


def _address_response(packet):
    return _response(packet, answers=(_record(1, b"\xc0\x00\x02\x01"),))


def _authenticated_address_response(packet, key, identifier=0):
    request = Message.from_wire(packet)
    assert request.id == identifier
    authentication = verify(packet, key)
    assert authentication.original_id == identifier
    address = from_tokens(request.questions[0].name, 60, "IN", "A", ("192.0.2.1",))
    response = replace(make_response(request), answers=(address,))
    return sign(response.to_wire(), key, request_mac=authentication.mac)[0]


def test_tcp_helpers_leave_persistent_socket_open_and_restore_timeout():
    client, peer = socket.socketpair()
    with client, peer, ThreadPoolExecutor(max_workers=1) as worker:
        client.settimeout(7)

        def serve():
            for _ in range(2):
                request, _ = receive_tcp(peer)
                count, _ = send_tcp(peer, make_response(request))
                assert count == len(make_response(request).to_wire()) + 2

        completion = worker.submit(serve)
        for identifier in (1, 2):
            query = make_query("example.", identifier=identifier)
            assert tcp_query(query, "unused.invalid", sock=client).id == identifier
            assert client.gettimeout() == 7
        completion.result(timeout=5)


def test_caller_owned_udp_socket_ignores_bad_replies_and_remains_open():
    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client,
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        peer.bind(("127.0.0.1", 0))
        peer.settimeout(5)
        client.settimeout(7)

        def serve():
            packet, address = peer.recvfrom(65535)
            peer.sendto(b"bad packet", address)
            peer.sendto(_address_response(packet) + b"extra", address)

        completion = worker.submit(serve)
        query = make_query("example.", identifier=117)
        reply = udp_query(
            query,
            "127.0.0.1",
            port=peer.getsockname()[1],
            sock=client,
            ignore_trailing=True,
        )
        assert query.is_response(reply)
        assert decoded(reply.answers[0]) == (ipaddress.IPv4Address("192.0.2.1"),)
        assert client.gettimeout() == 7
        completion.result(timeout=5)


@pytest.mark.parametrize("backend", ["sync", "trio", "sync-query"])
def test_verified_dns_over_tls(dns_tls_identity, backend, monkeypatch):
    cert_file, key_file = dns_tls_identity
    server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_context.load_cert_chain(cert_file, key_file)
    client_context = ssl.create_default_context(cafile=cert_file)
    query = Message(42, 0x0100, (Question.from_text("example.", "A"),))
    with socket.socket() as sock, ThreadPoolExecutor(max_workers=1) as worker:
        sock.bind(("127.0.0.1", 0))
        sock.listen()
        sock.settimeout(5)

        def serve():
            connection, _ = sock.accept()
            with (
                connection,
                server_context.wrap_socket(connection, server_side=True) as secure,
            ):
                channel = DnsStream(secure, deadline_after(5))
                channel.send(_address_response(channel.receive()))

        server = worker.submit(serve)
        options = dict(
            port=sock.getsockname()[1],
            server_name="localhost",
            context=client_context,
            certificate_ip="127.0.0.1",
        )
        if backend == "trio":
            import trio

            async def exchange():
                return await async_transport.tls_query(
                    query, "127.0.0.1", source=("127.0.0.1", 0), **options
                )

            result = trio.run(exchange)
        elif backend == "sync-query":
            from tba_provider_dns_resolver import query as sync

            calls = []

            def factory(af, kind, proto):
                calls.append((af, kind, proto))
                return socket.socket(af, kind, proto)

            monkeypatch.setattr(sync, "socket_factory", factory)
            result = sync.tls(
                query,
                "127.0.0.1",
                timeout=3,
                port=options["port"],
                ssl_context=client_context,
                server_hostname="localhost",
            )
            assert calls == [(socket.AF_INET, socket.SOCK_STREAM, 0)]
        else:
            result = tls_query(query, "127.0.0.1", **options)
        assert result.id == 42
        assert decoded(result.answers[0]) == (ipaddress.IPv4Address("192.0.2.1"),)
        server.result(timeout=5)


def _source_tcp_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.mark.parametrize("post", [False, True])
@pytest.mark.parametrize("signed", [False, True])
@pytest.mark.parametrize("bound", [False, True])
@pytest.mark.parametrize("sync_query", [False, True])
def test_verified_dns_over_https(dns_tls_identity, post, signed, bound, sync_query):
    import base64
    from urllib.parse import parse_qs, urlsplit

    cert_file, key_file = dns_tls_identity
    server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_context.minimum_version = ssl.TLSVersion.TLSv1_2
    server_context.load_cert_chain(cert_file, key_file)
    client_context = ssl.create_default_context(cafile=cert_file)
    query = Message(43, 0x0100, (Question.from_text("example.", "A"),))
    key = TsigKey((b"fixture",), b"test HTTPS TSIG secret")

    source_port = _source_tcp_port() if bound else 0

    class Peer(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _reply(self, packet):
            if bound:
                assert self.client_address == ("127.0.0.1", source_port)
            assert self.headers.get("Accept") == "application/dns-message"
            response = (
                _authenticated_address_response(packet, key, 43 if sync_query else 0)
                if signed
                else _address_response(packet)
            )
            self.send_response(202 if sync_query else 200)
            if not sync_query:
                self.send_header("Content-Type", "application/dns-message")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        def do_POST(self):
            assert self.headers.get("Content-Type") == "application/dns-message"
            self._reply(self.rfile.read(int(self.headers["Content-Length"])))

        def do_GET(self):
            encoded = parse_qs(urlsplit(self.path).query)["dns"][0]
            self._reply(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))

    with (
        HTTPServer(("127.0.0.1", 0), Peer) as peer,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        peer.socket = server_context.wrap_socket(peer.socket, server_side=True)
        peer.timeout = 5
        server = worker.submit(peer.handle_request)
        url = f"https://127.0.0.1:{peer.server_port}/dns-query"
        if sync_query:
            from tba_provider_dns_resolver import query as sync

            result = sync.https(
                query.use_tsig(key) if signed else query,
                url,
                timeout=3,
                post=post,
                verify=client_context,
                http_version=1,
                source="127.0.0.1" if bound else None,
                source_port=source_port,
            )
            if signed:
                assert result.tsig_key == key
        elif bound:
            from tba_provider_dns_resolver import asyncquery

            if signed:
                query = replace(query, id=0).use_tsig(key)
            result = asyncio.run(
                asyncquery.https(
                    query,
                    url,
                    timeout=3,
                    post=post,
                    verify=client_context,
                    source="127.0.0.1",
                    source_port=source_port,
                )
            )
        elif signed:
            from tba_provider_dns_resolver.client import HttpsNameserver

            resolver = Resolver(
                [HttpsNameserver(url, post=post, context=client_context)]
            )
            resolver.use_tsig(key)
            result = resolver.query(query.questions[0])
        else:
            result = https_query(query, url, post=post, context=client_context)
        assert result.id == (0 if signed and not sync_query else 43)
        assert decoded(result.answers[0]) == (ipaddress.IPv4Address("192.0.2.1"),)
        server.result(timeout=5)


@pytest.mark.parametrize("backend", ["sync", "asyncio", "sync-query"])
def test_borrowed_https_session_reuses_tls_connection(dns_tls_identity, backend):
    import httpx

    cert_file, key_file = dns_tls_identity
    server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_context.minimum_version = ssl.TLSVersion.TLSv1_2
    server_context.load_cert_chain(cert_file, key_file)
    trust = ssl.create_default_context(cafile=cert_file)
    endpoints = []

    class Peer(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self):
            endpoints.append(self.client_address)
            response = _address_response(
                self.rfile.read(int(self.headers["Content-Length"]))
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/dns-message")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    with (
        HTTPServer(("127.0.0.1", 0), Peer) as peer,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        peer.socket = server_context.wrap_socket(peer.socket, server_side=True)
        peer.timeout = 5
        exchange = worker.submit(peer.handle_request)
        url = f"https://127.0.0.1:{peer.server_port}/dns-query"
        queries = [make_query("example.", identifier=i) for i in (1, 2)]
        if backend in ("sync", "sync-query"):
            from tba_provider_dns_resolver import query as sync

            exchange_query = sync.https if backend == "sync-query" else https_query
            with httpx.Client(verify=trust, trust_env=False) as session:
                results = [
                    exchange_query(query, url, session=session) for query in queries
                ]
                assert not session.is_closed
        else:

            async def run():
                async with httpx.AsyncClient(verify=trust, trust_env=False) as session:
                    return [
                        await async_transport.https_query(query, url, session=session)
                        for query in queries
                    ]

            results = asyncio.run(run())
        exchange.result(timeout=5)
        assert [result.id for result in results] == [1, 2]
        assert len(endpoints) == 2 and endpoints[0] == endpoints[1]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mode",
    [
        "plain",
        "signed",
        "reuse",
        "source",
        "signed-asyncquery",
        "signed-borrowed",
        "signed-trio",
        "signed-session",
        "bad-mac",
        "sync",
        "sync-wire",
        "sync-manager",
        "asyncio-manager",
        "trio-manager",
        "trio-native",
    ],
)
async def test_verified_dns_over_quic(dns_tls_identity, mode, monkeypatch):
    pytest.importorskip("aioquic")
    from aioquic.asyncio import serve
    from aioquic.quic.configuration import QuicConfiguration

    cert_file, key_file = dns_tls_identity
    config = QuicConfiguration(is_client=False, alpn_protocols=["doq"])
    config.load_cert_chain(cert_file, key_file)
    query = Message(44, 0x0100, (Question.from_text("example.", "A"),))
    key = TsigKey((b"fixture",), b"test QUIC TSIG secret")
    async_signed_modes = (
        "signed-asyncquery",
        "signed-borrowed",
        "signed-trio",
        "signed-session",
        "bad-mac",
    )
    signed = mode in async_signed_modes or mode in ("signed", "sync", "sync-wire")
    tasks = []

    async def handle(reader, writer):
        length = int.from_bytes(await reader.readexactly(2), "big")
        packet = await reader.readexactly(length)
        assert Message.from_wire(packet).id == 0
        assert await reader.read() == b""
        response = (
            _authenticated_address_response(packet, key)
            if signed
            else _address_response(packet)
        )
        if mode == "bad-mac":
            response = response[:-8] + bytes([response[-8] ^ 1]) + response[-7:]
        writer.write(len(response).to_bytes(2, "big") + response)
        writer.write_eof()

    def on_stream(reader, writer):
        tasks.append(asyncio.create_task(handle(reader, writer)))

    from aioquic.asyncio import QuicConnectionProtocol
    from aioquic.quic.events import HandshakeCompleted

    sources = []
    handshakes = []

    class SourceObservingProtocol(QuicConnectionProtocol):
        def datagram_received(self, data, addr):
            sources.append(addr)
            super().datagram_received(data, addr)

        def quic_event_received(self, event):
            if isinstance(event, HandshakeCompleted):
                handshakes.append(event)
            super().quic_event_received(event)

    server = await serve(
        "127.0.0.1",
        0,
        configuration=config,
        stream_handler=on_stream,
        create_protocol=SourceObservingProtocol,
    )
    port = server._transport.get_extra_info("sockname")[1]
    try:
        if mode == "reuse":
            async with quic_session(
                "127.0.0.1", port=port, server_name="localhost", ca_file=cert_file
            ) as session:
                first, result = await asyncio.gather(
                    session.query(replace(query, id=43)), session.query(query)
                )
                assert first.id == 43
                assert len(tasks) == 2
        elif mode in ("asyncio-manager", "trio-manager"):
            from tba_provider_dns_resolver import asyncquery, quic

            async def run():
                context, make_manager = quic.factories_for_backend()
                async with context() as backend_context:
                    async with make_manager(
                        backend_context, verify_mode=cert_file, server_name="localhost"
                    ) as manager:
                        connection = manager.connect(
                            "127.0.0.1", port, source="127.0.0.1"
                        )
                        assert manager.connect("127.0.0.1", port) is connection
                        replies = {}

                        async def call(identifier):
                            replies[identifier] = await asyncquery.quic(
                                replace(query, id=identifier),
                                "127.0.0.1",
                                timeout=3,
                                connection=connection,
                            )

                        if mode == "trio-manager":
                            import trio

                            async with trio.open_nursery() as nursery:
                                nursery.start_soon(call, 43)
                                nursery.start_soon(call, 44)
                        else:
                            await asyncio.gather(call(43), call(44))
                        assert replies[43].id == 43
                    with pytest.raises(RuntimeError, match="closed"):
                        manager.connect("127.0.0.1", port)
                return replies[44]

            if mode == "trio-manager":
                import trio

                result = await asyncio.to_thread(trio.run, run)
            else:
                result = await run()
            assert len(tasks) == 2 and len(handshakes) == 1
        elif mode == "sync-manager":
            from tba_provider_dns_resolver import query as sync
            from tba_provider_dns_resolver import quic

            created = []

            def factory(af, kind, proto):
                sock = socket.socket(af, kind, proto)
                created.append(sock)
                return sock

            monkeypatch.setattr(quic, "socket_factory", factory)

            def exchange():
                manager = quic.SyncQuicManager(
                    verify_mode=cert_file, server_name="localhost"
                )
                with manager, ThreadPoolExecutor(max_workers=2) as worker:
                    connection = manager.connect("127.0.0.1", port, source="127.0.0.1")
                    assert manager.connect("127.0.0.1", port) is connection
                    replies = [
                        worker.submit(
                            sync.quic,
                            replace(query, id=identifier),
                            "127.0.0.1",
                            timeout=3,
                            connection=connection,
                        )
                        for identifier in (45, 44)
                    ]
                    first, last = [reply.result(timeout=5) for reply in replies]
                    assert first.id == 45
                with pytest.raises(RuntimeError, match="closed"):
                    manager.connect("127.0.0.1", port)
                return last

            result = await asyncio.to_thread(exchange)
            assert len(tasks) == 2 and len(handshakes) == 1
            assert len(created) == 1 and created[0].fileno() == -1
        elif mode in ("source", "sync", "sync-wire", "trio-native"):
            from tba_provider_dns_resolver import asyncquery

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as binding:
                binding.bind(("127.0.0.1", 0))
                expected = binding.getsockname()
            options = dict(
                timeout=3,
                port=port,
                source=expected[0],
                source_port=expected[1],
                hostname="localhost",
                verify=cert_file,
            )
            if mode == "sync":
                from tba_codec_dns import message as editable
                from tba_provider_dns_resolver import query as sync

                signed_query = editable.make_query("example.", id=44)
                signed_query.use_tsig(key)
                result = await asyncio.to_thread(
                    sync.quic, signed_query, "127.0.0.1", **options
                )
                assert signed_query.id == 0
                assert result.keyring == key
                result = result._wire_message()
            elif mode == "sync-wire":
                from tba_provider_dns_resolver import query as sync

                result = await asyncio.to_thread(
                    sync.quic, query.use_tsig(key), "127.0.0.1", **options
                )
                assert result.tsig_key == key
            elif mode == "trio-native":
                import trio

                async def exchange():
                    return await asyncquery.quic(query, "127.0.0.1", **options)

                result = await asyncio.to_thread(trio.run, exchange)
            else:
                result = await asyncquery.quic(query, "127.0.0.1", **options)
            assert sources and set(sources) == {expected}
        elif mode in async_signed_modes:
            from tba_codec_dns.tsig import TsigError
            from tba_provider_dns_resolver import asyncquery

            signed_query = query.use_tsig(key, original_id=44)
            options = dict(
                timeout=3,
                port=port,
                hostname="localhost",
                verify=cert_file,
            )
            if mode == "signed-borrowed":
                from tba_codec_dns import message as editable
                from tba_provider_dns_resolver.quic import AsyncioQuicManager

                signed_query = editable.make_query("example.", id=44)
                signed_query.use_tsig(key)
                assert verify(signed_query.to_wire(), key).original_id == 44
                async with AsyncioQuicManager(
                    verify_mode=cert_file, server_name="localhost"
                ) as manager:
                    connection = manager.connect("127.0.0.1", port)
                    reply = await asyncquery.quic(
                        signed_query, "127.0.0.1", connection=connection, **options
                    )
                assert signed_query.id == 0 and reply.keyring == key
                result = reply._wire_message()
            elif mode == "signed-trio":
                import trio

                async def exchange():
                    return await asyncquery.quic(signed_query, "127.0.0.1", **options)

                result = await asyncio.to_thread(trio.run, exchange)
            elif mode == "signed-session":
                async with quic_session(
                    "127.0.0.1", port=port, server_name="localhost", ca_file=cert_file
                ) as session:
                    result = await session.query(signed_query)
            elif mode == "bad-mac":
                with pytest.raises(TsigError):
                    await asyncquery.quic(signed_query, "127.0.0.1", **options)
                await asyncio.gather(*tasks)
                return
            else:
                result = await asyncquery.quic(signed_query, "127.0.0.1", **options)
            assert result.tsig_key == key
            assert signed_query.id == (0 if mode == "signed-borrowed" else 44)
        elif signed:
            from tba_provider_dns_resolver.client import QuicNameserver

            resolver = AsyncResolver(
                [QuicNameserver("127.0.0.1", "localhost", port, cert_file)]
            )
            resolver.use_tsig(key)
            result = await resolver.query(query.questions[0])
        else:
            result = await quic_query(
                query,
                "127.0.0.1",
                port=port,
                server_name="localhost",
                ca_file=cert_file,
            )
        assert result.id == (0 if signed else 44)
        assert decoded(result.answers[0]) == (ipaddress.IPv4Address("192.0.2.1"),)
        await asyncio.gather(*tasks)
    finally:
        server.close()


def test_sync_quic_handshake_timeout_releases_owned_socket(monkeypatch):
    from tba_provider_dns_resolver import quic

    created = []

    def factory(af, kind, proto):
        sock = socket.socket(af, kind, proto)
        created.append(sock)
        return sock

    monkeypatch.setattr(quic, "socket_factory", factory)
    with socket.socket(type=socket.SOCK_DGRAM) as silent:
        silent.bind(("127.0.0.1", 0))
        with quic.SyncQuicManager(verify_mode=False) as manager:
            connection = manager.connect(*silent.getsockname())
            with pytest.raises(TimeoutError):
                connection.make_stream(0.2)
        assert len(created) == 1 and created[0].fileno() == -1


@pytest.mark.parametrize("backend", ["asyncio", "trio"])
def test_async_quic_handshake_timeout_releases_connection(backend):
    from tba_provider_dns_resolver.quic import (
        AsyncioQuicManager,
        TrioQuicManager,
        UnexpectedEOF,
    )

    with socket.socket(type=socket.SOCK_DGRAM) as silent:
        silent.bind(("127.0.0.1", 0))
        endpoint = silent.getsockname()

        async def exercise():
            cls = TrioQuicManager if backend == "trio" else AsyncioQuicManager
            async with cls(verify_mode=False) as manager:
                connection = manager.connect(*endpoint)
                with pytest.raises(TimeoutError):
                    await connection.make_stream(0.05)
                assert manager.connect(*endpoint) is connection
            with pytest.raises(UnexpectedEOF):
                await connection.make_stream(0.05)

        if backend == "trio":
            import trio

            trio.run(exercise)
        else:
            asyncio.run(exercise())


@pytest.mark.parametrize(
    ("backend", "bootstrap"),
    [
        ("sync", False),
        ("asyncio", False),
        ("trio", False),
        ("asyncio", True),
        ("trio", True),
        ("asyncio-bound", True),
        ("trio-bound", False),
        ("sync-query-bound", True),
    ],
)
def test_verified_dns_over_http2(dns_tls_identity, backend, bootstrap):
    from h2.config import H2Configuration
    from h2.connection import H2Connection
    from h2.events import DataReceived, StreamEnded

    cert_file, key_file = dns_tls_identity
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    context.set_alpn_protocols(["h2"])
    finished = Event()
    bound = backend.endswith("-bound")
    source_port = _source_tcp_port() if bound else 0
    with socket.socket() as sock, ThreadPoolExecutor(max_workers=1) as worker:
        sock.bind(("127.0.0.1", 0))
        sock.listen()
        sock.settimeout(5)

        def serve():
            connection, address = sock.accept()
            if bound:
                assert address == ("127.0.0.1", source_port)
            with (
                connection,
                context.wrap_socket(connection, server_side=True) as secure,
            ):
                secure.settimeout(5)
                assert secure.selected_alpn_protocol() == "h2"
                h2 = H2Connection(config=H2Configuration(client_side=False))
                h2.initiate_connection()
                secure.sendall(h2.data_to_send())
                payload = bytearray()
                while True:
                    packet = secure.recv(65535)
                    assert packet
                    for event in h2.receive_data(packet):
                        if isinstance(event, DataReceived):
                            payload.extend(event.data)
                            h2.acknowledge_received_data(
                                event.flow_controlled_length, event.stream_id
                            )
                        if isinstance(event, StreamEnded):
                            h2.send_headers(
                                event.stream_id,
                                [
                                    (b":status", b"200"),
                                    (b"content-type", b"application/dns-message"),
                                ],
                            )
                            h2.send_data(
                                event.stream_id,
                                _address_response(bytes(payload)),
                                end_stream=True,
                            )
                            secure.sendall(h2.data_to_send())
                            finished.wait(5)
                            return
                    if pending := h2.data_to_send():
                        secure.sendall(pending)

        server = worker.submit(serve)
        query = Question.from_text("example.", "A").query_message(46)
        host = "localhost" if bootstrap else "127.0.0.1"
        endpoint = f"https://{host}:{sock.getsockname()[1]}/dns-query"
        options = dict(http_version=2, ca_file=cert_file)
        if bootstrap:
            options.update(bootstrap_address="127.0.0.1", certificate_ip="127.0.0.1")
        try:
            if backend == "sync":
                answer = https_query(query, endpoint, **options)
            elif backend == "sync-query-bound":
                from tba_provider_dns_resolver import query as sync

                answer = sync.https(
                    query,
                    endpoint,
                    timeout=3,
                    verify=cert_file,
                    http_version=2,
                    source="127.0.0.1",
                    source_port=source_port,
                    bootstrap_address=options["bootstrap_address"],
                )
                assert answer.id == 46
            else:

                async def exchange():
                    if bound:
                        from tba_provider_dns_resolver import asyncquery

                        return await asyncquery.https(
                            query,
                            endpoint,
                            timeout=3,
                            verify=cert_file,
                            http_version=2,
                            source="127.0.0.1",
                            source_port=source_port,
                            bootstrap_address=options.get("bootstrap_address"),
                        )
                    return await async_transport.https_query(query, endpoint, **options)

                if backend.startswith("trio"):
                    import trio

                    answer = trio.run(exchange)
                else:
                    answer = asyncio.run(exchange())
        finally:
            finished.set()
        assert decoded(answer.answers[0]) == (ipaddress.IPv4Address("192.0.2.1"),)
        server.result(timeout=5)


@pytest.mark.parametrize("http_version", [1, 2])
def test_https_bootstrap_pin_rejects_before_sending_dns(tmp_path, http_version):
    cert_file, key_file = _make_dns_tls_identity(tmp_path, include_ip=False)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert_file, key_file)
    context.num_tickets = 0
    if http_version == 2:
        context.set_alpn_protocols(["h2"])
    with socket.socket() as peer, ThreadPoolExecutor(max_workers=1) as worker:
        peer.bind(("127.0.0.1", 0))
        peer.listen()
        peer.settimeout(5)

        def receive():
            connection, _ = peer.accept()
            try:
                with (
                    connection,
                    context.wrap_socket(connection, server_side=True) as secure,
                ):
                    secure.settimeout(5)
                    return secure.recv(4096)
            except (ConnectionAbortedError, ConnectionResetError):
                return b""

        request = worker.submit(receive)
        with pytest.raises(WireError, match="certificate does not cover"):
            https_query(
                make_query("example."),
                f"https://localhost:{peer.getsockname()[1]}/dns-query",
                http_version=http_version,
                ca_file=cert_file,
                bootstrap_address="127.0.0.1",
                certificate_ip="127.0.0.1",
            )
        assert request.result(timeout=5) == b""


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "trust",
    [
        "file",
        "context",
        "sync-context",
        "sync-query-context",
        "sync-manager",
        "asyncio-manager",
        "trio-manager",
        "trio-native",
        "wrong-name",
        "fallback",
        "fallback-resolver",
        "sync-fallback",
        "sync-fallback-resolver",
        "tsig-native",
        "tsig-borrowed",
        "tsig-fallback",
        "tsig-transport",
        "tsig-legacy-transport",
        "tsig-bad-mac",
        "missing-ca",
        "crl-leaf",
        "crl-chain",
        "revoked",
        "missing-crl",
        "no-hostname",
    ],
)
async def test_verified_dns_over_http3(dns_tls_identity, trust, tmp_path, monkeypatch):
    pytest.importorskip("aioquic")
    from aioquic.asyncio import QuicConnectionProtocol, serve
    from aioquic.h3.connection import H3_ALPN, H3Connection
    from aioquic.h3.events import DataReceived
    from aioquic.quic.configuration import QuicConfiguration

    cert_file, key_file = dns_tls_identity
    config = QuicConfiguration(is_client=False, alpn_protocols=H3_ALPN)
    if trust in ("crl-leaf", "crl-chain", "revoked"):
        from pathlib import Path

        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec

        issuer = x509.load_pem_x509_certificate(Path(cert_file).read_bytes())
        issuer_key = serialization.load_pem_private_key(
            Path(key_file).read_bytes(), password=None
        )
        private = ec.generate_private_key(ec.SECP256R1())
        now = datetime.now(timezone.utc)
        leaf = (
            x509.CertificateBuilder()
            .subject_name(
                x509.Name(
                    [x509.NameAttribute(x509.NameOID.COMMON_NAME, "DNS test leaf")]
                )
            )
            .issuer_name(issuer.subject)
            .public_key(private.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - timedelta(days=1))
            .not_valid_after(now + timedelta(days=1))
            .add_extension(
                x509.BasicConstraints(ca=False, path_length=None), critical=True
            )
            .add_extension(
                x509.SubjectAlternativeName(
                    [x509.IPAddress(ipaddress.IPv4Address("127.0.0.1"))]
                ),
                critical=False,
            )
            .sign(issuer_key, hashes.SHA256())
        )
        config.certificate = leaf
        config.private_key = private
        builder = (
            x509.CertificateRevocationListBuilder()
            .issuer_name(issuer.subject)
            .last_update(now - timedelta(hours=1))
            .next_update(now + timedelta(days=1))
        )
        if trust == "revoked":
            builder = builder.add_revoked_certificate(
                x509.RevokedCertificateBuilder()
                .serial_number(leaf.serial_number)
                .revocation_date(now - timedelta(minutes=1))
                .build()
            )
        crl_file = tmp_path / "issuer.crl"
        crl_file.write_bytes(
            builder.sign(issuer_key, hashes.SHA256()).public_bytes(
                serialization.Encoding.PEM
            )
        )
    else:
        config.load_cert_chain(cert_file, key_file)
    requests = []
    key = TsigKey((b"fixture",), b"test HTTP/3 TSIG secret")

    class Peer(QuicConnectionProtocol):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.http = H3Connection(self._quic)
            self.bodies = {}

        def quic_event_received(self, event):
            for item in self.http.handle_event(event):
                if not isinstance(item, DataReceived):
                    continue
                body = self.bodies.setdefault(item.stream_id, bytearray())
                body.extend(item.data)
                if item.stream_ended:
                    packet = bytes(self.bodies.pop(item.stream_id))
                    requests.append(packet)
                    response = (
                        _authenticated_address_response(packet, key)
                        if trust.startswith("tsig-")
                        else _address_response(packet)
                    )
                    if trust == "tsig-bad-mac":
                        response = (
                            response[:-8] + bytes([response[-8] ^ 1]) + response[-7:]
                        )
                    self.http.send_headers(
                        item.stream_id,
                        [
                            (b":status", b"200"),
                            (b"content-type", b"application/dns-message"),
                        ],
                    )
                    self.http.send_data(
                        item.stream_id,
                        response,
                        end_stream=True,
                    )
                    self.transmit()

    server = await serve("127.0.0.1", 0, configuration=config, create_protocol=Peer)
    port = server._transport.get_extra_info("sockname")[1]
    try:
        query = Question.from_text("example.", "A").query_message(47)
        from tba_provider_dns_resolver import asyncquery

        url = f"https://127.0.0.1:{port}/dns-query"
        if trust.startswith("tsig-"):
            from tba_codec_dns.tsig import TsigError

            signed_query = query.use_tsig(key, original_id=query.id)
            options = dict(timeout=3, verify=cert_file, http_version=3)
            if trust == "tsig-borrowed":
                from tba_codec_dns import message as editable
                from tba_provider_dns_resolver.quic import AsyncioQuicManager

                request = editable.make_query("example.", id=47)
                request.use_tsig(key)
                assert verify(request.to_wire(), key).original_id == 47
                async with AsyncioQuicManager(
                    verify_mode=cert_file, h3=True
                ) as manager:
                    connection = manager.connect("127.0.0.1", port)
                    reply = await asyncquery.https(
                        request, url, client=connection, timeout=3
                    )
                assert request.id == 0 and reply.keyring == key
                answer = reply._wire_message()
            elif trust == "tsig-transport":
                answer = await async_transport.https_query(
                    signed_query, url, timeout=3, ca_file=cert_file, http_version=3
                )
            elif trust == "tsig-legacy-transport":
                from tba_provider_dns_resolver.transport import https3_query

                answer = await https3_query(
                    signed_query, url, timeout=3, ca_file=cert_file
                )
            elif trust == "tsig-bad-mac":
                with pytest.raises(TsigError):
                    await asyncquery.https(signed_query, url, **options)
                assert len(requests) == 1
                return
            else:
                if trust == "tsig-fallback":
                    monkeypatch.setattr(asyncquery, "have_doh", False)
                    del options["http_version"]
                answer = await asyncquery.https(signed_query, url, **options)
            assert signed_query.id == 47
            assert len(requests) == 1 and answer.id == 0 and answer.tsig_key == key
        elif trust == "file":
            answer = await async_transport.https_query(
                query, url, ca_file=cert_file, http_version=3
            )
        elif trust == "sync-context":
            from tba_provider_dns_resolver.transport import https_query

            context = ssl.create_default_context(cafile=cert_file)
            answer = await asyncio.to_thread(
                https_query, query, url, context=context, http_version=3
            )
        elif trust == "sync-query-context":
            from tba_provider_dns_resolver import query as sync

            context = ssl.create_default_context(cafile=cert_file)
            answer = await asyncio.to_thread(
                sync.https, query, url, timeout=3, verify=context, http_version=3
            )
            assert answer.id == query.id
        elif trust == "sync-manager":
            from tba_provider_dns_resolver import query as sync
            from tba_provider_dns_resolver.quic import SyncQuicManager

            def exercise():
                context = ssl.create_default_context(cafile=cert_file)
                with SyncQuicManager(
                    verify_mode=context, server_name="localhost", h3=True
                ) as manager:
                    peer = manager.connect("127.0.0.1", port)
                    with ThreadPoolExecutor(max_workers=2) as worker:
                        futures = [
                            worker.submit(
                                sync.https,
                                replace(query, id=identifier),
                                url,
                                session=peer,
                                timeout=3,
                            )
                            for identifier in (46, 47)
                        ]
                        first, last = [future.result(timeout=5) for future in futures]
                    assert first.id == 46
                    return last

            answer = await asyncio.to_thread(exercise)
            assert len(requests) == 2 and answer.id == 47
        elif trust in ("asyncio-manager", "trio-manager"):
            from tba_provider_dns_resolver.quic import (
                AsyncioQuicManager,
                TrioQuicManager,
            )

            async def exercise():
                manager_cls = (
                    TrioQuicManager if trust == "trio-manager" else AsyncioQuicManager
                )
                context = ssl.create_default_context(cafile=cert_file)
                async with manager_cls(
                    verify_mode=context, server_name="localhost", h3=True
                ) as manager:
                    connection = manager.connect("127.0.0.1", port)
                    first = await asyncquery.https(
                        replace(query, id=46), url, client=connection, timeout=3
                    )
                    assert first.id == 46
                    return await asyncquery.https(
                        query, url, client=connection, timeout=3
                    )

            if trust == "trio-manager":
                import trio

                answer = await asyncio.to_thread(trio.run, exercise)
            else:
                answer = await exercise()
            assert len(requests) == 2 and answer.id == 47
        elif trust == "trio-native":
            import trio

            async def exercise():
                return await asyncquery.https(
                    query, url, timeout=3, verify=cert_file, http_version=3
                )

            answer = await asyncio.to_thread(trio.run, exercise)
            assert len(requests) == 1
        elif trust in ("sync-fallback", "sync-fallback-resolver"):
            from tba_provider_dns_resolver import query as sync
            from tba_provider_dns_resolver import resolver

            if sync.have_doh:
                monkeypatch.setattr(sync, "have_doh", False)
            calls = []

            class BootstrapResolver:
                def resolve_name(self, hostname, *, family):
                    calls.append((hostname, family))
                    return ["127.0.0.1"]

            monkeypatch.setattr(resolver, "get_default_resolver", BootstrapResolver)
            if trust == "sync-fallback-resolver":
                url = f"https://localhost:{port}/dns-query"

            def exchange():
                options = dict(timeout=3, verify=cert_file, family=socket.AF_INET)
                response = sync.https(query, url, **options)
                for version in (sync.HTTPVersion.H1, sync.HTTPVersion.H2):
                    with pytest.raises(sync.NoDOH):
                        sync.https(query, url, http_version=version, **options)
                return response

            answer = await asyncio.to_thread(exchange)
            expected = (
                [("localhost", socket.AF_INET)]
                if trust == "sync-fallback-resolver"
                else []
            )
            assert calls == expected
            assert len(requests) == 1 and answer.id == 47
        elif trust in ("fallback", "fallback-resolver"):
            from tba_provider_dns_resolver import asyncresolver

            if asyncquery.have_doh:
                monkeypatch.setattr(asyncquery, "have_doh", False)
            calls = []

            class BootstrapResolver:
                async def resolve_name(self, hostname, *, family):
                    calls.append((hostname, family))
                    return ["127.0.0.1"]

            monkeypatch.setattr(
                asyncresolver, "get_default_resolver", BootstrapResolver
            )
            if trust == "fallback-resolver":
                url = f"https://localhost:{port}/dns-query"
            answer = await asyncquery.https(
                query, url, timeout=3, verify=cert_file, family=socket.AF_INET
            )
            for version in (asyncquery.HTTPVersion.H1, asyncquery.HTTPVersion.H2):
                with pytest.raises(asyncquery.NoDOH):
                    await asyncquery.https(
                        query, url, timeout=3, verify=cert_file, http_version=version
                    )
            expected = (
                [("localhost", socket.AF_INET)] if trust == "fallback-resolver" else []
            )
            assert calls == expected
            assert len(requests) == 1 and answer.id == 47
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            if trust == "missing-ca":
                with pytest.raises(ValueError, match="no exportable CA"):
                    await asyncquery.https(query, url, verify=context, http_version=3)
                return
            context.load_verify_locations(cert_file)
            if trust == "no-hostname":
                context.check_hostname = False
                answer = await asyncquery.https(
                    query,
                    f"https://wrong.invalid:{port}/dns-query",
                    timeout=2,
                    verify=context,
                    bootstrap_address="127.0.0.1",
                    http_version=3,
                )
                assert decoded(answer.answers[0]) == (
                    ipaddress.IPv4Address("192.0.2.1"),
                )
                return
            if trust == "missing-crl":
                context.verify_flags |= ssl.VERIFY_CRL_CHECK_LEAF
                with pytest.raises(ValueError, match="configure_http3_crls"):
                    await asyncquery.https(query, url, verify=context, http_version=3)
                return
            if trust in ("crl-leaf", "crl-chain", "revoked"):
                asyncquery.configure_http3_crls(context, crl_file)
                context.verify_flags |= (
                    ssl.VERIFY_CRL_CHECK_CHAIN
                    if trust == "crl-chain"
                    else ssl.VERIFY_CRL_CHECK_LEAF
                )
                if trust == "revoked":
                    with pytest.raises(WireError, match="certificate revoked"):
                        await asyncquery.https(
                            query, url, verify=context, http_version=3
                        )
                    assert not requests
                    return
            if trust == "wrong-name":
                with pytest.raises(ConnectionError):
                    await asyncquery.https(
                        query,
                        f"https://wrong.invalid:{port}/dns-query",
                        timeout=2,
                        verify=context,
                        http_version=3,
                        bootstrap_address="127.0.0.1",
                    )
                return
            answer = await asyncquery.https(query, url, verify=context, http_version=3)
        assert decoded(answer.answers[0]) == (ipaddress.IPv4Address("192.0.2.1"),)
    finally:
        server.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "identity",
    [
        "trusted",
        "sync-query",
        "shared-context",
        "combined-pem",
        "missing",
        "untrusted",
        "wrong-server",
    ],
)
async def test_native_http3_mutual_tls_against_quic_peer(
    dns_tls_identity, identity, tmp_path
):
    pytest.importorskip("aioquic")
    from pathlib import Path

    from aioquic import tls
    from aioquic.asyncio import QuicConnectionProtocol, serve
    from aioquic.h3.connection import H3_ALPN, H3Connection
    from aioquic.h3.events import DataReceived
    from aioquic.quic.configuration import QuicConfiguration
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from tba_provider_dns_resolver import asyncquery

    server_cert, server_key = dns_tls_identity
    client_ca_dir = tmp_path / "client-ca"
    client_ca_dir.mkdir()
    client_ca, client_ca_key = _make_dns_tls_identity(client_ca_dir)
    trust = Path(client_ca).read_bytes()
    issuer = x509.load_pem_x509_certificate(trust)
    issuer_key = serialization.load_pem_private_key(
        Path(client_ca_key).read_bytes(), None
    )
    private = ec.generate_private_key(ec.SECP256R1())
    now = datetime.now(timezone.utc)
    client_certificate = (
        x509.CertificateBuilder()
        .subject_name(
            x509.Name(
                [x509.NameAttribute(x509.NameOID.COMMON_NAME, "DNS HTTP3 client")]
            )
        )
        .issuer_name(issuer.subject)
        .public_key(private.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(hours=1))
        .not_valid_after(now + timedelta(hours=1))
        .add_extension(
            x509.ExtendedKeyUsage([x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH]),
            critical=False,
        )
        .sign(issuer_key, hashes.SHA256())
    )
    client_cert_file = tmp_path / "client.pem"
    client_key_file = tmp_path / "client-key.pem"
    client_cert_file.write_bytes(
        client_certificate.public_bytes(serialization.Encoding.PEM) + trust
    )
    client_key_file.write_bytes(
        private.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.BestAvailableEncryption(b"test password"),
        )
    )
    config = QuicConfiguration(is_client=False, alpn_protocols=H3_ALPN)
    config.load_cert_chain(server_cert, server_key)
    authenticated = []
    dns_requests = []

    class Peer(QuicConnectionProtocol):
        def __init__(self, connection, **kwargs):
            super().__init__(connection, **kwargs)
            self.http = H3Connection(connection)
            self.body = bytearray()
            initialize = connection._initialize

            def initialize_mtls(peer_cid):
                initialize(peer_cid)
                engine = connection.tls
                # This aioquic test peer explicitly requires a trusted client
                # certificate and the TLS engine verifies possession of its key.
                engine._request_client_certificate = True
                finish = engine._server_handle_finished

                def require_client_certificate(input_buf, output_buf):
                    cert = engine._peer_certificate
                    chain = engine._peer_certificate_chain
                    if cert is None:
                        raise tls.AlertBadCertificate("client certificate required")
                    tls.verify_certificate(
                        certificate=cert,
                        chain=chain,
                        cadata=Path(server_cert).read_bytes()
                        if identity == "untrusted"
                        else trust,
                    )
                    finish(input_buf, output_buf)
                    authenticated.append((cert.serial_number, len(chain)))

                engine._server_handle_finished = require_client_certificate

            connection._initialize = initialize_mtls

        def quic_event_received(self, event):
            for item in self.http.handle_event(event):
                if not isinstance(item, DataReceived):
                    continue
                self.body.extend(item.data)
                if item.stream_ended:
                    assert authenticated
                    dns_requests.append(bytes(self.body))
                    self.http.send_headers(
                        item.stream_id,
                        [
                            (b":status", b"200"),
                            (b"content-type", b"application/dns-message"),
                        ],
                    )
                    self.http.send_data(
                        item.stream_id,
                        _address_response(bytes(self.body)),
                        end_stream=True,
                    )
                    self.transmit()

    if identity in ("shared-context", "combined-pem"):
        context = asyncquery.HTTP3SSLContext()
        context.load_verify_locations(cafile=server_cert)
        calls = []

        def password():
            calls.append(True)
            return "test password"

        if identity == "combined-pem":
            combined = tmp_path / "combined.pem"
            combined.write_bytes(
                client_cert_file.read_bytes() + client_key_file.read_bytes()
            )
            context.load_cert_chain(combined, password=password)
        else:
            context.load_cert_chain(
                client_cert_file, client_key_file, password=password
            )
        assert calls == [True]
        with pytest.raises(ValueError, match="do not match"):
            context.load_cert_chain(client_cert_file, client_ca_key)

        tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        tls_context.load_cert_chain(server_cert, server_key)
        tls_context.load_verify_locations(cafile=client_ca)
        tls_context.verify_mode = ssl.CERT_REQUIRED
        tls_peer_cert = asyncio.get_running_loop().create_future()

        async def accept_tls(reader, writer):
            try:
                tls_object = writer.get_extra_info("ssl_object")
                tls_peer_cert.set_result(tls_object.getpeercert(binary_form=True))
                writer.write(b"verified")
                await writer.drain()
            finally:
                writer.close()
                await writer.wait_closed()

        async with await asyncio.start_server(
            accept_tls, "127.0.0.1", 0, ssl=tls_context
        ) as peer:
            local_port = peer.sockets[0].getsockname()[1]
            reader, writer = await asyncio.open_connection(
                "127.0.0.1", local_port, ssl=context
            )
            try:
                assert await asyncio.wait_for(reader.readexactly(8), 3) == b"verified"
                assert await asyncio.wait_for(
                    tls_peer_cert, 3
                ) == client_certificate.public_bytes(serialization.Encoding.DER)
            finally:
                writer.close()
                await writer.wait_closed()
    else:
        context = ssl.create_default_context(cafile=server_cert)
        if identity == "trusted":
            with pytest.raises(ValueError, match="do not match"):
                asyncquery.configure_http3_client_identity(
                    context, client_cert_file, client_ca_key
                )
        if identity != "missing":
            asyncquery.configure_http3_client_identity(
                context,
                client_cert_file,
                client_key_file,
                password="test password",
            )
    server = await serve("127.0.0.1", 0, configuration=config, create_protocol=Peer)
    port = server._transport.get_extra_info("sockname")[1]
    try:
        host = "wrong.invalid" if identity == "wrong-server" else "127.0.0.1"
        endpoint = f"https://{host}:{port}/dns-query"
        question = make_query("example.")
        options = dict(
            http_version=3,
            timeout=3,
            verify=context,
            bootstrap_address="127.0.0.1",
        )
        if identity == "sync-query":
            from tba_provider_dns_resolver import query as sync

            request = asyncio.to_thread(sync.https, question, endpoint, **options)
        else:
            request = asyncquery.https(question, endpoint, **options)
        if identity in ("trusted", "sync-query", "shared-context", "combined-pem"):
            answer = await request
            assert decoded(answer.answers[0]) == (ipaddress.IPv4Address("192.0.2.1"),)
            assert authenticated == [(client_certificate.serial_number, 1)]
            assert len(dns_requests) == 1
        else:
            with pytest.raises((OSError, TimeoutError)):
                await request
            assert not authenticated and not dns_requests
    finally:
        server.close()


def test_svcb_round_trip_preserves_known_and_private_parameters():
    zone = Zone.from_text(
        r"""
$ORIGIN example.
$TTL 300
@ HTTPS 1 . mandatory=alpn,port alpn="h2,h3" port=443 ipv4hint=192.0.2.1 key65400="\001"
""",
        check_origin=False,
    )
    binding = decoded(zone.get("@", "HTTPS").records[0])[0]
    assert binding.priority == 1
    assert binding.target == ()
    assert dict(binding.params)[65400] == b"\x01"
    clone = Zone.from_text(zone.to_text(), "example.", check_origin=False)
    assert decoded(clone.get("@", "HTTPS").records[0])[0] == binding


def test_dns_update_and_edns_message_text_round_trip():
    update = Update("example.")
    update.absent("absent", "A")
    update.present("@", "SOA")
    update.delete("old", "TXT")
    original = update.message(123)
    assert Message.from_text(original.to_text()).to_wire() == original.to_wire()
    query = Question.from_text("example.", "TXT").query_message(
        7, want_dnssec=True, edns_options=(ExtendedError(15, "Blocked").to_option(),)
    )
    assert Message.from_text(query.to_text()) == query


def test_typed_edns_rejects_invalid_host_bits_and_round_trips():
    subnet = ClientSubnet.from_text("2001:db8:1234::/49", scope=32)
    cookie = Cookie(b"01234567", b"89abcdef")
    assert decoded_option(subnet.to_option()) == subnet
    assert decoded_option(cookie.to_option()) == cookie
    assert decoded_option(ExtendedError(15, "Blocked").to_option()) == ExtendedError(
        15, "Blocked"
    )
    malformed = EdnsOption(8, b"\0\x01\x19\0\xc0\x00\x02\x01")
    with pytest.raises(WireError, match="nonzero host bits"):
        decoded_option(malformed)


@pytest.mark.parametrize(
    ("record", "rdata"),
    [
        ("APL", "1:192.0.2.0/24 !2:2001:db8::/32"),
        ("LOC", "37 23 30 N 122 4 30 W 10m 1m 500m 5m"),
        ("IPSECKEY", "10 3 2 gw.example. AQID"),
        ("HIP", "2 00112233 AQID rendezvous.example."),
        ("AMTRELAY", "10 1 3 relay.example."),
        ("DSYNC", "CDS NOTIFY 53 notify.example."),
        ("NID", "100 0011:2233:4455:6677"),
        ("L64", "100 0011:2233:4455:6677"),
        ("NSAP", "0x00112233"),
        ("WKS", "192.0.2.1 tcp 22 53 443"),
        ("TKEY", "gss-tsig. 100 200 3 0 AQID BA=="),
    ],
)
def test_variable_rdata_formats_round_trip_in_zone(record, rdata):
    zone = Zone.from_text(
        f"owner 300 IN {record} {rdata}", "example.", check_origin=False
    )
    clone = Zone.from_text(zone.to_text(), "example.", check_origin=False)
    assert (
        zone.get("owner", record).records[0].data
        == clone.get("owner", record).records[0].data
    )


def test_zonemd_rfc8976_simple_zone():
    zone = Zone.from_text(
        """
@ 86400 IN SOA ns1 admin 2018031900 1800 900 604800 86400
@ 86400 IN NS ns1
@ 86400 IN NS ns2
ns1 3600 IN A 203.0.113.63
ns2 3600 IN AAAA 2001:db8::63
""",
        "example.",
    )
    record = make_zonemd(zone)
    assert record.data[6:].hex() == (
        "c68090d90a7aed716bc459f9340e3d7c1370d4d24b7e2fc3"
        "a1ddc0b9a87153b9a9713b3c9ae5cc27777f98b8e730044c"
    )
    with zone.transaction() as change:
        change.add(record)
    assert verify_zonemd(zone) == record


def test_gss_tsig_provider_and_truncated_hmac_signatures():
    class MicContext:
        def get_signature(self, message):
            return hmac.digest(b"fixture gss key", message, "sha256")

        def verify_signature(self, message, signature):
            if not hmac.compare_digest(self.get_signature(message), signature):
                raise ValueError("invalid fixture MIC")
            return 0

    query = Question.from_text("example.", "A").query_message(48).to_wire()
    gss_key = GssTsigKey((b"gss",), MicContext())
    truncated_key = TsigKey((b"key",), b"secret", (b"hmac-sha256-128",))
    for key, size in ((gss_key, 32), (truncated_key, 16)):
        signed, mac = sign(query, key, now=100)
        assert len(mac) == size
        assert verify(signed, key, now=100).mac == mac
        assert Message.from_wire(signed).to_wire(compress=True) == signed
        with pytest.raises(WireError, match="signed again"):
            replace(Message.from_wire(signed), id=49).to_wire()


def test_ddr_checks_resolver_ip_in_certificate(dns_tls_identity, monkeypatch):
    from tba_provider_dns_resolver.client import TlsNameserver

    cert_file, key_file = dns_tls_identity
    server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server_context.load_cert_chain(cert_file, key_file)
    server_context.num_tickets = 0
    context = ssl.create_default_context(cafile=cert_file)
    resolver = Resolver(["127.0.0.1"])
    with socket.socket() as sock, ThreadPoolExecutor(max_workers=1) as worker:
        sock.bind(("127.0.0.1", 0))
        sock.listen()
        sock.settimeout(5)
        port = sock.getsockname()[1]
        svcb = from_tokens(
            parse_name("_dns.resolver.arpa."),
            3600,
            "IN",
            "SVCB",
            ["1", "localhost.", "alpn=dot", f"port={port}"],
        )
        monkeypatch.setattr(resolver, "_resolve", lambda *args, **kwargs: (svcb,))

        def serve():
            connection, _ = sock.accept()
            with connection, server_context.wrap_socket(connection, server_side=True):
                pass
            connection, _ = sock.accept()
            with (
                connection,
                server_context.wrap_socket(connection, server_side=True) as secure,
            ):
                channel = DnsStream(secure, deadline_after(5))
                channel.send(_address_response(channel.receive()))

        peer = worker.submit(serve)
        assert try_ddr(resolver, context=context)
        assert resolver.nameservers == (
            TlsNameserver("127.0.0.1", "localhost", port, context, "127.0.0.1"),
        )
        result = resolver.query(Question.from_text("example.", "A"))
        assert str(decoded(result.answers[0])[0]) == "192.0.2.1"
        peer.result(timeout=5)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("alpn", "include_ip"), [("doq", True), ("doq", False), ("h3", True)]
)
async def test_ddr_over_quic_uses_verified_certificate_and_bootstrap_address(
    tmp_path, alpn, include_ip
):
    from aioquic.asyncio import QuicConnectionProtocol, serve
    from aioquic.h3.connection import H3Connection
    from aioquic.h3.events import DataReceived
    from aioquic.quic.configuration import QuicConfiguration
    from tba_provider_dns_resolver.client import HttpsNameserver, QuicNameserver

    cert_file, key_file = _make_dns_tls_identity(tmp_path, include_ip=include_ip)
    context = ssl.create_default_context(cafile=cert_file)
    configuration = QuicConfiguration(is_client=False, alpn_protocols=[alpn])
    configuration.load_cert_chain(cert_file, key_file)
    queries = []

    async def doq_answer(reader, writer):
        size = int.from_bytes(await reader.readexactly(2), "big")
        packet = await reader.readexactly(size)
        queries.append(packet)
        response = _address_response(packet)
        writer.write(len(response).to_bytes(2, "big") + response)
        writer.write_eof()

    class Http3Peer(QuicConnectionProtocol):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.http = H3Connection(self._quic)
            self.data = bytearray()

        def quic_event_received(self, event):
            for item in self.http.handle_event(event):
                if not isinstance(item, DataReceived):
                    continue
                self.data.extend(item.data)
                if item.stream_ended:
                    queries.append(bytes(self.data))
                    self.http.send_headers(
                        item.stream_id,
                        [
                            (b":status", b"200"),
                            (b"content-type", b"application/dns-message"),
                        ],
                    )
                    self.http.send_data(
                        item.stream_id,
                        _address_response(bytes(self.data)),
                        end_stream=True,
                    )
                    self.transmit()

    server_args = (
        {
            "stream_handler": lambda reader, writer: asyncio.create_task(
                doq_answer(reader, writer)
            )
        }
        if alpn == "doq"
        else {"create_protocol": Http3Peer}
    )
    peer = await serve("127.0.0.1", 0, configuration=configuration, **server_args)
    port = peer._transport.get_extra_info("sockname")[1]

    class Bootstrap(asyncio.DatagramProtocol):
        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, sender):
            query = Message.from_wire(data)
            assert query.questions == (
                Question.from_text("_dns.resolver.arpa.", "SVCB"),
            )
            params = ["1", "localhost.", f"alpn={alpn}", f"port={port}"]
            if alpn == "h3":
                params.append('dohpath="/dns-query{?dns}"')
            rr = from_tokens(query.questions[0].name, 300, "IN", "SVCB", params)
            answer = replace(make_response(query), answers=(rr,))
            self.transport.sendto(answer.to_wire(), sender)

    bootstrap, _ = await asyncio.get_running_loop().create_datagram_endpoint(
        Bootstrap,
        local_addr=("127.0.0.1", 0),
    )
    try:
        resolver = AsyncResolver(
            ["127.0.0.1"], port=bootstrap.get_extra_info("sockname")[1]
        )
        assert await try_ddr_async(resolver, context=context, lifetime=5) is include_ip
        if not include_ip:
            assert resolver.nameservers == ("127.0.0.1",)
            assert queries == []
            return
        expected = QuicNameserver if alpn == "doq" else HttpsNameserver
        assert isinstance(resolver.nameservers[0], expected)
        assert resolver.nameservers[0].certificate_ip == "127.0.0.1"
        result = await resolver.resolve("example.", "A", lifetime=5)
        assert result[0].address == "192.0.2.1"
        assert len(queries) == 1
    finally:
        bootstrap.close()
        peer.close()


def test_trio_resolver_and_query_with_loopback_peer():
    import trio

    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        sock.bind(("127.0.0.1", 0))
        sock.settimeout(5)
        port = sock.getsockname()[1]

        def serve():
            for _ in range(2):
                request, sender = sock.recvfrom(65535)
                sock.sendto(_address_response(request), sender)

        async def check():
            resolver = AsyncResolver(["127.0.0.1"], port=port)
            assert (await resolver.resolve("example."))[0].address == "192.0.2.1"
            query = Question.from_text("example.", "A").query_message(59)
            assert (
                await async_transport.udp_query(query, "127.0.0.1", port=port)
            ).id == 59

        peer = worker.submit(serve)
        trio.run(check)
        peer.result(timeout=5)


def test_trio_udp_timeout_uses_the_dns_lifetime():
    import trio

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer:
        peer.bind(("127.0.0.1", 0))
        query = Question.from_text("example.", "A").query_message(59)

        async def check():
            with pytest.raises(TimeoutError), trio.fail_after(2):
                await async_transport.udp_query(
                    query, "127.0.0.1", port=peer.getsockname()[1], timeout=0.05
                )

        trio.run(check)


def test_socket_override_preserves_numeric_resolution_and_restores_original(
    monkeypatch,
):
    from tba_provider_dns_resolver.system_resolver import override_system_resolver

    resolver = Resolver([])
    address = ipaddress.IPv4Address("192.0.2.1")

    class Addresses:
        def addresses(self):
            return iter((str(address),))

    monkeypatch.setattr(resolver, "resolve_name", lambda *_, **__: Addresses())
    monkeypatch.setattr(resolver, "canonical_name", lambda *_: parse_name("example."))
    original = socket.getaddrinfo
    with override_system_resolver(resolver):
        assert socket.gethostbyname("test.example") == str(address)
        assert socket.gethostbyname_ex("test.example") == (
            "example",
            [],
            [str(address)],
        )
        assert socket.getaddrinfo(
            "test.example", 443, type=socket.SOCK_STREAM, flags=socket.AI_CANONNAME
        )[0][3:] == ("example", (str(address), 443))
        assert socket.getaddrinfo("127.0.0.1", 80) == original("127.0.0.1", 80)
    assert socket.getaddrinfo is original


def test_versioned_zone_retains_immutable_snapshots_and_reads_rrsets():
    zone = VersionedZone.from_text(_ZONE)
    version = zone.version()
    with zone.transaction() as change:
        change.delete(zone.origin, "MX")
    assert zone.version(version.revision) == version
    assert any(rr.type == RecordType.MX for rr in version.records())
    assert not any(rr.type == RecordType.MX for rr in zone.version().records())
    rows = read_rrsets("www 300 IN A 192.0.2.1\nwww 60 IN A 192.0.2.2", "example.")
    assert len(rows) == 1
    assert rows[0].ttl == 60 and len(rows[0].records) == 2


def test_idna_and_dns_name_operations():
    assert parse_name("faß\u3002example.") == (b"fass", b"example")
    assert parse_name("faß\u3002example.", encode_label=encode_idna2008) == (
        b"xn--fa-hia",
        b"example",
    )
    owner, origin = parse_name("www.example."), parse_name("example.")
    assert concatenate(relativize(owner, origin), origin) == owner
    assert (
        parent(owner) == common_ancestor(owner, parse_name("else.example.")) == origin
    )
    assert is_absolute_text("example\u3002")
    assert not is_absolute_text(r"example\.")


@pytest.mark.parametrize("algorithm", [1, 3, 8, 10, 13, 14, 16])
def test_dnssec_supported_algorithm_families(algorithm):
    from cryptography.hazmat.primitives.asymmetric import dsa, ec, ed448, rsa

    if algorithm in (1, 8, 10):
        private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    elif algorithm == 3:
        private = dsa.generate_private_key(key_size=1024)
    elif algorithm in (13, 14):
        private = ec.generate_private_key(
            ec.SECP256R1() if algorithm == 13 else ec.SECP384R1()
        )
    else:
        private = ed448.Ed448PrivateKey.generate()
    key = make_dnskey("example.", private.public_key(), algorithm)
    record = from_tokens(parse_name("example."), 3600, "IN", "A", ["192.0.2.8"])
    if algorithm in (1, 3):
        with pytest.raises(ValidationError, match="not permitted for signing"):
            sign_rrset((record,), key, private, inception=100, expiration=300)
    policy = Policy(
        sign_algorithms=frozenset({algorithm}),
        validate_algorithms=frozenset({algorithm}),
    )
    signature = sign_rrset(
        (record,), key, private, inception=100, expiration=300, policy=policy
    )
    validate_rrsig((record,), signature, (key,), now=200, policy=policy)


@pytest.mark.parametrize("api", ["transfer", "sync", "async"])
def test_signed_unchanged_ixfr_can_complete_over_udp(api):
    from tba_protocol_dns.xfr import make_query
    from tba_provider_dns_resolver import asyncquery, query

    baseline = Zone.from_text(_ZONE)
    original = baseline.to_text()
    soa = baseline.get("@", "SOA").records[0]
    key = TsigKey((b"fixture",), b"udp transfer fixture secret")
    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        sock.bind(("127.0.0.1", 0))
        sock.settimeout(5)

        def serve():
            packet, sender = sock.recvfrom(65535)
            query = Message.from_wire(packet)
            assert query.questions[0].type == RecordType.IXFR
            request_mac = verify(packet, key).mac
            response = Message(query.id, 0x8400, query.questions, (soa,))
            sock.sendto(
                sign(response.to_wire(), key, request_mac=request_mac)[0], sender
            )

        peer = worker.submit(serve)
        port = sock.getsockname()[1]
        if api == "transfer":
            result = transfer(
                "example.", "127.0.0.1", port=port, base_soa=soa, key=key, try_udp=True
            )
            assert result.apply(baseline).to_text() == original
        else:
            request, _ = make_query(baseline, keyring=key)
            options = dict(
                port=port, timeout=3, query=request, udp_mode=query.UDPMode.ONLY
            )
            if api == "sync":
                query.inbound_xfr("127.0.0.1", baseline, **options)
            else:
                asyncio.run(asyncquery.inbound_xfr("127.0.0.1", baseline, **options))
            assert baseline.to_text() == original
        peer.result(timeout=5)


def test_udp_update_authenticates_response_without_zone_section():
    key = TsigKey((b"update",), b"fixture update key")
    update = Update("example.")
    update.delete("old", "A")
    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock,
        ThreadPoolExecutor(max_workers=1) as worker,
    ):
        sock.bind(("127.0.0.1", 0))

        def serve():
            request, _, sender = receive_udp(sock)
            assert request.opcode == 5
            assert len(request.authority) == 1
            request_signature = verify(request.to_wire(), key).mac
            response = replace(make_response(request), questions=())
            data, _ = sign(response.to_wire(), key, request_mac=request_signature)
            assert send_udp(sock, data, sender)[0] == len(data)

        peer = worker.submit(serve)
        response = send_update(
            update, "127.0.0.1", port=sock.getsockname()[1], key=key, udp=True
        )
        assert response.rcode == 0 and not response.questions
        peer.result(timeout=5)


def test_query_response_and_owner_compression():
    query = make_query("Example.", "A", identifier=271, want_dnssec=True)
    answer = from_tokens(query.questions[0].name, 30, "IN", "A", ["192.0.2.3"])
    message = replace(make_response(query, authoritative=True), answers=(answer,))
    compressed = message.to_wire(compress=True)
    assert len(compressed) < len(message.to_wire())
    assert Message.from_wire(compressed) == message

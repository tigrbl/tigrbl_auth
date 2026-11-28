"""Installed-wheel coverage for DNS object and socket interfaces."""

import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import pytest
from tba_codec_dns import message, rdata, wire
from tba_codec_dns.rdtypes.ANY.LOC import LOC
from tba_codec_dns.rdtypes.ANY.NINFO import NINFO
from tba_codec_dns.rdtypes.ANY.SPF import SPF
from tba_codec_dns.rdtypes.ANY.WALLET import WALLET
from tba_codec_dns.rdtypes.CH.A import A as ChaosA
from tba_codec_dns.rdtypes.IN.A import A
from tba_codec_dns.rdtypes.IN.HTTPS import HTTPS
from tba_codec_dns.rdtypes.svcbbase import ALPNParam, PortParam
from tba_concrete_dns_zone.btreezone import ImmutableNode, Zone
from tba_primitives_dns_name.name import from_text
from tba_provider_dns_resolver import async_transport, asyncbackend


def test_rdata_modules_share_the_registry_and_class_specific_wire_format():
    assert rdata.get_rdata_class("IN", "A") is A
    assert rdata.get_rdata_class("CH", "A") is ChaosA
    chaos = rdata.from_text("CH", "A", "chaos.example. 1234")
    assert chaos.domain == from_text("chaos.example.")
    assert chaos.address == 0o1234
    assert chaos.to_wire().endswith(0o1234.to_bytes(2, "big"))
    assert rdata.from_wire("CH", "A", chaos.to_wire()) == chaos
    for record in (NINFO, SPF, WALLET):
        value = rdata.from_text("IN", record.__name__, '"a" "b"')
        assert type(value) is record
        assert value.strings == (b"a", b"b")
    loc = rdata.from_text("IN", "LOC", "52 30 0 N 13 24 0 E 30m")
    assert isinstance(loc, LOC)
    assert loc.float_latitude == 52.5
    https = HTTPS(
        "IN", "HTTPS", 1, "example.", {1: ALPNParam([b"h2"]), 3: PortParam(443)}
    )
    assert rdata.from_wire("IN", "HTTPS", https.to_wire()).params == https.params


def test_message_rrsets_edns_and_tsig_are_editable_and_roundtrip():
    query = message.make_query("example.", "A", id=266)
    query.use_edns(payload=1472)
    query.want_dnssec()
    assert query.ednsflags & 0x8000
    response = message.make_response(query)
    answer = response.find_rrset(response.answer, "example.", "IN", "A", create=True)
    answer.add(A("IN", "A", "192.0.2.1"), ttl=60)
    assert response.find_rrset(message.ANSWER, "example.", "IN", "A") is answer
    response.set_rcode(16)
    response.use_tsig({"key.": b"test key material"}, keyname="key.")
    payload = response.to_wire()
    checked = message.from_wire(payload, keyring={"key.": b"test key material"})
    assert checked.id == 266
    assert checked.rcode() == 16
    assert checked.had_tsig and checked.mac
    assert checked.answer[0][0].address == "192.0.2.1"
    assert checked.resolve_chaining().minimum_ttl == 60


def test_committed_zone_nodes_are_immutable_and_writers_wait():
    zone = Zone.from_text(
        "$ORIGIN example.\n$TTL 60\n@ SOA ns admin 1 2 3 4 5\n"
        "@ NS ns\nchild NS ns.child\nns.child A 192.0.2.1\n"
    )
    original = zone.version()
    node = original.get_node("ns.child")
    assert isinstance(node, ImmutableNode) and node.is_glue()
    assert original.delegations.is_glue(from_text("ns.child", origin=None))
    with pytest.raises(TypeError):
        node.flags = 0
    with pytest.raises(TypeError):
        node.rdatasets[0].ttl = 1
    started, entered = Event(), Event()

    def concurrent_writer():
        started.set()
        with zone.writer() as writer:
            entered.set()
            writer.update_serial()

    with ThreadPoolExecutor(max_workers=1) as pool:
        with zone.writer() as writer:
            future = pool.submit(concurrent_writer)
            assert started.wait(1)
            assert not entered.wait(0.05)
            writer.update_serial()
        future.result(timeout=1)
    assert zone.get_soa().serial == 3
    assert original.get_node("@").rdatasets[0]


@pytest.mark.parametrize("library", ["asyncio", "trio"])
def test_native_backend_datagrams_and_borrowed_socket(library):
    async def check():
        backend = asyncbackend.get_backend(library)
        assert backend.name() == library
        query = wire.make_query("example.", id=123)
        async with await backend.make_socket(
            socket.AF_INET, socket.SOCK_DGRAM, source=("127.0.0.1", 0)
        ) as server:
            address = await server.getsockname()
            async with await backend.make_socket(
                socket.AF_INET, socket.SOCK_DGRAM, destination=address
            ) as client:
                size, _ = await async_transport.send_udp(client, query, None)
                assert size == len(query.to_wire())
                received, _, remote = await async_transport.receive_udp(server)
                assert received == query
                await async_transport.send_udp(
                    server, wire.make_response(query), remote
                )
                received, _, _ = await async_transport.receive_udp(client)
                assert query.is_response(received)

                async def respond():
                    request, _, peer = await async_transport.receive_udp(server)
                    await async_transport.send_udp(
                        server, wire.make_response(request), peer
                    )

                async def exchange():
                    reply = await async_transport.udp_query(
                        query, address[0], port=address[1], sock=client, backend=backend
                    )
                    assert query.is_response(reply)
                    assert await client.getpeername() == address

                if library == "asyncio":
                    await asyncio.gather(respond(), exchange())
                else:
                    import trio

                    async with trio.open_nursery() as nursery:
                        nursery.start_soon(respond)
                        nursery.start_soon(exchange)

    if library == "asyncio":
        asyncio.run(check())
    else:
        pytest.importorskip("trio").run(check)


def test_mutable_messages_preserve_update_sections_and_tsig_stream_context():
    update = message.UpdateMessage("example.", id=122)
    update.delete("remove", "A")
    update.replace("add", 60, "A", "192.0.2.2")
    parsed = message.from_wire(update.to_wire())
    assert parsed.zone[0].name == from_text("example.")
    assert parsed.update[0].deleting == wire.RecordClass.ANY

    keys = {"key.": b"test key material"}
    first = message.make_query("example.", "SOA", id=17)
    first.use_tsig(keys)
    first_wire = first.to_wire(multi=True)
    first_read = message.from_wire(first_wire, keyring=keys, multi=True)
    second = message.make_query("example.", "SOA", id=17)
    second.use_tsig(keys)
    second_wire = second.to_wire(multi=True, tsig_ctx=first.tsig_ctx)
    second_read = message.from_wire(
        second_wire, multi=True, tsig_ctx=first_read.tsig_ctx
    )
    assert second_read.mac == second.mac


def test_active_version_survives_retention_limit_until_reader_exits():
    zone = Zone.from_text(
        "$ORIGIN example.\n$TTL 60\n@ SOA ns admin 1 2 3 4 5\n@ NS ns\n"
    )
    first = zone.version().id
    with zone.reader(id=first):
        with zone.writer() as writer:
            with pytest.raises(RuntimeError, match="active writer"), zone.writer():
                pass
            writer.update_serial()
        assert zone.version(first).id == first
    with pytest.raises(KeyError):
        zone.version(first)


def test_named_rdata_registration_and_styled_record_text():
    class Custom(rdata.Rdata):
        @classmethod
        def from_text(cls, rdclass, rdtype, text, origin=None):
            return cls(rdclass, rdtype, int(text).to_bytes(2, "big"))

        @classmethod
        def from_wire_parser(cls, rdclass, rdtype, parser):
            return cls(rdclass, rdtype, parser.get_bytes(2))

    rdata.register_type(Custom, 65076, "TBA-TEST", is_singleton=True)
    data = rdata.from_text("IN", "TBA-TEST", "1234")
    assert type(data) is Custom
    assert wire.type_text(data.rdtype) == "TBA-TEST"
    assert data.data == b"\x04\xd2"
    mx = rdata.from_text("IN", "MX", "10 mail.example.")
    style = rdata.RdataStyle(origin=from_text("example."), relativize=True)
    assert mx.to_styled_text(style) == "10 mail"
    nsec = rdata.from_text("IN", "NSEC", "next.example. A AAAA")
    assert nsec.replace(windows=nsec.windows) == nsec


def test_glue_update_exposes_nested_cuts_and_retains_snapshot_flags():
    zone = Zone.from_text(
        "$ORIGIN example.\n$TTL 60\n@ SOA ns admin 1 2 3 4 5\n@ NS ns\n"
        "child NS ns.child\nns.child A 192.0.2.1\n"
        "grand.child NS ns.grand.child\nns.grand.child A 192.0.2.2\n"
    )
    before = zone.version()
    with zone.writer() as writer:
        writer.update_glue_flag("child", False)
        assert writer.get_node("grand.child").is_delegation()
        assert not writer.get_node("ns.child").is_glue()
        assert writer.get_node("ns.grand.child").is_glue()
    after = zone.version()
    assert before.get_node("grand.child").is_glue()
    assert after.get_node("grand.child").is_delegation()
    with zone.writer() as writer:
        writer.update_glue_flag("child", True)
        assert writer.get_node("grand.child").is_glue()


def test_compat_asyncquery_udp_options_and_fallback_share_deadline():
    from collections import deque
    from time import time

    from tba_provider_dns_resolver import asyncquery

    q = message.make_query("example.", "A", id=123)
    correct = message.make_response(q).to_wire()
    bad_id = b"\x00\x01" + correct[2:]
    truncated = correct[:2] + bytes([correct[2] | 2]) + correct[3:]
    peer = ("127.0.0.1", 5353)

    class Datagram(asyncbackend.DatagramSocket):
        def __init__(self, replies):
            super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
            self.replies = deque(replies)

        async def getpeername(self):
            return None

        async def sendto(self, what, destination, timeout):
            assert destination == peer
            assert timeout > 0
            return len(what)

        async def recvfrom(self, size, timeout):
            return self.replies.popleft()

        async def close(self):
            pytest.fail("borrowed datagram closed")

    class Stream(asyncbackend.StreamSocket):
        def __init__(self):
            super().__init__(socket.AF_INET, socket.SOCK_STREAM)
            self.reply = bytearray(len(correct).to_bytes(2, "big") + correct)

        async def sendall(self, packet, timeout):
            assert int.from_bytes(packet[:2], "big") == len(packet) - 2
            assert 0 < timeout <= 1

        async def recv(self, size, timeout):
            data = self.reply[:size]
            del self.reply[:size]
            return data

        async def close(self):
            pytest.fail("borrowed stream closed")

    async def exercise():
        with pytest.raises(asyncquery.BadResponse):
            await asyncquery.udp(
                q, peer[0], 1, peer[1], sock=Datagram([(bad_id, peer)])
            )
        with pytest.raises(asyncquery.UnexpectedSource):
            await asyncquery.udp(
                q, peer[0], 1, peer[1], sock=Datagram([(correct, ("127.0.0.2", 5353))])
            )
        response = await asyncquery.udp(
            q,
            peer[0],
            1,
            peer[1],
            ignore_unexpected=True,
            ignore_trailing=True,
            ignore_errors=True,
            sock=Datagram([(b"invalid", peer), (bad_id, peer), (correct + b"x", peer)]),
        )
        assert isinstance(response, message.QueryMessage) and q.is_response(response)
        response, tcp = await asyncquery.udp_with_fallback(
            q,
            peer[0],
            1,
            peer[1],
            udp_sock=Datagram([(truncated, peer)]),
            tcp_sock=Stream(),
        )
        assert tcp and q.is_response(response)
        _, sent = await asyncquery.send_udp(Datagram([]), q, peer, time() + 1)
        assert abs(sent - time()) < 1

    asyncio.run(exercise())


def test_compat_asyncquery_doh_and_doq_borrow_sessions():
    import httpx
    from tba_provider_dns_resolver import asyncquery

    q = message.make_query("example.", id=333)

    def respond(request):
        assert request.method == "POST"
        sent = message.from_wire(request.content)
        assert sent.id == 0
        packet = message.make_response(sent).to_wire() + b"x"
        return httpx.Response(
            200,
            headers={"Content-Type": "application/dns-message"},
            stream=httpx.ByteStream(packet),
            extensions={"http_version": b"HTTP/2"},
        )

    class Stream:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            pass

        async def send(self, packet, end_stream):
            assert end_stream
            self.query = message.from_wire(packet)
            assert self.query.id == 0

        async def receive(self, timeout):
            assert timeout is None
            return message.make_response(self.query).to_wire() + b"x"

    class Connection:
        async def make_stream(self, timeout):
            assert timeout is None
            return Stream()

    async def exercise():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            reply = await asyncquery.https(
                q,
                "resolver.example",
                client=client,
                http_version=asyncquery.HTTPVersion.H2,
                ignore_trailing=True,
            )
            assert q.is_response(reply) and not client.is_closed
        reply = await asyncquery.quic(
            q,
            "127.0.0.1",
            connection=Connection(),
            ignore_trailing=True,
        )
        assert q.is_response(reply)

    asyncio.run(exercise())


@pytest.mark.parametrize(
    ("incremental", "incomplete", "udp_first", "sync"),
    [
        (False, False, False, False),
        (True, False, False, False),
        (True, True, False, False),
        (True, False, True, False),
        (False, False, False, True),
        (True, False, False, True),
        (True, True, False, True),
        (True, False, True, True),
    ],
)
def test_inbound_xfr_commits_only_after_final_tcp_frame(
    incremental, incomplete, udp_first, sync, monkeypatch
):
    from tba_codec_dns.tsig import StreamSigner, TsigError, TsigKey, sign, verify
    from tba_protocol_dns.xfr import UseTCP, make_query
    from tba_provider_dns_resolver import asyncquery, query

    created = []

    def factory(af, kind, proto):
        sock = socket.socket(af, kind, proto)
        created.append((kind, proto, sock))
        return sock

    monkeypatch.setattr(query, "socket_factory", factory)
    zone_text = "$ORIGIN example.\n$TTL 60\n@ SOA ns admin {} 2 3 4 5\n@ NS ns\nns A 192.0.2.{}\n"
    before = Zone.from_text(zone_text.format(1, 1))
    after = Zone.from_text(zone_text.format(2, 2))
    zone = before if incremental else Zone("example.")
    opening = after.get("@", "SOA").records[0]
    old_soa = before.get("@", "SOA").records[0]
    old_ip = before.get("ns", "A").records[0]
    new_ip = after.get("ns", "A").records[0]
    signed = sync and not udp_first
    key = TsigKey((b"transfer", b"example"), b"transfer-fixture")

    async def serve(reader, writer):
        try:
            length = int.from_bytes(await reader.readexactly(2), "big")
            request = await reader.readexactly(length)
            query = wire.Message.from_wire(request)
            if incremental:
                assert query.questions[0].type == wire.RecordType.IXFR
                first = (opening, old_soa, old_ip)
                last = (opening, new_ip, opening)
            else:
                assert query.questions[0].type == wire.RecordType.AXFR
                first = (opening, *after.get("@", "NS").records)
                last = (new_ip, opening)
            signer = StreamSigner(key) if signed else None
            mac = verify(request, key).mac if signed else None
            messages = (first,) if incomplete and not signed else (first, last)
            for index, answers in enumerate(messages):
                packet = wire.Message(
                    query.id, 0x8400, query.questions, answers
                ).to_wire()
                if signed and (not incomplete or index == 0):
                    packet, _ = sign(packet, key, request_mac=mac, context=signer)
                writer.write(len(packet).to_bytes(2, "big") + packet)
                await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    class TruncatingDatagram(asyncbackend.DatagramSocket):
        def __init__(self, destination):
            super().__init__(socket.AF_INET, socket.SOCK_DGRAM)
            self.destination = destination

        async def sendto(self, packet, destination, timeout):
            assert destination is None
            query = wire.Message.from_wire(packet)
            assert query.questions[0].type == wire.RecordType.IXFR
            self.reply = wire.Message(query.id, 0x8600, query.questions)
            return len(packet)

        async def recvfrom(self, size, timeout):
            return self.reply.to_wire(), self.destination

        async def close(self):
            pass

    async def exercise():
        native = asyncbackend.get_default_backend()

        class TransferBackend:
            async def make_socket(self, af, kind, proto, source, destination, timeout):
                if kind == socket.SOCK_DGRAM:
                    return TruncatingDatagram(destination)
                return await native.make_socket(
                    af, kind, proto, source, destination, timeout
                )

        backend = TransferBackend() if udp_first else native
        async with await asyncio.start_server(serve, "127.0.0.1", 0) as peer:
            port = peer.sockets[0].getsockname()[1]
            if sync:
                if udp_first:

                    class TruncatingPeer(asyncio.DatagramProtocol):
                        def connection_made(self, transport):
                            self.transport = transport

                        def datagram_received(self, data, address):
                            request = wire.Message.from_wire(data)
                            answer = wire.Message(request.id, 0x8600, request.questions)
                            self.transport.sendto(answer.to_wire(), address)

                    (
                        datagrams,
                        _,
                    ) = await asyncio.get_running_loop().create_datagram_endpoint(
                        TruncatingPeer, local_addr=("127.0.0.1", port)
                    )
                try:
                    options = dict(port=port, timeout=2, lifetime=3, source="127.0.0.1")
                    if signed:
                        options["query"], _ = make_query(zone, keyring=key)
                    if udp_first:
                        with pytest.raises(UseTCP):
                            await asyncio.to_thread(
                                query.inbound_xfr,
                                "127.0.0.1",
                                zone,
                                udp_mode=query.UDPMode.ONLY,
                                **options,
                            )
                        assert zone.get_soa().serial == 1
                        options["udp_mode"] = query.UDPMode.TRY_FIRST
                    if incomplete:
                        with pytest.raises(TsigError if signed else wire.WireError):
                            await asyncio.to_thread(
                                query.inbound_xfr, "127.0.0.1", zone, **options
                            )
                    else:
                        await asyncio.to_thread(
                            query.inbound_xfr, "127.0.0.1", zone, **options
                        )
                    if not incremental:
                        from tba_concrete_dns_zone.zone import from_xfr

                        def fetch_zone():
                            frames = list(
                                query.xfr(
                                    "127.0.0.1",
                                    "example.",
                                    port=port,
                                    timeout=2,
                                    keyring=key if signed else None,
                                )
                            )
                            assert len(frames) == 2
                            assert all(frame.had_tsig == signed for frame in frames)
                            assert not frames[0].answer[0].name.is_absolute()
                            return from_xfr(frames)

                        assert (
                            await asyncio.to_thread(fetch_zone)
                        ).get_soa().serial == 2
                finally:
                    if udp_first:
                        datagrams.close()
                return
            if udp_first:
                with pytest.raises(UseTCP):
                    await asyncquery.inbound_xfr(
                        "127.0.0.1",
                        zone,
                        port=port,
                        timeout=2,
                        udp_mode=asyncquery.UDPMode.ONLY,
                        backend=backend,
                    )
                assert zone.get_soa().serial == 1
            transfer = asyncquery.inbound_xfr(
                "127.0.0.1",
                zone,
                port=port,
                timeout=2,
                lifetime=3,
                source="127.0.0.1",
                udp_mode=asyncquery.UDPMode.TRY_FIRST
                if udp_first
                else asyncquery.UDPMode.NEVER,
                backend=backend,
            )
            if incomplete:
                with pytest.raises(wire.WireError):
                    await transfer
            else:
                await transfer

    asyncio.run(exercise())
    expected = []
    if sync:
        if udp_first:
            expected.extend((socket.SOCK_DGRAM, socket.SOCK_DGRAM))
        expected.append(socket.SOCK_STREAM)
        if not incremental:
            expected.append(socket.SOCK_STREAM)
    assert [kind for kind, _, _ in created] == expected
    assert all(proto == 0 and sock.fileno() == -1 for _, proto, sock in created)
    assert zone.get_soa().serial == (1 if incomplete else 2)
    assert zone.get("ns", "A").records[0].data == (
        old_ip.data if incomplete else new_ip.data
    )


@pytest.mark.parametrize("status", [200, 503])
def test_borrowed_http3_stream_honors_headers_options_and_ownership(status):
    from tba_provider_dns_resolver import asyncquery

    query = message.make_query("example.", id=87)
    released = []

    class Stream:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *exc):
            released.append(True)

        def send_h3(self, url, packet, post):
            assert url == "https://resolver.example:443/dns-query"
            assert post is False
            self.request = message.from_wire(packet)
            assert self.request.id == 0

        async def receive(self, timeout):
            assert 0 < timeout <= 1
            return message.make_response(self.request).to_wire() + b"x"

        def headers(self):
            return [
                (b":status", str(status).encode()),
                (b"content-type", b"application/dns-message"),
            ]

    class Connection:
        async def make_stream(self, timeout):
            assert 0 < timeout <= 1
            return Stream()

    async def exercise():
        call = asyncquery.https(
            query,
            "resolver.example",
            timeout=1,
            client=Connection(),
            ignore_trailing=True,
            post=False,
        )
        if status == 200:
            assert query.is_response(await call)
        else:
            with pytest.raises(wire.WireError, match="503"):
                await call

    asyncio.run(exercise())
    assert released == [True]


@pytest.mark.parametrize("use_http3", [False, True])
def test_sync_borrows_quic_stream_and_checks_dns_reply(use_http3):
    from contextlib import contextmanager

    from tba_provider_dns_resolver import query

    class Stream:
        def send(self, packet, end):
            self.request = message.from_wire(packet)
            assert self.request.id == 0
            assert end

        def send_h3(self, url, packet, post):
            assert url == "https://resolver.example:443/dns-query"
            assert not post
            self.send(packet, True)

        def receive(self, timeout):
            assert 0 < timeout <= 2
            return message.make_response(self.request).to_wire() + b"trailing"

        def headers(self):
            return {b":status": b"202"}

    released = []

    class Connection:
        @contextmanager
        def make_stream(self, timeout):
            assert timeout == 2
            try:
                yield Stream()
            finally:
                released.append(True)

    request = message.make_query("example.", id=142)
    if use_http3:
        response = query.https(
            request,
            "resolver.example",
            timeout=2,
            session=Connection(),
            ignore_trailing=True,
            post=False,
        )
    else:
        response = query.quic(
            request,
            "127.0.0.1",
            timeout=2,
            connection=Connection(),
            ignore_trailing=True,
        )
    assert request.id == 0 and request.is_response(response)
    assert released == [True]


def test_doq_uses_explicit_backend_and_validates_response():
    from tba_provider_dns_resolver import asyncquery

    query = message.make_query("example.", id=76)
    calls = []

    class Backend:
        async def quic_query(self, request, server, **options):
            calls.append((server, options))
            assert request.id == 76
            response = wire.make_response(request)
            if len(calls) == 2:
                from dataclasses import replace

                return replace(response, id=77)
            return response

    async def exercise():
        backend = Backend()
        result = await asyncquery.quic(
            query,
            "192.0.2.53",
            2,
            8853,
            "192.0.2.10",
            50000,
            one_rr_per_rrset=True,
            ignore_trailing=True,
            backend=backend,
            hostname="resolver.example",
        )
        assert query.is_response(result)
        with pytest.raises(asyncquery.BadResponse):
            await asyncquery.quic(query, "192.0.2.53", backend=backend)
        with pytest.raises(NotImplementedError, match="does not support DoQ"):
            await asyncquery.quic(query, "192.0.2.53", backend=object())

    asyncio.run(exercise())
    assert calls[0] == (
        "192.0.2.53",
        {
            "timeout": 2,
            "port": 8853,
            "local_port": 50000,
            "local_address": "192.0.2.10",
            "server_name": "resolver.example",
            "ca_file": None,
            "verify": True,
            "one_rr_per_rrset": True,
            "ignore_trailing": True,
        },
    )

"""Compatibility behavior checked using DNS fixtures and independent HTTP peers."""

import asyncio
from dataclasses import FrozenInstanceError, replace
from io import BytesIO, StringIO

import httpx
import pytest
from tba_codec_dns import rdata, wire
from tba_codec_dns.rdataset import from_rdata
from tba_codec_dns.tsig import TsigError, TsigKey, TsigRecord
from tba_primitives_dns_name.name import from_text
from tba_provider_dns_resolver import async_transport, asyncbackend
from tba_concrete_dns_zone.btreezone import ImmutableVersion, WritableVersion
from tba_concrete_dns_zone.btreezone import Zone as BTreeZone
from tba_provider_dns_resolver.client import AsyncResolver
from tba_provider_dns_resolver.transport import https_query


def test_typed_rdata_construction_and_decoding_share_class():
    mx_class = rdata.get_rdata_class("IN", "MX")
    owner = from_text("mail.example.")
    first = mx_class("IN", "MX", 10, exchange=owner)
    assert type(rdata.from_text("IN", "MX", "10 mail.example.")) is mx_class
    assert type(rdata.from_wire("IN", "MX", first.to_wire())) is mx_class
    assert first.preference == 10 and first.exchange == owner
    assert first.replace(preference=20).to_text() == "20 mail.example."
    assert rdata.get_rdata_class("IN", "TYPE65012", use_generic=False) is None
    assert rdata.get_rdata_class("IN", "TYPE65012") is rdata.GenericRdata
    with pytest.raises(FrozenInstanceError):
        first.extra = 4
    binding = rdata.HTTPS("IN", "HTTPS", 1, owner, {3: b"\x01\xbb"})
    assert binding.params[3].port == 443
    assert binding.raw_params == {3: b"\x01\xbb"}
    assert type(rdata.from_wire("IN", "HTTPS", binding.to_wire())) is rdata.HTTPS
    assert binding.replace(priority=2).priority == 2


def test_rdata_wire_compression_and_relative_presentation():
    origin = from_text("example.")
    record = rdata.from_text("IN", "MX", "10 mail", origin, relativize=True)
    assert record.exchange == from_text("mail", None)
    assert record.replace(exchange="backup").to_text() == "10 backup"
    with BytesIO(bytes(12)) as packet:
        packet.seek(12)
        compression = {}
        origin.to_wire(packet, compression)
        start = packet.tell()
        record.to_wire(packet, compression)
        raw = packet.getvalue()
        assert raw[start:] == b"\x00\x0a\x04mail\xc0\x0c"
        parsed = rdata.from_wire("IN", "MX", raw, start, len(raw) - start, origin)
        assert parsed == record
        assert parsed.to_text() == "10 mail"


def test_message_tsig_authenticates_requests_responses_and_streams():
    key = TsigKey.from_text("test-key.example.", "Y29uZm9ybWFuY2U=")
    query = wire.make_query("example.", identifier=715)
    packet = query.use_tsig(key).to_wire()
    request = wire.from_wire(packet, {from_text("test-key.example."): key.secret})
    assert request.had_tsig and request.tsig_key == key
    assert request.to_wire() == packet
    reply = wire.make_response(request).to_wire()
    verified = wire.from_wire(reply, key, request_mac=request.mac, multi=True)
    assert query.is_response(verified)
    assert verified.tsig_ctx is not None
    unsigned = wire.make_response(query).to_wire()
    subsequent = wire.from_wire(unsigned, tsig_ctx=verified.tsig_ctx, multi=True)
    assert subsequent.to_wire() == unsigned
    with pytest.raises(TsigError, match="missing response"):
        wire.from_wire(unsigned, key, request_mac=request.mac)
    with pytest.raises(wire.UnknownTSIGKey):
        wire.from_wire(reply, None)
    changed = bytearray(reply)
    changed[3] ^= 0x10
    with pytest.raises(TsigError, match="digest verification"):
        wire.from_wire(bytes(changed), key, request_mac=request.mac)
    assert wire.from_wire(reply, False).tsig_key is None
    named = from_text("test-key.example.")
    signed = query.use_tsig(
        {named: key.secret}, keyname=named, original_id=300
    ).to_wire()
    parsed = wire.from_wire(signed, key)
    assert TsigRecord.from_data(parsed.additional[-1].data).original_id == 300


def test_query_builder_accepts_typed_names_and_edns_options():
    query = wire.make_query(
        from_text("example."),
        "A",
        "IN",
        id=4,
        flags=0x0010,
        use_edns=1,
        ednsflags=0x100,
        payload=1400,
        request_payload=512,
        options=[wire.EdnsOption(15, b"\0\1")],
        want_dnssec=True,
    )
    assert query.id == 4 and query.flags == 0x0010
    assert query.edns.version == 1 and query.edns.flags == 0x8100
    assert query.edns.payload == 1400 and query.request_payload == 512
    assert query.get_options(15) == (wire.EdnsOption(15, b"\0\1"),)
    assert wire.make_query("example.", use_edns=False, payload=1400).edns is None


def test_recovering_parser_reports_offsets_and_keeps_valid_records():
    query = wire.make_query("example.", identifier=11)
    answer = rdata.from_text("IN", "A", "192.0.2.1").record((b"example",), 60)
    malformed = replace(answer, data=b"xxx")
    reply = replace(wire.make_response(query), answers=(malformed, answer))
    packet = reply.to_wire() + b"extra"
    received = wire.from_wire(packet, continue_on_error=True)
    assert received.answers == (answer,)
    assert [item.offset for item in received.errors] == [
        len(query.to_wire()),
        len(packet) - 5,
    ]
    assert isinstance(received.errors[-1].exception, wire.TrailingJunk)


def test_message_parser_groups_rrsets_and_reads_separate_text_messages():
    query = wire.make_query("example.", "SOA", identifier=99)
    first, next_soa = (
        rdata.from_text(
            "IN", "SOA", f"ns.example. admin.example. {serial} 3600 60 7200 30"
        ).record((b"example",), 60)
        for serial in (20, 21)
    )
    reply = replace(wire.make_response(query), answers=(first, next_soa))
    packet = reply.to_wire()
    assert len(wire.from_wire(packet).rrsets("answer")) == 1
    transfer = wire.from_wire(packet, origin="example.", xfr=True)
    assert [rrset[0].serial for rrset in transfer.rrsets("answer")] == [20, 21]
    assert transfer.get_rrset("answer", "@", "IN", "SOA").name == from_text("@", None)
    with StringIO(query.to_text() + "\n\n" + reply.to_text()) as source:
        assert wire.from_file(source) == query
        assert wire.from_file(source) == reply


def test_zone_hooks_and_version_factories_keep_rejected_edits_atomic():
    class Writer(WritableVersion):
        pass

    class Snapshot(ImmutableVersion):
        pass

    class Zone(BTreeZone):
        writable_version_factory = Writer
        immutable_version_factory = Snapshot

    zone = Zone("example.", versions=2)
    address = from_rdata(60, rdata.from_text("IN", "A", "192.0.2.1"))
    text = from_rdata(60, rdata.from_text("IN", "TXT", '"blocked"'))
    checks = []

    def put(transaction, owner, dataset):
        checks.append((owner, dataset.rdtype))
        if dataset.rdtype == wire.RecordType.TXT:
            assert transaction.get(owner, "A") is not None
            raise ValueError("TXT rejected")

    def prohibit(*args):
        raise ValueError("delete rejected")

    with zone.writer() as writer:
        assert isinstance(writer, Writer)
        writer.check_put_rdataset(put)
        with pytest.raises(ValueError, match="TXT rejected"):
            writer.add("host", address, text)
        assert not writer.name_exists("host")
        writer.put_rdataset("host", address)
        writer.check_delete_rdataset(prohibit)
        writer.check_delete_name(prohibit)
        with pytest.raises(ValueError, match="delete rejected"):
            writer.delete("host", "A")
        with pytest.raises(ValueError, match="delete rejected"):
            writer.delete("host")
    assert isinstance(zone.version(), Snapshot)
    assert zone.get_rdataset("host", "A") == address
    assert len(checks) == 3


def test_async_resolver_uses_injected_backend_for_search_and_alias():
    class FakeBackend:
        def __init__(self):
            self.names = []

        async def query(self, request, server, *, port, timeout, tcp):
            question = request.questions[0]
            owner = question.name
            self.names.append(owner)
            assert (server, port, tcp) == ("192.0.2.53", 5353, True)
            if owner[0] == b"alias":
                value = rdata.from_text("IN", "CNAME", "target.example.")
            else:
                value = rdata.from_text("IN", "A", "192.0.2.4")
            return replace(
                wire.make_response(request), answers=(value.record(owner, 60),)
            )

        async def sleep(self, interval):
            pytest.fail("the resolver unexpectedly retried")

    async def run():
        backend = FakeBackend()
        resolver = AsyncResolver(["192.0.2.53"], port=5353, search=["example."])
        answer = await resolver.resolve_answer(
            "alias", search=True, tcp=True, backend=backend
        )
        assert answer.canonical_name == from_text("target.example.")
        assert backend.names == [(b"alias", b"example"), (b"target", b"example")]
        assert asyncbackend.sniff() == "asyncio"
        assert (
            asyncbackend.set_default_backend("asyncio")
            is asyncbackend.get_default_backend()
        )

    asyncio.run(run())


def test_sync_and_async_doh_sessions_are_borrowed_without_following_redirects():
    requests = []

    def respond(request):
        requests.append(request)
        if request.url.path == "/redirect":
            return httpx.Response(302, headers={"Location": "/dns-query"})
        dns_request = wire.from_wire(request.content)
        assert dns_request.id == 0
        body = wire.make_response(dns_request).to_wire()
        return httpx.Response(
            200,
            headers={"Content-Type": "application/dns-message"},
            stream=httpx.ByteStream(body),
            extensions={"http_version": b"HTTP/2"},
        )

    query = wire.make_query("example.", identifier=1)
    url = "https://resolver.example/dns-query"
    with httpx.Client(
        transport=httpx.MockTransport(respond), follow_redirects=True
    ) as client:
        for _ in range(2):
            assert https_query(query, url, http_version=2, session=client).id == 1
        with pytest.raises(wire.WireError, match="302"):
            https_query(query, "https://resolver.example/redirect", session=client)
        assert not client.is_closed

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            assert (
                await async_transport.https_query(query, url, session=client)
            ).id == 1
            assert not client.is_closed

    asyncio.run(run())
    assert [request.url.path for request in requests] == [
        "/dns-query",
        "/dns-query",
        "/redirect",
        "/dns-query",
    ]

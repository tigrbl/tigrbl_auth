from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import replace
from errno import EACCES, EADDRINUSE
from io import StringIO
import socket

import pytest
from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA44PrivateKey

from tba_codec_dns import flags, message, rdata, rrset, wire
from tba_codec_dns.rdtypes.ANY.CDS import CDS
from tba_codec_dns.rdtypes.ANY.DS import DS
from tba_concrete_dns_zone.btreezone import Zone as BTreeZone
from tba_concrete_dns_zone.transaction import TooManyChanges, TransactionLimiter
from tba_concrete_dns_zone.zone import DigestVerificationFailure, Zone, from_xfr
from tba_primitives_dns_name.name import from_text as name
from tba_protocol_dns import dnssec
from tba_provider_dns_resolver import asyncresolver, query as syncquery, resolver


def test_response_matching_accepts_empty_transfer_continuations_only():
    query = message.make_query("example.", "AXFR", id=13)
    response = message.make_response(query)
    response.question.clear()
    assert not query.is_response(response)
    assert query.is_response(response, xfr_continuation=True)
    response.id = 14
    assert not query.is_response(response, xfr_continuation=True)

    ordinary = message.make_query("example.", "A", id=15)
    ordinary_response = message.make_response(ordinary)
    relative = message.from_wire(ordinary_response.to_wire(), origin=name("example."))
    assert ordinary.is_response(relative)
    ordinary_response.question.clear()
    assert not ordinary.is_response(ordinary_response, xfr_continuation=True)


def test_message_flag_text_preserves_unnamed_bits():
    query = wire.make_query(
        "example.", id=15, flags=flags.RD | 64, ednsflags=flags.DO | 2, use_edns=0
    )
    rendered = query.to_text()
    assert "flags RD FLAG6" in rendered
    assert "eflags DO FLAG1" in rendered
    parsed = wire.Message.from_text(rendered)
    assert parsed.flags == query.flags
    assert parsed.edns.flags == query.edns.flags
    assert flags.from_text(flags.to_text(0xFFFF)) == 0xFFFF
    assert flags.edns_from_text(flags.edns_to_text(0xFFFF)) == 0xFFFF


@pytest.mark.parametrize(
    ("rdtype", "header", "length"),
    [
        ("TLSA", (3, 1, 1), 32),
        ("SMIMEA", (3, 1, 2), 64),
        ("SSHFP", (4, 1), 20),
    ],
)
def test_association_records_check_known_digest_lengths(rdtype, header, length):
    fields = " ".join(map(str, header))
    data = b"\x01" * length
    value = rdata.from_text("IN", rdtype, f"{fields} {data.hex()}")
    assert value.to_wire() == bytes(header) + data
    with pytest.raises(wire.WireError, match="octets"):
        rdata.from_text("IN", rdtype, f"{fields} 01")
    with pytest.raises(wire.WireError, match="octets"):
        rdata.from_wire("IN", rdtype, bytes(header) + data[:-1])

    query = wire.make_query("example.", rdtype)
    record = value.record((b"example",), 30)
    packet = replace(
        wire.make_response(query), answers=(replace(record, data=record.data[:-1]),)
    ).to_wire()
    with pytest.raises(wire.WireError, match="octets"):
        wire.Message.from_wire(packet)
    recovered = wire.Message.from_wire(packet, continue_on_error=True)
    assert not recovered.answers and len(recovered.errors) == 1


def test_nsec3_next_hash_and_ttl_unit_syntax():
    with pytest.raises(wire.WireError, match="nonempty"):
        rdata.from_wire("IN", "NSEC3", bytes((1, 0, 0, 0, 0, 0)))
    assert rdata.parse_ttl("1h0s") == 3600
    with pytest.raises(ValueError, match="TTL"):
        rdata.parse_ttl("1h0")


_ZONE = """$ORIGIN example.
$TTL 300
@ SOA ns hostmaster 1 300 300 300 300
@ NS ns
$GENERATE 1-2 item$$-$ TXT "item${0,3,d}-$"
"""


@pytest.mark.parametrize("zone_class", [Zone, BTreeZone])
def test_zone_loaders_stream_records_through_transaction_setup(zone_class):
    observed = []

    def setup(txn):
        assert not tuple(txn.iterate_names())
        txn.check_put_rdataset(lambda _, owner, dataset: observed.append(owner))

    zone = zone_class.from_text(_ZONE, transaction_setup=setup)
    assert len(observed) == 4
    assert zone.get_rdataset("item$-1", "TXT")[0].strings == (b"item001-1",)
    from_file = zone_class.from_file(StringIO(_ZONE), transaction_setup=setup)
    assert list(from_file.records()) == list(zone.records())

    limiter = TransactionLimiter(3)
    with pytest.raises(TooManyChanges, match="3 changes"):
        zone_class.from_text(_ZONE, origin=name("example."), transaction_setup=limiter)
    assert limiter.changes == 3


@pytest.mark.parametrize("modifier", ["${oops}", "${0,128,d}"])
def test_generate_rejects_invalid_modifiers(modifier):
    text = _ZONE + f"$GENERATE 1-1 host{modifier} A 192.0.2.1\n"
    with pytest.raises(ValueError, match="GENERATE"):
        Zone.from_text(text)


def test_typed_ds_and_cds_follow_digest_policy_and_preserve_wire_calls():
    keypair = MLDSA44PrivateKey.from_seed_bytes(bytes(range(32)))
    key = dnssec.make_dnskey(keypair.public_key(), "MLDSA44", flags=257)
    owner = name("example", origin=None)
    ds = dnssec.make_ds(owner, key, "SHA256", origin=name("com."))
    assert isinstance(ds, DS)
    assert ds.key_tag == 59829
    assert (
        ds.digest.hex()
        == "812cb1a22af04380e2f72d91c06c14eb1a918cf30037a8a9c67497e9264b4bfa"
    )
    cds = dnssec.make_cds("example.com.", key, "SHA256")
    assert isinstance(cds, CDS) and cds.digest == ds.digest
    legacy = dnssec.make_ds(key.record((b"example", b"com"), 7200), "SHA256")
    assert legacy.ttl == 7200 and legacy.data == ds.to_wire()
    with pytest.raises(dnssec.DeniedByPolicy):
        dnssec.make_ds("example.com.", key, "SHA1")
    assert (
        len(dnssec.make_ds("example.com.", key, "SHA1", validating=True).digest) == 20
    )
    deny_sha256 = dnssec.SimpleDeny((), (), {dnssec.DSDigest.SHA256}, ())
    with pytest.raises(dnssec.DeniedByPolicy):
        dnssec.make_ds("example.com.", key, "SHA256", policy=deny_sha256)


def test_zone_from_xfr_ignores_outside_glue_and_checks_zone_class_and_soa():
    q = wire.make_query("example.", "AXFR")
    records = tuple(Zone.from_text(_ZONE).records())
    soa = next(record for record in records if record.type == wire.RecordType.SOA)
    glue = rdata.from_text("IN", "A", "192.0.2.1").record((b"outside",), 30)
    answers = (soa, *(record for record in records if record is not soa), glue, soa)
    frame = replace(wire.make_response(q), answers=answers)
    zone = from_xfr(iter((frame,)), BTreeZone)
    assert set(zone.records()) == set(records)
    bad = replace(soa, name=(b"child", b"example"))
    with pytest.raises(wire.WireError, match="non-origin SOA"):
        from_xfr(iter((replace(frame, answers=(*answers, bad)),)))
    bad = replace(records[-1], rdclass=wire.RecordClass.CH)
    with pytest.raises(wire.WireError, match="wrong record class"):
        from_xfr(iter((replace(frame, answers=(*answers, bad)),)))


def test_ds_dataset_rrset_form_preserves_292_record_type_and_class():
    owner = name("example.")
    key = dnssec.make_dnskey(
        MLDSA44PrivateKey.from_seed_bytes(bytes(range(32))).public_key(), "MLDSA44"
    )
    keys = rrset.from_rdata(owner, 600, key)
    child = dnssec.make_ds_rdataset(keys, {"SHA256", "SHA384"})
    assert child.rdtype == wire.RecordType.CDS
    assert child.ttl == 600
    delegation = dnssec.make_ds_rdataset((owner, child), {"SHA256"})
    assert delegation.rdtype == wire.RecordType.DS
    assert len(delegation) == 1 and delegation[0].digest_type == 2


@pytest.mark.parametrize("zone_class", [Zone, BTreeZone])
def test_zone_digest_rejects_duplicate_algorithms_and_old_serials(zone_class):
    zone = zone_class.from_text(_ZONE)
    valid = zone.compute_digest(1)
    assert zone.verify_digest(valid) is None
    duplicate = valid.replace(digest=bytes(len(valid.digest)))
    with zone.writer() as txn:
        txn.add("@", 300, valid, duplicate)
    with pytest.raises(DigestVerificationFailure):
        zone.verify_digest()
    with zone.writer() as txn:
        txn.replace("@", 300, valid)
    assert zone.verify_digest() is None
    with pytest.raises(DigestVerificationFailure):
        zone.verify_digest(valid.replace(serial=valid.serial - 1))


def test_sync_resolver_functions_and_zone_authority_inference(monkeypatch):
    default = resolver.Resolver(configure=False)
    monkeypatch.setattr(resolver, "get_default_resolver", lambda: default)
    question_seen = []

    def reply(question, deadline, **options):
        question_seen.append((question, options["tcp"]))
        soa = rdata.from_text(
            "CH", "SOA", "ns.example. hostmaster.example. 1 300 300 300 300"
        )
        return replace(
            wire.make_response(question.query_message(1)),
            authority=(soa.record((b"example",), 300),),
        )

    monkeypatch.setattr(default, "_query", reply)
    assert resolver.zone_for_name("www.example.", "CH", tcp=True) == name("example.")
    assert len(question_seen) == 1
    question, tcp = question_seen[0]
    assert tcp and question.rdclass == wire.RecordClass.CH
    server = resolver.make_resolver_at("192.0.2.53", port=5053)
    assert server.nameservers[0].answer_nameserver() == "192.0.2.53"
    assert server.nameservers[0].answer_port() == 5053


@pytest.mark.asyncio
async def test_async_resolver_at_resolves_names_and_forwards_options(monkeypatch):
    class Addresses:
        def addresses(self):
            return iter(("192.0.2.53", "192.0.2.54"))

    class Bootstrap:
        async def resolve_name(self, where, family):
            assert where == name("resolver.example.") and family == socket.AF_INET
            return Addresses()

    async def fake_resolve(self, *args):
        assert [endpoint.answer_port() for endpoint in self.nameservers] == [5053, 5053]
        assert [endpoint.answer_nameserver() for endpoint in self.nameservers] == [
            "192.0.2.53",
            "192.0.2.54",
        ]
        return args

    monkeypatch.setattr(asyncresolver.Resolver, "resolve", fake_resolve)
    backend = object()
    result = await asyncresolver.resolve_at(
        name("resolver.example."),
        "www.example.",
        source="192.0.2.1",
        source_port=4321,
        port=5053,
        family=socket.AF_INET,
        backend=backend,
        resolver=Bootstrap(),
    )
    assert result[:2] == ("www.example.", wire.RecordType.A)
    assert result[4] == "192.0.2.1" and result[6] == 4321
    assert result[-1] is backend


@contextmanager
def _dual_protocol_listener():
    for attempt in range(10):
        with socket.socket() as listener, socket.socket(type=socket.SOCK_DGRAM) as udp:
            listener.bind(("127.0.0.1", 0))
            try:
                udp.bind(listener.getsockname())
            except OSError as exc:
                if exc.errno not in (EACCES, EADDRINUSE, 10013, 10048) or attempt == 9:
                    raise
                continue
            listener.listen()
            listener.settimeout(3)
            udp.settimeout(3)
            yield listener, udp
            return


@pytest.mark.parametrize("mode", ["owned", "borrowed", "resolver"])
def test_sync_query_udp_tcp_fallback_matches_the_query_and_keeps_borrowed_udp_socket(
    mode, monkeypatch
):
    borrow_udp = mode == "borrowed"
    created = []

    def factory(family, kind, proto):
        sock = syncquery.default_socket_factory(family, kind, proto)
        created.append((kind, proto, sock))
        return sock

    monkeypatch.setattr(syncquery, "socket_factory", factory)
    with (
        _dual_protocol_listener() as (listener, udp_peer),
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as borrowed,
        ThreadPoolExecutor(max_workers=1) as executor,
    ):
        host, port = listener.getsockname()
        borrowed.bind((host, 0))
        original_source = borrowed.getsockname()
        borrowed.settimeout(0.25)

        def peer():
            data, source = udp_peer.recvfrom(65535)
            if borrow_udp:
                assert source == original_source
            request = message.from_wire(data)
            if mode != "resolver":
                assert request.id == 900
            reply = message.make_response(request)
            reply.flags |= flags.TC
            udp_peer.sendto(reply.to_wire(), source)
            connection, _ = listener.accept()
            with connection:
                received, _ = syncquery.receive_tcp(connection)
                assert received.question == request.question
                response = message.make_response(received)
                answer = response.find_rrset(
                    response.answer,
                    name("example."),
                    "IN",
                    "A",
                    create=True,
                )
                answer.add(rdata.from_text("IN", "A", "192.0.2.10"), 60)
                syncquery.send_tcp(connection, response)

        completed = executor.submit(peer)
        if mode == "resolver":
            client = resolver.Resolver([host], port=port, timeout=3)
            assert client.resolve("example.", "A")[0].address == "192.0.2.10"
        else:
            request = message.make_query("example.", "A", id=900)
            response, used_tcp = syncquery.udp_with_fallback(
                request,
                host,
                timeout=3,
                port=port,
                udp_sock=borrowed if borrow_udp else None,
            )
            assert used_tcp and response.answer[0][0].address == "192.0.2.10"
        completed.result(timeout=3)
        assert (
            borrowed.getsockname() == original_source and borrowed.gettimeout() == 0.25
        )
        expected = [socket.SOCK_STREAM]
        if not borrow_udp:
            expected.insert(0, socket.SOCK_DGRAM)
        assert [kind for kind, _, _ in created] == expected
        assert all(proto == 0 and sock.fileno() == -1 for _, proto, sock in created)


def test_sync_socket_factory_closes_socket_when_source_binding_fails(monkeypatch):
    allocated = []

    def factory(*args):
        connection = socket.socket(*args)
        allocated.append(connection)
        return connection

    monkeypatch.setattr(syncquery, "socket_factory", factory)
    with pytest.raises(OSError):
        syncquery.make_socket(socket.AF_INET, socket.SOCK_STREAM, ("::1", 0))
    assert len(allocated) == 1 and allocated[0].fileno() == -1

"""Behavior checks for the public in-house DNS toolkit APIs."""

import socket
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from io import BytesIO, StringIO
from time import time

import pytest
from tba_codec_dns import rdata, rdataset, rrset
from tba_codec_dns.edns import ExtendedError
from tba_codec_dns.wire import (
    CopyMode,
    EdnsOption,
    Message,
    Parser,
    RecordClass,
    RecordType,
    Section,
    ShortHeader,
    TooBig,
    TrailingJunk,
    Truncated,
    WireError,
    make_query,
    make_response,
)
from tba_primitives_dns_name import e164, name, reversename
from tba_provider_dns_resolver.client import Cache, NoAnswer, Resolver
from tba_protocol_dns.dnssec import (
    Algorithm,
    Flag,
    ValidationError,
    algorithm_from_text,
    algorithm_to_text,
    make_cdnskey,
    make_dnskey,
    make_ds_rdataset,
    sign_rrset,
    validate_rrsig,
)
from tba_provider_dns_resolver.tsig import TsigKey, sign, verify
from tba_protocol_dns.update import Update
from tba_concrete_dns_zone.zone import Zone


def test_public_dns_name_representation_order_and_wire_compression():
    origin = name.from_text("Example.")
    relative = name.from_text(r"MiX.a\.b", origin=None)
    owner = relative.derelativize(origin)
    assert owner == name.from_text(r"mix.a\.b.example.")
    assert owner.labels == (b"MiX", b"a.b", b"Example", b"")
    assert owner.relativize(origin) == relative
    assert owner.fullcompare(origin) == (name.NameRelation.SUBDOMAIN, 1, 2)
    assert relative < name.root < origin < owner
    assert owner.split(2) == (relative, origin)
    assert owner.to_digestable() == b"\x03mix\x03a.b\x07example\0"
    mapping = name.NameDict({origin: "zone", owner: "host", name.root: "root"})
    assert (
        mapping.get_deepest_match(name.from_text(r"child.MIX.a\.b.example."))[1]
        == "host"
    )
    assert mapping.max_depth == 4 and mapping.max_depth_items == 1

    stream = BytesIO()
    offsets = {}
    origin.to_wire(stream, offsets)
    start = stream.tell()
    owner.to_wire(stream, offsets)
    assert stream.getvalue().endswith(b"\xc0\0")
    assert name.from_wire(stream.getvalue(), start) == (owner, stream.tell() - start)
    assert name.from_unicode("faß.example.").to_unicode(idna2008=True) == "faß.example."
    assert (
        reversename.to_address(reversename.from_address("2001:db8::2")) == "2001:db8::2"
    )
    assert e164.to_e164(e164.from_e164("+44 20 7946 0123")) == "+442079460123"


def test_dnssec_canonical_predecessor_and_successor():
    origin = name.from_text("example.com.")
    target = name.from_text("Foo", origin=None)
    after = target.successor(origin)
    before = target.predecessor(origin)
    assert after.labels == (b"\0", b"foo")
    assert before < target < after
    assert after.predecessor(origin) == target
    assert before.successor(origin) == target
    assert target.successor(origin, prefix_ok=False) == name.Name((b"foo\0",))
    assert origin.predecessor(origin).successor(origin) == origin


def test_wire_parser_keeps_rdata_bounds_and_can_read_compressed_names():
    parser = Parser(b"\x07example\0\xc0\0\xc0\x00\x02\x09", 9)
    with parser.restrict_to(2):
        assert name.from_wire_parser(parser) == name.from_text("example.")
    with parser.restrict_to(4):
        value = rdata.from_wire_parser("IN", "A", parser)
        assert value.address == "192.0.2.9"
    with pytest.raises(WireError, match="truncated"):
        parser.get_uint8()
    with pytest.raises(WireError, match="unconsumed"):
        with Parser(b"abc").restrict_to(2) as field:
            field.get_uint8()


def test_custom_rdata_codec_feeds_zone_wire_and_canonical_comparison():
    class CounterCodec:
        def from_tokens(self, tokens, origin):
            (counter,) = tokens
            return int(counter).to_bytes(2, "big")

        def decode(self, record):
            parser = Parser(record.data)
            with parser.restrict_to(2):
                return (parser.get_uint16(),)

        def to_text(self, fields):
            return str(fields[0])

        def to_wire(self, fields, *, canonical):
            return fields[0].to_bytes(2, "big")

    rdata.register_type("IN", 65401, CounterCodec())
    value = rdata.from_text("IN", "TYPE65401", "300")
    assert value.to_wire() == b"\x01\x2c"
    assert value == rdata.from_wire("IN", 65401, b"\x01\x2c")
    assert value.to_text() == "300"
    assert isinstance(rdata.from_wire("CH", 65401, b"\x01\x2c"), rdata.GenericRdata)
    with pytest.raises(WireError):
        rdata.from_wire("IN", 65401, b"\x01")
    with pytest.raises(ValueError, match="already registered"):
        rdata.register_type("IN", 65401, CounterCodec())
    zone = Zone.from_text("$TTL 1\n@ TYPE65401 300", "example.", check_origin=False)
    assert zone["@"].get_rdataset("IN", 65401)[0] == value


def test_idna_styles_keep_unquoted_unicode_and_canonical_ascii():
    unicode_name = name.from_unicode("faß.example.", idna_codec=name.IDNA_2008_Strict)
    assert unicode_name.to_text() == "xn--fa-hia.example."
    assert (
        unicode_name.to_text(
            style=name.NameStyle(omit_final_dot=True, idna_codec=name.IDNA_2008_Strict)
        )
        == "faß.example"
    )


def test_zone_transactions_keep_reader_snapshot_and_roll_back():
    zone = Zone("example.")
    host = name.from_text("www", origin=None)
    dataset = rdataset.from_text("IN", "A", 60, "192.0.2.5")
    with zone.reader() as old:
        with zone.writer() as writer:
            assert not writer.changed()
            writer.replace(host, dataset)
            assert writer.changed()
            assert writer.get(host, "A") == dataset
        assert not old.name_exists(host)
        with pytest.raises(RuntimeError, match="read-only"):
            old.replace(host, dataset)
    assert list(zone.get(host, "A")) == list(dataset)
    with zone.writer(replacement=True) as writer:
        assert writer.changed()
        assert not writer.name_exists(host)
        writer.rollback()
    assert zone.get_rdataset(host, "A") == dataset
    with pytest.raises(ValueError, match="abort transaction"):
        with zone.writer(replacement=True):
            raise ValueError("abort transaction")
    assert zone.get_rdataset(host, "A") == dataset


def test_zone_serial_updates_wrap_and_share_the_writer_transaction():
    zone = Zone.from_text(
        "$TTL 60\n@ SOA ns admin 4294967295 900 300 86400 60\n@ NS ns", "example."
    )
    with zone.reader() as before, zone.writer() as writer:
        writer.update_serial()
        assert writer.get("@", "SOA")[0].serial == 0
        assert before.get("@", "SOA")[0].serial == 4294967295
    assert zone.get_soa().serial == 0
    assert zone.find_rrset("example.", "SOA")[0].serial == 0


def test_update_builds_prerequisites_and_edits_from_text_or_datasets():
    value = rdata.from_text("IN", "A", "192.0.2.1")
    dataset = rdataset.from_rdata(300, value)
    update = Update(name.from_text("example."))
    update.present("host", dataset)
    update.add("host", dataset)
    update.delete("host", value)
    update.replace("host", 120, "MX", "10 mail")
    with pytest.raises(ValueError):
        update.add("host", 10, "A", "192.0.2.2", "invalid")
    decoded = Message.from_wire(update.message(37).to_wire())
    assert decoded.opcode == 5
    assert rdata.from_record(decoded.answers[0]) == value
    assert [(rr.type, rr.rdclass, rr.ttl) for rr in decoded.authority] == [
        (RecordType.A, RecordClass.IN, 300),
        (RecordType.A, RecordClass.NONE, 0),
        (RecordType.MX, RecordClass.ANY, 0),
        (RecordType.MX, RecordClass.IN, 120),
    ]
    assert rdata.from_record(decoded.authority[-1]).exchange == name.from_text(
        "mail.example."
    )


def test_rdata_rrsets_and_zone_dataset_access(tmp_path):
    origin = name.from_text("example.")
    mx = rdata.from_text("IN", "MX", "10 MAIL", origin)
    assert mx.exchange == name.from_text("mail.example.")
    assert mx.preference == 10
    assert mx.to_text(origin) == "10 MAIL"
    assert mx == rdata.from_text(1, 15, "10 mail.example.")
    wire = mx.to_wire()
    assert rdata.from_wire("IN", "MX", wire) == mx
    changed = mx.replace(preference=20, exchange="backup.example.")
    unknown = rdata.from_text("IN", "TYPE65400", r"\# 2 12AB")
    assert isinstance(unknown, rdata.GenericRdata)
    assert unknown.to_text() == r"\# 2 12AB"
    first = rdataset.from_rdata(300, mx)
    second = rdataset.from_rdata(60, changed)
    combined = first.union(second)
    assert list(combined) == [mx, changed] and combined.ttl == 60
    assert tuple(combined.difference(second)) == (mx,)
    with pytest.raises(ValueError, match="does not match"):
        combined.add(unknown)
    typed_set = rrset.from_rdataset("example.", combined)
    assert typed_set.name == origin
    assert tuple(typed_set) == (mx, changed)

    zone = Zone.from_text(
        "$TTL 600\n@ SOA ns admin 5 900 300 86400 60\n@ NS ns", "example."
    )
    zone.replace_rdataset(name.empty, combined)
    assert zone["@"].get_rdataset("IN", "MX").ttl == 60
    assert origin in list(zone)
    assert list(zone.iterate_rdatasets("MX"))[0][0] == origin
    path = tmp_path / "db.example"
    zone.to_file(path)
    loaded = Zone.from_file(path, "example.")
    assert loaded.find_rdataset(origin, "MX") == combined
    loaded.delete_rdataset(origin, "MX")
    assert loaded.get_rdataset(origin, "MX") is None


def test_message_rrset_lookup_and_text_file(tmp_path):
    query = make_query("www.example.", "A", identifier=177)
    values = rrset.from_text("www.example.", 60, "IN", "A", "192.0.2.4", "192.0.2.6")
    result = replace(make_response(query), answers=values.records)
    assert result.section_number("answer") == Section.ANSWER
    assert (
        result.find_rrset(Section.QUESTION, "www.example.", "IN", "A").name
        == values.name
    )
    assert (
        result.find_rrset(result.answers, values.name, "IN", "A").records
        == values.records
    )
    assert result.get_rrset("authority", values.name, "IN", "SOA") is None
    assert Message.from_file(StringIO(result.to_text())) == result
    path = tmp_path / "reply.txt"
    path.write_text(result.to_text(), encoding="utf-8")
    assert Message.from_file(path) == result


def test_message_size_limit_preserves_complete_rrsets_and_edns():
    query = make_query("www.example.", "A", edns_payload=1232)
    response = make_response(query)
    addresses = rrset.from_text(
        "www.example.", 60, "IN", "A", "192.0.2.4", "192.0.2.5"
    ).records
    answer = replace(response, answers=addresses)
    one = replace(response, answers=addresses[:1])
    size = len(one.to_wire(compress=True))
    with pytest.raises(TooBig):
        answer.to_wire(compress=True, max_size=size)
    cut = answer.to_wire(
        compress=True, max_size=size, prefer_truncation=True, prepend_length=True
    )
    assert int.from_bytes(cut[:2], "big") == len(cut) - 2
    result = Message.from_wire(cut[2:])
    assert result.flags & 0x0200 and not result.answers
    assert result.edns == response.edns
    optional = replace(response, additional=(*response.additional, *addresses))
    result = Message.from_wire(
        optional.to_wire(max_size=len(response.to_wire()), prefer_truncation=True)
    )
    assert result.edns == response.edns and not result.flags & 0x0200


def test_message_question_only_parser_copy_policy_and_extended_errors():
    error = ExtendedError(15, "test response")
    query = make_query("example.", edns_options=(error.to_option(),))
    assert query.get_options(15) == (error.to_option(),)
    assert query.extended_errors() == (error,)
    additional = rdata.from_text("IN", "A", "192.0.2.4").record((b"example",), 60)
    query = replace(query, additional=(*query.additional, additional))
    assert make_response(query, copy_mode=CopyMode.NOTHING).questions == ()
    full = make_response(query, copy_mode=CopyMode.EVERYTHING)
    assert full.questions == query.questions and full.additional[0] == additional
    assert not full.extended_errors()
    packet = full.to_wire()
    assert Message.from_wire(packet, question_only=True).questions == full.questions
    assert Message.from_wire(packet, question_only=True).additional == ()
    assert Message.from_wire(packet + b"extra", ignore_trailing=True) == full
    with pytest.raises(WireError, match="trailing"):
        Message.from_wire(packet + b"extra")


def test_message_padding_uses_serialized_length_and_respects_limits():
    query = make_query("example.", pad=128)
    wire = query.to_wire(compress=True)
    assert len(wire) == 128
    padded = Message.from_wire(wire)
    assert len(padded.get_options(12)) == 1
    response = make_response(padded)
    assert len(response.to_wire()) == 468
    assert not Message.from_wire(response.to_wire(max_size=128)).get_options(12)
    assert not Message.from_wire(make_response(padded, pad=0).to_wire()).get_options(12)


def test_wire_reports_truncation_with_a_partial_response_and_preserves_input():
    query = make_query("example.", identifier=21)
    response = replace(make_response(query), flags=0x8200)
    packet = response.to_wire()
    assert Message.from_wire(packet).wire == packet
    with pytest.raises(Truncated) as exc:
        Message.from_wire(packet, raise_on_truncation=True)
    assert query.is_response(exc.value.partial)
    with pytest.raises(ShortHeader):
        Message.from_wire(packet[:11])
    with pytest.raises(TrailingJunk):
        Message.from_wire(packet + b"extra")


def test_typed_rdata_names_and_fields_round_trip():
    host = rdata.from_text("IN", "RP", "abuse.example. policy.example.")
    assert host.mbox == name.from_text("abuse.example.")
    assert host.replace(txt="documentation.example.").txt == name.from_text(
        "documentation.example."
    )
    fingerprint = rdata.from_text("IN", "SSHFP", "4 2 " + "ABBA" * 16)
    assert fingerprint.fingerprint == b"\xab\xba" * 16
    assert (
        fingerprint.replace(fp_type=1, fingerprint=b"\xab\xba" * 10).to_text()
        == "4 1 " + "ABBA" * 10
    )
    parameters = rdata.from_text("IN", "NSEC3PARAM", "1 0 10 AB")
    assert parameters.iterations == 10
    assert rdata.from_wire("IN", "NSEC3PARAM", parameters.to_wire()) == parameters


def test_revoked_dnssec_key_only_validates_its_dnskey_rrset():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    private = Ed25519PrivateKey.from_private_bytes(bytes(32))
    key = make_dnskey(
        "example.",
        private.public_key(),
        Algorithm.ED25519,
        flags=Flag.ZONE | Flag.REVOKE,
    )
    key_signature = sign_rrset((key,), key, private, inception=100, expiration=200)
    validate_rrsig((key,), key_signature, (key,), now=150)
    address = rdata.from_text("IN", "A", "192.0.2.4").record((b"example",), 60)
    signature = sign_rrset((address,), key, private, inception=100, expiration=200)
    with pytest.raises(ValidationError, match="no DNSKEY"):
        validate_rrsig((address,), signature, (key,), now=150)


def test_resolver_answer_retains_aliases_and_configures_cache_and_edns():
    cache = Cache()
    config = StringIO("nameserver 127.0.0.1\nsearch example.\noptions ndots:2\n")
    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer,
        ThreadPoolExecutor(max_workers=1) as pool,
    ):
        peer.bind(("127.0.0.1", 0))
        peer.settimeout(5)
        resolver = Resolver(
            filename=config,
            cache=cache,
            use_search_by_default=True,
            nameserver_ports={"127.0.0.1": peer.getsockname()[1]},
        )
        resolver.use_edns(0, payload=1400, options=(EdnsOption(12, b"\0"),))

        def serve():
            packet, caller = peer.recvfrom(65535)
            query = Message.from_wire(packet)
            assert query.edns.payload == 1400
            assert query.edns.options == (EdnsOption(12, b"\0"),)
            (alias,) = query.questions
            assert alias.name == (b"alias", b"example")
            answers = (
                rdata.from_text("IN", "CNAME", "real.example.").record(alias.name, 15),
                rdata.from_text("IN", "A", "192.0.2.7").record(
                    (b"real", b"example"), 60
                ),
            )
            response = replace(make_response(query), answers=answers)
            peer.sendto(response.to_wire(), caller)

        completed = pool.submit(serve)
        start = time()
        answer = resolver.resolve_answer(name.from_text("alias", origin=None))
        assert answer.qname == name.from_text("alias.example.")
        assert answer.canonical_name == name.from_text("real.example.")
        assert answer.aliases[0].type == RecordType.CNAME
        assert answer.rrset.ttl == 60
        assert start + 14 <= answer.expiration <= time() + 15
        assert len(answer) == 1
        assert list(resolver.resolve("alias")) == [
            rdata.from_record(rr) for rr in answer.records
        ]
        stats = cache.get_statistics_snapshot()
        assert (stats.hits, stats.misses) == (1, 1)
        completed.result(timeout=5)


def test_resolver_servfail_retry_and_tsig_verification():
    key = TsigKey((b"key", b"example"), b"isolated resolver test key")
    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer,
        ThreadPoolExecutor(max_workers=1) as pool,
    ):
        peer.bind(("127.0.0.1", 0))
        peer.settimeout(5)
        resolver = Resolver(
            ["127.0.0.1"], port=peer.getsockname()[1], retry_servfail=True
        )
        resolver.use_tsig(key)

        def serve():
            for code in (2, 0):
                data, caller = peer.recvfrom(65535)
                request = Message.from_wire(data)
                mac = verify(data, key).mac
                response = make_response(request, rcode=code)
                if code == 0:
                    response = replace(
                        response,
                        answers=(
                            rdata.from_text("IN", "A", "192.0.2.9").record(
                                request.questions[0].name, 60
                            ),
                        ),
                    )
                wire, _ = sign(response.to_wire(), key, request_mac=mac)
                peer.sendto(wire, caller)

        completed = pool.submit(serve)
        records = resolver.resolve("example.")
        assert records[0].address == "192.0.2.9"
        completed.result(timeout=5)


def test_resolver_nodata_can_return_an_empty_answer(monkeypatch):
    resolver = Resolver(configure=False)

    def mock_query(question, *_args, **_kwargs):
        response = make_response(question.query_message(133))
        soa = rdata.from_text(
            "IN", "SOA", "ns.example. admin.example. 1 1800 600 86400 10"
        )
        return replace(response, authority=(soa.record((b"example",), 3600),))

    monkeypatch.setattr(resolver, "_query", mock_query)
    before = time()
    answer = resolver.resolve_answer("example.", "TXT", raise_on_no_answer=False)
    assert answer.rrset is None and len(answer) == 0
    assert before + 9 <= answer.expiration <= time() + 10
    with pytest.raises(NoAnswer) as error:
        resolver.resolve("example.", "TXT")
    assert error.value.answer.response.rcode() == 0


def test_dnssec_algorithm_and_digest_dataset_apis():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    public = Ed25519PrivateKey.generate().public_key()
    assert algorithm_from_text("ED25519") == Algorithm.ED25519
    assert algorithm_to_text(15) == "ED25519"
    key = make_dnskey("example.", public, "ED25519")
    child_key = make_cdnskey("example.", public, "ED25519")
    assert child_key.type == RecordType.CDNSKEY
    keys = rdataset.from_records((key,))
    delegation = make_ds_rdataset("example.", keys, ("SHA-256", "SHA384"))
    assert delegation.rdtype == RecordType.DS
    assert {item.digest_type for item in delegation} == {2, 4}
    assert make_ds_rdataset("example.", keys, cds=True).rdtype == RecordType.CDS

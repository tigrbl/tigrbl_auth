from dataclasses import replace
from functools import partial
from io import StringIO
import asyncio
import socket
from concurrent.futures import ThreadPoolExecutor
from time import time

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.mldsa import MLDSA44PrivateKey

from tba_codec_dns import message, rdata, rdataset, rrset, wire
from tba_codec_dns.rdtypes.ANY.CDNSKEY import CDNSKEY
from tba_codec_dns.rdtypes.ANY.DNSKEY import DNSKEY
from tba_codec_dns.tsig import TsigKey
from tba_concrete_dns_zone.zone import Zone
from tba_concrete_dns_zone.zonefile import Reader, read_rrsets
from tba_primitives_dns_name.name import from_text as name
from tba_protocol_dns import dnssec, xfr
from tba_provider_dns_resolver.client import (
    Answer,
    AsyncResolver,
    Cache,
    LRUCache,
    NXDOMAIN,
    NoAnswer,
    Resolver,
)
from tba_provider_dns_resolver.nameserver import (
    Do53Nameserver,
    DoHNameserver,
    DoQNameserver,
    DoTNameserver,
)


def test_nsec3_base32hex_text_is_canonical():
    assert rdata.from_text("IN", "NSEC3", "1 0 0 - 00 A").next == b"\0"
    with pytest.raises(ValueError, match="noncanonical"):
        rdata.from_text("IN", "NSEC3", "1 0 0 - 01 A")


def test_mldsa44_dnskey_and_cds_match_published_vector():
    # The IETF ML-DSA DNSSEC draft, section 6, publishes this seed and DS digest.
    secret = MLDSA44PrivateKey.from_seed_bytes(bytes(range(32)))
    owner = "example.com."
    key = dnssec.make_dnskey(secret.public_key(), "ML-DSA-44", flags=257).record(
        name(owner).labels[:-1],
        3600,
    )
    assert len(rdata.from_record(key).key) == 1312
    dataset = rdataset.from_records((key,))
    cds = dnssec.dnskey_rdataset_to_cds_rdataset(
        name("example", origin=None), dataset, "SHA256", name("com.")
    )
    assert cds.rdtype == wire.RecordType.CDS
    assert cds.ttl == dataset.ttl
    assert cds[0].key_tag == 59829
    assert (
        cds[0].digest.hex()
        == "812cb1a22af04380e2f72d91c06c14eb1a918cf30037a8a9c67497e9264b4bfa"
    )
    ds = dnssec.cds_rdataset_to_ds_rdataset(cds)
    assert ds.rdtype == wire.RecordType.DS and ds[0].digest == cds[0].digest
    child = dnssec.dnskey_rdataset_to_cdnskey_rdataset(dataset)
    assert child.rdtype == wire.RecordType.CDNSKEY and child[0].key == dataset[0].key
    assert dnssec.key_id(dataset[0]) == cds[0].key_tag
    mx = rdata.from_text("IN", "MX", "10 mail.example.com.").record(key.name, key.ttl)
    sig = dnssec.sign_rrset((mx,), key, secret, inception=100, expiration=200)
    assert len(rdata.from_record(sig).signature) == 2420
    dnssec.validate_rrsig((mx,), sig, (key,), now=150)
    with pytest.raises(dnssec.ValidationError):
        dnssec.validate_rrsig(
            (replace(mx, data=b"\x00\x01" + mx.data[2:]),), sig, (key,), now=150
        )


def test_set_id_updates_a_pending_tsig():
    key = TsigKey((b"key", b"example"), b"shared secret")
    query = message.make_query("example.", id=123)
    query.use_tsig(key, original_id=123)
    query.set_id(0)
    verified = message.from_wire(query.to_wire(), keyring=key)
    assert verified.id == 0
    assert rdata.from_record(verified._tsig).original_id == 0


_ZONE_TEXT = """$TTL 3600
@ IN SOA ns.example. hostmaster.example. 7 3600 600 86400 60
@ IN NS ns.example.
ns IN A 192.0.2.53
"""


def test_zonefile_reader_uses_caller_transaction_and_forced_fields():
    zone = Zone("example.", relativize=True)
    with zone.writer() as txn:
        Reader(StringIO(_ZONE_TEXT), "IN", txn).read()
        Reader(
            "192.0.2.2\n",
            "IN",
            txn,
            allow_directives=False,
            force_name="www",
            force_ttl=30,
            force_rdclass="IN",
            force_rdtype="A",
        ).read()
        assert not tuple(zone.records())
    assert zone.get_soa().serial == 7
    assert zone.get_rdataset("www", "A").ttl == 30
    with pytest.raises(ValueError, match="directive"):
        with zone.writer() as txn:
            Reader("$TTL 30\n", "IN", txn, allow_directives=False).read()


def test_xfr_low_level_query_and_atomic_axfr():
    dest = Zone("example.", relativize=True)
    src = Zone.from_text(_ZONE_TEXT, "example.")
    opening = next(rr for rr in src.records() if rr.type == wire.RecordType.SOA)
    contents = tuple(rr for rr in src.records() if rr != opening)
    query, serial = xfr.make_query(dest, use_edns=True, payload=1400)
    assert serial is None and xfr.extract_serial_from_query(query) is None
    assert query.payload == 1400
    first = wire.Message(query.id, 0x8400, answers=(opening, *contents))
    last = replace(first, answers=(opening,))
    with xfr.Inbound(dest) as transfer:
        assert not transfer.process_message(first)
    assert not tuple(dest.records())
    checks = []
    with xfr.Inbound(dest, transaction_setup=checks.append) as transfer:
        assert not transfer.process_message(first)
        assert transfer.process_message(last)
    assert len(checks) == 1
    assert set(dest.records()) == set(src.records())
    ixfr, serial = xfr.make_query(dest)
    assert serial == 7 and xfr.extract_serial_from_query(ixfr) == 7
    assert xfr.extract_serial_from_query(xfr.make_query(dest, 42)[0]) == 42
    with xfr.Inbound(dest, wire.RecordType.IXFR, 7, is_udp=True) as transfer:
        assert transfer.process_message(last)
    with pytest.raises(xfr.TransferError) as failure:
        with xfr.Inbound(dest) as transfer:
            transfer.process_message(replace(first, flags=0x8405))
    assert failure.value.rcode == 5


def test_cache_public_answer_keys_and_lru():
    q = wire.make_query("example.", "A")
    answer = Answer(
        q.questions[0], wire.make_response(q), name("example."), None, time() + 60
    )
    first = (answer.qname, answer.rdtype, answer.rdclass)
    second = (name("other.example."), answer.rdtype, answer.rdclass)
    for cache in (Cache(cleaning_interval=10), LRUCache(1)):
        cache.put(first, answer)
        assert cache.get(first) is answer
        assert cache.get_statistics_snapshot().hits == 1
        cache.put(second, answer)
        if isinstance(cache, LRUCache):
            assert cache.get(first) is None
            assert cache.get(second) is answer
            assert cache.get_hits_for_key(second) == 1
        cache.flush(second)
        assert cache.get(second) is None


@pytest.mark.asyncio
async def test_resolve_binds_source_and_handles_no_answer():
    with (
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer,
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as reservation,
        ThreadPoolExecutor(max_workers=1) as pool,
    ):
        peer.bind(("127.0.0.1", 0))
        peer.settimeout(5)
        reservation.bind(("127.0.0.1", 0))
        source_port = reservation.getsockname()[1]
        reservation.close()
        endpoint = Do53Nameserver("127.0.0.1", peer.getsockname()[1])

        def serve():
            for _ in range(3):
                packet, sender = peer.recvfrom(65535)
                query = wire.Message.from_wire(packet)
                peer.sendto(wire.make_response(query).to_wire(), sender)
                assert sender == ("127.0.0.1", source_port)

        completed = pool.submit(serve)
        options = {"source": "127.0.0.1", "source_port": source_port}
        plain = Resolver([endpoint])
        invoke = asyncio.get_running_loop().run_in_executor

        result = await invoke(
            None,
            partial(plain.resolve, "example.", raise_on_no_answer=False, **options),
        )
        assert isinstance(result, Answer) and result.rrset is None
        asynchronous = AsyncResolver([endpoint])
        result = await asynchronous.resolve(
            "example.", raise_on_no_answer=False, **options
        )
        assert isinstance(result, Answer) and result.rrset is None
        with pytest.raises(NoAnswer):
            await asynchronous.resolve("example.", **options)
        completed.result(timeout=5)


def test_nameserver_metadata_and_discovery_methods(monkeypatch):
    from tba_provider_dns_resolver import ddr

    for endpoint, kind, port in (
        (Do53Nameserver("127.0.0.1"), "Do53", 53),
        (DoTNameserver("127.0.0.1"), "DoT", 853),
        (DoQNameserver("127.0.0.1"), "DoQ", 853),
        (DoHNameserver("https://example.test:8443/dns-query"), "DoH", 8443),
    ):
        assert endpoint.kind() == kind
        assert endpoint.answer_port() == port
        assert Resolver([endpoint]).nameservers == (endpoint,)
    resolver = Resolver(["127.0.0.1"])
    monkeypatch.setattr(ddr, "discover", lambda resolver, **kwargs: (endpoint,))
    assert resolver.try_ddr() is None
    assert resolver.nameservers == (endpoint,)


def test_zonefile_read_rrsets_with_forced_fields():
    (result,) = read_rrsets(
        StringIO("192.0.2.1\n192.0.2.2\n"),
        name="www",
        origin="example.",
        ttl=120,
        rdtype="A",
        relativize=True,
    )
    assert result.name == name("www", origin=None)
    assert result.ttl == 120
    assert [item.address for item in result] == ["192.0.2.1", "192.0.2.2"]


def test_low_level_ixfr_applies_only_exact_deletions():
    zone = Zone.from_text(_ZONE_TEXT, "example.")
    soa = next(rr for rr in zone.records() if rr.type == wire.RecordType.SOA)
    address = next(rr for rr in zone.records() if rr.type == wire.RecordType.A)
    new_soa = zone.get_soa().replace(serial=8).record(soa.name, soa.ttl)
    new_address = rdata.from_text("IN", "A", "192.0.2.2").record(
        address.name, address.ttl
    )
    first = wire.Message(12, 0x8400, answers=(new_soa, soa, address))
    last = replace(first, answers=(new_soa, new_address, new_soa))
    with xfr.Inbound(zone, wire.RecordType.IXFR, 7) as transfer:
        assert not transfer.process_message(first)
        assert zone.get_soa().serial == 7
        assert transfer.process_message(last)
    assert zone.get_soa().serial == 8
    assert zone.get_rdataset("ns", "A")[0].address == "192.0.2.2"


def test_host_answers_use_socket_families_and_return_typed_data(monkeypatch):
    resolver = Resolver(configure=False)

    def reply(question, *_args, **_kwargs):
        query = question.query_message(10)
        text = {wire.RecordType.AAAA: "2001:db8::1", wire.RecordType.A: "192.0.2.1"}[
            question.type
        ]
        record = rdata.from_text("IN", question.type, text).record(question.name, 60)
        return replace(wire.make_response(query), answers=(record,)), "192.0.2.53", 53

    monkeypatch.setattr(resolver, "_query", reply)
    answers = resolver.resolve_name("example.")
    assert list(answers.addresses()) == ["2001:db8::1", "192.0.2.1"]
    assert list(answers.addresses(socket.AF_INET)) == ["192.0.2.1"]
    assert answers.canonical_name() == name("example.")
    v4 = answers[wire.RecordType.A]
    assert v4[0].address == "192.0.2.1"
    assert v4.response.rcode() == 0
    assert v4.nameserver == "192.0.2.53" and v4.port == 53
    assert v4.chaining_result.minimum_ttl == 60


def test_typed_dnssec_sign_and_validate_rrset():
    secret = MLDSA44PrivateKey.from_seed_bytes(bytes(range(32)))
    owner = name("example.")
    key = dnssec.make_dnskey(owner.to_text(), secret.public_key(), "MLDSA44")
    mx = rrset.from_text(owner, 90, "IN", "MX", "10 mail.example.")
    sig = dnssec.sign(mx, secret, owner, rdata.from_record(key), 100, 200, verify=True)
    signatures = rrset.from_rdata(owner, 90, sig)
    keys = {owner: rdataset.from_records((key,))}
    dnssec.validate(mx, signatures, keys, now=150)
    dnssec.validate_rrsig(mx, sig, keys, now=150.25)


def test_resolver_exposes_nxdomain_responses_for_search_candidates(monkeypatch):
    resolver = Resolver(configure=False, search=["example."])

    def missing(question, *_args, **_kwargs):
        return replace(wire.make_response(question.query_message(5)), flags=0x8103)

    monkeypatch.setattr(resolver, "_query", missing)
    with pytest.raises(NXDOMAIN) as failure:
        resolver.resolve("missing", search=True)
    candidates = [name("missing.example."), name("missing.")]
    assert failure.value.qnames() == candidates
    assert failure.value.canonical_name == candidates[0]
    assert set(failure.value.responses()) == set(candidates)
    for candidate in candidates:
        assert failure.value.response(candidate).rcode() == 3


def test_key_factories_return_typed_rdata_and_accept_protocol():
    public = Ed25519PrivateKey.from_private_bytes(bytes(range(32))).public_key()

    key = dnssec.make_dnskey(public, "ED25519", 257, 255)
    assert isinstance(key, DNSKEY)
    assert (key.rdclass, key.rdtype, key.flags, key.protocol, key.algorithm) == (
        wire.RecordClass.IN,
        wire.RecordType.DNSKEY,
        257,
        255,
        15,
    )
    assert (
        key.key.hex()
        == "03a107bff3ce10be1d70dd18e74bc09967e4d6309ba50d5f1ddc8664125531b8"
    )
    assert (
        dnssec.make_dnskey(public_key=public, algorithm=15, flags=257, protocol=255)
        == key
    )
    child = dnssec.make_cdnskey(public, "ED25519", flags=257, protocol=255)
    assert isinstance(child, CDNSKEY)
    assert child.rdtype == wire.RecordType.CDNSKEY
    assert (child.flags, child.protocol, child.algorithm, child.key) == (
        key.flags,
        key.protocol,
        key.algorithm,
        key.key,
    )

    legacy = dnssec.make_dnskey(
        "EXAMPLE.", public_key=public, algorithm="ED25519", ttl=120
    )
    assert legacy.name == (b"example",)
    assert legacy == dnssec.make_dnskey(public, 15).record(legacy.name, ttl=120)
    child_record = dnssec.make_cdnskey(
        owner="example.", public_key=public, algorithm=15, ttl=120
    )
    assert child_record == replace(legacy, type=wire.RecordType.CDNSKEY)


def test_key_factories_report_invalid_algorithm_and_key_pairing():
    public = Ed25519PrivateKey.generate().public_key()
    with pytest.raises(dnssec.UnsupportedAlgorithm):
        dnssec.make_dnskey(public, 200)
    with pytest.raises(dnssec.AlgorithmKeyMismatch):
        dnssec.make_dnskey(public, "ED448")
    with pytest.raises(TypeError):
        dnssec.make_dnskey(object(), "ED25519")
    with pytest.raises(ValueError, match="wire range"):
        dnssec.make_dnskey(public, "ED25519", protocol=256)

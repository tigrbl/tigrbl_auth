from io import StringIO

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from tba_codec_dns import rdata
from tba_codec_dns.tokenizer import (
    COMMENT,
    EOF,
    EOL,
    IDENTIFIER,
    QUOTED_STRING,
    WHITESPACE,
    SyntaxError,
    Token,
    Tokenizer,
    UnexpectedEnd,
    UngetBufferFull,
)
from tba_codec_dns.wire import RecordType
from tba_concrete_dns_zone.btreezone import Zone as BTreeZone
from tba_concrete_dns_zone.zone import Zone
from tba_concrete_dns_zone.zonefile import Reader
from tba_primitives_dns_name.name import IDNA_2008, from_text as name
from tba_protocol_dns.dnssec import key_id, make_dnskey, sign_zone, validate_rrsig


def test_tokenizer_stream_preserves_lexical_and_physical_boundaries():
    stream = StringIO('  owner ( "first\rsecond" ; followed by CRLF\r\n next )\r;final')
    tok = Tokenizer(stream, "example.zone")
    assert tok.where() == ("example.zone", 1)
    assert tok.get(want_leading=True) == Token(WHITESPACE, " ")
    assert tok.get() == Token(IDENTIFIER, "owner")
    assert tok.get() == Token(QUOTED_STRING, "first\rsecond")
    assert tok.get(want_comment=True) == Token(COMMENT, " followed by CRLF")
    assert tok.get() == Token(IDENTIFIER, "next")
    assert tok.get_eol_as_token() == Token(EOL, "\n")
    assert tok.where() == ("example.zone", 3)
    assert tok.get().comment == "final"
    assert tok.get() == Token(EOF)
    assert list(Tokenizer(b'a""\t b\n')) == [
        Token(IDENTIFIER, "a"),
        Token(QUOTED_STRING),
        Token(IDENTIFIER, "b"),
        Token(EOL, "\n"),
    ]


def test_tokenizer_pushback_escapes_and_typed_accessors():
    tok = Tokenizer(r'abc\046def "café\255" 255 Ff 4294967295 FFFFFFFFFFFF 1h30m')
    first = tok.get()
    assert first.has_escape and first.unescape().value == "abc.def"
    tok.unget(first)
    with pytest.raises(UngetBufferFull):
        tok.unget(first)
    assert tok.get_identifier() == "abc.def"
    assert tok.get_bytes() == b"caf\xc3\xa9\xff"
    assert tok.get_uint8() == 255
    assert tok.get_uint16(16) == 255
    assert tok.get_uint32() == 4294967295
    assert tok.get_uint48(16) == 281474976710655
    assert tok.get_ttl() == 5400
    assert tok.get_eol() == ""
    tok = Tokenizer("01 02 03\n")
    assert [token.value for token in tok.get_remaining(2)] == ["01", "02"]
    assert tok.concatenate_remaining_identifiers() == "03"
    assert tok.get_eol() == "\n"
    assert not tok.concatenate_remaining_identifiers(allow_empty=True)


@pytest.mark.parametrize("text", ["+1", "1_0", "-1", "0x20", "١"])
def test_tokenizer_rejects_noncanonical_integer_spellings(text):
    with pytest.raises(SyntaxError, match="unsigned"):
        Tokenizer(text).get_int(16)


def test_tokenizer_reports_incomplete_records_and_range_errors():
    with pytest.raises(UnexpectedEnd, match="quoted"):
        Tokenizer('"open').get()
    with pytest.raises(SyntaxError, match="parentheses"):
        list(Tokenizer("( abc"))
    with pytest.raises(SyntaxError, match="8-bit"):
        Tokenizer("256").get_uint8()
    with pytest.raises(SyntaxError, match="numeric escape"):
        Tokenizer(r"\300").get_bytes()
    with pytest.raises(UnexpectedEnd, match="numeric escape"):
        Tokenizer(r"\12").get_string()


def test_zone_reader_and_rdata_consume_existing_tokenizer():
    tok = Tokenizer(
        "skip\r\n$TTL 600\r\nfaß IN CNAME faß.example.\r\n"
        'svc IN HTTPS 1 . alpn="h2,h3"\r\n',
        idna_codec=IDNA_2008,
    )
    assert tok.get_identifier() == "skip"
    tok.get_eol()
    zone = Zone("example.")
    with zone.writer() as change:
        Reader(tok, "IN", change).read()
    owner = name("faß.example.", idna_codec=IDNA_2008)
    assert zone.get_rdataset(owner, "CNAME")[0].target == owner
    assert zone.get_rdataset("svc", "HTTPS").ttl == 600
    assert tok.get().is_eof()

    tokens = Tokenizer("mail.example.\r\n192.0.2.2", idna_codec=IDNA_2008)
    assert rdata.from_text("IN", "PTR", tokens).target == name("mail.example.")
    assert tokens.get_eol() == "\n"
    assert rdata.from_text("IN", "A", tokens).address == "192.0.2.2"
    assert Tokenizer("faß", idna_codec=IDNA_2008).get_name(
        name("example."), relativize=True
    ) == name("faß", origin=None, idna_codec=IDNA_2008)


_APEX = """$TTL 600
@ SOA ns hostmaster 7 600 600 600 900
@ NS ns
"""


def _signing_key(flags):
    private_key = Ed25519PrivateKey.generate()
    dnskey = make_dnskey("example.", private_key.public_key(), "ED25519", flags=flags)
    return private_key, rdata.from_record(dnskey)


@pytest.mark.parametrize("zone_class", [Zone, BTreeZone])
def test_sign_zone_commits_own_transaction_and_closes_relativized_apex_chain(
    zone_class,
):
    zone = zone_class.from_text(_APEX, "example.", relativize=True)
    ksk, zsk = _signing_key(257), _signing_key(256)
    assert sign_zone(zone, keys=[ksk, zsk], inception=100, lifetime=100) is None
    nsec = zone.get_rdataset("@", "NSEC")
    assert nsec.ttl == 900
    assert nsec[0].next == name("example.")
    keys = zone.get_rdataset("@", "DNSKEY")
    assert keys.ttl == 600 and len(keys) == 2
    for kind, key in [("DNSKEY", ksk[1]), ("SOA", zsk[1]), ("NSEC", zsk[1])]:
        rrset = zone.get_rrset("@", kind)
        sig = zone.get_rdataset("@", "RRSIG", covers=kind)[0]
        assert sig.key_tag == key_id(key)
        validate_rrsig(rrset, sig, {name("example."): keys}, now=150)


def test_sign_zone_stages_writes_in_supplied_transaction_and_uses_live_records():
    zone = BTreeZone.from_text(_APEX, "example.")
    private, key = _signing_key(256)
    with zone.writer() as change:
        change.add("new", 180, rdata.from_text("IN", "A", "192.0.2.1"))
        assert (
            sign_zone(
                zone,
                change,
                [(private, key)],
                True,
                1234,
                100,
                200,
            )
            is None
        )
        assert change.get("@", "DNSKEY").ttl == 1234
        assert change.get("new", "RRSIG", "A")
        assert zone.get_rdataset("new", "A") is None
        change.rollback()
    assert zone.get_rdataset("@", "DNSKEY") is None
    assert zone.get_rdataset("new", "A") is None


def test_sign_zone_custom_signer_and_delegation_boundaries():
    zone = Zone.from_text(
        _APEX + "branch NS ns.branch\nns.branch A 192.0.2.1\n", "example."
    )
    observed = []

    def inspect(change, rrset):
        assert change.get(rrset.name, rrset.rdtype)
        observed.append((rrset.name, rrset.rdtype))

    sign_zone(zone, keys=[_signing_key(256)], add_dnskey=False, rrset_signer=inspect)
    assert (name("branch.example."), RecordType.NSEC) in observed
    assert (name("branch.example."), RecordType.NS) not in observed
    assert zone.get_rdataset("ns.branch", "NSEC") is None
    assert zone.get_rdataset("@", "DNSKEY") is None

    def reject(*_):
        raise ValueError("signer rejected RRset")

    with pytest.raises(ValueError, match="signer rejected"):
        sign_zone(zone, keys=[_signing_key(256)], rrset_signer=reject)
    assert zone.get_rdataset("@", "DNSKEY") is None
    with pytest.raises(NotImplementedError, match="NSEC3"):
        sign_zone(zone, nsec3=rdata.from_text("IN", "NSEC3PARAM", "1 0 0 -"))


def test_sign_zone_custom_signer_sees_relative_owner_in_caller_transaction():
    zone = Zone.from_text(_APEX, "example.", relativize=True)
    seen = []
    with zone.writer() as change:
        change.add("www", 180, rdata.from_text("IN", "A", "192.0.2.1"))
        sign_zone(
            zone,
            txn=change,
            rrset_signer=lambda txn, rrset: seen.append((txn, rrset.name)),
        )
        assert zone.get_rdataset("www", "NSEC") is None
        assert change.get("www", "NSEC")
    assert all(txn is change for txn, _ in seen)
    assert {owner for _, owner in seen} == {
        name("@", origin=None),
        name("www", origin=None),
    }
    assert zone.get_rdataset("www", "NSEC")

"""Exercise the in-house client against BIND and a real MIT Kerberos KDC."""

import time
from importlib.util import find_spec

import gssapi
from tba_codec_dns.rdata import decoded
from tba_codec_dns.wire import Message, RecordType
from tba_provider_dns_resolver.client import NXDOMAIN, NoAnswer, Resolver
from tba_protocol_dns.gss_tsig import negotiate
from tba_provider_dns_resolver.transport import tcp_query
from tba_provider_dns_resolver.tsig import TsigRecord, sign
from tba_protocol_dns.update import Update, send_update

SERVER = "127.0.0.1"
PORT = 1053
ZONE = "interop.test."


def update_for(owner: str, ip: str) -> Update:
    update = Update(ZONE)
    update.replace(owner, 300, "A", ip)
    return update


def main() -> None:
    assert find_spec("dns") is None
    resolver = Resolver([SERVER], port=PORT, timeout=1)
    for attempt in range(20):
        try:
            assert resolver.resolve(ZONE, "SOA", tcp=True)
            break
        except OSError:
            if attempt == 19:
                raise
            time.sleep(0.1)

    context = gssapi.SecurityContext(
        name=gssapi.Name(
            "DNS@ns.interop.test", name_type=gssapi.NameType.hostbased_service
        ),
        mech=gssapi.OID.from_int_seq("1.3.6.1.5.5.2"),
        flags=[
            gssapi.RequirementFlag.mutual_authentication,
            gssapi.RequirementFlag.replay_detection,
            gssapi.RequirementFlag.integrity,
        ],
        usage="initiate",
    )
    key = negotiate(SERVER, context, port=PORT)
    assert context.complete
    allowed = "allowed.interop.test."
    forbidden = "forbidden.interop.test."

    original = update_for(allowed, "192.0.2.8").message().use_tsig(key)
    request = Message.from_wire(original.to_wire())
    reply = tcp_query(request, SERVER, port=PORT)
    accepted = Message.from_wire(reply.to_wire(), key, request_mac=request.mac)
    assert accepted.had_tsig and accepted.tsig_key is key
    assert accepted.rcode == 0
    assert str(decoded(resolver.resolve(allowed, "A", tcp=True)[0])[0]) == "192.0.2.8"

    denied = send_update(update_for(forbidden, "192.0.2.9"), SERVER, port=PORT, key=key)
    assert denied.rcode == 5
    try:
        resolver.resolve(forbidden, "A", tcp=True)
    except (NoAnswer, NXDOMAIN):
        pass
    else:
        raise AssertionError(
            "BIND applied an update outside the Kerberos principal's policy"
        )

    candidate = update_for(allowed, "192.0.2.10").message()
    signed, _ = sign(candidate.to_wire(), key)
    assert signed.count(b"\xc0\x00\x02\x0a") == 1
    tampered = signed.replace(b"\xc0\x00\x02\x0a", b"\xc0\x00\x02\x0b")
    rejected = tcp_query(Message.from_wire(tampered), SERVER, port=PORT)
    assert rejected.rcode == 9
    token = next(rr for rr in rejected.additional if rr.type == RecordType.TSIG)
    assert TsigRecord.from_data(token.data).error == 16
    assert str(decoded(resolver.resolve(allowed, "A", tcp=True)[0])[0]) == "192.0.2.8"
    print(
        "BIND GSS-TSIG passed TKEY negotiation, signed UPDATE and reply, policy denial, and BADSIG rejection"
    )


if __name__ == "__main__":
    main()

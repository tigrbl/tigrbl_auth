"""Client-side GSS-TSIG negotiation using a caller's GSS context (RFC 3645)."""

import secrets
import time
from collections.abc import Iterable
from typing import Protocol
from uuid import uuid4

from tba_codec_dns.tkey import Tkey
from tba_codec_dns.tsig import GssContext, GssTsigKey, TsigError, verify
from tba_codec_dns.wire import Message, Question, RecordClass, RecordType
from tba_primitives_dns_name.names import parse_name
from tba_provider_dns_resolver.async_transport import run_blocking
from tba_provider_dns_resolver.transport import deadline_after, remaining, tcp_query


class InitiatorContext(GssContext, Protocol):
    @property
    def complete(self) -> bool: ...

    @property
    def actual_flags(self) -> Iterable[int]: ...

    def step(self, token: bytes | None) -> bytes | None: ...


def _advance(context: InitiatorContext, token: bytes | None) -> bytes | None:
    try:
        output = context.step(token)
        if context.complete and not {2, 4, 32}.issubset(map(int, context.actual_flags)):
            raise TsigError(
                "GSS context requires mutual authentication, replay detection, and integrity"
            )
        return output
    except TsigError:
        raise
    except Exception as exc:
        raise TsigError("could not establish the GSS-TSIG security context") from exc


def negotiate(
    server: str,
    context: InitiatorContext,
    *,
    port: int = 53,
    timeout: float = 10,
    name: str | None = None,
) -> GssTsigKey:
    """Establish a mutually authenticated GSS-TSIG key with a DNS server."""
    owner = parse_name(
        f"{uuid4().hex}.gss-tsig." if name is None else name, canonical=True
    )
    key = GssTsigKey(owner, context)
    deadline = deadline_after(timeout)
    question = Question(owner, RecordType.TKEY, RecordClass.ANY)
    token = _advance(context, None)
    for _ in range(10):
        if not token:
            raise TsigError("GSS context produced no TKEY negotiation token")
        now = int(time.time())
        record = Tkey(key.algorithm, now, now + 3600, 3, key=token).record(owner)
        query = Message(secrets.randbits(16), 0, (question,), additional=(record,))
        response = tcp_query(query, server, port=port, timeout=remaining(deadline))
        if response.rcode:
            raise TsigError(
                f"TKEY negotiation failed with DNS response code {response.rcode}"
            )
        answers = [
            rr
            for rr in response.answers
            if rr.type == RecordType.TKEY
            and rr.name == owner
            and rr.rdclass == RecordClass.ANY
        ]
        if len(answers) != 1:
            raise TsigError("TKEY negotiation requires one answer for its key name")
        answer = Tkey.from_wire(answers[0].data)
        if (
            tuple(label.lower() for label in answer.algorithm) != key.algorithm
            or answer.mode != 3
        ):
            raise TsigError("unexpected GSS-TSIG negotiation algorithm or mode")
        if answer.error:
            raise TsigError(
                f"GSS-TSIG negotiation failed with TKEY error {answer.error}"
            )
        token = None if context.complete else _advance(context, answer.key or None)
        signed = any(rr.type == RecordType.TSIG for rr in response.additional)
        if context.complete and signed:
            verify(response.to_wire(), key)
        if context.complete and not token:
            if not signed:
                raise TsigError(
                    "completed GSS-TSIG negotiation requires a signed TKEY response"
                )
            return key
    raise TsigError("GSS-TSIG negotiation exceeded ten token exchanges")


async def negotiate_async(
    server: str, context: InitiatorContext, **kwargs
) -> GssTsigKey:
    return await run_blocking(negotiate, server, context, **kwargs)

"""Read DNS master-file records into a zone transaction."""

from dataclasses import replace
from pathlib import Path

from tba_codec_dns.rdata import from_record, parse_ttl
from tba_codec_dns.tokenizer import Tokenizer
from tba_codec_dns.wire import RecordClass, record_class, record_type
from tba_primitives_dns_name.name import root
from tba_primitives_dns_name.names import is_subdomain, parse_name

from .zone import Zone, _MasterReader, _origin_labels


class Reader:
    def __init__(
        self,
        tok,
        rdclass,
        txn,
        allow_include=False,
        allow_directives=True,
        force_name=None,
        force_ttl=None,
        force_rdclass=None,
        force_rdtype=None,
        default_ttl=None,
        rfc2308_ttl=True,
    ):
        self.tok = tok if isinstance(tok, Tokenizer) else Tokenizer(tok)
        self.txn = txn
        origin, _, effective_origin = txn.manager.origin_information()
        self._origin = _origin_labels(origin)
        if allow_directives is True:
            directives = {"$GENERATE", "$ORIGIN", "$TTL", "$UNICODE"}
            if allow_include:
                directives.add("$INCLUDE")
        elif allow_directives is False:
            directives = set()
        else:
            directives = {
                "$" + directive.upper().lstrip("$") for directive in allow_directives
            }

        include = None
        if "$INCLUDE" in directives:
            filename = self.tok.filename
            if str(filename).startswith("<"):
                filename = getattr(self.tok.file, "name", None) or "."
            base = Path(filename).resolve()
            if not base.is_dir():
                base = base.parent

            def include(name):
                path = (base / name).resolve()
                if not path.is_relative_to(base):
                    raise ValueError("$INCLUDE is outside the DNS zone directory")
                return path.read_text(encoding="utf-8")

        if isinstance(force_name, str):
            force_name = parse_name(
                force_name, self._origin, encode_label=self.tok.idna_codec.encode
            )
        elif force_name is not None:
            force_name = force_name.derelativize(origin).labels[:-1]
        self._default_owner = effective_origin.derelativize(origin).labels[:-1]
        self._reader = _MasterReader(
            self._origin,
            record_class(rdclass),
            include,
            rfc2308_ttl,
            directives=directives,
            force_name=force_name,
            force_ttl=force_ttl,
            force_rdclass=None
            if force_rdclass is None
            else record_class(force_rdclass),
            force_rdtype=None if force_rdtype is None else record_type(force_rdtype),
            default_ttl=default_ttl,
        )

    def read(self):
        """Consume the tokenizer into the caller-owned transaction."""
        for record in self._reader.read(
            self.tok, self._origin, owner=self._default_owner
        ):
            if is_subdomain(record.name, self._origin):
                self.txn.add(record.name, record.ttl, from_record(record))


def read_rrsets(
    text,
    name=None,
    ttl=None,
    rdclass=RecordClass.IN,
    default_rdclass=RecordClass.IN,
    rdtype=None,
    default_ttl=None,
    idna_codec=None,
    origin=root,
    relativize=False,
    rfc2308_ttl=True,
):
    """Read records without requiring apex SOA and NS records."""
    if idna_codec is not None:
        from tba_primitives_dns_name.name import from_text

        if isinstance(origin, str):
            origin = from_text(origin, idna_codec=idna_codec)
        if isinstance(name, str):
            name = from_text(name, origin=origin, idna_codec=idna_codec)
    zone_class = default_rdclass if rdclass is None else rdclass
    zone = Zone(
        root if origin is None else origin, rdclass=zone_class, relativize=relativize
    )
    with zone.writer() as txn:
        Reader(
            text
            if isinstance(text, Tokenizer)
            else Tokenizer(text, idna_codec=idna_codec),
            zone_class,
            txn,
            allow_directives=False,
            force_name=name,
            force_ttl=parse_ttl(ttl) if isinstance(ttl, str) else ttl,
            force_rdclass=rdclass,
            force_rdtype=rdtype,
            default_ttl=parse_ttl(default_ttl)
            if isinstance(default_ttl, str)
            else default_ttl,
            rfc2308_ttl=rfc2308_ttl,
        ).read()
    absolute_origin, _, _ = zone.origin_information()
    return [
        replace(rrset, origin=absolute_origin) if relativize else rrset
        for rrset in zone.rrsets()
    ]

"""Editable DNS messages backed by the in-house wire codec."""

from dataclasses import dataclass, replace
from secrets import randbits

from tba_primitives_dns_name.name import Name
from tba_primitives_dns_name.name import from_text as parse_name

from . import wire
from .rdata import Rdata, from_record
from .rdataset import Rdataset
from .rdataset import from_text as parse_dataset
from .wire import CopyMode, RecordClass, RecordType, Section, record_class, record_type

QUESTION = Section.QUESTION
ANSWER = Section.ANSWER
AUTHORITY = Section.AUTHORITY
ADDITIONAL = Section.ADDITIONAL


class RRset(Rdataset):
    """An editable owner-qualified dataset in a message section."""

    def __init__(self, name, rdclass, rdtype, covers=0, deleting=None):
        super().__init__(rdclass, rdtype, covers)
        self.name = name
        self.deleting = deleting

    def to_records(self, origin=None):
        name = self.name if self.name.is_absolute() else self.name.derelativize(origin)
        owner = name.labels[:-1]
        if self.deleting is None and self:
            return self.records(owner)
        rdclass = self.rdclass if self.deleting is None else self.deleting
        if self:
            return tuple(
                replace(record, rdclass=rdclass) for record in self.records(owner)
            )
        return (wire.ResourceRecord(owner, self.rdtype, rdclass, self.ttl, b""),)


class Message:
    """Editable DNS message sections and rendering controls."""

    def __init__(self, id=None):
        self.id = randbits(16) if id is None else id
        self.flags = 0
        self.sections = [[], [], [], []]
        self.index = {}
        self._state = wire.Message(self.id, self.flags)
        self._opt = None
        self._tsig = None
        self.wire = None

    @property
    def question(self):
        return self.sections[QUESTION]

    @property
    def answer(self):
        return self.sections[ANSWER]

    @property
    def authority(self):
        return self.sections[AUTHORITY]

    @property
    def additional(self):
        return self.sections[ADDITIONAL]

    @classmethod
    def _from_wire_message(cls, packet):
        if cls is Message:
            cls = {0: QueryMessage, 5: UpdateMessage}.get(packet.opcode, cls)
        result = cls(id=packet.id)
        result.flags = packet.flags
        result._state = packet
        result._opt = next(
            (r for r in packet.additional if r.type == RecordType.OPT), None
        )
        result._tsig = next(
            (r for r in packet.additional if r.type == RecordType.TSIG), None
        )
        result.wire = packet.wire or None
        update_class = (
            packet.questions[0].rdclass
            if packet.opcode == 5 and packet.questions
            else None
        )
        grouped = (
            replace(packet, one_rr_per_rrset=True) if packet.opcode == 5 else packet
        )
        for section in Section:
            for group in grouped.rrsets(section):
                deleting = None
                rdclass = group.rdclass
                if (
                    update_class is not None
                    and section in (ANSWER, AUTHORITY)
                    and rdclass in (RecordClass.ANY, RecordClass.NONE)
                ):
                    deleting, rdclass = rdclass, update_class
                entry = RRset(group.name, rdclass, group.rdtype, group.covers, deleting)
                entry.ttl = group.ttl
                for record in group.records:
                    if record.data or deleting is None:
                        entry.add(from_record(replace(record, rdclass=rdclass)))
                result.sections[section].append(entry)
        return result

    def _wire_message(self):
        questions = []
        for item in self.question:
            name = item.name
            if not name.is_absolute():
                name = name.derelativize(self.origin)
            questions.append(wire.Question(name.labels[:-1], item.rdtype, item.rdclass))

        def records(section):
            for rrset in section:
                if isinstance(rrset, RRset):
                    yield from rrset.to_records(self.origin)
                else:
                    yield from rrset.records

        special = tuple(r for r in (self._opt, self._tsig) if r is not None)
        return replace(
            self._state,
            id=self.id,
            flags=self.flags,
            questions=tuple(questions),
            answers=tuple(records(self.answer)),
            authority=tuple(records(self.authority)),
            additional=(*records(self.additional), *special),
        )

    @property
    def origin(self):
        return self._state.origin

    @origin.setter
    def origin(self, origin):
        self._state = replace(self._state, origin=origin)

    @property
    def request_payload(self):
        return self._state.request_payload

    @request_payload.setter
    def request_payload(self, payload):
        self._state = replace(self._state, request_payload=payload)

    @property
    def request_mac(self):
        return self._state.request_mac

    @request_mac.setter
    def request_mac(self, value):
        self._state = replace(self._state, request_mac=value)

    @property
    def edns(self):
        return -1 if self._opt is None else (self._opt.ttl >> 16) & 255

    @property
    def ednsflags(self):
        return 0 if self._opt is None else self._opt.ttl & 0xFF00FFFF

    @property
    def payload(self):
        return 0 if self._opt is None else self._opt.rdclass

    @property
    def options(self):
        return () if self._opt is None else wire.Edns.from_record(self._opt).options

    @property
    def tsig_ctx(self):
        return self._state.tsig_ctx

    @property
    def keyname(self):
        key = self.keyring
        if key is None and self._tsig is None:
            return None
        labels = self._tsig.name if key is None else key.name
        return Name((*labels, b""))

    @property
    def keyalgorithm(self):
        if self.keyring is not None:
            return Name((*self.keyring.algorithm, b""))
        if self._tsig is None:
            return None
        from .tsig import TsigRecord

        return Name((*TsigRecord.from_data(self._tsig.data).algorithm, b""))

    @property
    def had_tsig(self):
        return self._tsig is not None

    @property
    def mac(self):
        if self._tsig is None:
            return b""
        from .tsig import TsigRecord

        return TsigRecord.from_data(self._tsig.data).mac

    @property
    def keyring(self):
        return self._state.tsig_key

    def section_number(self, section):
        if isinstance(section, str):
            return Section[section.upper()]
        if isinstance(section, int):
            return Section(section)
        for number, value in enumerate(self.sections):
            if section is value:
                return Section(number)
        raise ValueError("section does not belong to the DNS message")

    def find_rrset(
        self,
        section,
        name,
        rdclass,
        rdtype,
        covers=0,
        deleting=None,
        create=False,
        force_unique=False,
        idna_codec=None,
    ):
        section = self.section_number(section)
        if isinstance(name, str):
            name = parse_name(name, origin=self.origin, idna_codec=idna_codec)
        if self.origin is not None:
            name = name.relativize(self.origin)
        elif not name.is_absolute():
            name = name.derelativize(Name((b"",)))
        rdclass, rdtype, covers = (
            record_class(rdclass),
            record_type(rdtype),
            record_type(covers),
        )
        if deleting is not None:
            deleting = record_class(deleting)
        key = (section, name, rdclass, rdtype, covers, deleting)
        found = None
        if not (force_unique and create):
            for candidate in self.sections[section]:
                if (
                    candidate.name,
                    candidate.rdclass,
                    candidate.rdtype,
                    candidate.covers,
                    getattr(candidate, "deleting", None),
                ) == key[1:]:
                    found = candidate
                    break
        if found is None:
            if not create:
                raise KeyError(key)
            found = RRset(name, rdclass, rdtype, covers, deleting)
            self.sections[section].append(found)
        if self.index is not None:
            self.index[key] = found
        return found

    def get_rrset(
        self,
        section,
        name,
        rdclass,
        rdtype,
        covers=0,
        deleting=None,
        create=False,
        force_unique=False,
        idna_codec=None,
    ):
        try:
            return self.find_rrset(
                section,
                name,
                rdclass,
                rdtype,
                covers,
                deleting,
                create,
                force_unique,
                idna_codec,
            )
        except KeyError:
            return None

    def rcode(self):
        return (self.flags & 15) | ((self.ednsflags >> 24) << 4)

    def set_rcode(self, rcode):
        if not 0 <= rcode < 4096:
            raise ValueError("DNS RCODE outside its wire range")
        if rcode > 15 and self._opt is None:
            self.use_edns()
        if self._opt is not None:
            self._opt = replace(
                self._opt, ttl=(self._opt.ttl & 0x00FFFFFF) | ((rcode >> 4) << 24)
            )
        self.flags = (self.flags & ~15) | (rcode & 15)

    def opcode(self):
        return (self.flags >> 11) & 15

    def set_opcode(self, opcode):
        if not 0 <= opcode <= 15:
            raise ValueError("DNS opcode outside its wire range")
        self.flags = (self.flags & ~0x7800) | (opcode << 11)

    def use_edns(
        self,
        edns=0,
        ednsflags=0,
        payload=1232,
        request_payload=None,
        options=None,
        pad=0,
    ):
        if edns is None or edns is False or edns == -1:
            self._opt = None
            self._state = replace(self._state, request_payload=0, _pad=0)
            return
        if not 0 <= pad <= 65535:
            raise ValueError("DNS padding block size is outside the wire range")
        self._opt = wire.opt_record(
            payload,
            version=0 if edns is True else edns,
            flags=ednsflags & 65535,
            rcode=ednsflags >> 24,
            options=tuple(options or ()),
        )
        self._state = replace(
            self._state,
            request_payload=payload if request_payload is None else request_payload,
            _pad=pad,
        )

    def want_dnssec(self, wanted=True):
        if self._opt is None and wanted:
            self.use_edns()
        if self._opt is not None:
            flag = 0x8000 if wanted else 0
            self._opt = replace(self._opt, ttl=(self._opt.ttl & ~0x8000) | flag)

    def get_options(self, otype):
        return [option for option in self.options if option.code == otype]

    def extended_errors(self):
        return list(self._wire_message().extended_errors())

    def use_tsig(
        self,
        keyring,
        keyname=None,
        fudge=300,
        original_id=None,
        tsig_error=0,
        other_data=b"",
        algorithm="hmac-sha256.",
    ):
        self._tsig = None
        self._state = self._state.use_tsig(
            keyring,
            keyname,
            fudge,
            original_id,
            tsig_error,
            other_data,
            algorithm,
            request_mac=self.request_mac,
        )

    def is_response(self, other):
        return self._wire_message().is_response(other._wire_message())

    def to_wire(
        self,
        origin=None,
        max_size=0,
        multi=False,
        tsig_ctx=None,
        prepend_length=False,
        prefer_truncation=False,
        **kwargs,
    ):
        if origin is not None:
            self.origin = parse_name(origin) if isinstance(origin, str) else origin
        packet = self._wire_message()
        if self._state._sign_on_wire:
            packet = replace(
                packet,
                additional=tuple(
                    r for r in packet.additional if r.type != RecordType.TSIG
                ),
            )
        if multi and self._state._sign_on_wire and tsig_ctx is None:
            from .tsig import StreamSigner

            tsig_ctx = StreamSigner(self._state.tsig_key)
        kwargs.setdefault("compress", True)
        # Keep the context unchanged when rendering is rejected by the size limit.
        previous_mac = None if tsig_ctx is None else tsig_ctx.previous_mac
        try:
            self.wire = packet.to_wire(
                max_size=max_size,
                prefer_truncation=prefer_truncation,
                tsig_ctx=tsig_ctx,
                **kwargs,
            )
        except BaseException:
            if tsig_ctx is not None:
                tsig_ctx.previous_mac = previous_mac
            raise
        if self._state._sign_on_wire:
            signed = wire.Message.from_wire(self.wire)
            self._tsig = signed.additional[-1]
            self._state = replace(self._state, tsig_ctx=tsig_ctx)
        if prepend_length:
            return len(self.wire).to_bytes(2, "big") + self.wire
        return self.wire

    def to_text(self):
        return self._wire_message().to_text()

    __str__ = to_text


class NotQueryResponse(wire.WireError):
    pass


class AnswerForNXDOMAIN(wire.WireError):
    pass


class ChainTooLong(wire.WireError):
    pass


@dataclass(frozen=True)
class ChainingResult:
    canonical_name: Name
    answer: RRset | None
    minimum_ttl: int
    cnames: list[RRset]


class QueryMessage(Message):
    def canonical_name(self):
        return self.resolve_chaining().canonical_name

    def resolve_chaining(self):
        if not self.flags & 0x8000:
            raise NotQueryResponse("DNS chaining requires a response")
        if len(self.question) != 1:
            raise wire.WireError("DNS chaining requires one question")
        question = self.question[0]
        name = question.name
        cnames = []
        minimum = 0xFFFFFFFF
        for _ in range(17):
            answer = self.get_rrset(ANSWER, name, question.rdclass, question.rdtype)
            if answer is not None:
                if self.rcode() == 3:
                    raise AnswerForNXDOMAIN("NXDOMAIN response contains an answer")
                return ChainingResult(name, answer, min(minimum, answer.ttl), cnames)
            cname = self.get_rrset(ANSWER, name, question.rdclass, RecordType.CNAME)
            if cname is None:
                for soa in self.authority:
                    if soa.rdtype == RecordType.SOA and name.is_subdomain(soa.name):
                        minimum = min(minimum, soa.ttl, soa[0].minimum)
                return ChainingResult(name, None, minimum, cnames)
            cnames.append(cname)
            name = cname[0].target
            minimum = min(minimum, cname.ttl)
        raise ChainTooLong("DNS CNAME chain exceeds 16 aliases")


class UpdateMessage(Message):
    """Editable DNS UPDATE with its RFC 2136 section names."""

    def __init__(
        self,
        zone=None,
        rdclass=RecordClass.IN,
        keyring=None,
        keyname=None,
        keyalgorithm="hmac-sha256.",
        id=None,
    ):
        super().__init__(id)
        self.set_opcode(5)
        if zone is not None:
            zone = parse_name(zone) if isinstance(zone, str) else zone
            if not zone.is_absolute():
                raise ValueError("DNS UPDATE requires an absolute zone name")
            self.find_rrset(QUESTION, zone, rdclass, RecordType.SOA, create=True)
            self.origin = zone
        if keyring is not None:
            self.use_tsig(keyring, keyname, algorithm=keyalgorithm)

    @property
    def zone(self):
        return self.question

    @property
    def prerequisite(self):
        return self.answer

    @property
    def update(self):
        return self.authority

    def section_number(self, section):
        aliases = {"ZONE": QUESTION, "PREREQUISITE": ANSWER, "UPDATE": AUTHORITY}
        if isinstance(section, str):
            section = aliases.get(section.upper(), section)
        return super().section_number(section)

    def _owner(self, name):
        if not self.zone:
            raise ValueError("DNS UPDATE has no zone question")
        apex = self.zone[0].name
        if not apex.is_absolute():
            apex = apex.derelativize(self.origin)
        owner = parse_name(name, origin=apex) if isinstance(name, str) else name
        if not owner.is_absolute():
            owner = owner.derelativize(apex)
        if not owner.is_subdomain(apex):
            raise ValueError("DNS UPDATE owner is outside the zone")
        return owner, apex

    def _dataset(self, args, ttl, origin):
        if not args:
            raise ValueError("DNS UPDATE requires RDATA")
        if isinstance(args[0], Rdataset) and len(args) == 1:
            return args[0]
        if isinstance(args[0], Rdata):
            first = args[0]
            return Rdataset(first.rdclass, first.rdtype, first.covers(), ttl, args)
        kind, *text = args
        if not text:
            raise ValueError("DNS UPDATE requires RDATA")
        return parse_dataset(self.zone[0].rdclass, kind, ttl, *text, origin=origin)

    def _value_set(self, section, owner, dataset, deleting=None, ttl=None):
        rdclass = self.zone[0].rdclass
        if dataset.rdclass != rdclass:
            raise ValueError("DNS UPDATE RDATA class does not match its zone")
        record = self.find_rrset(
            section,
            owner,
            rdclass,
            dataset.rdtype,
            dataset.covers,
            deleting,
            create=True,
            force_unique=True,
        )
        record.ttl = dataset.ttl if ttl is None else ttl
        for value in dataset:
            record.add(value)

    def _empty_set(self, section, owner, rdtype, deleting):
        self.find_rrset(
            section,
            owner,
            self.zone[0].rdclass,
            RecordType.ANY if rdtype is None else rdtype,
            deleting=deleting,
            create=True,
            force_unique=True,
        )

    def _add(self, name, args, replace_existing):
        owner, apex = self._owner(name)
        if not args:
            raise ValueError("DNS UPDATE requires records to add")
        if isinstance(args[0], Rdataset):
            datasets = args
        else:
            ttl, *values = args
            datasets = (self._dataset(values, ttl, apex),)
        if any(
            not isinstance(dataset, Rdataset) or dataset.rdclass != self.zone[0].rdclass
            for dataset in datasets
        ):
            raise ValueError("DNS UPDATE dataset does not match its zone")
        for dataset in datasets:
            if replace_existing:
                self._empty_set(AUTHORITY, owner, dataset.rdtype, RecordClass.ANY)
            self._value_set(AUTHORITY, owner, dataset)

    def add(self, name, *args):
        self._add(name, args, False)

    def replace(self, name, *args):
        self._add(name, args, True)

    def delete(self, name, *args):
        owner, apex = self._owner(name)
        if not args or (len(args) == 1 and isinstance(args[0], (int, str))):
            self._empty_set(
                AUTHORITY, owner, args[0] if args else None, RecordClass.ANY
            )
            return
        self._value_set(
            AUTHORITY, owner, self._dataset(args, 0, apex), RecordClass.NONE, ttl=0
        )

    def present(self, name, *args):
        owner, apex = self._owner(name)
        if not args or (len(args) == 1 and isinstance(args[0], (int, str))):
            self._empty_set(ANSWER, owner, args[0] if args else None, RecordClass.ANY)
            return
        self._value_set(ANSWER, owner, self._dataset(args, 0, apex), ttl=0)

    def absent(self, name, rdtype=None):
        owner, _ = self._owner(name)
        self._empty_set(ANSWER, owner, rdtype, RecordClass.NONE)


def from_wire(wire_data, *args, **kwargs):
    return Message._from_wire_message(
        wire.Message.from_wire(wire_data, *args, **kwargs)
    )


def from_text(text):
    return Message._from_wire_message(wire.Message.from_text(text))


def from_file(source):
    return Message._from_wire_message(wire.Message.from_file(source))


def make_query(qname, rdtype=RecordType.A, rdclass=RecordClass.IN, **kwargs):
    return QueryMessage._from_wire_message(
        wire.make_query(qname, rdtype, rdclass, **kwargs)
    )


def make_response(query, **kwargs):
    return Message._from_wire_message(
        wire.make_response(query._wire_message(), **kwargs)
    )


__all__ = [
    "ADDITIONAL",
    "ANSWER",
    "AUTHORITY",
    "QUESTION",
    "AnswerForNXDOMAIN",
    "ChainTooLong",
    "ChainingResult",
    "CopyMode",
    "Message",
    "NotQueryResponse",
    "QueryMessage",
    "RRset",
    "UpdateMessage",
    "from_file",
    "from_text",
    "from_wire",
    "make_query",
    "make_response",
]

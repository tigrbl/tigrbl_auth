"""DNS message flags, codes, and text conversion."""

from tba_primitives_dns_name.names import name_text, parse_name

from . import flags as dns_flags
from .rdata import from_tokens, parse_ttl, record_text
from .tokenizer import master_tokens
from .wire import (
    EdnsOption,
    Message,
    Question,
    RecordType,
    WireError,
    class_text,
    opt_record,
    record_class,
    record_type,
    type_text,
)

_OPCODES = {
    "QUERY": 0,
    "IQUERY": 1,
    "STATUS": 2,
    "NOTIFY": 4,
    "UPDATE": 5,
    "DSO": 6,
}
_RCODES = {
    "NOERROR": 0,
    "FORMERR": 1,
    "SERVFAIL": 2,
    "NXDOMAIN": 3,
    "NOTIMP": 4,
    "REFUSED": 5,
    "YXDOMAIN": 6,
    "YXRRSET": 7,
    "NXRRSET": 8,
    "NOTAUTH": 9,
    "NOTZONE": 10,
    "DSOTYPENI": 11,
    "BADVERS": 16,
    "BADKEY": 17,
    "BADTIME": 18,
    "BADMODE": 19,
    "BADNAME": 20,
    "BADALG": 21,
    "BADTRUNC": 22,
    "BADCOOKIE": 23,
}
_SECTIONS = ("QUESTION", "ANSWER", "AUTHORITY", "ADDITIONAL")
_UPDATE_SECTIONS = ("ZONE", "PREREQUISITE", "UPDATE", "ADDITIONAL")
_CODES = {"id", "opcode", "rcode", "flags", "edns", "eflags", "payload", "option"}


def _code(text: str, values: dict[str, int], maximum: int) -> int:
    if text.upper() in values:
        return values[text.upper()]
    if not text.isascii() or not text.isdecimal() or int(text) > maximum:
        raise ValueError(f"unknown DNS code {text!r}")
    return int(text)


def _code_text(code: int, values: dict[str, int]) -> str:
    return next((name for name, value in values.items() if value == code), str(code))


def message_text(message: Message) -> str:
    flags = dns_flags.to_text(message.flags & 0x87F0)
    lines = [
        f"id {message.id}",
        f"opcode {_code_text(message.opcode, _OPCODES)}",
        f"rcode {_code_text(message.rcode, _RCODES)}",
        f"flags {flags}".rstrip(),
    ]
    if edns := message.edns:
        lines.extend(
            (
                f"edns {edns.version}",
                f"eflags {dns_flags.edns_to_text(edns.flags)}".rstrip(),
                f"payload {edns.payload}",
            )
        )
        lines.extend(
            f"option {option.code} {option.data.hex().upper()}".rstrip()
            for option in edns.options
        )
    names = _UPDATE_SECTIONS if message.opcode == 5 else _SECTIONS
    lines.append(";" + names[0])
    lines.extend(
        f"{name_text(q.name)} {class_text(q.rdclass)} {type_text(q.type)}"
        for q in message.questions
    )
    for name, records in zip(
        names[1:], (message.answers, message.authority, message.additional)
    ):
        lines.append(";" + name)
        lines.extend(record_text(rr) for rr in records if rr.type != RecordType.OPT)
    return "\n".join(lines)


def parse_message(text: str) -> Message:
    questions: list[Question] = []
    answer, authority, additional = [], [], []
    sections = (questions, answer, authority, additional)
    identifier = opcode = rcode = flags = edns_flags = 0
    edns_version = section = None
    payload = 1232
    options = []
    for line in text.splitlines():
        marker = line.strip().removeprefix(";").upper()
        names = _UPDATE_SECTIONS if opcode == 5 else _SECTIONS
        if line.lstrip().startswith(";") and marker in names:
            section = names.index(marker)
            continue
        for _, _, tokens in master_tokens(line):
            if section is None:
                label, *args = tokens
                label = label.lower()
                if label not in _CODES:
                    raise ValueError(f"unknown DNS message header {label!r}")
                if label == "flags":
                    flags |= dns_flags.from_text(
                        " ".join(
                            "FLAG6" if flag.upper() == "Z" else flag for flag in args
                        )
                    )
                elif label == "eflags":
                    edns_flags = (
                        _code(args[0], {}, 65535)
                        if len(args) == 1 and args[0].isascii() and args[0].isdecimal()
                        else dns_flags.edns_from_text(" ".join(args))
                    )
                elif label == "option":
                    if not args:
                        raise ValueError("missing EDNS option code")
                    options.append(
                        EdnsOption(
                            _code(args[0], {}, 65535), bytes.fromhex("".join(args[1:]))
                        )
                    )
                else:
                    if len(args) != 1:
                        raise ValueError(f"DNS message header {label} takes one value")
                    value = args[0]
                    if label == "id":
                        identifier = _code(value, {}, 65535)
                    elif label == "opcode":
                        opcode = _code(value, _OPCODES, 15)
                    elif label == "rcode":
                        rcode = _code(value, _RCODES, 4095)
                    elif label == "edns":
                        edns_version = _code(value, {}, 255)
                    elif label == "payload":
                        payload = _code(value, {}, 65535)
            elif section == 0:
                if len(tokens) != 3:
                    raise ValueError(
                        "expected DNS question in name, class, type format"
                    )
                questions.append(Question.from_text(tokens[0], tokens[2], tokens[1]))
            else:
                if len(tokens) < 4:
                    raise ValueError("incomplete DNS message resource record")
                owner, ttl, rdclass, rdtype, *data = tokens
                sections[section].append(
                    from_tokens(
                        parse_name(owner),
                        parse_ttl(ttl),
                        record_class(rdclass),
                        record_type(rdtype),
                        data,
                    )
                )
    if edns_version is not None or options or rcode > 15 or edns_flags:
        opt = opt_record(
            payload,
            version=edns_version or 0,
            flags=edns_flags,
            rcode=rcode >> 4,
            options=tuple(options),
        )
        if additional and additional[-1].type == RecordType.TSIG:
            additional.insert(len(additional) - 1, opt)
        else:
            additional.append(opt)
    if any(rr.type == RecordType.OPT for rr in (*answer, *authority)):
        raise WireError("misplaced EDNS OPT record")
    return Message(
        identifier,
        flags | (opcode << 11) | (rcode & 15),
        tuple(questions),
        tuple(answer),
        tuple(authority),
        tuple(additional),
    )

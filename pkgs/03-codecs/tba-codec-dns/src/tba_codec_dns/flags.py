"""DNS header and EDNS flag names and textual representations."""

from enum import IntFlag


class Flag(IntFlag):
    QR = 0x8000
    AA = 0x0400
    TC = 0x0200
    RD = 0x0100
    RA = 0x0080
    AD = 0x0020
    CD = 0x0010


class EDNSFlag(IntFlag):
    DO = 0x8000


QR, AA, TC, RD, RA, AD, CD = tuple(Flag)
DO = EDNSFlag.DO


def _parse(text, flag_type):
    flags = 0
    for name in text.upper().split():
        member = flag_type.__members__.get(name)
        if member is not None:
            flags |= member
        elif name.startswith("FLAG") and name[4:].isascii() and name[4:].isdecimal():
            bit = int(name[4:])
            if not 0 <= bit < 16:
                raise ValueError("DNS flag bit outside 0..15")
            flags |= 1 << bit
        else:
            raise ValueError(f"unknown DNS flag {name!r}")
    return int(flags)


def _format(flags, flag_type):
    names = {int(flag): flag.name for flag in flag_type}
    return " ".join(
        names.get(1 << bit, f"FLAG{bit}")
        for bit in range(15, -1, -1)
        if flags & (1 << bit)
    )


def from_text(text):
    return _parse(text, Flag)


def to_text(flags):
    return _format(flags, Flag)


def edns_from_text(text):
    return _parse(text, EDNSFlag)


def edns_to_text(flags):
    return _format(flags, EDNSFlag)

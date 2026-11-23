"""Syntax and normalization for OAuth client contact addresses."""

import re
import unicodedata
from typing import Annotated

import idna
from pydantic import AfterValidator, WithJsonSchema

_ATEXT = frozenset("!#$%&'*+-/=?^_`{|}~")
_DISPLAY_ADDRESS = re.compile(r'[\s\w."\-]*<([^<>]+)>')
_SPECIAL_USE = {
    "arpa",
    "invalid",
    "local",
    "localhost",
    "onion",
    "test",
}


def _atom_character(character: str) -> bool:
    if character.isascii():
        return character.isalnum() or character in _ATEXT
    return unicodedata.category(character)[0] not in "CZ"


def _normalize(value: str) -> str:
    address = value.strip()
    display = _DISPLAY_ADDRESS.fullmatch(address)
    if display:
        address = display[1].strip()
    local, separator, domain = address.rpartition("@")
    local = unicodedata.normalize("NFC", local)
    if not separator or not all(
        atom and all(map(_atom_character, atom)) for atom in local.split(".")
    ):
        raise ValueError("invalid email local part")
    try:
        ascii_domain = idna.encode(domain, uts46=True, std3_rules=True).decode("ascii")
        normalized_domain = idna.decode(ascii_domain)
    except (UnicodeError, idna.IDNAError) as exc:
        raise ValueError("invalid email domain") from exc
    suffix = ascii_domain.rsplit(".", 1)[-1]
    if (
        "." not in ascii_domain
        or not suffix[-1:].isalpha()
        or suffix in _SPECIAL_USE
        or ascii_domain.endswith(".")
    ):
        raise ValueError("invalid email domain")
    if len(local.encode("utf-8")) + 1 + len(ascii_domain) > 254:
        raise ValueError("email address exceeds 254 octets")
    return f"{local}@{normalized_domain}"


ContactEmail = Annotated[
    str,
    AfterValidator(_normalize),
    WithJsonSchema({"type": "string", "format": "email"}),
]

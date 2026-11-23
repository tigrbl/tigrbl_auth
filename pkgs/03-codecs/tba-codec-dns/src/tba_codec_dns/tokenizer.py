"""Tokenize DNS master-file and record presentation syntax."""

import sys
from collections.abc import Iterator
from dataclasses import dataclass, field
from io import StringIO
from string import ascii_lowercase, digits

from tba_primitives_dns_name.name import IDNA_2003, from_text
from tba_primitives_dns_name.names import _escape

EOF = 0
EOL = 1
WHITESPACE = 2
IDENTIFIER = 3
QUOTED_STRING = 4
COMMENT = 5
DELIMITER = 6

_DELIMITERS = frozenset(' \t\n;()"')
_DIGITS = digits + ascii_lowercase


class UngetBufferFull(ValueError):
    """The one-token pushback buffer is occupied."""


class SyntaxError(ValueError):
    """Invalid DNS presentation syntax."""


class UnexpectedEnd(SyntaxError):
    """Input ended in the middle of a token."""


@dataclass
class Token:
    ttype: int
    value: str | bytes = ""
    has_escape: bool = field(default=False, compare=False)
    comment: str | None = field(default=None, compare=False)

    def is_eof(self):
        return self.ttype == EOF

    def is_eol(self):
        return self.ttype == EOL

    def is_whitespace(self):
        return self.ttype == WHITESPACE

    def is_identifier(self):
        return self.ttype == IDENTIFIER

    def is_quoted_string(self):
        return self.ttype == QUOTED_STRING

    def is_comment(self):
        return self.ttype == COMMENT

    def is_delimiter(self):
        return self.ttype == DELIMITER

    def is_eol_or_eof(self):
        return self.ttype in (EOL, EOF)

    def __str__(self):
        return f'{self.ttype} "{self.value}"'

    def _unescaped(self):
        pos = 0
        while pos < len(self.value):
            char = self.value[pos]
            pos += 1
            if char != "\\":
                yield char
                continue
            if pos == len(self.value):
                raise UnexpectedEnd("unfinished DNS escape")
            numeric = self.value[pos] in digits
            if numeric and len(self.value) - pos < 3:
                raise UnexpectedEnd("unfinished DNS numeric escape")
            try:
                data, pos = _escape(self.value, pos)
            except ValueError as exc:
                raise SyntaxError(str(exc)) from exc
            yield data[0] if numeric else data.decode("utf-8")

    def unescape(self):
        if not self.has_escape:
            return self
        return Token(
            self.ttype,
            "".join(
                chr(part) if isinstance(part, int) else part
                for part in self._unescaped()
            ),
        )

    def unescape_to_bytes(self):
        if isinstance(self.value, bytes):
            return Token(self.ttype, self.value)
        return Token(
            self.ttype,
            b"".join(
                bytes((part,)) if isinstance(part, int) else part.encode("utf-8")
                for part in self._unescaped()
            ),
        )


class Tokenizer:
    """Read DNS tokens from text, UTF-8 bytes, or a text stream."""

    def __init__(self, f=sys.stdin, filename=None, idna_codec=None):
        if isinstance(f, (str, bytes)):
            self.file = StringIO(f.decode() if isinstance(f, bytes) else f)
            default_filename = "<string>"
        else:
            self.file = f
            default_filename = "<stdin>" if f is sys.stdin else "<file>"
        self.filename = default_filename if filename is None else filename
        self.idna_codec = IDNA_2003 if idna_codec is None else idna_codec
        self.line_number = 1
        self.multiline = 0
        self.quoting = False
        self.eof = False
        self.after_cr = False
        self.ungotten_char = None
        self.ungotten_token = None

    def where(self):
        return self.filename, self.line_number

    def _peek(self):
        if self.ungotten_char is None:
            char = "" if self.eof else self.file.read(1)
            if self.after_cr and char == "\n":
                char = self.file.read(1)
            self.after_cr = char == "\r" and not self.quoting
            if self.after_cr:
                char = "\n"
            if char == "\n":
                self.line_number += 1
            self.eof = not char
            self.ungotten_char = char
        return self.ungotten_char

    def _take(self):
        char = self._peek()
        self.ungotten_char = None
        return char

    def skip_whitespace(self):
        count = 0
        whitespace = (" ", "\t", "\n") if self.multiline else (" ", "\t")
        while self._peek() in whitespace:
            self._take()
            count += 1
        return count

    def _value(self, quoted):
        parts = []
        if quoted:
            self._take()
            self.quoting = True
        try:
            while char := self._peek():
                if quoted:
                    if char == '"':
                        self._take()
                        return "".join(parts)
                    if char == "\n":
                        raise SyntaxError("newline in a quoted DNS string")
                elif char in _DELIMITERS:
                    break
                parts.append(self._take())
                if char == "\\":
                    escaped = self._take()
                    if not escaped or (escaped == "\n" and not quoted):
                        raise UnexpectedEnd("unfinished DNS escape")
                    parts.append(escaped)
            if quoted:
                raise UnexpectedEnd("unfinished quoted DNS string")
            return "".join(parts)
        finally:
            self.quoting = False

    def get(self, want_leading=False, want_comment=False):
        return self._get(want_leading, want_comment, presentation=False)

    def _get(self, want_leading, want_comment, *, presentation):
        token = self.ungotten_token
        self.ungotten_token = None
        if token is not None and (
            (want_leading or not token.is_whitespace())
            and (want_comment or not token.is_comment())
        ):
            if presentation and token.is_quoted_string():
                return Token(IDENTIFIER, f'"{token.value}"', token.has_escape)
            return token
        if self.skip_whitespace() and want_leading:
            return Token(WHITESPACE, " ")
        while True:
            char = self._peek()
            if char in ("(", ")"):
                self._take()
                if char == ")" and not self.multiline:
                    raise SyntaxError("unmatched closing parenthesis")
                self.multiline += 1 if char == "(" else -1
                self.skip_whitespace()
            elif char == ";":
                self._take()
                chars = []
                while self._peek() not in ("\n", ""):
                    chars.append(self._take())
                comment = "".join(chars)
                if want_comment:
                    return Token(COMMENT, comment)
                if self.multiline and self._peek():
                    self.skip_whitespace()
                    continue
                end = self._take()
                if self.multiline:
                    raise SyntaxError("unclosed DNS parentheses")
                return Token(EOL if end else EOF, end, comment=comment)
            elif char in ("\n", ""):
                self._take()
                if not char and self.multiline:
                    raise SyntaxError("unclosed DNS parentheses")
                return Token(EOL if char else EOF, char)
            else:
                break

        quoted = char == '"'
        value = self._value(quoted)
        if presentation:
            # Record codecs consume raw spellings such as alpn="h2,h3".
            parts = [f'"{value}"' if quoted else value]
            while (char := self._peek()) and (char not in _DELIMITERS or char == '"'):
                fragment = self._value(char == '"')
                parts.append(f'"{fragment}"' if char == '"' else fragment)
            value = "".join(parts)
            quoted = False
        return Token(QUOTED_STRING if quoted else IDENTIFIER, value, "\\" in value)

    def unget(self, token):
        if self.ungotten_token is not None:
            raise UngetBufferFull("a DNS token is already buffered")
        self.ungotten_token = token

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get()
        if token.is_eof():
            raise StopIteration
        return token

    next = __next__

    def get_remaining(self, max_tokens=None):
        return self._remaining(max_tokens, presentation=False)

    def _remaining(self, max_tokens=None, *, presentation):
        tokens = []
        while True:
            token = self._get(False, False, presentation=presentation)
            if token.is_eol_or_eof():
                self.unget(token)
                return tokens
            tokens.append(token)
            if len(tokens) == max_tokens:
                return tokens

    def concatenate_remaining_identifiers(self, allow_empty=False):
        value = "".join(
            self.as_identifier(token.unescape()) for token in self.get_remaining()
        )
        if not value and not allow_empty:
            raise SyntaxError("expected a DNS identifier")
        return value

    def as_identifier(self, token):
        if not token.is_identifier():
            raise SyntaxError("expected a DNS identifier")
        return token.value

    def get_identifier(self):
        return self.as_identifier(self.get().unescape())

    def as_int(self, token, base=10):
        value = self.as_identifier(token)
        if (
            not 2 <= base <= 36
            or not value
            or not value.isascii()
            or any(char not in _DIGITS[:base] for char in value.lower())
        ):
            raise SyntaxError("expected an unsigned DNS integer")
        return int(value, base)

    def _uint(self, token, bits, base=10):
        value = self.as_int(token, base)
        if value >= 1 << bits:
            raise SyntaxError(f"expected an unsigned {bits}-bit DNS integer")
        return value

    def get_int(self, base=10):
        return self.as_int(self.get().unescape(), base)

    def as_uint8(self, token):
        return self._uint(token, 8)

    def as_uint16(self, token, base=10):
        return self._uint(token, 16, base)

    def as_uint32(self, token, base=10):
        return self._uint(token, 32, base)

    def as_uint48(self, token, base=10):
        return self._uint(token, 48, base)

    def get_uint8(self):
        return self.as_uint8(self.get().unescape())

    def get_uint16(self, base=10):
        return self.as_uint16(self.get().unescape(), base)

    def get_uint32(self, base=10):
        return self.as_uint32(self.get().unescape(), base)

    def get_uint48(self, base=10):
        return self.as_uint48(self.get().unescape(), base)

    def as_string(self, token, max_length=None):
        if not (token.is_identifier() or token.is_quoted_string()):
            raise SyntaxError("expected a DNS string")
        if max_length and len(token.value) > max_length:
            raise SyntaxError("DNS string is too long")
        return token.value

    def as_bytes(self, token, max_length=None):
        value = self.as_string(token)
        if isinstance(value, str):
            value = value.encode("utf-8")
        if max_length and len(value) > max_length:
            raise SyntaxError("DNS byte string is too long")
        return value

    def get_string(self, max_length=None):
        return self.as_string(self.get().unescape(), max_length)

    def get_bytes(self, max_length=None):
        return self.as_bytes(self.get().unescape_to_bytes(), max_length)

    def as_name(self, token, origin=None, relativize=False, relativize_to=None):
        value = from_text(self.as_identifier(token), origin, self.idna_codec)
        return value.choose_relativity(relativize_to or origin, relativize)

    def get_name(self, origin=None, relativize=False, relativize_to=None):
        return self.as_name(self.get(), origin, relativize, relativize_to)

    def get_eol_as_token(self):
        token = self.get()
        if not token.is_eol_or_eof():
            raise SyntaxError(f"expected end of DNS line, got {token}")
        return token

    def get_eol(self):
        return self.get_eol_as_token().value

    def get_ttl(self):
        from .rdata import parse_ttl

        return parse_ttl(self.get_identifier())


def master_tokens(text: str | Tokenizer) -> Iterator[tuple[int, bool, tuple[str, ...]]]:
    """Yield line number, owner omission, and raw presentation fields."""
    tokenizer = text if isinstance(text, Tokenizer) else Tokenizer(text)
    while True:
        lineno = tokenizer.line_number - (tokenizer.ungotten_char == "\n")
        first = tokenizer._get(True, False, presentation=True)
        omitted = first.is_whitespace()
        if omitted:
            first = tokenizer._get(False, False, presentation=True)
        if first.is_eof():
            return
        if not first.is_eol():
            rest = tokenizer._remaining(presentation=True)
            tokenizer.get_eol()
            yield lineno, omitted, (first.value, *(token.value for token in rest))

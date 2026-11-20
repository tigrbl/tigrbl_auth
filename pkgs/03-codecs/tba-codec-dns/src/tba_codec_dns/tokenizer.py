"""Tokenize DNS master-file and record presentation syntax."""

import re
from collections.abc import Iterator

_TOKEN = re.compile(r'(?:\\.|"(?:(?:\\.)|[^"\\])*"|[^\s;()"\\])+|[();]')


def master_tokens(text: str) -> Iterator[tuple[int, bool, tuple[str, ...]]]:
    """Yield line number, owner omission, and presentation-format tokens."""
    depth = 0
    tokens = []
    owner_omitted = False
    start = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        if not tokens and not depth:
            start = lineno
            owner_omitted = bool(line[:1].isspace())
        offset = 0
        while offset < len(line):
            if line[offset].isspace():
                offset += 1
                continue
            match = _TOKEN.match(line, offset)
            if match is None:
                raise ValueError(f"line {lineno} has an unfinished quote or escape")
            token, offset = match[0], match.end()
            if token == ";":
                break
            if token == "(":
                depth += 1
            elif token == ")":
                depth -= 1
                if depth < 0:
                    raise ValueError(
                        f"line {lineno} has an unmatched closing parenthesis"
                    )
            else:
                tokens.append(token)
        if depth == 0 and tokens:
            yield start, owner_omitted, tuple(tokens)
            tokens.clear()
    if depth:
        raise ValueError("unclosed DNS master-file parentheses")

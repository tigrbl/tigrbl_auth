"""Entrypoint for the Tigrbl-native operator CLI."""

from __future__ import annotations

import sys

from tba_cli_identity.cli.handlers import HANDLER_MAP
from tba_cli_identity.cli.metadata import build_parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.output_stream = sys.stdout
    handler_name = getattr(args, "handler_name", None)
    if not handler_name:
        parser.error("no handler selected")
    handler = HANDLER_MAP[handler_name]
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from acme_notes_cli.device_login import DeviceLoginClient, persist_tokens


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="acme-notes")
    subparsers = parser.add_subparsers(dest="command", required=True)

    login_parser = subparsers.add_parser("login", help="Authenticate via tigrbl_auth device authorization")
    login_parser.add_argument("--issuer", required=True)
    login_parser.add_argument("--client-id", required=True)
    login_parser.add_argument("--scope", default="openid profile email")
    login_parser.add_argument(
        "--token-cache",
        default=str(Path.home() / ".acme-notes" / "tokens.json"),
    )
    return parser


async def _run_login(args: argparse.Namespace) -> int:
    client = DeviceLoginClient(
        issuer=args.issuer,
        client_id=args.client_id,
        scope=args.scope,
    )
    device, tokens = await client.login()
    persist_tokens(Path(args.token_cache), tokens)
    print(f"Open: {device.verification_uri_complete}")
    print(f"Code: {device.user_code}")
    print(f"Cached tokens: {args.token_cache}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "login":
        return asyncio.run(_run_login(args))
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

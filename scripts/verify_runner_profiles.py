from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tba_auth.cli.artifacts import deployment_from_options
from tba_auth.cli.runtime import write_runtime_profile_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate and verify runner profile readiness reports.")
    parser.add_argument("--profile", choices=["baseline", "production", "hardening", "peer-claim"], default="baseline")
    parser.add_argument("--environment", default="development")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--access-log", dest="access_log", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--lifespan", choices=["auto", "on", "off"], default="auto")
    parser.add_argument("--graceful-timeout", type=int, default=30)
    parser.add_argument("--report-dir", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    deployment = deployment_from_options(profile=args.profile)
    report = write_runtime_profile_report(
        ROOT,
        deployment=deployment,
        environment=args.environment,
        host=args.host,
        port=args.port,
        workers=args.workers,
        access_log=bool(args.access_log),
        lifespan=args.lifespan,
        graceful_timeout=int(args.graceful_timeout),
        report_dir=Path(args.report_dir).resolve() if args.report_dir else None,
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Start a WPT receiver, submit a protected write, or read the fixture ledger."""

import argparse
import json
from pathlib import Path

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from tba_provider_jose_cryptography import JwsCryptographyProvider

from .wpt import WptCaller, WptReceiver


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", choices=["receive", "call", "readback"])
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.role == "receive":
        with WptReceiver(
            config.get("port", 0), config["certificate"], config["private_key"],
            config["dns_name"], config["trust_by_domain"],
            bound_token_headers=config.get("bound_token_headers", ()),
        ) as receiver:
            print(json.dumps({"host": "127.0.0.1", "port": receiver.server_port}), flush=True)
            try:
                receiver.serve_forever()
            except KeyboardInterrupt:
                pass
        return 0

    key = load_pem_private_key(Path(config["private_key"]).read_bytes(), password=None)
    caller = WptCaller(
        JwsCryptographyProvider({"workload": key}),
        Path(config["wit_file"]).read_text(encoding="utf-8").strip(),
        "workload", config["trust_anchor"],
    )
    result = caller.request(
        config.get("host", "127.0.0.1"), config["port"], config["dns_name"],
        readback=args.role == "readback",
    )
    print(json.dumps(result))
    return 0 if 200 <= result["http_status"] < 300 else 2


if __name__ == "__main__":
    raise SystemExit(main())

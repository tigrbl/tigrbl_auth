"""Separate caller and receiver commands for partner interop tests."""

import argparse
import json
from pathlib import Path
import ssl

from .wic import RejectedServerIdentity, TlsFiles, WicCaller, WicReceiver, WorkloadVerifier, certificate_status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", choices=["receive", "call", "readback"])
    parser.add_argument("config", type=Path, help="JSON fixture configuration")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    tls = TlsFiles(**config["tls"])
    verifier = WorkloadVerifier(
        config["expected_peer"], config["domain_anchors"],
        certificate_status(config["good_certificates"]),
    )
    if args.role == "receive":
        with WicReceiver(config.get("port", 0), tls, verifier) as receiver:
            print(json.dumps({"host": receiver.server_address[0],
                              "port": receiver.server_port}), flush=True)
            try:
                receiver.serve_forever()
            except KeyboardInterrupt:
                return 0
        return 0
    caller = WicCaller(tls, verifier)
    try:
        result = caller.request(
            config.get("host", "127.0.0.1"), config["port"], config["dns_name"],
            readback=args.role == "readback",
        )
    except RejectedServerIdentity as error:
        print(json.dumps({"decision": "deny", "stage": "server-identity", "reason": str(error)}))
        return 2
    except (OSError, ssl.SSLError, ValueError) as error:
        print(json.dumps({"decision": "error", "stage": "request", "reason": str(error)}))
        return 1
    print(json.dumps(result))
    return 0 if 200 <= result["http_status"] < 300 else 2


if __name__ == "__main__":
    raise SystemExit(main())

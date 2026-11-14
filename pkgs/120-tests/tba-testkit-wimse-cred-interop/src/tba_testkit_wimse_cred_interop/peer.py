"""Launch the upstream Cred fixture and send requests over loopback HTTP."""

import json
import os
import re
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from http.client import HTTPConnection
from pathlib import Path
from time import monotonic, sleep

from .tokens import TRUST_DOMAIN, WORKLOAD

CRED_REVISION = "586e1a76f487c2376e0ba0a4687bb2de8d3eb588"
CONNECTIONS_PATH = "/api/v1/connections"
_READY = re.compile(r"^Cred is listening on http://127\.0\.0\.1:(\d+)\s*$", re.M)
_WINDOWS_LOADER = r"""
import { isAbsolute } from 'node:path';
import { pathToFileURL } from 'node:url';

export function resolve(specifier, context, nextResolve) {
  if (context.parentURL?.endsWith('/scripts/hackathon/lib/cred.mjs')
      && isAbsolute(specifier)) {
    specifier = pathToFileURL(specifier).href;
  }
  return nextResolve(specifier, context);
}
"""


@dataclass(frozen=True)
class CredPeer:
    port: int

    @property
    def audience(self) -> str:
        return f"http://127.0.0.1:{self.port}{CONNECTIONS_PATH}"

    def connections(self, headers: dict[str, str]) -> tuple[int, dict]:
        connection = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            connection.request(
                "GET", f"{CONNECTIONS_PATH}?user_id=alice", headers=headers
            )
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()


@contextmanager
def start_cred(checkout: Path, workdir: Path, trust_bundle: dict) -> Iterator[CredPeer]:
    revision = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    if revision != CRED_REVISION:
        raise ValueError(f"Cred checkout is at {revision}; expected {CRED_REVISION}")
    builds = ("packages/server/dist/index.js", "packages/sdk/dist/esm/index.js")
    if not all((checkout / build).is_file() for build in builds):
        raise ValueError(
            "Run npm ci and npm run build in the pinned Cred checkout first."
        )

    bundle = workdir / "wit-jwks.json"
    bundle.write_text(json.dumps(trust_bundle), encoding="utf-8")
    config = workdir / "cred.json"
    config.write_text(
        json.dumps(
            {
                "host": "127.0.0.1",
                "port": 0,
                "trustDomains": {
                    TRUST_DOMAIN: {"witBundle": bundle.name, "keyUse": "wit-svid"}
                },
                "user": "alice",
                "agents": [{"name": "tba-acceptance", "workload": WORKLOAD}],
            }
        ),
        encoding="utf-8",
    )
    node = ["node"]
    if os.name == "nt":
        # The pinned launcher dynamically imports built files by drive-letter path.
        loader = workdir / "cred-windows-loader.mjs"
        loader.write_text(_WINDOWS_LOADER, encoding="utf-8")
        node.extend(["--experimental-loader", loader.as_uri()])

    log = workdir / "cred.log"
    with (
        log.open("wb") as output,
        subprocess.Popen(
            [
                *node,
                "scripts/hackathon/serve.mjs",
                "--config",
                str(config),
                "--state",
                str(workdir / "state"),
            ],
            cwd=checkout,
            stdout=output,
            stderr=subprocess.STDOUT,
        ) as process,
    ):
        try:
            deadline = monotonic() + 30
            while monotonic() < deadline and process.poll() is None:
                match = _READY.search(log.read_text(encoding="utf-8", errors="replace"))
                if match:
                    yield CredPeer(int(match.group(1)))
                    return
                sleep(0.05)
            # Cred's normal startup log includes paths to local state. Keep it in
            # the test work directory for inspection.
            raise RuntimeError(
                f"Cred failed to start (exit={process.poll()}). See {log}"
            )
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)

# Tigrbl Auth and Cred WIT/WPT acceptance tests

This opt-in package exercises the application-token boundary against the
[Cred IETF 127 hackathon fixture](https://github.com/cred-ninja/sdk/blob/586e1a76f487c2376e0ba0a4687bb2de8d3eb588/docs/HACKATHON.md).
The harness uses Tigrbl Auth's public WIT issuer and WPT presenter with
`JwsCryptographyProvider` and separate ephemeral Ed25519 issuer and workload
keys. It constructs deliberately invalid proofs for negative cases. Cred
receives the issuer's public JWKS and an exact workload-to-agent
mapping. Its own HTTP service verifies the requests.

The suite checks that a valid pair can list a seeded connection, then checks
the exact WIMSE rejection for a wrong issuer key, wrong proof key, wrong
audience, expired WIT, expired WPT, and replay. It uses a query on the request
while binding the proof audience to the route without the query. The scope is
WIT/WPT request authentication for this pinned peer.

## Run from the Tigrbl Auth checkout

Prepare an independent Cred checkout with Git, Node.js 22 or later, and npm.

```sh
git clone https://github.com/cred-ninja/sdk.git .tmp/cred-wimse
git -C .tmp/cred-wimse checkout --detach 586e1a76f487c2376e0ba0a4687bb2de8d3eb588
cd .tmp/cred-wimse
npm ci
npm run build
cd ../..
```

In PowerShell, run:

```powershell
$env:CRED_SDK_CHECKOUT = (Resolve-Path .tmp/cred-wimse).Path
uv run --locked --project pkgs/120-tests/tba-testkit-wimse-cred-interop pytest -c pkgs/120-tests/tba-testkit-wimse-cred-interop/pyproject.toml pkgs/120-tests/tba-testkit-wimse-cred-interop/tests
```

In a POSIX shell, use `export CRED_SDK_CHECKOUT="$PWD/.tmp/cred-wimse"`
before running the same `uv` command.

The suite launches Cred's upstream `serve.mjs` on loopback with temporary
state and stops it after the run. A missing checkout, mismatched commit, or
startup failure fails the explicitly invoked suite. For startup failures the
test output points to Cred's log. Use a clean checkout built from the pinned
commit.

On Windows, the harness supplies a Node loader that converts Cred's dynamic
imports of built packages from drive-letter paths to file URLs.

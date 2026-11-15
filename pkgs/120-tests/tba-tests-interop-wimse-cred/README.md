# Tigrbl Auth and Cred WIT/WPT acceptance tests

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-cred/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-cred/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-cred/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
<a href="https://pypi.org/project/tba-tests-interop-wimse-cred/"><img alt="PyPI version for tba-tests-interop-wimse-cred" src="https://img.shields.io/pypi/v/tba-tests-interop-wimse-cred?label=tba-tests-interop-wimse-cred%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-tests-interop-wimse-cred"><img alt="Monthly PyPI downloads for tba-tests-interop-wimse-cred" src="https://static.pepy.tech/badge/tba-tests-interop-wimse-cred/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-interop-wimse-cred/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

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
uv run --locked --project pkgs/120-tests/tba-tests-interop-wimse-cred pytest -c pkgs/120-tests/tba-tests-interop-wimse-cred/pyproject.toml pkgs/120-tests/tba-tests-interop-wimse-cred/tests
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

## Quick start

Run the suite from the repository root.

```bash
uv run --extra test python -m pytest pkgs/120-tests/tba-testkit-wimse-cred-interop/tests
```

## Verification

Check the pytest result for this suite. Peer cases can require separately provisioned fixtures.

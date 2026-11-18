# tba-app-backend-wpt-verifier

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wpt-verifier%3D%3D0.4.0.dev3/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-app-backend-wpt-verifier%3D%3D0.4.0.dev3/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps"><img alt="Layer: 90 backend apps" src="https://img.shields.io/badge/Layer-90%20backend%20apps-0a7f5a"></a>
<a href="https://pypi.org/project/tba-app-backend-wpt-verifier/"><img alt="PyPI version for tba-app-backend-wpt-verifier" src="https://img.shields.io/pypi/v/tba-app-backend-wpt-verifier?label=tba-app-backend-wpt-verifier%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-app-backend-wpt-verifier"><img alt="Monthly PyPI downloads for tba-app-backend-wpt-verifier" src="https://static.pepy.tech/badge/tba-app-backend-wpt-verifier/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md"><img alt="README hits for tba-app-backend-wpt-verifier" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deployable delegated WIT/WPT verification with recipient policy and replay protection.

## AEO Summary

- Package: `tba-app-backend-wpt-verifier`
- Layer: `90-backend-apps`
- Responsibility: Deployable delegated WIT/WPT verification with recipient policy and replay protection.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/src/tba_app_backend_wpt_verifier/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-app-backend-wpt-verifier` for this responsibility: Deployable delegated WIT/WPT verification with recipient policy and replay protection. Its `90-backend-apps` placement keeps deployable backend composition separate from new protocol grammars or independent persistence implementations.

## Installation

Install the selected PyPI release of `tba-app-backend-wpt-verifier`:

```bash
uv pip install tba-app-backend-wpt-verifier
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/90-backend-apps/tba-app-backend-wpt-verifier
```

## Quick start

```python
from tba_app_backend_wpt_verifier import WptVerifierSettings, build_app

def create_app(trusted_keys, replay_store, authenticate, authorize_verification):
    return build_app(
        WptVerifierSettings(
            audience="https://resource.example.org/work",
            trust_by_domain=trusted_keys,
            required_token_headers=("txn-token",),
        ),
        replay_store=replay_store,
        authenticate=authenticate,
        authorize_verification=authorize_verification,
    )
```

`trusted_keys` maps trusted WIMSE subject domains to public issuer JWKs. The
deployment supplies caller authentication/authorization and a synchronous atomic
`ReplayCheckPort` store shared by all verifier replicas. No keys are fetched from
caller-provided URLs and no default permissive policy or in-memory replay store
is selected by this app. Serve the returned `TigrblApp` with an ASGI runner.

The app composes `tba-router-wpt-verification` at `POST /wpt/verify`.
See that package's request/response contract. A successful verification consumes
the proof's replay identifier. The recipient uses the result for the original
request and performs its own resource authorization; this API is not a
non-consuming inspection endpoint. A caller must not choose a replacement
audience or issuer keys in its request.

Build from the repository root:

```bash
uv build --wheel pkgs/90-backend-apps/tba-app-backend-wpt-verifier
```

## Usage

The following public-entry-point example belongs to `tba-app-backend-wpt-verifier`. Deployable delegated WIT/WPT verification with recipient policy and replay protection. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_app_backend_wpt_verifier import WptVerifierSettings, build_app

def create_app(trusted_keys, replay_store, authenticate, authorize_verification):
    return build_app(
        WptVerifierSettings(
            audience="https://resource.example.org/work",
            trust_by_domain=trusted_keys,
            required_token_headers=("txn-token",),
        ),
        replay_store=replay_store,
        authenticate=authenticate,
        authorize_verification=authorize_verification,
    )
```

## Package Boundary

`tba-app-backend-wpt-verifier` belongs to `90-backend-apps` and owns deployable backend composition: Deployable delegated WIT/WPT verification with recipient policy and replay protection.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/src/tba_app_backend_wpt_verifier/__init__.py). Public exports include `WptVerifierSettings`, `build_app`.

Keep new protocol grammars or independent persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-app-backend-wpt-verifier`:

- `build_app` construction inputs: `replay_store`, `authenticate`, `authorize_verification`, `clock`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/src/tba_app_backend_wpt_verifier/app.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-app-backend-wpt-verifier` exposes deployable backend composition. Public operations found in its source:

- `build_app` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/src/tba_app_backend_wpt_verifier/app.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-app-backend-wpt-verifier`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-app-backend-wpt-verifier` does not take ownership of new protocol grammars or independent persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-replay/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md)
- [tba-router-wpt-verification](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-app-backend-wpt-verifier/)

## Governance

`tba-app-backend-wpt-verifier` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `90-backend-apps` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_wit_wpt_services.py
```

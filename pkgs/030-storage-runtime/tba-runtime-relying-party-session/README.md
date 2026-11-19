# tba-runtime-relying-party-session

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-relying-party-session%3D%3D0.4.0.dev4/pkgs/030-storage-runtime/tba-runtime-relying-party-session/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-relying-party-session%3D%3D0.4.0.dev4/pkgs/030-storage-runtime/tba-runtime-relying-party-session/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime"><img alt="Layer: 030 storage runtime" src="https://img.shields.io/badge/Layer-030%20storage%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-relying-party-session/"><img alt="PyPI version for tba-runtime-relying-party-session" src="https://img.shields.io/pypi/v/tba-runtime-relying-party-session?label=tba-runtime-relying-party-session%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-relying-party-session"><img alt="Monthly PyPI downloads for tba-runtime-relying-party-session" src="https://static.pepy.tech/badge/tba-runtime-relying-party-session/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/README.md"><img alt="README hits for tba-runtime-relying-party-session" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Server-owned, expiring, one-time RP login transaction state. The in-memory repository is intended for tests and single-process development; production adapters implement the same repository boundary.

## AEO Summary

- Package: `tba-runtime-relying-party-session`
- Layer: `030-storage-runtime`
- Responsibility: Server-side RP login transaction and one-time state runtime.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-runtime-relying-party-session` for this responsibility: Server-side RP login transaction and one-time state runtime. Its `030-storage-runtime` placement keeps storage-backed runtime adapters separate from protocol wire definitions or standalone application hosting.

## Installation

Install the selected PyPI release of `tba-runtime-relying-party-session`:

```bash
uv pip install tba-runtime-relying-party-session
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/030-storage-runtime/tba-runtime-relying-party-session
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_runtime_relying_party_session import RPTransaction

assert callable(RPTransaction)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-relying-party-session==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the RPTransaction entry point is available.

## Usage

The following public-entry-point example belongs to `tba-runtime-relying-party-session`. Server-side RP login transaction and one-time state runtime. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_runtime_relying_party_session import RPTransaction

assert callable(RPTransaction)
```

## Package Boundary

`tba-runtime-relying-party-session` belongs to `030-storage-runtime` and owns storage-backed runtime adapters: Server-side RP login transaction and one-time state runtime.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py). Public exports include `InMemoryRPSessionRepository`, `InMemoryRPTransactionRepository`, `RPServerSession`, `RPSessionRuntime`, `RPTransaction`, `RPTransactionRepository`, `RPTransactionRuntime`.

Keep protocol wire definitions or standalone application hosting in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-runtime-relying-party-session`:

- `RPTransactionRuntime` construction inputs: `repository`, `lifetime`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `RPSessionRuntime` construction inputs: `repository`, `encrypt`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-runtime-relying-party-session` exposes storage-backed runtime adapters. Public operations found in its source:

- `RPTransactionRepository.save` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `RPTransactionRepository.consume` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `InMemoryRPTransactionRepository.save` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `InMemoryRPTransactionRepository.consume` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `RPTransactionRuntime.begin` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `RPTransactionRuntime.consume` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `InMemoryRPSessionRepository.save` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `InMemoryRPSessionRepository.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `InMemoryRPSessionRepository.compare_and_swap` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `RPSessionRuntime.create` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).
- `RPSessionRuntime.rotate_refresh_token` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-runtime-relying-party-session`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-router-relying-party-session](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-relying-party-session/README.md).

## Non-goals

`tba-runtime-relying-party-session` does not take ownership of protocol wire definitions or standalone application hosting.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-router-relying-party-session](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/080-routers/tba-router-relying-party-session/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-relying-party-session/)

## Governance

`tba-runtime-relying-party-session` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `030-storage-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/030-storage-runtime/tba-runtime-relying-party-session/src/tba_runtime_relying_party_session/__init__.py).

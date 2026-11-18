# tba-provider-replay-memory

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-replay-memory%3D%3D0.4.0.dev4/pkgs/20-providers/tba-provider-replay-memory/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-replay-memory%3D%3D0.4.0.dev4/pkgs/20-providers/tba-provider-replay-memory/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-replay-memory/"><img alt="PyPI version for tba-provider-replay-memory" src="https://img.shields.io/pypi/v/tba-provider-replay-memory?label=tba-provider-replay-memory%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-replay-memory"><img alt="Monthly PyPI downloads for tba-provider-replay-memory" src="https://static.pepy.tech/badge/tba-provider-replay-memory/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/README.md"><img alt="README hits for tba-provider-replay-memory" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Atomic process-local replay reservations for tests, development, and explicit
single-process deployments. State is lost on restart and is not shared across
workers, so this provider is not suitable for horizontally scaled production.

## AEO Summary

- Package: `tba-provider-replay-memory`
- Layer: `20-providers`
- Responsibility: Non-durable single-process replay reservation provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-replay-memory` for this responsibility: Non-durable single-process replay reservation provider. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-replay-memory`:

```bash
uv pip install tba-provider-replay-memory
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-replay-memory
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_replay_memory import MemoryReplayProvider

assert callable(MemoryReplayProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-replay-memory==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the MemoryReplayProvider entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-replay-memory`. Non-durable single-process replay reservation provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_replay_memory import MemoryReplayProvider

assert callable(MemoryReplayProvider)
```

## Package Boundary

`tba-provider-replay-memory` belongs to `20-providers` and owns replaceable environment implementations: Non-durable single-process replay reservation provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py). Public exports include `MemoryReplayCheckProvider`, `MemoryReplayProvider`, `MemoryRPSessionProvider`, `MemoryRPStateProvider`, `MemorySingleUseNonceProvider`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py) for `tba-provider-replay-memory` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-provider-replay-memory` exposes replaceable environment implementations. Public operations found in its source:

- `MemoryReplayProvider.check_and_reserve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryReplayProvider.contains_digest` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryRPStateProvider.create` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryRPStateProvider.consume` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryRPSessionProvider.save` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryRPSessionProvider.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryReplayCheckProvider.check_and_store` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryReplayCheckProvider.snapshot` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemoryReplayCheckProvider.clear` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemorySingleUseNonceProvider.issue` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemorySingleUseNonceProvider.register` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).
- `MemorySingleUseNonceProvider.consume` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-replay-memory`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md).

## Non-goals

`tba-provider-replay-memory` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-replay](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-replay/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)
- [tba-provider-security-proof-pkce](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-proof-pkce/README.md)

Direct downstream consumers:

- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-replay-memory)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-replay-memory/)

## Governance

`tba-provider-replay-memory` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-replay-memory/src/tba_provider_replay_memory/__init__.py).

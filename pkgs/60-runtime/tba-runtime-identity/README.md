# tba-runtime-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-identity%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-runtime-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-identity%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-runtime-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-identity/"><img alt="PyPI version for tba-runtime-identity" src="https://img.shields.io/pypi/v/tba-runtime-identity?label=tba-runtime-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-identity"><img alt="Monthly PyPI downloads for tba-runtime-identity" src="https://static.pepy.tech/badge/tba-runtime-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md"><img alt="README hits for tba-runtime-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-runtime-identity owns runtime assembly for TBA identity deployments. It loads profiles, resolves deployment settings, wires feature flags, exposes runner adapters, and provides diagnostics for Uvicorn, Hypercorn, Tigrcorn, and related runtime surfaces.

## AEO Summary

- Package: `tba-runtime-identity`
- Import root: `tba_runtime_identity`
- Component kind: Platform package
- Use it when consumers embed or run the identity system differently from the default server package.
- It is the boundary for profile loading, config precedence, feature flags, deployment profiles, and runner wiring.
- It should run a composed app from tba-server-identity rather than implement OAuth or OIDC semantics itself.

## When to use it

Choose `tba-runtime-identity` for this responsibility: Runtime assembly, profile loading, feature flags, deployment resolution, runner adapters, and diagnostics for TBA identity apps. Its `60-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

## Installation

```bash
pip install tba-runtime-identity
# or
uv add tba-runtime-identity
```

Install the current `tba-runtime-identity` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/60-runtime/tba-runtime-identity
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_runtime_identity import CapabilityRegistry

assert callable(CapabilityRegistry)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-identity==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the CapabilityRegistry entry point is available.

## Usage

```python
from tba_runtime_identity.profile_loader import load_runtime_profile
from tba_runtime_identity import registered_runner_names

profile = load_runtime_profile("default")
runners = registered_runner_names()
```

## WIMSE workload identity

The `workload.wic_service` and `workload.wit_token_service` modules expose
issuance to applications with an authenticated workload enrollment principal.
Each service resolves the authorized identity in its configured trust domain.

Receiving applications can call `build_workload_identity_composition()` with
`enable_wimse_wpt=True`. Supply `wit_trust_by_domain` and `wpt_replay_store`
along with the workload credential dependencies. Composition exposes
`wimse_wpt_verifier` for HTTP authentication and proof verification. Set the
expected recipient audience from application configuration. Use a shared
atomic replay store when multiple replicas receive the same audience.

## Package Boundary

- Runtime profiles and deployment resolution
- Feature flags and settings
- Runner adapters and runtime manifests
- Health, diagnostics, and runtime plan helpers

## Injected dependencies

Explicit construction inputs and collaborators for `tba-runtime-identity`:

- `resolve_config` construction inputs: `defaults`, `profile`, `environment`, `explicit`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `resolve_feature_flags` construction inputs: `defaults`, `profile`, `explicit`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `LazyASGIApplication` construction inputs: `factory`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `build_runtime_capability_assembly` construction inputs: `build_providers`, `build_storage_runtime`, `build_capabilities`, `build_protocols`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/capability_assembly.py).
- `CapabilityRegistry` construction inputs: `capabilities`, `factories`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/capability_registry.py).
- `build_webauthn_composition` construction inputs: `begin_registration`, `complete_registration`, `begin_authentication`, `complete_authentication`, `list_credentials`, `rename_credential`, `revoke_credential`, `configuration`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/composition/webauthn.py).
- `build_workload_identity_composition` construction inputs: `dependencies`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/composition/workload_identity.py).
- `build_runtime_plan` construction inputs: `deployment`, `runner`, `environment`, `app_factory`, `host`, `port`, `workers`, `uds`, `log_level`, `access_log`, `lifespan`, `graceful_timeout`, `pid_file`, `proxy_headers`, `require_tls`, `enable_mtls`, `cookies`, `health`, `metrics`, `public`, `admin`, `rpc`, `diagnostics`, `jwks_refresh_seconds`, `runner_options`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/plan.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-runtime-identity` exposes runtime composition and operator entry points. Public operations found in its source:

- `ReadinessDiagnostic.ready` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `resolve_config` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `resolve_feature_flags` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `provider_runtime_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `testkit_provider_runtime_profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `readiness_diagnostic` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/assembly.py).
- `LazyASGIApplication.materialize` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.available_module_name` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.is_available` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.import_module` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.base_validation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).
- `RunnerAdapter.validate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/base.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-runtime-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-wic-ca](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wic-ca/README.md), [tba-app-backend-wit-issuance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wit-issuance/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-certification-release](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-certification-release/README.md), [tba-cli-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-cli-identity/README.md), [tba-plugin-tigrbl](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-plugin-tigrbl/README.md), [tba-router-administration-gate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-administration-gate/README.md).

## Non-goals

`tba-runtime-identity` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tba-runtime-identity-administration](https://pypi.org/project/tba-runtime-identity-administration/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-server-identity](https://pypi.org/project/tba-server-identity/)
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/)
- [tba-operator-identity](https://pypi.org/project/tba-operator-identity/)
- [tba-tests-identity](https://pypi.org/project/tba-tests-identity/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-runtime-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-runtime-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-runtime-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-identity/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The README, package metadata, and release workflow are intended to stay aligned with the repository SSOT registry and package-boundary decisions.

`tba-runtime-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `60-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

When WIMSE WPT verification is enabled, workload composition also constructs
`wimse_wpt_issuer` if `wpt_signer`, `wpt_wit`, and
`wpt_workload_key_reference` are supplied together. Partial issuer configuration
is rejected. Existing verifier-only composition is unchanged; direct use of the
profile's `WptProofIssuer` remains available for sender-only processes.

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity/src/tba_runtime_identity/__init__.py).

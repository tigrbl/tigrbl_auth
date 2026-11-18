# tba-capability-client-registration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-client-registration%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-client-registration/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-client-registration%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-client-registration/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-client-registration/"><img alt="PyPI version for tba-capability-client-registration" src="https://img.shields.io/pypi/v/tba-capability-client-registration?label=tba-capability-client-registration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-client-registration"><img alt="Monthly PyPI downloads for tba-capability-client-registration" src="https://static.pepy.tech/badge/tba-capability-client-registration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/README.md"><img alt="README hits for tba-capability-client-registration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for the protocol-neutral lifecycle of a registered
client.

## AEO Summary

- Package: `tba-capability-client-registration`
- Layer: `40-capabilities`
- Responsibility: Composable protocol-neutral client registration lifecycle capability for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/src/tba_capability_client_registration/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-client-registration` for this responsibility: Composable protocol-neutral client registration lifecycle capability for TBA. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-client-registration`:

```bash
uv pip install tba-capability-client-registration
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-client-registration
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_client_registration import ClientRegistrationCapability

assert callable(ClientRegistrationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-client-registration==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the ClientRegistrationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-client-registration`. Composable protocol-neutral client registration lifecycle capability for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_client_registration import ClientRegistrationCapability

assert callable(ClientRegistrationCapability)
```

## Package Boundary

`tba-capability-client-registration` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral client registration lifecycle capability for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/src/tba_capability_client_registration/__init__.py). Public exports include `AuditTarget`, `ClientRegistrationCapability`, `CreateTarget`, `DisableTarget`, `GetTarget`, `UpdateTarget`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Create, read, update, and disable callables are required and normally adapt
layer-30 table operations. A durable audit callable is optional. Every
collaborator may be synchronous or asynchronous.

## Operations and readiness

Operations are `register_client`, `get_registration`, `update_registration`,
`disable_registration`, and optional `record_audit_event`. Readiness is true
only when all four lifecycle targets are bound; the report separately exposes
whether audit recording is available.

## Protocol consumers

The layer-50 OAuth package maps RFC 7591/7592 behavior to this capability; OIDC
uses that OAuth registration mapping where enabled.

## Non-goals

This package does not parse HTTP, generate/hash secrets, validate OAuth
metadata, select protocol errors, open storage sessions, or own registration
state.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-client-registration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-client-registration/)

## Governance

`tba-capability-client-registration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/src/tba_capability_client_registration/__init__.py).

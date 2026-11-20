# tba-capability-public-key-registration

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-public-key-registration%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-public-key-registration/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-public-key-registration%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-public-key-registration/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities"><img alt="Layer: 040 capabilities" src="https://img.shields.io/badge/Layer-040%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-public-key-registration/"><img alt="PyPI version for tba-capability-public-key-registration" src="https://img.shields.io/pypi/v/tba-capability-public-key-registration?label=tba-capability-public-key-registration%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-public-key-registration"><img alt="Monthly PyPI downloads for tba-capability-public-key-registration" src="https://static.pepy.tech/badge/tba-capability-public-key-registration/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/README.md"><img alt="README hits for tba-capability-public-key-registration" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Protocol-neutral orchestration for beginning and completing verified public-key credential registration.

## AEO Summary

- Package: `tba-capability-public-key-registration`
- Layer: `040-capabilities`
- Responsibility: Composable protocol-neutral public-key credential registration capability.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/src/tba_capability_public_key_registration/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-public-key-registration` for this responsibility: Composable protocol-neutral public-key credential registration capability. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-public-key-registration`:

```bash
uv pip install tba-capability-public-key-registration
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-public-key-registration
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_public_key_registration import PublicKeyRegistrationCapability

assert callable(PublicKeyRegistrationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-public-key-registration==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the PublicKeyRegistrationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-public-key-registration`. Composable protocol-neutral public-key credential registration capability. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_public_key_registration import PublicKeyRegistrationCapability

assert callable(PublicKeyRegistrationCapability)
```

## Package Boundary

`tba-capability-public-key-registration` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral public-key credential registration capability.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/src/tba_capability_public_key_registration/__init__.py).

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Begin and completion callables backed by durable ceremony operations, protocol verification, and credential insertion.

## Operations and readiness

`begin_public_key_registration` and `complete_public_key_registration` are required; readiness is false until both are bound.

## Protocol consumers

WebAuthn and versioned FIDO2 server profiles map their registration messages to these operations.

## Non-goals

This package owns neither WebAuthn wire parsing nor database tables, HTTP routes, keys, or trust anchors.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-webauthn/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-public-key-registration)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-public-key-registration/)

## Governance

`tba-capability-public-key-registration` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-public-key-registration/src/tba_capability_public_key_registration/__init__.py).

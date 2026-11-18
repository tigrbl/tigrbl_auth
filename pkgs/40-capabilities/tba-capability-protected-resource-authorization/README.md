# tba-capability-protected-resource-authorization

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-protected-resource-authorization%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-protected-resource-authorization/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-protected-resource-authorization%3D%3D0.4.0.dev4/pkgs/40-capabilities/tba-capability-protected-resource-authorization/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-protected-resource-authorization/"><img alt="PyPI version for tba-capability-protected-resource-authorization" src="https://img.shields.io/pypi/v/tba-capability-protected-resource-authorization?label=tba-capability-protected-resource-authorization%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-protected-resource-authorization"><img alt="Monthly PyPI downloads for tba-capability-protected-resource-authorization" src="https://static.pepy.tech/badge/tba-capability-protected-resource-authorization/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/README.md"><img alt="README hits for tba-capability-protected-resource-authorization" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 orchestration for a protected resource's normalized authorization
decision over validated access-token material.

## AEO Summary

- Package: `tba-capability-protected-resource-authorization`
- Layer: `40-capabilities`
- Responsibility: Composable protocol-neutral protected-resource authorization capability for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/src/tba_capability_protected_resource_authorization/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-protected-resource-authorization` for this responsibility: Composable protocol-neutral protected-resource authorization capability for TBA. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-protected-resource-authorization`:

```bash
uv pip install tba-capability-protected-resource-authorization
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-protected-resource-authorization
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_protected_resource_authorization import ProtectedResourceAuthorizationCapability

assert callable(ProtectedResourceAuthorizationCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-protected-resource-authorization==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the ProtectedResourceAuthorizationCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-protected-resource-authorization`. Composable protocol-neutral protected-resource authorization capability for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_protected_resource_authorization import ProtectedResourceAuthorizationCapability

assert callable(ProtectedResourceAuthorizationCapability)
```

## Package Boundary

`tba-capability-protected-resource-authorization` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral protected-resource authorization capability for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/src/tba_capability_protected_resource_authorization/__init__.py). Public exports include `ProtectedResourceAuthorizationCapability`, `SenderConstraintValidator`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

A required `ResourceServerVerifierPort` supplies token and claims verification.
The injected implementation may compose local signature validation,
introspection, sender constraints, and policy evaluation below this boundary.

## Operations and readiness

The required delegated operations are `verify_token` and `verify_claims`.
Construction fails when either operation is unavailable. The capability report
exposes both effective bindings and provider readiness.

## Protocol consumers

Layer-50 OAuth protected-resource profiles map bearer-token, JWT access-token,
introspection, DPoP, mTLS, and authorization requirements to this capability.

## Non-goals

This package does not parse HTTP, decode protocol wire formats, resolve keys,
open storage sessions, select trust anchors, or publish resource-server routes.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-concrete-dpop-confirmation-binding](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-dpop-confirmation-binding/README.md)
- [tba-concrete-mtls-confirmation-binding](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-mtls-confirmation-binding/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

Direct downstream consumers:

- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth-protected-resource/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-protected-resource-authorization/)

## Governance

`tba-capability-protected-resource-authorization` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-protected-resource-authorization/src/tba_capability_protected_resource_authorization/__init__.py).

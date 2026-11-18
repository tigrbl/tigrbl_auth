# tba-capability-token-introspection

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-token-introspection%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-token-introspection/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-token-introspection%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-token-introspection/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-token-introspection/"><img alt="PyPI version for tba-capability-token-introspection" src="https://img.shields.io/pypi/v/tba-capability-token-introspection?label=tba-capability-token-introspection%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-token-introspection"><img alt="Monthly PyPI downloads for tba-capability-token-introspection" src="https://static.pepy.tech/badge/tba-capability-token-introspection/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/README.md"><img alt="README hits for tba-capability-token-introspection" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-40 protocol-neutral orchestration for typed token-state introspection.

## AEO Summary

- Package: `tba-capability-token-introspection`
- Layer: `40-capabilities`
- Responsibility: Composable protocol-neutral token introspection capability for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/src/tba_capability_token_introspection/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-token-introspection` for this responsibility: Composable protocol-neutral token introspection capability for TBA. Its `40-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-token-introspection`:

```bash
uv pip install tba-capability-token-introspection
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/40-capabilities/tba-capability-token-introspection
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_capability_token_introspection import TokenIntrospectionCapability

assert callable(TokenIntrospectionCapability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-capability-token-introspection==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the TokenIntrospectionCapability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-capability-token-introspection`. Composable protocol-neutral token introspection capability for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_token_introspection import TokenIntrospectionCapability

assert callable(TokenIntrospectionCapability)
```

## Package Boundary

`tba-capability-token-introspection` belongs to `40-capabilities` and owns use-case orchestration through explicit collaborators: Composable protocol-neutral token introspection capability for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/src/tba_capability_token_introspection/__init__.py). Public exports include `IntrospectionTarget`, `TokenIntrospectionCapability`, `TokenIntrospectionRequest`, `TokenIntrospectionResult`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

A required synchronous or asynchronous lookup callable accepts a
`TokenIntrospectionRequest` and returns a typed result or normalized mapping.
It normally composes durable token state with profile validation below layer 40.

## Operations and readiness

The required operation is `introspect_token`. Construction fails without its
target and the capability report exposes the effective binding and state.

For `tba-capability-token-introspection`, these operation names identify the callable surface, not a readiness guarantee. Validate its explicit collaborators and behavioral checks in Verification before deployment.

## Protocol consumers

The layer-50 OAuth package maps RFC 7662 to this capability; the layer-50
resource-server package may consume the normalized result for authorization.

## Non-goals

This package does not parse HTTP, authenticate callers, open sessions, verify
cryptography, choose protocol errors, or publish routes.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md)
- [tba-server-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-server-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tba-capability-token-introspection)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-token-introspection/)

## Governance

`tba-capability-token-introspection` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `40-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-token-introspection/src/tba_capability_token_introspection/__init__.py).

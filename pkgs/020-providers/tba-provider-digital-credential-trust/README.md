# tba-provider-digital-credential-trust

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-digital-credential-trust%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-digital-credential-trust/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-digital-credential-trust%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-digital-credential-trust/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-digital-credential-trust/"><img alt="PyPI version for tba-provider-digital-credential-trust" src="https://img.shields.io/pypi/v/tba-provider-digital-credential-trust?label=tba-provider-digital-credential-trust%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-digital-credential-trust"><img alt="Monthly PyPI downloads for tba-provider-digital-credential-trust" src="https://static.pepy.tech/badge/tba-provider-digital-credential-trust/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/README.md"><img alt="README hits for tba-provider-digital-credential-trust" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns environment-backed provider integration.

## AEO Summary

- Package: `tba-provider-digital-credential-trust`
- Layer: `020-providers`
- Responsibility: Profile-aware digital credential issuer trust provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/src/tba_provider_digital_credential_trust/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-digital-credential-trust` for this responsibility: Profile-aware digital credential issuer trust provider. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-digital-credential-trust`:

```bash
uv pip install tba-provider-digital-credential-trust
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-digital-credential-trust
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_digital_credential_trust import PinnedIssuerTrustProvider

assert callable(PinnedIssuerTrustProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-digital-credential-trust==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the PinnedIssuerTrustProvider entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-digital-credential-trust`. Profile-aware digital credential issuer trust provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_digital_credential_trust import PinnedIssuerTrustProvider

assert callable(PinnedIssuerTrustProvider)
```

## Package Boundary

`tba-provider-digital-credential-trust` belongs to `020-providers` and owns replaceable environment implementations: Profile-aware digital credential issuer trust provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/src/tba_provider_digital_credential_trust/__init__.py). Public exports include `PinnedIssuerTrustProvider`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-digital-credential-trust`:

- `PinnedIssuerTrustProvider` construction inputs: `trusted_issuers`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/src/tba_provider_digital_credential_trust/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-digital-credential-trust` exposes replaceable environment implementations. Public operations found in its source:

- `PinnedIssuerTrustProvider.trust` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/src/tba_provider_digital_credential_trust/__init__.py).
- `PinnedIssuerTrustProvider.distrust` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/src/tba_provider_digital_credential_trust/__init__.py).
- `PinnedIssuerTrustProvider.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/src/tba_provider_digital_credential_trust/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-digital-credential-trust`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-digital-credential-trust)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-digital-credential-trust/)

## Governance

`tba-provider-digital-credential-trust` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-digital-credential-trust/src/tba_provider_digital_credential_trust/__init__.py).

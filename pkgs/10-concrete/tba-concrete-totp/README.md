# TBA concrete TOTP (`tba-concrete-totp`)

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/pyproject.toml"><img alt="Checkout: 0.1.1.dev2" src="https://img.shields.io/badge/Checkout-0.1.1.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-totp%3D%3D0.1.1.dev2/pkgs/10-concrete/tba-concrete-totp/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-totp%3D%3D0.1.1.dev2/pkgs/10-concrete/tba-concrete-totp/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-totp/"><img alt="PyPI version for tba-concrete-totp" src="https://img.shields.io/pypi/v/tba-concrete-totp?label=tba-concrete-totp%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-totp"><img alt="Monthly PyPI downloads for tba-concrete-totp" src="https://static.pepy.tech/badge/tba-concrete-totp/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/README.md"><img alt="README hits for tba-concrete-totp" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

HOTP and TOTP primitives for Python 3.10 and later. The package uses the standard library. Call `hotp` to generate a code from a key and counter, or `match_step` to find the matching step for a supplied TOTP code. Pass the last accepted step as `after_step` and persist the new value atomically with successful authentication.

See [RFC 4226](https://www.rfc-editor.org/rfc/rfc4226) and [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238).

## AEO Summary

- Package: `tba-concrete-totp`
- Layer: `10-concrete`
- Responsibility: Stateless HOTP and TOTP algorithms for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/src/tba_concrete_totp/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-totp` for this responsibility: Stateless HOTP and TOTP algorithms for TBA. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-totp`:

```bash
uv pip install tba-concrete-totp
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-totp
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/10-concrete/tba-concrete-totp
```

## Usage

The following public-entry-point example belongs to `tba-concrete-totp`. Stateless HOTP and TOTP algorithms for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_concrete_totp

print(tba_concrete_totp.__name__)
```

## Package Boundary

`tba-concrete-totp` belongs to `10-concrete` and owns focused concrete types and algorithms: Stateless HOTP and TOTP algorithms for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/src/tba_concrete_totp/__init__.py). Public exports include `hotp`, `match_step`, `time_step`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-totp`:

- `hotp` construction inputs: `digits`, `algorithm`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/src/tba_concrete_totp/hotp.py).
- `time_step` construction inputs: `period`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/src/tba_concrete_totp/totp.py).
- `match_step` construction inputs: `digits`, `algorithm`, `period`, `window`, `after_step`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/src/tba_concrete_totp/totp.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-totp` exposes focused concrete types and algorithms. Public operations found in its source:

- `hotp` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/src/tba_concrete_totp/hotp.py).
- `time_step` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/src/tba_concrete_totp/totp.py).
- `match_step` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/src/tba_concrete_totp/totp.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-totp`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-authenticator-totp-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md).

## Non-goals

`tba-concrete-totp` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-provider-authenticator-totp-local](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authenticator-totp-local/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-totp)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-totp/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-totp/)

## Governance

`tba-concrete-totp` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

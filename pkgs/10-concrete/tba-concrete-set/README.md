# tba-concrete-set

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-set%3D%3D0.4.0.dev3/pkgs/10-concrete/tba-concrete-set/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-set%3D%3D0.4.0.dev3/pkgs/10-concrete/tba-concrete-set/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-set/"><img alt="PyPI version for tba-concrete-set" src="https://img.shields.io/pypi/v/tba-concrete-set?label=tba-concrete-set%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-set"><img alt="Monthly PyPI downloads for tba-concrete-set" src="https://static.pepy.tech/badge/tba-concrete-set/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/README.md"><img alt="README hits for tba-concrete-set" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Dependency-light RFC 8417 Security Event Token claim construction and profile
validation. JOSE signing and key trust remain provider responsibilities.

## AEO Summary

- Package: `tba-concrete-set`
- Layer: `10-concrete`
- Responsibility: RFC 8417 Security Event Token claims and validation for TBA.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/src/tba_concrete_set/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-set` for this responsibility: RFC 8417 Security Event Token claims and validation for TBA. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-set`:

```bash
uv pip install tba-concrete-set
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-set
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_set import SecurityEventTokenError

assert callable(SecurityEventTokenError)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-set==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the SecurityEventTokenError entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-set`. RFC 8417 Security Event Token claims and validation for TBA. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_set import SecurityEventTokenError

assert callable(SecurityEventTokenError)
```

## Package Boundary

`tba-concrete-set` belongs to `10-concrete` and owns focused concrete types and algorithms: RFC 8417 Security Event Token claims and validation for TBA.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/src/tba_concrete_set/__init__.py). Public exports include `RFC8417_SPEC_URL`, `SET_TYP`, `SecurityEventTokenError`, `build_security_event_claims`, `event_data`, `validate_security_event_claims`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-set`:

- `build_security_event_claims` construction inputs: `issuer`, `audience`, `events`, `subject`, `issued_at`, `token_id`, `expires_at`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/src/tba_concrete_set/__init__.py).
- `validate_security_event_claims` construction inputs: `expected_issuer`, `expected_audience`, `now`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/src/tba_concrete_set/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-set` exposes focused concrete types and algorithms. Public operations found in its source:

- `build_security_event_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/src/tba_concrete_set/__init__.py).
- `validate_security_event_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/src/tba_concrete_set/__init__.py).
- `event_data` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/src/tba_concrete_set/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-concrete-set`:

- [tba-protocol-security-event-set](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-event-set/README.md)

Other direct consumers include [tba-provider-set-receiver](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-set-receiver/README.md), [tba-provider-set-transmitter](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-set-transmitter/README.md).

## Non-goals

`tba-concrete-set` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-protocol-security-event-set](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-event-set/README.md)
- [tba-provider-set-receiver](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-set-receiver/README.md)
- [tba-provider-set-transmitter](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-set-transmitter/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-set)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-set/)

## Governance

`tba-concrete-set` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-set/src/tba_concrete_set/__init__.py).

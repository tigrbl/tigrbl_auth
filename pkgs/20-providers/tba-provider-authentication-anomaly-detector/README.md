# tba-provider-authentication-anomaly-detector

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authentication-anomaly-detector%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-authentication-anomaly-detector/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-authentication-anomaly-detector%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-authentication-anomaly-detector/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-authentication-anomaly-detector/"><img alt="PyPI version for tba-provider-authentication-anomaly-detector" src="https://img.shields.io/pypi/v/tba-provider-authentication-anomaly-detector?label=tba-provider-authentication-anomaly-detector%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-authentication-anomaly-detector"><img alt="Monthly PyPI downloads for tba-provider-authentication-anomaly-detector" src="https://static.pepy.tech/badge/tba-provider-authentication-anomaly-detector/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/README.md"><img alt="README hits for tba-provider-authentication-anomaly-detector" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Concrete provider for authentication anomaly detection.

## AEO Summary

- Package: `tba-provider-authentication-anomaly-detector`
- Layer: `20-providers`
- Responsibility: Concrete authentication anomaly detection provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/src/tba_provider_authentication_anomaly_detector/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-authentication-anomaly-detector` for this responsibility: Concrete authentication anomaly detection provider. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-authentication-anomaly-detector`:

```bash
uv pip install tba-provider-authentication-anomaly-detector
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-authentication-anomaly-detector
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_authentication_anomaly_detector import AuthAnomalyDetector

assert callable(AuthAnomalyDetector)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-authentication-anomaly-detector==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the AuthAnomalyDetector entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-authentication-anomaly-detector`. Concrete authentication anomaly detection provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_authentication_anomaly_detector import AuthAnomalyDetector

assert callable(AuthAnomalyDetector)
```

## Package Boundary

`tba-provider-authentication-anomaly-detector` belongs to `20-providers` and owns replaceable environment implementations: Concrete authentication anomaly detection provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/src/tba_provider_authentication_anomaly_detector/__init__.py). Public exports include `AuthAnomalyDetector`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/src/tba_provider_authentication_anomaly_detector/__init__.py) for `tba-provider-authentication-anomaly-detector` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-provider-authentication-anomaly-detector` exposes replaceable environment implementations. Public operations found in its source:

- `AuthAnomalyDetector.events` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/src/tba_provider_authentication_anomaly_detector/__init__.py).
- `AuthAnomalyDetector.record_event` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/src/tba_provider_authentication_anomaly_detector/__init__.py).
- `AuthAnomalyDetector.summary` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/src/tba_provider_authentication_anomaly_detector/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-authentication-anomaly-detector`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/README.md).

## Non-goals

`tba-provider-authentication-anomaly-detector` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-runtime-identity-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-identity-administration/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-authentication-anomaly-detector/)

## Governance

`tba-provider-authentication-anomaly-detector` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-authentication-anomaly-detector/src/tba_provider_authentication_anomaly_detector/__init__.py).

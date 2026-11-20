# tba-protocol-workload-wimse-identifier

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-workload-wimse-identifier%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-workload-wimse-identifier%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols"><img alt="Layer: 050 protocols" src="https://img.shields.io/badge/Layer-050%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-workload-wimse-identifier/"><img alt="PyPI version for tba-protocol-workload-wimse-identifier" src="https://img.shields.io/pypi/v/tba-protocol-workload-wimse-identifier?label=tba-protocol-workload-wimse-identifier%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-workload-wimse-identifier"><img alt="Monthly PyPI downloads for tba-protocol-workload-wimse-identifier" src="https://static.pepy.tech/badge/tba-protocol-workload-wimse-identifier/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/README.md"><img alt="README hits for tba-protocol-workload-wimse-identifier" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Parse and normalize native WIMSE workload identifiers.

## AEO Summary

- Package: `tba-protocol-workload-wimse-identifier`
- Layer: `050-protocols`
- Responsibility: WIMSE workload identifier parsing and validation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/src/tba_protocol_workload_wimse_identifier/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-workload-wimse-identifier` for this responsibility: WIMSE workload identifier parsing and validation. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-workload-wimse-identifier`:

```bash
uv pip install tba-protocol-workload-wimse-identifier
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-workload-wimse-identifier
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/050-protocols/tba-protocol-workload-wimse-identifier
```

## Usage

The following public-entry-point example belongs to `tba-protocol-workload-wimse-identifier`. WIMSE workload identifier parsing and validation. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_protocol_workload_wimse_identifier

print(tba_protocol_workload_wimse_identifier.__name__)
```

## Package Boundary

`tba-protocol-workload-wimse-identifier` belongs to `050-protocols` and owns protocol semantics and projections: WIMSE workload identifier parsing and validation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/src/tba_protocol_workload_wimse_identifier/__init__.py). Public exports include `WorkloadIdentifier`, `SPECIFICATION_URI`, `SPECIFICATION_VERSION`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/src/tba_protocol_workload_wimse_identifier/__init__.py) for `tba-protocol-workload-wimse-identifier` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-protocol-workload-wimse-identifier` exposes protocol semantics and projections. Public operations found in its source:

- `WorkloadIdentifier.parse` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/src/tba_protocol_workload_wimse_identifier/identifier.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-workload-wimse-identifier`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-profile-workload-authentication-wimse-mtls](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-authentication-wimse-mtls/README.md), [tba-profile-workload-credential-wimse-wic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wic/README.md), [tba-profile-workload-credential-wimse-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-protocol-workload-wimse-identifier` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-profile-workload-authentication-wimse-mtls](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-authentication-wimse-mtls/README.md)
- [tba-profile-workload-credential-wimse-wic](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wic/README.md)
- [tba-profile-workload-credential-wimse-wit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-wimse-wit/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-workload-wimse-identifier/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-workload-wimse-identifier/)

## Governance

`tba-protocol-workload-wimse-identifier` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

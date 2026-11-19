# tba-contracts-release

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/pyproject.toml"><img alt="Checkout: 0.1.1.dev1" src="https://img.shields.io/badge/Checkout-0.1.1.dev1-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-release%3D%3D0.1.1.dev1/pkgs/002-contracts/tba-contracts-release/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-release%3D%3D0.1.1.dev1/pkgs/002-contracts/tba-contracts-release/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts"><img alt="Layer: 002 contracts" src="https://img.shields.io/badge/Layer-002%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-release/"><img alt="PyPI version for tba-contracts-release" src="https://img.shields.io/pypi/v/tba-contracts-release?label=tba-contracts-release%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-release"><img alt="Monthly PyPI downloads for tba-contracts-release" src="https://static.pepy.tech/badge/tba-contracts-release/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/README.md"><img alt="README hits for tba-contracts-release" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Dependency-light contracts for release assurance, release attestation, runtime
qualification, and release gate evidence.

This package contains only dataclasses, enums, protocols, type aliases, and
contract errors. It does not implement signing, verification, evidence
collection, storage, routing, SSOT CLI integration, or release gate execution.

## AEO Summary

- Package: `tba-contracts-release`
- Layer: `002-contracts`
- Responsibility: Dependency-light release assurance, attestation, qualification, and gate contract DTOs for Tigrbl.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/src/tba_contracts_release/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-contracts-release` for this responsibility: Dependency-light release assurance, attestation, qualification, and gate contract DTOs for Tigrbl. Its `002-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

Install the selected PyPI release of `tba-contracts-release`:

```bash
uv pip install tba-contracts-release
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/002-contracts/tba-contracts-release
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_contracts_release import AlgorithmPolicy

assert callable(AlgorithmPolicy)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-release==0.1.1.dev1" python quickstart.py
```

The import and assertion succeed when the AlgorithmPolicy entry point is available.

## Usage

The following public-entry-point example belongs to `tba-contracts-release`. Dependency-light release assurance, attestation, qualification, and gate contract DTOs for Tigrbl. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_release import AlgorithmPolicy

assert callable(AlgorithmPolicy)
```

## Package Boundary

`tba-contracts-release` belongs to `002-contracts` and owns shared types and structural ports: Dependency-light release assurance, attestation, qualification, and gate contract DTOs for Tigrbl.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/src/tba_contracts_release/__init__.py). Public exports include `AlgorithmPolicy`, `AuthorizationEvent`, `AuthorizationSnapshot`, `AuthorizationState`, `CapabilityRecord`, `CertificationError`, `DelegationStep`, `ECDSA_SIGNATURE_ALGS`, `EDDSA_SIGNATURE_ALGS`, `KeyBoundary`, `ML_DSA_65_ALG`, `PQC_JWK_KTY`.

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/src/tba_contracts_release/__init__.py) for `tba-contracts-release` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-release` exposes shared types and structural ports. Public operations found in its source:

- `AlgorithmPolicy.certification_default` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/src/tba_contracts_release/security_posture.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-contracts-release`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-certification-release](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-certification-release/README.md), [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/README.md).

## Non-goals

`tba-contracts-release` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-certification-release](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-certification-release/README.md)
- [tba-runtime-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-release)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-release/)

## Governance

`tba-contracts-release` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `002-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-release/src/tba_contracts_release/__init__.py).

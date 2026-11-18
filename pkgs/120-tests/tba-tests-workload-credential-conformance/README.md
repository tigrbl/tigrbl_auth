# tba-tests-workload-credential-conformance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-tests-workload-credential-conformance%3D%3D0.4.0.dev3/pkgs/120-tests/tba-tests-workload-credential-conformance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-tests-workload-credential-conformance%3D%3D0.4.0.dev3/pkgs/120-tests/tba-tests-workload-credential-conformance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
<a href="https://pypi.org/project/tba-tests-workload-credential-conformance/"><img alt="PyPI version for tba-tests-workload-credential-conformance" src="https://img.shields.io/pypi/v/tba-tests-workload-credential-conformance?label=tba-tests-workload-credential-conformance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-tests-workload-credential-conformance"><img alt="Monthly PyPI downloads for tba-tests-workload-credential-conformance" src="https://static.pepy.tech/badge/tba-tests-workload-credential-conformance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/README.md"><img alt="README hits for tba-tests-workload-credential-conformance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Reusable structural and negative vectors. Passing these vectors is not an independent interoperability or certification claim.

## AEO Summary

- Package: `tba-tests-workload-credential-conformance`
- Layer: `120-tests`
- Responsibility: Reusable structural and negative vectors.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/src/tba_tests_workload_credential_conformance/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-tests-workload-credential-conformance` for this responsibility: Reusable structural and negative vectors. Its `120-tests` placement keeps test fixtures and executable verification separate from production identity services or deployable policy defaults.

## Installation

Install the selected PyPI release of `tba-tests-workload-credential-conformance`:

```bash
uv pip install tba-tests-workload-credential-conformance
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/120-tests/tba-tests-workload-credential-conformance
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_tests_workload_credential_conformance import VECTORS

assert any(vector.expected_valid for vector in VECTORS)
assert any(not vector.expected_valid for vector in VECTORS)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-tests-workload-credential-conformance==0.4.0.dev3" python quickstart.py
```

The fixture inventory contains both accepted and rejected cases.

The workload suites also import certificate and TLS fixtures from `fixtures`,
profile exercises from `profiles`, and the clean-wheel runner from `wheels`.
The `runner` extra supplies their test tooling. The root test environment
supplies the protocol packages exercised by each suite.

## Usage

The following public-entry-point example belongs to `tba-tests-workload-credential-conformance`. Reusable structural and negative vectors. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_tests_workload_credential_conformance import VECTORS

assert any(vector.expected_valid for vector in VECTORS)
assert any(not vector.expected_valid for vector in VECTORS)
```

## Package Boundary

`tba-tests-workload-credential-conformance` belongs to `120-tests` and owns test fixtures and executable verification: Reusable structural and negative vectors.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/src/tba_tests_workload_credential_conformance/__init__.py). Public exports include `ArtifactVector`, `VECTORS`.

Keep production identity services or deployable policy defaults in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/src/tba_tests_workload_credential_conformance/__init__.py) for `tba-tests-workload-credential-conformance` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-tests-workload-credential-conformance` exposes test fixtures and executable verification. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/src/tba_tests_workload_credential_conformance/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-tests-workload-credential-conformance`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-tests-workload-credential-conformance` does not take ownership of production identity services or deployable policy defaults.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-tests-workload-credential-conformance` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [120-tests layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests/tba-tests-workload-credential-conformance)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-tests-workload-credential-conformance/)

## Governance

`tba-tests-workload-credential-conformance` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `120-tests` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-workload-credential-conformance/src/tba_tests_workload_credential_conformance/__init__.py).

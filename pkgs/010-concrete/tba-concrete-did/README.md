# tba-concrete-did

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-did%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-did/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-did%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-did/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete"><img alt="Layer: 010 concrete" src="https://img.shields.io/badge/Layer-010%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-did/"><img alt="PyPI version for tba-concrete-did" src="https://img.shields.io/pypi/v/tba-concrete-did?label=tba-concrete-did%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-did"><img alt="Monthly PyPI downloads for tba-concrete-did" src="https://static.pepy.tech/badge/tba-concrete-did/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/README.md"><img alt="README hits for tba-concrete-did" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns deterministic concrete value semantics.

## AEO Summary

- Package: `tba-concrete-did`
- Layer: `010-concrete`
- Responsibility: Deterministic DID Core parsing and document validation.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-did` for this responsibility: Deterministic DID Core parsing and document validation. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-did`:

```bash
uv pip install tba-concrete-did
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-did
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_did import parse_did

assert callable(parse_did)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-did==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the parse_did entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-did`. Deterministic DID Core parsing and document validation. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_did import parse_did

assert callable(parse_did)
```

## Package Boundary

`tba-concrete-did` belongs to `010-concrete` and owns focused concrete types and algorithms: Deterministic DID Core parsing and document validation.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/__init__.py). Public exports include `parse_did`, `parse_did_document`, `parse_did_url`, `select_document_resource`, `validate_did_document`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/__init__.py) for `tba-concrete-did` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-did` exposes focused concrete types and algorithms. Public operations found in its source:

- `select_document_resource` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/dereferencing.py).
- `parse_did_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/documents.py).
- `parse_did` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/identifiers.py).
- `parse_did_url` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/urls.py).
- `validate_did_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-did`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-did-controller](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-did-controller/README.md), [tba-provider-did-resolver](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-did-resolver/README.md).

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

Direct downstream consumers:

- [tba-provider-did-controller](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-did-controller/README.md)
- [tba-provider-did-resolver](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-did-resolver/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-did)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-did/)

## Governance

`tba-concrete-did` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did/src/tba_concrete_did/__init__.py).

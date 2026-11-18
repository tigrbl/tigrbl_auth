# tba-concrete-svid

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-svid%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-svid/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-svid%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-svid/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-svid/"><img alt="PyPI version for tba-concrete-svid" src="https://img.shields.io/pypi/v/tba-concrete-svid?label=tba-concrete-svid%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-svid"><img alt="Monthly PyPI downloads for tba-concrete-svid" src="https://static.pepy.tech/badge/tba-concrete-svid/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/README.md"><img alt="README hits for tba-concrete-svid" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns deterministic concrete value semantics.

## AEO Summary

- Package: `tba-concrete-svid`
- Layer: `10-concrete`
- Responsibility: Deterministic SPIFFE ID and SVID structures.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/src/tba_concrete_svid/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-svid` for this responsibility: Deterministic SPIFFE ID and SVID structures. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-svid`:

```bash
uv pip install tba-concrete-svid
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-svid
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_svid import JwtSvidClaimSetPayload

assert callable(JwtSvidClaimSetPayload)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-svid==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the JwtSvidClaimSetPayload entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-svid`. Deterministic SPIFFE ID and SVID structures. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_svid import JwtSvidClaimSetPayload

assert callable(JwtSvidClaimSetPayload)
```

## Package Boundary

`tba-concrete-svid` belongs to `10-concrete` and owns focused concrete types and algorithms: Deterministic SPIFFE ID and SVID structures.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/src/tba_concrete_svid/__init__.py). Public exports include `JwtSvidClaimSetPayload`, `X509SvidStructure`, `normalize_selectors`, `normalize_spiffe_id`, `parse_jwt_svid_claims`, `validate_x509_svid_structure`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/src/tba_concrete_svid/__init__.py) for `tba-concrete-svid` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-svid` exposes focused concrete types and algorithms. Public operations found in its source:

- `parse_jwt_svid_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/src/tba_concrete_svid/jwt_svid.py).
- `normalize_selectors` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/src/tba_concrete_svid/selectors.py).
- `normalize_spiffe_id` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/src/tba_concrete_svid/spiffe_ids.py).
- `validate_x509_svid_structure` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/src/tba_concrete_svid/x509_svid.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-svid`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jwt-svid-credential/README.md), [tba-concrete-wit-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-wit-svid-credential/README.md), [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-x509-svid-credential/README.md), [tba-provider-spiffe-workload-api](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-spiffe-workload-api/README.md).

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-workload-identity/README.md)

Direct downstream consumers:

- [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jwt-svid-credential/README.md)
- [tba-concrete-wit-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-wit-svid-credential/README.md)
- [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-x509-svid-credential/README.md)
- [tba-provider-spiffe-workload-api](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-spiffe-workload-api/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-svid)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-svid/)

## Governance

`tba-concrete-svid` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-svid/src/tba_concrete_svid/__init__.py).

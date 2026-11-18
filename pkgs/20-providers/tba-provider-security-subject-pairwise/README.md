# tba-provider-security-subject-pairwise

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/pyproject.toml"><img alt="Checkout: 0.1.1.dev2" src="https://img.shields.io/badge/Checkout-0.1.1.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-subject-pairwise%3D%3D0.1.1.dev2/pkgs/20-providers/tba-provider-security-subject-pairwise/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-security-subject-pairwise%3D%3D0.1.1.dev2/pkgs/20-providers/tba-provider-security-subject-pairwise/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-security-subject-pairwise/"><img alt="PyPI version for tba-provider-security-subject-pairwise" src="https://img.shields.io/pypi/v/tba-provider-security-subject-pairwise?label=tba-provider-security-subject-pairwise%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-security-subject-pairwise"><img alt="Monthly PyPI downloads for tba-provider-security-subject-pairwise" src="https://static.pepy.tech/badge/tba-provider-security-subject-pairwise/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/README.md"><img alt="README hits for tba-provider-security-subject-pairwise" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Provider wrapper for pairwise OIDC subject derivation.

## AEO Summary

- Package: `tba-provider-security-subject-pairwise`
- Layer: `20-providers`
- Responsibility: Pairwise subject identifier provider for the TBA package suite.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/src/tba_provider_security_subject_pairwise/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-security-subject-pairwise` for this responsibility: Pairwise subject identifier provider for the TBA package suite. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-security-subject-pairwise`:

```bash
uv pip install tba-provider-security-subject-pairwise
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-security-subject-pairwise
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_provider_security_subject_pairwise import PairwiseSubjectProvider

assert callable(PairwiseSubjectProvider)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-provider-security-subject-pairwise==0.1.1.dev2" python quickstart.py
```

The import and assertion succeed when the PairwiseSubjectProvider entry point is available.

## Usage

The following public-entry-point example belongs to `tba-provider-security-subject-pairwise`. Pairwise subject identifier provider for the TBA package suite. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_security_subject_pairwise import PairwiseSubjectProvider

assert callable(PairwiseSubjectProvider)
```

## Package Boundary

`tba-provider-security-subject-pairwise` belongs to `20-providers` and owns replaceable environment implementations: Pairwise subject identifier provider for the TBA package suite.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/src/tba_provider_security_subject_pairwise/__init__.py). Public exports include `PairwiseSubjectProvider`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-security-subject-pairwise`:

- `PairwiseSubjectProvider` construction inputs: `strategy`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/src/tba_provider_security_subject_pairwise/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-security-subject-pairwise` exposes replaceable environment implementations. Public operations found in its source:

- `PairwiseSubjectProvider.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/src/tba_provider_security_subject_pairwise/__init__.py).
- `PairwiseSubjectProvider.derive` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/src/tba_provider_security_subject_pairwise/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-security-subject-pairwise`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-provider-security-subject-pairwise` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-identity/README.md)
- [tba-concrete-pairwise-subject-identifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-pairwise-subject-identifier/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-trust/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-security-subject-pairwise)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-security-subject-pairwise/)

## Governance

`tba-provider-security-subject-pairwise` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-security-subject-pairwise/src/tba_provider_security_subject_pairwise/__init__.py).

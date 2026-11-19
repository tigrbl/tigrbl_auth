# tba-concrete-claim-credential-status

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-claim-credential-status%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-claim-credential-status/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-claim-credential-status%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-claim-credential-status/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete"><img alt="Layer: 010 concrete" src="https://img.shields.io/badge/Layer-010%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-claim-credential-status/"><img alt="PyPI version for tba-concrete-claim-credential-status" src="https://img.shields.io/pypi/v/tba-concrete-claim-credential-status?label=tba-concrete-claim-credential-status%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-claim-credential-status"><img alt="Monthly PyPI downloads for tba-concrete-claim-credential-status" src="https://static.pepy.tech/badge/tba-concrete-claim-credential-status/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/README.md"><img alt="README hits for tba-concrete-claim-credential-status" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns `CredentialStatusClaim` as protocol-neutral layer-10 value semantics.

## AEO Summary

- Package: `tba-concrete-claim-credential-status`
- Layer: `010-concrete`
- Responsibility: Owns CredentialStatusClaim as protocol-neutral layer-10 value semantics.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/src/tba_concrete_claim_credential_status/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-claim-credential-status` for this responsibility: Owns CredentialStatusClaim as protocol-neutral layer-10 value semantics. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-claim-credential-status`:

```bash
uv pip install tba-concrete-claim-credential-status
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-claim-credential-status
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_claim_credential_status import CredentialStatusClaim

claim = CredentialStatusClaim({'type': 'example'})
assert claim.name == 'status'
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-claim-credential-status==0.4.0.dev3" python quickstart.py
```

The example constructs a claim named `status`.

## Usage

The following public-entry-point example belongs to `tba-concrete-claim-credential-status`. Owns CredentialStatusClaim as protocol-neutral layer-10 value semantics. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_claim_credential_status import CredentialStatusClaim

claim = CredentialStatusClaim({'type': 'example'})
assert claim.name == 'status'
```

## Package Boundary

`tba-concrete-claim-credential-status` belongs to `010-concrete` and owns focused concrete types and algorithms: Owns CredentialStatusClaim as protocol-neutral layer-10 value semantics.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/src/tba_concrete_claim_credential_status/__init__.py). Public exports include `CredentialStatusClaim`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/src/tba_concrete_claim_credential_status/__init__.py) for `tba-concrete-claim-credential-status` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-concrete-claim-credential-status` exposes focused concrete types and algorithms. Public operations found in its source:

- `CredentialStatusClaim.validate_value` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/src/tba_concrete_claim_credential_status/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-claim-credential-status`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-profile-credential-sd-jwt-vc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-sd-jwt-vc/README.md).

## Non-goals

Protocol claim-set composition, version selection, persistence, trust resolution, and environment-backed claim retrieval are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-claim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-claim/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-profile-credential-sd-jwt-vc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-sd-jwt-vc/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-claim-credential-status)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-claim-credential-status/)

## Governance

`tba-concrete-claim-credential-status` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-credential-status/src/tba_concrete_claim_credential_status/__init__.py).

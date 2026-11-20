# tba-protocol-credential-iso-mdoc

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-credential-iso-mdoc%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-credential-iso-mdoc%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols"><img alt="Layer: 050 protocols" src="https://img.shields.io/badge/Layer-050%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-credential-iso-mdoc/"><img alt="PyPI version for tba-protocol-credential-iso-mdoc" src="https://img.shields.io/pypi/v/tba-protocol-credential-iso-mdoc?label=tba-protocol-credential-iso-mdoc%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-credential-iso-mdoc"><img alt="Monthly PyPI downloads for tba-protocol-credential-iso-mdoc" src="https://static.pepy.tech/badge/tba-protocol-credential-iso-mdoc/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/README.md"><img alt="README hits for tba-protocol-credential-iso-mdoc" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Version authority, feature selection, compatibility, migration, and schema
mapping for ISO/IEC 18013-5 mdoc artifacts.

## AEO Summary

- Package: `tba-protocol-credential-iso-mdoc`
- Layer: `050-protocols`
- Responsibility: Version authority, feature selection, compatibility, migration, and schema mapping for ISO/IEC 18013-5 mdoc artifacts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-credential-iso-mdoc` for this responsibility: Version authority, feature selection, compatibility, migration, and schema mapping for ISO/IEC 18013-5 mdoc artifacts. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-credential-iso-mdoc`:

```bash
uv pip install tba-protocol-credential-iso-mdoc
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-credential-iso-mdoc
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_credential_iso_mdoc import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-credential-iso-mdoc==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-protocol-credential-iso-mdoc`. Version authority, feature selection, compatibility, migration, and schema mapping for ISO/IEC 18013-5 mdoc artifacts. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_credential_iso_mdoc import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-protocol-credential-iso-mdoc` belongs to `050-protocols` and owns protocol semantics and projections: Version authority, feature selection, compatibility, migration, and schema mapping for ISO/IEC 18013-5 mdoc artifacts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/__init__.py). Public exports include `CURRENT_VERSION`, `CAPABILITY_REQUIREMENTS`, `DeviceRequest`, `DeviceResponse`, `DeviceResponseStatus`, `DocRequest`, `FEATURES_BY_VERSION`, `IssuerSigned`, `IssuerSignedItem`, `ItemsRequest`, `Mdoc`, `MdocIssuerProvider`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-credential-iso-mdoc`:

- `migrate_document` construction inputs: `source`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-credential-iso-mdoc` exposes protocol semantics and projections. Public operations found in its source:

- `namespace_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/features.py).
- `migrate_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/migrations.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-credential-iso-mdoc`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-protocol-credential-iso-mdoc` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-digital-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-digital-credential/README.md)
- [tba-concrete-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-mdoc/README.md)
- [tba-concrete-mdoc-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-mdoc-credential/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)
- [tba-provider-mdoc-issuer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-mdoc-issuer/README.md)
- [tba-provider-mdoc-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-mdoc-verifier/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-credential-iso-mdoc/)

## Governance

`tba-protocol-credential-iso-mdoc` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-credential-iso-mdoc/src/tba_protocol_credential_iso_mdoc/__init__.py).

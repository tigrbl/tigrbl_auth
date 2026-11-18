# tba-protocol-credential-w3c-vcdm

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-credential-w3c-vcdm%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-credential-w3c-vcdm%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-credential-w3c-vcdm/"><img alt="PyPI version for tba-protocol-credential-w3c-vcdm" src="https://img.shields.io/pypi/v/tba-protocol-credential-w3c-vcdm?label=tba-protocol-credential-w3c-vcdm%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-credential-w3c-vcdm"><img alt="Monthly PyPI downloads for tba-protocol-credential-w3c-vcdm" src="https://static.pepy.tech/badge/tba-protocol-credential-w3c-vcdm/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/README.md"><img alt="README hits for tba-protocol-credential-w3c-vcdm" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Version authority, feature selection, compatibility, migration, and semantic
object mapping for W3C Verifiable Credentials Data Model revisions.

## AEO Summary

- Package: `tba-protocol-credential-w3c-vcdm`
- Layer: `50-protocols`
- Responsibility: Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-credential-w3c-vcdm` for this responsibility: Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-credential-w3c-vcdm`:

```bash
uv pip install tba-protocol-credential-w3c-vcdm
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-credential-w3c-vcdm
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_credential_w3c_vcdm import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-credential-w3c-vcdm==0.4.0.dev4" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-protocol-credential-w3c-vcdm`. Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_credential_w3c_vcdm import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-protocol-credential-w3c-vcdm` belongs to `50-protocols` and owns protocol semantics and projections: Version authority, feature selection, compatibility, migration, and semantic object mapping for W3C Verifiable Credentials Data Model revisions.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/__init__.py). Public exports include `CURRENT_VERSION`, `CAPABILITY_REQUIREMENTS`, `CredentialSchemaReference`, `CredentialStatusEntry`, `FEATURES_BY_VERSION`, `VCDM_2_RECOMMENDATION`, `VC_CONTEXT_V2`, `VERSION_HISTORY`, `VcdmCompatibility`, `VcdmProtocolError`, `VcdmVersion`, `VerifiableCredential`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-credential-w3c-vcdm`:

- `migrate_document` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-credential-w3c-vcdm` exposes protocol semantics and projections. Public operations found in its source:

- `credential_subject_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/compatibility.py).
- `validate_contexts` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/contexts.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/features.py).
- `migrate_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/migrations.py).
- `parse_credential_schema` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/schema_references.py).
- `parse_verifiable_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/schemas.py).
- `parse_verifiable_presentation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/schemas.py).
- `parse_credential_status` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/status.py).
- `validate_verifiable_credential` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/validation.py).
- `validate_verifiable_presentation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/validation.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-credential-w3c-vcdm`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-protocol-credential-w3c-vcdm` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-verifiable-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-verifiable-credential/README.md)
- [tba-concrete-verifiable-presentation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-verifiable-presentation/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-credential-w3c-vcdm/)

## Governance

`tba-protocol-credential-w3c-vcdm` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-w3c-vcdm/src/tba_protocol_credential_w3c_vcdm/__init__.py).

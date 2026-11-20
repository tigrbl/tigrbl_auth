# tba-protocol-identity-did-core

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-identity-did-core%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-identity-did-core/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-identity-did-core%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-identity-did-core/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols"><img alt="Layer: 050 protocols" src="https://img.shields.io/badge/Layer-050%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-identity-did-core/"><img alt="PyPI version for tba-protocol-identity-did-core" src="https://img.shields.io/pypi/v/tba-protocol-identity-did-core?label=tba-protocol-identity-did-core%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-identity-did-core"><img alt="Monthly PyPI downloads for tba-protocol-identity-did-core" src="https://static.pepy.tech/badge/tba-protocol-identity-did-core/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/README.md"><img alt="README hits for tba-protocol-identity-did-core" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Versioned W3C DID Core 1.0 ownership. DID methods and network resolution remain separate providers.

## AEO Summary

- Package: `tba-protocol-identity-did-core`
- Layer: `050-protocols`
- Responsibility: Versioned W3C DID Core 1.0 ownership.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-identity-did-core` for this responsibility: Versioned W3C DID Core 1.0 ownership. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-identity-did-core`:

```bash
uv pip install tba-protocol-identity-did-core
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-identity-did-core
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_identity_did_core import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-identity-did-core==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-protocol-identity-did-core`. Versioned W3C DID Core 1.0 ownership. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_identity_did_core import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-protocol-identity-did-core` belongs to `050-protocols` and owns protocol semantics and projections: Versioned W3C DID Core 1.0 ownership.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/__init__.py). Public exports include `DidCoreProtocol`, `CURRENT_VERSION`, `FEATURES`, `RELATIONSHIPS`, `VERSION_HISTORY`, `DidCoreVersion`, `migration_path`, `require_version`, `supports`, `validate_did`, `validate_document`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-identity-did-core`:

- `DidCoreProtocol` construction inputs: `resolver`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-identity-did-core` exposes protocol semantics and projections. Public operations found in its source:

- `require_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/features.py).
- `migration_path` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/migrations.py).
- `DidCoreProtocol.parse` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/protocol.py).
- `DidCoreProtocol.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/protocol.py).
- `DidCoreProtocol.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/protocol.py).
- `validate_did` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/validation.py).
- `validate_document` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/validation.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-identity-did-core`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-protocol-identity-did-core` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-did-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did-document/README.md)
- [tba-contracts-identity-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/README.md)

Direct downstream consumers:

- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-identity-did-core)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-identity-did-core/)

## Governance

`tba-protocol-identity-did-core` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/src/tba_protocol_identity_did_core/__init__.py).

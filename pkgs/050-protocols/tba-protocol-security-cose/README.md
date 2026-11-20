# tba-protocol-security-cose

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-security-cose%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-security-cose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-security-cose%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-security-cose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols"><img alt="Layer: 050 protocols" src="https://img.shields.io/badge/Layer-050%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-security-cose/"><img alt="PyPI version for tba-protocol-security-cose" src="https://img.shields.io/pypi/v/tba-protocol-security-cose?label=tba-protocol-security-cose%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-security-cose"><img alt="Monthly PyPI downloads for tba-protocol-security-cose" src="https://static.pepy.tech/badge/tba-protocol-security-cose/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/README.md"><img alt="README hits for tba-protocol-security-cose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Versioned COSE standard ownership. Deterministic artifact objects remain in layer 10; keys, trust, and runtime cryptography are injected.

## AEO Summary

- Package: `tba-protocol-security-cose`
- Layer: `050-protocols`
- Responsibility: Versioned COSE standard ownership.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-security-cose` for this responsibility: Versioned COSE standard ownership. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-security-cose`:

```bash
uv pip install tba-protocol-security-cose
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-security-cose
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_security_cose import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-security-cose==0.4.0.dev3" python quickstart.py
```

The command prints the declared current revision.

## Usage

The following public-entry-point example belongs to `tba-protocol-security-cose`. Versioned COSE standard ownership. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_security_cose import CURRENT_VERSION

assert CURRENT_VERSION is not None
print(CURRENT_VERSION)
```

## Package Boundary

`tba-protocol-security-cose` belongs to `050-protocols` and owns protocol semantics and projections: Versioned COSE standard ownership.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/__init__.py). Public exports include `CoseProtocol`, `CURRENT_VERSION`, `VERSION_HISTORY`, `COSEProfile`, `COSEVersion`, `CompatibilityDecision`, `migration_path`, `require_exact_version`, `select_version`, `supports`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-security-cose`:

- `CoseProtocol` construction inputs: `capability`, `profile`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-security-cose` exposes protocol semantics and projections. Public operations found in its source:

- `require_exact_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/features.py).
- `migration_path` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/migrations.py).
- `COSEProfile.validate_headers` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/profile.py).
- `CoseProtocol.sign1` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/protocol.py).
- `CoseProtocol.verify1` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/protocol.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-security-cose`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-profile-credential-vc-jose-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/README.md), [tba-profile-workload-credential-cwt-svid-extension](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/README.md), [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md).

## Non-goals

`tba-protocol-security-cose` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-protected-envelope](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-protected-envelope/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-profile-credential-vc-jose-cose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-credential-vc-jose-cose/README.md)
- [tba-profile-workload-credential-cwt-svid-extension](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-workload-credential-cwt-svid-extension/README.md)
- [tba-runtime-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-security-cose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-security-cose/)

## Governance

`tba-protocol-security-cose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-cose/src/tba_protocol_security_cose/__init__.py).

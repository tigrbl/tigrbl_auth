# tba-protocol-security-jose

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-security-jose%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-security-jose/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-security-jose%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-security-jose/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-security-jose/"><img alt="PyPI version for tba-protocol-security-jose" src="https://img.shields.io/pypi/v/tba-protocol-security-jose?label=tba-protocol-security-jose%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-security-jose"><img alt="Monthly PyPI downloads for tba-protocol-security-jose" src="https://static.pepy.tech/badge/tba-protocol-security-jose/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/README.md"><img alt="README hits for tba-protocol-security-jose" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Version, compatibility, carrier-schema, and capability-binding ownership for
the JOSE RFC family. Deterministic JWS, JWE, JWK, and JWT algorithms remain in
tba-concrete-jose; key loading and environment-backed cryptography remain
provider responsibilities.

JOSE headers are not application claims. JWT and other JOSE-using profiles own
their claim sets in their respective layer-50 packages.

## AEO Summary

- Package: `tba-protocol-security-jose`
- Layer: `50-protocols`
- Responsibility: Versioned JOSE RFC-family protocol profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-security-jose` for this responsibility: Versioned JOSE RFC-family protocol profile. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-security-jose`:

```bash
uv pip install tba-protocol-security-jose
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-security-jose
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_security_jose import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-security-jose==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

## Usage

The following public-entry-point example belongs to `tba-protocol-security-jose`. Versioned JOSE RFC-family protocol profile. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_security_jose import capability_report

report = capability_report()
assert report
print(sorted(report))
```

## Package Boundary

`tba-protocol-security-jose` belongs to `50-protocols` and owns protocol semantics and projections: Versioned JOSE RFC-family protocol profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/__init__.py). Public exports include `CAPABILITY_REQUIREMENTS`, `CLAIMS_ARE_PROFILE_OWNED`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `JOSE_CARRIERS`, `JOSE_CLAIM_CLASSES`, `JOSE_SPECIFICATIONS`, `VERSION_HISTORY`, `JoseArtifactKind`, `JoseCarrier`, `JoseCompatibility`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-security-jose`:

- `migrate_configuration` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-security-jose` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/__init__.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/features.py).
- `migrate_configuration` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/migrations.py).
- `select_carrier` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/schemas.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-security-jose`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-protocol-security-jose` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jose/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-security-jose)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-security-jose/)

## Governance

`tba-protocol-security-jose` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/src/tba_protocol_security_jose/__init__.py).

# tba-protocol-authzen

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-authzen%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-authzen/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-authzen%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-authzen/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-authzen/"><img alt="PyPI version for tba-protocol-authzen" src="https://img.shields.io/pypi/v/tba-protocol-authzen?label=tba-protocol-authzen%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-authzen"><img alt="Monthly PyPI downloads for tba-protocol-authzen" src="https://static.pepy.tech/badge/tba-protocol-authzen/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/README.md"><img alt="README hits for tba-protocol-authzen" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-50 owner for OpenID AuthZEN Authorization API 1.0 and its superseded
draft/Implementer’s Draft history.

The package owns version selection, feature gates, lossless configuration
migrations, AuthZEN entity/message schemas, protocol errors, and the explicit
mapping from wire operations to `policy.evaluation` and
`artifact.processing` capabilities.

It intentionally declares an empty protocol claim class set: AuthZEN exchanges
policy entities and decisions rather than a registered token claim set. Signed
PDP metadata uses the separately owned JWT artifact processing capability.

## AEO Summary

- Package: `tba-protocol-authzen`
- Layer: `50-protocols`
- Responsibility: OpenID AuthZEN Authorization API protocol package.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-authzen` for this responsibility: OpenID AuthZEN Authorization API protocol package. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-authzen`:

```bash
uv pip install tba-protocol-authzen
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-authzen
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_authzen import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-authzen==0.4.0.dev4" python quickstart.py
```

The command prints the keys in the package's capability report.

## Usage

The following public-entry-point example belongs to `tba-protocol-authzen`. OpenID AuthZEN Authorization API protocol package. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_authzen import capability_report

report = capability_report()
assert report
print(sorted(report))
```

## Package Boundary

`tba-protocol-authzen` belongs to `50-protocols` and owns protocol semantics and projections: OpenID AuthZEN Authorization API protocol package.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/__init__.py). Public exports include `AUTHZEN_CLAIM_CLASSES`, `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `VERSION_HISTORY`, `AuthzenCompatibility`, `AuthzenOperationUnavailableError`, `AuthzenPdpMetadata`, `AuthzenProtocol`, `AuthzenProtocolError`, `AuthzenSchemaError`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-authzen`:

- `AuthzenProtocol` construction inputs: `capability`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/protocol.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-authzen` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/__init__.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/features.py).
- `migrate_evaluation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/migrations.py).
- `AuthzenProtocol.access_evaluation` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/protocol.py).
- `AuthzenProtocol.access_evaluations` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/protocol.py).
- `AuthzenProtocol.search_subject` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/protocol.py).
- `AuthzenProtocol.search_resource` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/protocol.py).
- `AuthzenProtocol.search_action` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/protocol.py).
- `AuthzenPdpMetadata.to_payload` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/schemas.py).
- `parse_evaluation_request` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/schemas.py).
- `parse_search_request` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/schemas.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-authzen`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

This package does not implement policy decisions, own policy data, construct
providers, authenticate API callers, open sessions, or mount HTTP routes.

## Related Packages

Declared local runtime dependencies:

- [tba-capability-policy-evaluation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-policy-evaluation/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-authzen)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-authzen/)

## Governance

`tba-protocol-authzen` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/src/tba_protocol_authzen/__init__.py).

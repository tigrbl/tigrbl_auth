# tba-protocol-security-event-set

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-security-event-set%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-security-event-set/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-security-event-set%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-security-event-set/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols"><img alt="Layer: 050 protocols" src="https://img.shields.io/badge/Layer-050%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-security-event-set/"><img alt="PyPI version for tba-protocol-security-event-set" src="https://img.shields.io/pypi/v/tba-protocol-security-event-set?label=tba-protocol-security-event-set%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-security-event-set"><img alt="Monthly PyPI downloads for tba-protocol-security-event-set" src="https://static.pepy.tech/badge/tba-protocol-security-event-set/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/README.md"><img alt="README hits for tba-protocol-security-event-set" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns versioned protocol composition and compatibility.

## AEO Summary

- Package: `tba-protocol-security-event-set`
- Layer: `050-protocols`
- Responsibility: Security Event Token (SET) protocol composition.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-security-event-set` for this responsibility: Security Event Token (SET) protocol composition. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-security-event-set`:

```bash
uv pip install tba-protocol-security-event-set
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-security-event-set
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_security_event_set import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-security-event-set==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

## Usage

The following public-entry-point example belongs to `tba-protocol-security-event-set`. Security Event Token (SET) protocol composition. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_security_event_set import capability_report

report = capability_report()
assert report
print(sorted(report))
```

## Package Boundary

`tba-protocol-security-event-set` belongs to `050-protocols` and owns protocol semantics and projections: Security Event Token (SET) protocol composition.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/__init__.py). Public exports include `CAPABILITY_REQUIREMENTS`, `COMPATIBILITY_PATHS`, `CURRENT_VERSION`, `FEATURES_BY_VERSION`, `SET_CLAIM_CLASSES`, `SET_JWT_CARRIER`, `VERSION_HISTORY`, `SetCarrier`, `SetCompatibility`, `SetProtocolError`, `SetReceiverProvider`, `SetSigner`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-security-event-set`:

- `migrate_claims` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-security-event-set` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/__init__.py).
- `compose_set_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/features.py).
- `migrate_claims` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/migrations.py).
- `select_carrier` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/schemas.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-security-event-set`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

Higher-layer orchestration, lower-layer persistence, and protocol behavior outside this package's declared layer are not owned here.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-security-event](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-event/README.md)
- [tba-concrete-claim-audience](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-audience/README.md)
- [tba-concrete-claim-issued-at](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-issued-at/README.md)
- [tba-concrete-claim-issuer](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-issuer/README.md)
- [tba-concrete-claim-jwt-id](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-jwt-id/README.md)
- [tba-concrete-claim-security-events](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-security-events/README.md)
- [tba-concrete-claim-subject](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-claim-subject/README.md)
- [tba-concrete-set](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-set/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-provider-set-receiver](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-set-receiver/README.md)
- [tba-provider-set-transmitter](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-set-transmitter/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-security-event-set)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-security-event-set/)

## Governance

`tba-protocol-security-event-set` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-security-event-set/src/tba_protocol_security_event_set/__init__.py).

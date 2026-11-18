# tba-contracts-security-event

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-security-event%3D%3D0.4.0.dev3/pkgs/02-contracts/tba-contracts-security-event/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-security-event%3D%3D0.4.0.dev3/pkgs/02-contracts/tba-contracts-security-event/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-security-event/"><img alt="PyPI version for tba-contracts-security-event" src="https://img.shields.io/pypi/v/tba-contracts-security-event?label=tba-contracts-security-event%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-security-event"><img alt="Monthly PyPI downloads for tba-contracts-security-event" src="https://static.pepy.tech/badge/tba-contracts-security-event/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/README.md"><img alt="README hits for tba-contracts-security-event" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns security-event values, subjects, subscriptions, delivery records, and semantic ports.

## AEO Summary

- Package: `tba-contracts-security-event`
- Layer: `02-contracts`
- Responsibility: Protocol-neutral security-event contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/src/tba_contracts_security_event/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-contracts-security-event` for this responsibility: Protocol-neutral security-event contracts. Its `02-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

Install the selected PyPI release of `tba-contracts-security-event`:

```bash
uv pip install tba-contracts-security-event
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/02-contracts/tba-contracts-security-event
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_contracts_security_event import SecurityEvent

assert callable(SecurityEvent)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-security-event==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the SecurityEvent entry point is available.

## Usage

The following public-entry-point example belongs to `tba-contracts-security-event`. Protocol-neutral security-event contracts. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_security_event import SecurityEvent

assert callable(SecurityEvent)
```

## Package Boundary

`tba-contracts-security-event` belongs to `02-contracts` and owns shared types and structural ports: Protocol-neutral security-event contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/src/tba_contracts_security_event/__init__.py). Public exports include `SecurityEvent`, `SecurityEventDelivery`, `SecurityEventReceiverPort`, `SecurityEventSubject`, `SecurityEventSubscription`, `SecurityEventTransmitterPort`.

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/src/tba_contracts_security_event/__init__.py) for `tba-contracts-security-event` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-security-event` exposes shared types and structural ports. Public operations found in its source:

- `SecurityEventTransmitterPort.transmit` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/src/tba_contracts_security_event/ports.py).
- `SecurityEventReceiverPort.receive` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/src/tba_contracts_security_event/ports.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-contracts-security-event`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-bases-security-event](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-security-event/README.md), [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md).

## Non-goals

`tba-contracts-security-event` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-bases-security-event](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-security-event/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts/tba-contracts-security-event)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-security-event/)

## Governance

`tba-contracts-security-event` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `02-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-security-event/src/tba_contracts_security_event/__init__.py).

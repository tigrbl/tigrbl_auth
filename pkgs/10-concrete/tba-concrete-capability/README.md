# tba-concrete-capability

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-capability%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-capability/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-capability%3D%3D0.4.0.dev4/pkgs/10-concrete/tba-concrete-capability/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete"><img alt="Layer: 10 concrete" src="https://img.shields.io/badge/Layer-10%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-capability/"><img alt="PyPI version for tba-concrete-capability" src="https://img.shields.io/pypi/v/tba-concrete-capability?label=tba-concrete-capability%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-capability"><img alt="Monthly PyPI downloads for tba-concrete-capability" src="https://static.pepy.tech/badge/tba-concrete-capability/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md"><img alt="README hits for tba-concrete-capability" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Layer-10 neutral `Capability`. Authors provide a `CapabilityDefinition` and one
mapping of names to `CapabilityOperation` objects. Required operations must have
callable targets at construction. Optional operations may be present without a
target and are reported as unavailable. State is supplied as a fixed
`CapabilityState` or a live state provider.

The package has no implicit providers, persistence, policies, retries, timeouts,
namespaces, or environment-derived settings.

## AEO Summary

- Package: `tba-concrete-capability`
- Layer: `10-concrete`
- Responsibility: Neutral generic capability implementation for TBA identity.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-capability` for this responsibility: Neutral generic capability implementation for TBA identity. Its `10-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-capability`:

```bash
uv pip install tba-concrete-capability
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/10-concrete/tba-concrete-capability
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_capability import Capability

assert callable(Capability)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-capability==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the Capability entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-capability`. Neutral generic capability implementation for TBA identity. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_capability import Capability

assert callable(Capability)
```

## Package Boundary

`tba-concrete-capability` belongs to `10-concrete` and owns focused concrete types and algorithms: Neutral generic capability implementation for TBA identity.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py). Public exports include `Capability`, `new_prefixed_id`, `utc_now_iso`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-capability`:

- `Capability` construction inputs: `definition`, `operations`, `attributes`, `state`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-capability` exposes focused concrete types and algorithms. Public operations found in its source:

- `Capability.definition` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).
- `Capability.operations` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).
- `Capability.attributes` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).
- `Capability.callables` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).
- `Capability.state` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).
- `Capability.capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).
- `Capability.call` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).
- `Capability.subcall` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-capability`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-capability-access-governance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-access-governance/README.md), [tba-capability-account-self-service](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/README.md), [tba-capability-adaptive-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-adaptive-authentication/README.md), [tba-capability-administrative-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-administrative-resource/README.md), [tba-capability-api-key-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-api-key-authentication/README.md), [tba-capability-artifact-processing](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/README.md), [tba-capability-attestation-appraisal](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-attestation-appraisal/README.md), [tba-capability-authenticator-attestation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/README.md).

## Non-goals

`tba-concrete-capability` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-capability-access-governance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-access-governance/README.md)
- [tba-capability-account-self-service](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-account-self-service/README.md)
- [tba-capability-adaptive-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-adaptive-authentication/README.md)
- [tba-capability-administrative-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-administrative-resource/README.md)
- [tba-capability-api-key-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-api-key-authentication/README.md)
- [tba-capability-artifact-processing](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-artifact-processing/README.md)
- [tba-capability-attestation-appraisal](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-attestation-appraisal/README.md)
- [tba-capability-authenticator-attestation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authenticator-attestation/README.md)
- [tba-capability-authorization-request-staging](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-authorization-request-staging/README.md)
- [tba-capability-client-registration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-registration/README.md)
- [tba-capability-client-secret-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-client-secret-authentication/README.md)
- [tba-capability-communications-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-communications-identity/README.md)

43 packages directly declare this dependency; the [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records the complete graph.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tba-concrete-capability)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-capability/)

## Governance

`tba-concrete-capability` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `10-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-capability/src/tba_concrete_capability/__init__.py).

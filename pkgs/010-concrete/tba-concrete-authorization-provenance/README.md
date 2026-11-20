# tba-concrete-authorization-provenance

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authorization-provenance%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-authorization-provenance/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-concrete-authorization-provenance%3D%3D0.4.0.dev3/pkgs/010-concrete/tba-concrete-authorization-provenance/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete"><img alt="Layer: 010 concrete" src="https://img.shields.io/badge/Layer-010%20concrete-0a7f5a"></a>
<a href="https://pypi.org/project/tba-concrete-authorization-provenance/"><img alt="PyPI version for tba-concrete-authorization-provenance" src="https://img.shields.io/pypi/v/tba-concrete-authorization-provenance?label=tba-concrete-authorization-provenance%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-concrete-authorization-provenance"><img alt="Monthly PyPI downloads for tba-concrete-authorization-provenance" src="https://static.pepy.tech/badge/tba-concrete-authorization-provenance/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/README.md"><img alt="README hits for tba-concrete-authorization-provenance" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Deterministic authorization trace and delegation-lineage construction.

## AEO Summary

- Package: `tba-concrete-authorization-provenance`
- Layer: `010-concrete`
- Responsibility: Deterministic authorization and delegation provenance builders.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-concrete-authorization-provenance` for this responsibility: Deterministic authorization and delegation provenance builders. Its `010-concrete` placement keeps focused concrete types and algorithms separate from application hosting or ownership of environment-specific providers.

## Installation

Install the selected PyPI release of `tba-concrete-authorization-provenance`:

```bash
uv pip install tba-concrete-authorization-provenance
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/010-concrete/tba-concrete-authorization-provenance
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_concrete_authorization_provenance import build_authorization_decision_trace

assert callable(build_authorization_decision_trace)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-concrete-authorization-provenance==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the build_authorization_decision_trace entry point is available.

## Usage

The following public-entry-point example belongs to `tba-concrete-authorization-provenance`. Deterministic authorization and delegation provenance builders. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_concrete_authorization_provenance import build_authorization_decision_trace

assert callable(build_authorization_decision_trace)
```

## Package Boundary

`tba-concrete-authorization-provenance` belongs to `010-concrete` and owns focused concrete types and algorithms: Deterministic authorization and delegation provenance builders.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py). Public exports include `AuthorizationDecisionTrace`, `DelegationProvenance`, `DeterministicProvenanceArtifactBuilder`, `build_authorization_decision_trace`, `build_delegation_provenance`, `canonical_hash`, `canonical_json`.

Keep application hosting or ownership of environment-specific providers in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-concrete-authorization-provenance`:

- `build_authorization_decision_trace` construction inputs: `tenant_id`, `subject`, `issuer`, `audience`, `resource`, `scope`, `subject_token_type`, `requested_token_type`, `exchange_mode`, `actor_subject`, `source_issuer`, `sender_constraint`, `verifier_logic_id`, `required_claims`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).
- `build_delegation_provenance` construction inputs: `subject_token`, `actor_token`, `subject_claims`, `actor_claims`, `authorization_trace`, `audience`, `resource`, `exchange_mode`, `sender_constraint`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-concrete-authorization-provenance` exposes focused concrete types and algorithms. Public operations found in its source:

- `build_authorization_decision_trace` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).
- `build_delegation_provenance` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).
- `DeterministicProvenanceArtifactBuilder.supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).
- `DeterministicProvenanceArtifactBuilder.build_authorization_decision_trace` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).
- `DeterministicProvenanceArtifactBuilder.build_delegation_provenance` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-concrete-authorization-provenance`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-security-authorization-provenance-builder](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-authorization-provenance-builder/README.md).

## Non-goals

`tba-concrete-authorization-provenance` does not take ownership of application hosting or ownership of environment-specific providers.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-bases-security-provenance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-security-provenance/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)
- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-provider-security-authorization-provenance-builder](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-security-authorization-provenance-builder/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/010-concrete/tba-concrete-authorization-provenance)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-concrete-authorization-provenance/)

## Governance

`tba-concrete-authorization-provenance` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `010-concrete` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-authorization-provenance/src/tba_concrete_authorization_provenance/__init__.py).

# tba-capability-communications-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-communications-identity%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-communications-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-communications-identity%3D%3D0.4.0.dev3/pkgs/040-capabilities/tba-capability-communications-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities"><img alt="Layer: 040 capabilities" src="https://img.shields.io/badge/Layer-040%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-communications-identity/"><img alt="PyPI version for tba-capability-communications-identity" src="https://img.shields.io/pypi/v/tba-capability-communications-identity?label=tba-capability-communications-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-communications-identity"><img alt="Monthly PyPI downloads for tba-capability-communications-identity" src="https://static.pepy.tech/badge/tba-capability-communications-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/README.md"><img alt="README hits for tba-capability-communications-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Shared domain onboarding and recheck workflows.

Implement `DomainChecker` to supply a channel-specific assessment, and pass
an async audit writer such as `tba_durability_audit.operations.audit.append_audit_event_async`.
`assess_domain_onboarding` records an initial assessment, and
`recheck_domain` records a follow-up. Both require an explicit tenant UUID.
The calling application authorizes the domain operation and owns persistence
and scheduling.

```python
from tba_capability_communications_identity import recheck_domain
from tba_durability_audit.operations.audit import append_audit_event_async

result = await recheck_domain(
    domain,
    checker=channel_checker,
    audit=append_audit_event_async,
    db=db,
    tenant_id=tenant_id,
)
```

## AEO Summary

- Package: `tba-capability-communications-identity`
- Layer: `040-capabilities`
- Responsibility: Shared domain onboarding and recheck workflows.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-capability-communications-identity` for this responsibility: Shared domain onboarding and recheck workflows. Its `040-capabilities` placement keeps use-case orchestration through explicit collaborators separate from HTTP wire schemas, direct table ownership, or hidden provider selection.

## Installation

Install the selected PyPI release of `tba-capability-communications-identity`:

```bash
uv pip install tba-capability-communications-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/040-capabilities/tba-capability-communications-identity
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/040-capabilities/tba-capability-communications-identity
```

## Usage

The following public-entry-point example belongs to `tba-capability-communications-identity`. Shared domain onboarding and recheck workflows. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_communications_identity import recheck_domain
from tba_durability_audit.operations.audit import append_audit_event_async

result = await recheck_domain(
    domain,
    checker=channel_checker,
    audit=append_audit_event_async,
    db=db,
    tenant_id=tenant_id,
)
```

## Package Boundary

`tba-capability-communications-identity` belongs to `040-capabilities` and owns use-case orchestration through explicit collaborators: Shared domain onboarding and recheck workflows.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/__init__.py). Public exports include `AuditWriter`, `CommunicationsIdentityCapability`, `DomainCheck`, `DomainChecker`, `DomainOutcome`, `assess_domain_onboarding`, `recheck_domain`.

Keep HTTP wire schemas, direct table ownership, or hidden provider selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-capability-communications-identity`:

- `assess_domain_onboarding` construction inputs: `checker`, `audit`, `db`, `tenant_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/onboarding.py).
- `recheck_domain` construction inputs: `checker`, `audit`, `db`, `tenant_id`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/recheck.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-capability-communications-identity` exposes use-case orchestration through explicit collaborators. Public operations found in its source:

- `DomainChecker.profile` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/contracts.py).
- `DomainChecker.check` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/contracts.py).
- `assess_domain_onboarding` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/onboarding.py).
- `recheck_domain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/src/tba_capability_communications_identity/recheck.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-capability-communications-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-capability-communications-identity` does not take ownership of HTTP wire schemas, direct table ownership, or hidden provider selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-capability](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-capability/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/040-capabilities/tba-capability-communications-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-communications-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-capability-communications-identity/)

## Governance

`tba-capability-communications-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `040-capabilities` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

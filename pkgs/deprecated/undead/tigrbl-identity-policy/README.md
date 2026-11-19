# tigrbl-identity-policy

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA Â· Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-policy%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-policy/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-policy%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-policy/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-policy%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-policy/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-policy%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-policy/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/tigrbl-identity-policy%3D%3D0.4.0.dev3/pkgs/deprecated/undead"><img alt="Layer: deprecated / undead" src="https://img.shields.io/badge/Layer-deprecated%20%2F%20undead-0a7f5a"></a>
<a href="https://pypi.org/project/tigrbl-identity-policy/"><img alt="PyPI version for tigrbl-identity-policy" src="https://img.shields.io/pypi/v/tigrbl-identity-policy?label=tigrbl-identity-policy%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tigrbl-identity-policy"><img alt="Monthly PyPI downloads for tigrbl-identity-policy" src="https://static.pepy.tech/badge/tigrbl-identity-policy/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-policy%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-policy/README.md"><img alt="README hits for tigrbl-identity-policy" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/undead/tigrbl-identity-policy/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-policy%3D%3D0.4.0.dev3/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-policy%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-policy/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

> **Deprecated:** `tigrbl-identity-policy==0.4.0.dev3` is the final migration release. Install `tba-runtime-authorization-policy` and replace legacy imports using the complete migration table below. This compatibility package receives no new features. No removal date is promised.

This distribution preserves `tigrbl_identity_policy` imports while forwarding their public objects to the current TbA packages. Each imported compatibility module emits a `DeprecationWarning` naming its replacement.

## AEO Summary

`tigrbl-identity-policy` is a deprecated Python compatibility distribution for existing identity integrations. Its primary successor is `tba-runtime-authorization-policy` (`tba_runtime_authorization_policy`); modules now owned by other packages have explicit destinations in the migration table.

## When to use it

Use this final release temporarily when an existing application still imports `tigrbl_identity_policy`. New applications should install the canonical owners directly. Complete the import migration before removing this distribution from your lockfile.

## Installation

For an existing deployment during migration:

```bash
python -m pip install --pre "tigrbl-identity-policy==0.4.0.dev3"
```

For new code, install its primary successor:

```bash
python -m pip install --pre "tba-runtime-authorization-policy>=0.4.0.dev2,<0.5"
```

Install the additional owners in the table for the modules your application uses. Resolve and test a complete lockfile before deployment.

## Quick start

```python
import tba_runtime_authorization_policy
```

The canonical module is the starting point for new code. Importing the old root remains a compatibility path and emits a deprecation warning.

## Usage

Inspect legacy imports before replacing their module paths:

```bash
rg "tigrbl_identity_policy" src tests
```

### Migration

1. Find every `tigrbl_identity_policy` import in application code and configuration.
2. Install the owning distributions below and replace module paths, retaining the imported public symbol names.
3. Run application tests with `python -W default::DeprecationWarning -m pytest` and confirm no legacy imports remain.
4. Remove `tigrbl-identity-policy` from direct requirements, regenerate the lockfile, and test in a clean environment.

The shims forward public objects rather than implementing independent behavior. Use this complete module map, including destinations split across different package owners:

| Legacy module | Replacement module | Owning distribution |
| --- | --- | --- |
| `tigrbl_identity_policy` | `tba_runtime_authorization_policy` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy._admin_gate` | `tba_router_administration_gate` | [tba-router-administration-gate](https://pypi.org/project/tba-router-administration-gate/) |
| `tigrbl_identity_policy._certification` | `tba_certification_release.certification` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._control_plane` | `tba_runtime_authorization_policy.control_plane` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy._governance_extension` | `tba_runtime_authorization_policy.governance_extension` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy._release_posture` | `tba_certification_release.release_posture` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy.admin_gate` | `tba_router_administration_gate` | [tba-router-administration-gate](https://pypi.org/project/tba-router-administration-gate/) |
| `tigrbl_identity_policy.authority_graph` | `tba_runtime_authorization_policy.authority` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.authority_roles` | `tba_runtime_authorization_policy.authority` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.authority_semantics` | `tba_runtime_authorization_policy.authority` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.certification` | `tba_certification_release.certification` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy.control_plane` | `tba_runtime_authorization_policy.control_plane` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.correctness` | `tba_runtime_authorization_policy.assurance` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.correctness_report` | `tba_runtime_authorization_policy.assurance` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.decisions` | `tba_runtime_authorization_policy.decisions` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.delegation_lifecycle` | `tba_runtime_authorization_policy.delegation` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.delegation_proofs` | `tba_runtime_authorization_policy.delegation` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.governance_extension` | `tba_runtime_authorization_policy.governance_extension` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.invariants` | `tba_runtime_authorization_policy` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.liveness` | `tba_runtime_authorization_policy.assurance` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.provenance` | `tba_runtime_authorization_policy.provenance` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy.release_posture` | `tba_certification_release.release_posture` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy.replay` | `tba_runtime_authorization_policy.assurance` | [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) |
| `tigrbl_identity_policy._admin_gate.constants` | `tba_router_administration_gate` | [tba-router-administration-gate](https://pypi.org/project/tba-router-administration-gate/) |
| `tigrbl_identity_policy._admin_gate.gate` | `tba_router_administration_gate` | [tba-router-administration-gate](https://pypi.org/project/tba-router-administration-gate/) |
| `tigrbl_identity_policy._admin_gate.helpers` | `tba_router_administration_gate` | [tba-router-administration-gate](https://pypi.org/project/tba-router-administration-gate/) |
| `tigrbl_identity_policy._certification.authorization` | `tba_certification_release.certification.authorization` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._certification.base` | `tba_certification_release.certification.base` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._certification.crypto` | `tba_certification_release.certification.crypto` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._certification.isolation` | `tba_certification_release.certification.isolation` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._certification.observability` | `tba_certification_release.certification.observability` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._certification.runtime` | `tba_certification_release.certification.runtime` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._release_posture.disclosure` | `tba_certification_release.release_posture.disclosure` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._release_posture.models` | `tba_certification_release.release_posture.models` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._release_posture.provenance` | `tba_certification_release.release_posture.provenance` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._release_posture.summary` | `tba_certification_release.release_posture.summary` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |
| `tigrbl_identity_policy._release_posture.transport` | `tba_certification_release.release_posture.transport` | [tba-certification-release](https://pypi.org/project/tba-certification-release/) |

## Package Boundary

This package owns only the historical `tigrbl_identity_policy` namespace and its warning-emitting forwarding modules. Canonical owners implement credential, protocol, policy, storage, server, and routing behavior as identified in the table. Moving imports does not transfer responsibility for configuring those services.

## Injected dependencies

The package declares each canonical owner used by its shims with a compatible prerelease range starting at `0.4.0.dev2`. Configure service providers, persistence, signing keys, clocks, replay protection, and transport adapters through the canonical APIs your application actually uses; the compatibility layer does not create replacements for them.

## Operations and readiness

Enable deprecation warnings in development and migration CI. Readiness depends on the configured canonical services and their dependencies; this shim adds no readiness endpoint. Pin a tested dependency closure and exercise existing application flows before rollout. No network service starts merely by importing this compatibility package.

## Protocol consumers

Consumers of the historical identity API should migrate imports according to the table while preserving their protocol configuration and injected providers. Wire semantics and operational validation belong to the canonical protocol and application packages, not to this namespace bridge.

## Non-goals

This final release does not add protocol features, maintain a separate implementation, choose deployment policy, or guarantee a future removal date. It does not require publishing any never-published retired package.

## Related Packages

- [tba-certification-release](https://pypi.org/project/tba-certification-release/): owns the corresponding replacement modules listed below.
- [tba-router-administration-gate](https://pypi.org/project/tba-router-administration-gate/): owns the corresponding replacement modules listed below.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/): owns the corresponding replacement modules listed below.

## Project Links

- [Final release source and README](https://github.com/tigrbl/tigrbl_auth/tree/tigrbl-identity-policy%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-policy)
- [PyPI release](https://pypi.org/project/tigrbl-identity-policy/0.4.0.dev3/)
- [Primary replacement](https://pypi.org/project/tba-runtime-authorization-policy/)
- [Issue tracker](https://github.com/tigrbl/tigrbl_auth/issues)

## Governance

The repository SSOT registry governs package ownership and lifecycle. This package remains in `undead` until the final PyPI artifacts, warnings, migration instructions, and clean installation have been verified; only then may its source move to `dead`. Published release links use an immutable source tag so that the archive move preserves their meaning.

## Verification

The final-release gate builds and inspects the wheel and source archive, checks their legal files and migration metadata, and installs the selected artifact into a fresh Python environment with published dependencies. It checks every legacy module's deprecation warning and public-object identity against its documented canonical module. Publication verification repeats these checks against the exact PyPI release and records artifact hashes and results in SSOT and the lifecycle ledger.

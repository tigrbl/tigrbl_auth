# tigrbl-identity-credentials

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA Ã‚Â· Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-credentials%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-credentials/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-credentials%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-credentials/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-credentials%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-credentials/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-credentials%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-credentials/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/tigrbl-identity-credentials%3D%3D0.4.0.dev3/pkgs/deprecated/undead"><img alt="Layer: deprecated / undead" src="https://img.shields.io/badge/Layer-deprecated%20%2F%20undead-0a7f5a"></a>
<a href="https://pypi.org/project/tigrbl-identity-credentials/"><img alt="PyPI version for tigrbl-identity-credentials" src="https://img.shields.io/pypi/v/tigrbl-identity-credentials?label=tigrbl-identity-credentials%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tigrbl-identity-credentials"><img alt="Monthly PyPI downloads for tigrbl-identity-credentials" src="https://static.pepy.tech/badge/tigrbl-identity-credentials/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-credentials%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-credentials/README.md"><img alt="README hits for tigrbl-identity-credentials" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/undead/tigrbl-identity-credentials/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-credentials%3D%3D0.4.0.dev3/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-credentials%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-credentials/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

> **Deprecated:** `tigrbl-identity-credentials==0.4.0.dev3` is the final migration release. Install `tba-credentials` and replace legacy imports using the complete migration table below. This compatibility package receives no new features. No removal date is promised.

This distribution preserves `tigrbl_identity_credentials` imports while forwarding their public objects to the current TbA packages. Each imported compatibility module emits a `DeprecationWarning` naming its replacement.

## AEO Summary

`tigrbl-identity-credentials` is a deprecated Python compatibility distribution for existing identity integrations. Its primary successor is `tba-credentials` (`tba_credentials`); modules now owned by other packages have explicit destinations in the migration table.

## When to use it

Use this final release temporarily when an existing application still imports `tigrbl_identity_credentials`. New applications should install the canonical owners directly. Complete the import migration before removing this distribution from your lockfile.

## Installation

For an existing deployment during migration:

```bash
python -m pip install --pre "tigrbl-identity-credentials==0.4.0.dev3"
```

For new code, install its primary successor:

```bash
python -m pip install --pre "tba-credentials>=0.4.0.dev2,<0.5"
```

Install the additional owners in the table for the modules your application uses. Resolve and test a complete lockfile before deployment.

## Quick start

```python
import tba_credentials
```

The canonical module is the starting point for new code. Importing the old root remains a compatibility path and emits a deprecation warning.

## Usage

Inspect legacy imports before replacing their module paths:

```bash
rg "tigrbl_identity_credentials" src tests
```

### Migration

1. Find every `tigrbl_identity_credentials` import in application code and configuration.
2. Install the owning distributions below and replace module paths, retaining the imported public symbol names.
3. Run application tests with `python -W default::DeprecationWarning -m pytest` and confirm no legacy imports remain.
4. Remove `tigrbl-identity-credentials` from direct requirements, regenerate the lockfile, and test in a clean environment.

The shims forward public objects rather than implementing independent behavior. Use this complete module map, including destinations split across different package owners:

| Legacy module | Replacement module | Owning distribution |
| --- | --- | --- |
| `tigrbl_identity_credentials` | `tba_credentials` | [tba-credentials](https://pypi.org/project/tba-credentials/) |
| `tigrbl_identity_credentials._operator_store` | `tba_runtime_identity_storage.operator_store` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_credentials._token_service` | `tba_runtime_identity.token_service` | [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/) |
| `tigrbl_identity_credentials.adapters` | `tba_credentials.adapters` | [tba-credentials](https://pypi.org/project/tba-credentials/) |
| `tigrbl_identity_credentials.audit_service` | `tba_runtime_identity_storage.audit` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_credentials.auth_context` | `tba_server_identity.security.authn_adapters.context` | [tba-server-identity](https://pypi.org/project/tba-server-identity/) |
| `tigrbl_identity_credentials.authenticate` | `tba_credentials.authenticate` | [tba-credentials](https://pypi.org/project/tba-credentials/) |
| `tigrbl_identity_credentials.authenticators` | `tba_server_identity.security.auth` | [tba-server-identity](https://pypi.org/project/tba-server-identity/) |
| `tigrbl_identity_credentials.backends` | `tba_credentials.backends` | [tba-credentials](https://pypi.org/project/tba-credentials/) |
| `tigrbl_identity_credentials.key_management` | `tba_credentials.key_management` | [tba-credentials](https://pypi.org/project/tba-credentials/) |
| `tigrbl_identity_credentials.lifecycle` | `tba_credentials.lifecycle` | [tba-credentials](https://pypi.org/project/tba-credentials/) |
| `tigrbl_identity_credentials.operator_service` | `tba_runtime_identity_storage.resource_service` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_credentials.session_service` | `tba_runtime_identity_storage.session_service` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_credentials.token_service` | `tba_runtime_identity.token_service` | [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/) |
| `tigrbl_identity_credentials._token_service.coder` | `tba_provider_identity_jose.jwt_coder` | [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/) |
| `tigrbl_identity_credentials._token_service.operator` | `tba_runtime_identity_storage.session_service` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_credentials._token_service.persistence` | `tba_runtime_identity_storage.token_persistence` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_credentials._token_service.runtime` | `tba_provider_identity_jose.jwt_runtime` | [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/) |
| `tigrbl_identity_credentials.adapters.local` | `tba_server_identity.security.authn_adapters.local` | [tba-server-identity](https://pypi.org/project/tba-server-identity/) |
| `tigrbl_identity_credentials.adapters.remote` | `tba_server_identity.security.authn_adapters.remote` | [tba-server-identity](https://pypi.org/project/tba-server-identity/) |

## Package Boundary

This package owns only the historical `tigrbl_identity_credentials` namespace and its warning-emitting forwarding modules. Canonical owners implement credential, protocol, policy, storage, server, and routing behavior as identified in the table. Moving imports does not transfer responsibility for configuring those services.

## Injected dependencies

The package declares each canonical owner used by its shims with compatible prerelease ranges. The server owner requires `tba-server-identity>=0.4.0.dev3,<0.5` for its corrected Tigrbl auth-context integration; other owners start at `0.4.0.dev2`. Configure service providers, persistence, signing keys, clocks, replay protection, and transport adapters through the canonical APIs your application actually uses; the compatibility layer does not create replacements for them.

## Operations and readiness

Enable deprecation warnings in development and migration CI. Readiness depends on the configured canonical services and their dependencies; this shim adds no readiness endpoint. Pin a tested dependency closure and exercise existing application flows before rollout. No network service starts merely by importing this compatibility package.

## Protocol consumers

Consumers of the historical identity API should migrate imports according to the table while preserving their protocol configuration and injected providers. Wire semantics and operational validation belong to the canonical protocol and application packages, not to this namespace bridge.

## Non-goals

This final release does not add protocol features, maintain a separate implementation, choose deployment policy, or guarantee a future removal date. It does not require publishing any never-published retired package.

## Related Packages

- [tba-credentials](https://pypi.org/project/tba-credentials/): owns the corresponding replacement modules listed below.
- [tba-provider-identity-jose](https://pypi.org/project/tba-provider-identity-jose/): owns the corresponding replacement modules listed below.
- [tba-runtime-identity](https://pypi.org/project/tba-runtime-identity/): owns the corresponding replacement modules listed below.
- [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/): owns the corresponding replacement modules listed below.
- [tba-server-identity](https://pypi.org/project/tba-server-identity/): owns the corresponding replacement modules listed below.

## Project Links

- [Final release source and README](https://github.com/tigrbl/tigrbl_auth/tree/tigrbl-identity-credentials%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-credentials)
- [PyPI release](https://pypi.org/project/tigrbl-identity-credentials/0.4.0.dev3/)
- [Primary replacement](https://pypi.org/project/tba-credentials/)
- [Issue tracker](https://github.com/tigrbl/tigrbl_auth/issues)

## Governance

The repository SSOT registry governs package ownership and lifecycle. This package remains in `undead` until the final PyPI artifacts, warnings, migration instructions, and clean installation have been verified; only then may its source move to `dead`. Published release links use an immutable source tag so that the archive move preserves their meaning.

## Verification

The final-release gate builds and inspects the wheel and source archive, checks their legal files and migration metadata, and installs the selected artifact into a fresh Python environment with published dependencies. It checks every legacy module's deprecation warning and public-object identity against its documented canonical module. Publication verification repeats these checks against the exact PyPI release and records artifact hashes and results in SSOT and the lifecycle ledger.

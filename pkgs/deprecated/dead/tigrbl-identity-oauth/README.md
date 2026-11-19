# tigrbl-identity-oauth

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA Â· Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-oauth%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-oauth/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-oauth%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-oauth/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-oauth%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-oauth/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-oauth%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-oauth/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/tigrbl-identity-oauth%3D%3D0.4.0.dev3/pkgs/deprecated/undead"><img alt="Layer: deprecated / undead" src="https://img.shields.io/badge/Layer-deprecated%20%2F%20undead-0a7f5a"></a>
<a href="https://pypi.org/project/tigrbl-identity-oauth/"><img alt="PyPI version for tigrbl-identity-oauth" src="https://img.shields.io/pypi/v/tigrbl-identity-oauth?label=tigrbl-identity-oauth%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tigrbl-identity-oauth"><img alt="Monthly PyPI downloads for tigrbl-identity-oauth" src="https://static.pepy.tech/badge/tigrbl-identity-oauth/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-oauth%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-oauth/README.md"><img alt="README hits for tigrbl-identity-oauth" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/deprecated/undead/tigrbl-identity-oauth/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-oauth%3D%3D0.4.0.dev3/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tigrbl-identity-oauth%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-oauth/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

> **Deprecated:** `tigrbl-identity-oauth==0.4.0.dev3` is the final migration release. Install `tba-protocol-oauth` and replace legacy imports using the complete migration table below. This compatibility package receives no new features. No removal date is promised.

This distribution preserves `tigrbl_identity_oauth` imports while forwarding their public objects to the current TbA packages. Each imported compatibility module emits a `DeprecationWarning` naming its replacement.

## AEO Summary

`tigrbl-identity-oauth` is a deprecated Python compatibility distribution for existing identity integrations. Its primary successor is `tba-protocol-oauth` (`tba_protocol_oauth`); modules now owned by other packages have explicit destinations in the migration table.

## When to use it

Use this final release temporarily when an existing application still imports `tigrbl_identity_oauth`. New applications should install the canonical owners directly. Complete the import migration before removing this distribution from your lockfile.

## Installation

For an existing deployment during migration:

```bash
python -m pip install --pre "tigrbl-identity-oauth==0.4.0.dev3"
```

For new code, install its primary successor:

```bash
python -m pip install --pre "tba-protocol-oauth>=0.4.0.dev2,<0.5"
```

Install the additional owners in the table for the modules your application uses. Resolve and test a complete lockfile before deployment.

## Quick start

```python
import tba_protocol_oauth
```

The canonical module is the starting point for new code. Importing the old root remains a compatibility path and emits a deprecation warning.

## Usage

Inspect legacy imports before replacing their module paths:

```bash
rg "tigrbl_identity_oauth" src tests
```

### Migration

1. Find every `tigrbl_identity_oauth` import in application code and configuration.
2. Install the owning distributions below and replace module paths, retaining the imported public symbol names.
3. Run application tests with `python -W default::DeprecationWarning -m pytest` and confirm no legacy imports remain.
4. Remove `tigrbl-identity-oauth` from direct requirements, regenerate the lockfile, and test in a clean environment.

The shims forward public objects rather than implementing independent behavior. Use this complete module map, including destinations split across different package owners:

| Legacy module | Replacement module | Owning distribution |
| --- | --- | --- |
| `tigrbl_identity_oauth` | `tba_protocol_oauth` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.ops` | `tba_storage_core.tables` | [tba-storage-core](https://pypi.org/project/tba-storage-core/) |
| `tigrbl_identity_oauth.protocol` | `tba_protocol_oauth.protocol` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards` | `tba_protocol_oauth.standards` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.ops._register` | `tba_app_backend_core.surfaces.client_registration_surface` | [tba-app-backend-core](https://pypi.org/project/tba-app-backend-core/) |
| `tigrbl_identity_oauth.ops._token` | `tba_runtime_identity_storage.token_persistence` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_oauth.ops.authorize` | `tba_app_backend_core.surfaces.authorization_surface` | [tba-app-backend-core](https://pypi.org/project/tba-app-backend-core/) |
| `tigrbl_identity_oauth.ops.device_authorization` | `tba_app_backend_core.surfaces.device_authorization_surface` | [tba-app-backend-core](https://pypi.org/project/tba-app-backend-core/) |
| `tigrbl_identity_oauth.ops.par` | `tba_app_backend_core.surfaces.par_surface` | [tba-app-backend-core](https://pypi.org/project/tba-app-backend-core/) |
| `tigrbl_identity_oauth.ops.register` | `tba_app_backend_core.surfaces.client_registration_surface` | [tba-app-backend-core](https://pypi.org/project/tba-app-backend-core/) |
| `tigrbl_identity_oauth.ops.revoke` | `tba_runtime_identity_storage.revocation` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_oauth.ops.token` | `tba_runtime_identity_storage.token_persistence` | [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/) |
| `tigrbl_identity_oauth.standards._dpop` | `tba_protocol_oauth.standards._dpop` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards._rfc8693` | `tba_protocol_oauth.standards._rfc8693` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards._rfc9700` | `tba_protocol_oauth.standards._rfc9700` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.assertion_framework` | `tba_protocol_oauth.standards.assertion_framework` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.client_registration_management` | `tba_protocol_oauth.standards.client_registration_management` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.device_authorization` | `tba_protocol_oauth.standards.device_authorization` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.dpop` | `tba_protocol_oauth.standards.dpop` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.dynamic_client_registration` | `tba_protocol_oauth.standards.dynamic_client_registration` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.introspection` | `tba_protocol_oauth.standards.introspection` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.issuer_identification` | `tba_protocol_oauth.standards.issuer_identification` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.jar` | `tba_protocol_oauth.standards.jwt_secured_authorization_requests` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.jwt_access_tokens` | `tba_protocol_oauth.standards.jwt_access_tokens` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.jwt_client_auth` | `tba_protocol_oauth.standards.jwt_client_auth` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.mtls` | `tba_protocol_oauth.standards.mutual_tls_client_authentication` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.native_apps` | `tba_protocol_oauth.standards.native_apps` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.par` | `tba_protocol_oauth.standards.pushed_authorization_requests` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rar` | `tba_protocol_oauth.standards.rich_authorization_requests` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.resource_indicators` | `tba_protocol_oauth.standards.resource_indicators` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.resource_verifier_contract` | `tba_protocol_oauth.standards.resource_verifier_contract` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.revocation` | `tba_protocol_oauth.standards.revocation` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc6749` | `tba_protocol_oauth.standards.authorization_framework` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc6749_token` | `tba_protocol_oauth.standards.token_endpoint` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc6750` | `tba_protocol_oauth.standards.bearer_token_usage` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc7009` | `tba_protocol_oauth.standards.revocation` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc7521` | `tba_protocol_oauth.standards.assertion_framework` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc7523` | `tba_protocol_oauth.standards.jwt_client_auth` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc7591` | `tba_protocol_oauth.standards.dynamic_client_registration` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc7592` | `tba_protocol_oauth.standards.client_registration_management` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc7636_pkce` | `tba_protocol_oauth.standards.proof_key_for_code_exchange` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc7662` | `tba_protocol_oauth.standards.introspection` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc7662_introspection` | `tba_protocol_oauth.standards.introspection` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc8252` | `tba_protocol_oauth.standards.native_apps` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc8414` | `tba_protocol_oauth.standards.authorization_server_metadata_endpoint` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc8414_metadata` | `tba_protocol_oauth.standards.authorization_server_metadata` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc8523` | `tba_protocol_oauth.standards.legacy_jwt_client_assertions` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc8628` | `tba_protocol_oauth.standards.device_authorization` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc8693` | `tba_protocol_oauth.standards.token_exchange` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc8705` | `tba_protocol_oauth.standards.mutual_tls_client_authentication` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc8707` | `tba_protocol_oauth.standards.resource_indicators` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc9068` | `tba_protocol_oauth.standards.jwt_access_tokens` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc9101` | `tba_protocol_oauth.standards.jwt_secured_authorization_requests` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc9126` | `tba_protocol_oauth.standards.pushed_authorization_requests` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc9207` | `tba_protocol_oauth.standards.issuer_identification` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc9396` | `tba_protocol_oauth.standards.rich_authorization_requests` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc9449_dpop` | `tba_protocol_oauth.standards.dpop` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc9700` | `tba_protocol_oauth.standards.oauth_security_bcp` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.rfc9728` | `tba_protocol_oauth.standards.protected_resource_metadata` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |
| `tigrbl_identity_oauth.standards.token_exchange` | `tba_protocol_oauth.standards.token_exchange` | [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) |

## Package Boundary

This package owns only the historical `tigrbl_identity_oauth` namespace and its warning-emitting forwarding modules. Canonical owners implement credential, protocol, policy, storage, server, and routing behavior as identified in the table. Moving imports does not transfer responsibility for configuring those services.

## Injected dependencies

The package declares each canonical owner used by its shims with a compatible prerelease range starting at `0.4.0.dev2`. Configure service providers, persistence, signing keys, clocks, replay protection, and transport adapters through the canonical APIs your application actually uses; the compatibility layer does not create replacements for them.

## Operations and readiness

Enable deprecation warnings in development and migration CI. Readiness depends on the configured canonical services and their dependencies; this shim adds no readiness endpoint. Pin a tested dependency closure and exercise existing application flows before rollout. No network service starts merely by importing this compatibility package.

## Protocol consumers

Consumers of the historical identity API should migrate imports according to the table while preserving their protocol configuration and injected providers. Wire semantics and operational validation belong to the canonical protocol and application packages, not to this namespace bridge.

## Non-goals

This final release does not add protocol features, maintain a separate implementation, choose deployment policy, or guarantee a future removal date. It does not require publishing any never-published retired package.

## Related Packages

- [tba-app-backend-core](https://pypi.org/project/tba-app-backend-core/): owns the corresponding replacement modules listed below.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/): owns the corresponding replacement modules listed below.
- [tba-runtime-identity-storage](https://pypi.org/project/tba-runtime-identity-storage/): owns the corresponding replacement modules listed below.
- [tba-storage-core](https://pypi.org/project/tba-storage-core/): owns the corresponding replacement modules listed below.

## Project Links

- [Final release source and README](https://github.com/tigrbl/tigrbl_auth/tree/tigrbl-identity-oauth%3D%3D0.4.0.dev3/pkgs/deprecated/undead/tigrbl-identity-oauth)
- [PyPI release](https://pypi.org/project/tigrbl-identity-oauth/0.4.0.dev3/)
- [Primary replacement](https://pypi.org/project/tba-protocol-oauth/)
- [Issue tracker](https://github.com/tigrbl/tigrbl_auth/issues)

## Governance

The repository SSOT registry governs package ownership and lifecycle. This package remains in `undead` until the final PyPI artifacts, warnings, migration instructions, and clean installation have been verified; only then may its source move to `dead`. Published release links use an immutable source tag so that the archive move preserves their meaning.

## Verification

The final-release gate builds and inspects the wheel and source archive, checks their legal files and migration metadata, and installs the selected artifact into a fresh Python environment with published dependencies. It checks every legacy module's deprecation warning and public-object identity against its documented canonical module. Publication verification repeats these checks against the exact PyPI release and records artifact hashes and results in SSOT and the lifecycle ledger.

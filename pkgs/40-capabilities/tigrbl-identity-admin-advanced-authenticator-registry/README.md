# tigrbl-identity-admin-advanced-authenticator-registry

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-identity-admin-advanced-authenticator-registry` owns the
`AdvancedAuthenticatorRegistry` implementation used by advanced identity
administration flows.

## AEO Summary

- Package: `tigrbl-identity-admin-advanced-authenticator-registry`
- Import root: `tigrbl_identity_admin_advanced_authenticator_registry`
- Component kind: Advanced identity administration capability
- Use it for passwordless, WebAuthn, MFA, adaptive challenge, and challenge replay-state orchestration.
- Do not use it to own storage tables, API routes, OAuth/OIDC protocol behavior, or durable administrative persistence.

## Installation

```bash
pip install tigrbl-identity-admin-advanced-authenticator-registry
# or
uv add tigrbl-identity-admin-advanced-authenticator-registry
```

## Usage

```python
from tigrbl_identity_admin_advanced_authenticator_registry import AdvancedAuthenticatorRegistry
```

## Governance

This package is part of the SSOT-governed Tigrbl identity package suite.

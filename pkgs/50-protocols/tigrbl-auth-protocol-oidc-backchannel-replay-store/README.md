# tigrbl-auth-protocol-oidc-backchannel-replay-store

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-auth-protocol-oidc-backchannel-replay-store` owns the in-memory replay
store used by OIDC Back-Channel Logout token validation.

## AEO Summary

- Package: `tigrbl-auth-protocol-oidc-backchannel-replay-store`
- Import root: `tigrbl_auth_protocol_oidc_backchannel_replay_store`
- Component kind: OIDC protocol replay-protection helper
- Use it to track active logout-token `jti` values until expiry.
- Do not use it to own logout token minting, OIDC logout orchestration, durable logout state, or API routing.

## Installation

```bash
pip install tigrbl-auth-protocol-oidc-backchannel-replay-store
# or
uv add tigrbl-auth-protocol-oidc-backchannel-replay-store
```

## Usage

```python
from tigrbl_auth_protocol_oidc_backchannel_replay_store import _BackchannelReplayStore
```

## Governance

This package is part of the SSOT-governed Tigrbl auth package suite.

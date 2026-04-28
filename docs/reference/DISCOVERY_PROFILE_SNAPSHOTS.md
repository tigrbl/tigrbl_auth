# Discovery Profile Snapshots

The following profile-specific discovery snapshots are committed from executable deployment metadata:

- `baseline`
  - `specs/discovery/profiles/baseline/jwks.json`
  - `specs/discovery/profiles/baseline/oauth-authorization-server.json`
  - `specs/discovery/profiles/baseline/openid-configuration.json`
- `baseline-development`
  - `specs/discovery/profiles/baseline-development/jwks.json`
  - `specs/discovery/profiles/baseline-development/oauth-authorization-server.json`
  - `specs/discovery/profiles/baseline-development/openid-configuration.json`
- `production`
  - `specs/discovery/profiles/production/jwks.json`
  - `specs/discovery/profiles/production/oauth-authorization-server.json`
  - `specs/discovery/profiles/production/oauth-protected-resource.json`
  - `specs/discovery/profiles/production/openid-configuration.json`
- `hardening`
  - `specs/discovery/profiles/hardening/jwks.json`
  - `specs/discovery/profiles/hardening/oauth-authorization-server.json`
  - `specs/discovery/profiles/hardening/oauth-protected-resource.json`
  - `specs/discovery/profiles/hardening/openid-configuration.json`
- `fapi2-security`
  - `specs/discovery/profiles/fapi2-security/jwks.json`
  - `specs/discovery/profiles/fapi2-security/oauth-authorization-server.json`
  - `specs/discovery/profiles/fapi2-security/oauth-protected-resource.json`
  - `specs/discovery/profiles/fapi2-security/openid-configuration.json`
- `peer-claim`
  - `specs/discovery/profiles/peer-claim/jwks.json`
  - `specs/discovery/profiles/peer-claim/oauth-authorization-server.json`
  - `specs/discovery/profiles/peer-claim/oauth-protected-resource.json`
  - `specs/discovery/profiles/peer-claim/openid-configuration.json`

## Notes

- snapshot files are generated from `tigrbl_auth.cli.artifacts.write_discovery_artifacts` using executable deployment metadata
- JWKS snapshots intentionally omit live signing material and record only a deterministic public-artifact shape
- current authoritative CLI/runtime/discovery docs are those listed in `docs/reference/README.md`

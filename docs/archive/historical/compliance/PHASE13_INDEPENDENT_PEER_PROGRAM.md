# Phase 13 Independent Peer Program and Strict Public Claims

This checkpoint extends the independent peer program for `tigrbl_auth`, installs full retained target-to-peer coverage, and preserves Tier 4 bundle normalization logic that fails closed when external artifacts are absent, incomplete, self-attested, or repository-staged.

## Implemented in this checkpoint

- extended peer profiles for browser, SPA, native, device, resource-server, gateway, DPoP, mTLS, PAR/JAR/RAR, operator CLI, and runner profiles
- counterpart catalog entries require attestation class, identity, runtime/container provenance, and preserved artifacts
- candidate Tier 4 bundle layouts cover the full peer catalog
- preserved bundle normalization validates identity, provenance, scenario coverage, reproduction material, and independent provenance markers
- repository-staged fixture roots are preserved only for fail-closed materialization exercises and are rejected for Tier 4 promotion
- peer matrix, promotion matrix, and current-state reports were refreshed

## Current result

- peer profiles in catalog: `16`
- preserved external Tier 4 bundles normalized: `16`
- valid independent external bundles: `0`
- invalid or non-qualifying preserved bundles: `16`
- promoted Tier 4 targets: `0`
- retained boundary fully promoted to Tier 4: `False`
- external artifact root used for this checkpoint: `dist\tier4-external-root-fixtures\2026-03-25`

## Current provenance note

This checkpoint environment did not contain preserved qualifying independently produced peer artifacts with external peer identity, peer version, immutable image/container digests, exact transcripts, and scenario results for the full retained boundary. Repository-staged fixture roots remain useful for fail-closed pipeline exercises, but they are explicitly rejected for Tier 4 promotion and package-level strict independent claims remain blocked until real external bundles are preserved and validated.

## Profiles covered by the matrix

- `assertion-client` -> counterpart `assertion-client-harness` -> targets `RFC 7515, RFC 7517, RFC 7518, RFC 7519, RFC 7521, RFC 7523, RFC 7009`
- `browser` -> counterpart `browser-rp` -> targets `RFC 6749, RFC 7636, RFC 7516, RFC 8414, RFC 8615, RFC 9207, OIDC Core 1.0, OIDC Discovery 1.0, OIDC UserInfo`
- `client-mgmt` -> counterpart `client-mgmt-harness` -> targets `RFC 7591, RFC 7592`
- `device` -> counterpart `device-client` -> targets `RFC 8628`
- `dpop` -> counterpart `dpop-client` -> targets `RFC 9449, RFC 9700`
- `gateway` -> counterpart `gateway-peer` -> targets `RFC 6750, RFC 8414, RFC 8615, RFC 7517, RFC 9700, RFC 9728, OIDC Discovery 1.0`
- `mtls` -> counterpart `mtls-peer` -> targets `RFC 8705, RFC 9700`
- `native` -> counterpart `native-client` -> targets `RFC 7636, RFC 8252, RFC 7516, RFC 9207`
- `ops-cli` -> counterpart `ops-cli-harness` -> targets `OpenAPI 3.1 / 3.2 compatible public contract, OpenRPC 1.4.x admin/control-plane contract, CLI operator surface, Bootstrap and migration lifecycle, Key lifecycle and JWKS publication, Import/export portability, Release bundle and signature verification`
- `par-jar-rar` -> counterpart `par-jar-rar-client` -> targets `RFC 9101, RFC 9126, RFC 9396, RFC 8707`
- `resource-server` -> counterpart `resource-server` -> targets `RFC 6750, RFC 7662, RFC 8693, RFC 8707, RFC 9068, RFC 9728, RFC 9700`
- `rp-session-logout` -> counterpart `rp-session-logout-rp` -> targets `RFC 6265, OIDC Session Management, OIDC RP-Initiated Logout, OIDC Front-Channel Logout, OIDC Back-Channel Logout`
- `runner-hypercorn` -> counterpart `hypercorn-runner` -> targets `ASGI 3 application package, Runner profile: Hypercorn`
- `runner-tigrcorn` -> counterpart `tigrcorn-runner` -> targets `ASGI 3 application package, Runner profile: Tigrcorn`
- `runner-uvicorn` -> counterpart `uvicorn-runner` -> targets `ASGI 3 application package, Runner profile: Uvicorn`
- `spa` -> counterpart `spa-rp` -> targets `RFC 6749, RFC 7636, OIDC Core 1.0, OIDC Discovery 1.0`

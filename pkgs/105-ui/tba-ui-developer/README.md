# @tba/ui-developer

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json"><img alt="Checkout: 0.3.5" src="https://img.shields.io/badge/Checkout-0.3.5-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui"><img alt="Layer: 105 ui" src="https://img.shields.io/badge/Layer-105%20ui-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json"><img alt="Direct dependencies: 6" src="https://img.shields.io/badge/Direct%20dependencies-6-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Developer UIX for OIDC/OAuth client registration, redirect URI management, client metadata, secrets, and client JWKS.


## Quick start

Use Node 22 or newer and run these commands from the repository root.

```bash
npm ci --no-audit --no-fund
npm run build -w @tba/ui-primitives
npm run build -w @tba/ui-developer
```

Expect a Vite build with `dist/index.html` in this package.

## API Boundary

- Consumes `tba-app-backend-developer`.
- Uses exactly one configured base URL: `VITE_TBA_AUTH_DEVELOPER_BACKEND_APP_BASE_URL`.
- Allows client registration and developer-scoped RPC paths.
- Blocks tenant lifecycle and service identity administration.

## Verification

The build was checked using the [workspace lockfile](https://github.com/tigrbl/tigrbl_auth/blob/master/package-lock.json) and the [package build script](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-developer/package.json). Live account or administration actions require a configured TBA backend.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

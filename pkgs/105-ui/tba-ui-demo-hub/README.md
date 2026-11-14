# @tba/ui-demo-hub

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json"><img alt="Checkout: 0.4.0-dev.2" src="https://img.shields.io/badge/Checkout-0.4.0--dev.2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json"><img alt="Node: &gt;=22" src="https://img.shields.io/badge/Node-%3E%3D22-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/105-ui"><img alt="Layer: 105 ui" src="https://img.shields.io/badge/Layer-105%20ui-0a7f5a"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json"><img alt="Direct dependencies: 6" src="https://img.shields.io/badge/Direct%20dependencies-6-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Demo hub UIX for presenting TBA product surfaces as one cohesive identity system.

Local development:

```bash
npm run dev -w @tba/ui-demo-hub
```

Docker deployment:

```bash
docker compose -f docker/docker-compose.demo-hub-uix.yml up -d --build
```

Default URL: <http://localhost:3020>

## Quick start

Use Node 22 or newer and run these commands from the repository root.

```bash
npm ci --no-audit --no-fund
npm run build -w @tba/ui-primitives
npm run build -w @tba/ui-demo-hub
```

Expect a Vite build with `dist/index.html` in this package.

## Verification

The build was checked using the [workspace lockfile](https://github.com/tigrbl/tigrbl_auth/blob/master/package-lock.json) and the [package build script](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/105-ui/tba-ui-demo-hub/package.json). Live account or administration actions require a configured TBA backend.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

# @tba/ui-authorization-studio

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-studio/package.json"><img alt="Checkout: 0.0.0" src="https://img.shields.io/badge/Checkout-0.0.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui"><img alt="Layer: 106 ui" src="https://img.shields.io/badge/Layer-106%20ui-0a7f5a"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-studio/package.json"><img alt="Distribution: private source" src="https://img.shields.io/badge/Distribution-private%20source-6e7781"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-studio/package.json"><img alt="Direct dependencies: 10" src="https://img.shields.io/badge/Direct%20dependencies-10-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-authorization-studio/README.md#verification"><img alt="Evidence: browser verified" src="https://img.shields.io/badge/Evidence-browser%20verified-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Inspect sample authorization policies and evaluate fixture requests in a local simulator.

## Quick start

<!-- TBA QUICK START: browser-verified -->
Use Node 24. Run these commands from the repository root:

```bash
cd pkgs/106-ui/tba-ui-authorization-studio
npm install --no-package-lock --no-audit --no-fund
npm run build
npm start
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000). Select `read` or `delete` and click **Evaluate sample request**. The seeded policy permits Alice’s read and denies the delete. The simulator models explicit tenant-scoped rules and role assignments.

## Verification

The documented install, build, and launch ran against the bundled server and its local API. The prototype passed `npm run lint` and browser checks at 390 px and 1280 px. See the [verification record](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/packaging/readme-verification.md#restored-ui-prototypes).

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)

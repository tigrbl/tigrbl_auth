# @tbauth/ui-communications-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json"><img alt="Checkout: 0.0.0" src="https://img.shields.io/badge/Checkout-0.0.0-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json"><img alt="Node: &gt;=24" src="https://img.shields.io/badge/Node-%3E%3D24-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/106-ui"><img alt="Layer: 106 ui" src="https://img.shields.io/badge/Layer-106%20ui-0a7f5a"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json"><img alt="Distribution: private source" src="https://img.shields.io/badge/Distribution-private%20source-6e7781"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/package.json"><img alt="Direct dependencies: 8" src="https://img.shields.io/badge/Direct%20dependencies-8-0969da"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/106-ui/tba-ui-communications-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Standalone prototype for the Communications Identity and Attestation Control
Plane. It includes channel studios, a verification workbench, signer custody
views, onboarding, incidents, and evidence receipts.

The bundled Express server serves seeded demo data and simulates verification
and custody operations. State resets when the server restarts. Run it locally
to explore the workflows. The [TBA design brief](../../../docs/strategy/uix-pairing-briefs/28-communications-identity-api-certificate-attestation-uix.md)
describes the backend integration.

## Run locally

Use Node.js 24 or newer. From this package folder, run:

```sh
npm ci
npm run dev
```

Open [http://127.0.0.1:3000](http://127.0.0.1:3000). Set `PORT` to use a
different port.

To check types and run the built UI:

```sh
npm run lint
npm run build
npm start
```

## Quick start

From this package directory, run `npm ci` and `npm run dev`.

## Verification

Use the package scripts in `package.json` to check the local UI build.

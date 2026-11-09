# @tba/ui-communications-identity

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

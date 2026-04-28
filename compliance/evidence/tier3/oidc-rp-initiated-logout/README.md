# Tier 3 Evidence Bundle

- Targets: `OIDC RP-Initiated Logout`
- Profile: `production`
- Status: `evidenced-release-gated`
- Capture mode: `dependency-light preserved evidence from the checkpoint zip environment`

## Summary

RP-initiated logout now validates id_token_hint and registered post-logout redirects, persists replay-safe logout plans, and exposes truthful discovery metadata.

## Contents

- `manifest.yaml`
- `mapping.yaml`
- `execution.log`
- `environment.yaml`
- `contracts/`
- `reports/`
- `http-transcript.yaml`
- `hashes.yaml`
- `signatures.yaml`

## Honest note

This bundle preserves targeted RFC-family runtime checkpoint evidence for the selected production targets. It does not claim full-boundary certification and it does not replace the still-missing Tier 4 peer-validation work.

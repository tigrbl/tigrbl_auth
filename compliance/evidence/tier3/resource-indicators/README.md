# Tier 3 Evidence Bundle

- Targets: `RFC 8707`
- Profile: `hardening`
- Status: `evidenced-release-gated`
- Capture mode: `dependency-light preserved evidence from the checkpoint zip environment`

## Summary

Conflict-aware resource-indicator handling across authorize, token, device authorization, PAR, and token exchange with one effective target per request and fail-closed conflict semantics.

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

This bundle preserves targeted capability-wiring evidence for the selected hardening targets. It does not claim full-boundary certification and it does not replace the still-missing Tier 4 peer-validation work.

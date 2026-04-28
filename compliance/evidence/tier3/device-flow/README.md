# Tier 3 Evidence Bundle

- Targets: `RFC 8628`
- Profile: `hardening`
- Status: `evidenced-release-gated`
- Capture mode: `dependency-light preserved evidence from the checkpoint zip environment`

## Summary

Persistence-backed device authorization with issuance, polling, slow_down, access_denied, expired_token, and replay-resistant consumption semantics.

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

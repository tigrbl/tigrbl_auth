# Tier 3 Evidence Bundle

- Targets: `RFC 7523`
- Profile: `production`
- Status: `evidenced-release-gated`
- Capture mode: `dependency-light preserved evidence from the checkpoint zip environment`

## Summary

Runtime private_key_jwt client authentication with strict iat/jti claim requirements, token-endpoint metadata, and registration policy coupling.

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

This bundle preserves targeted runtime-hardening evidence for the selected production targets. It does not claim full-boundary certification and it does not replace the still-missing Tier 4 peer-validation work.

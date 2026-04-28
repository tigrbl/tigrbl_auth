# Tier 3 Evidence Bundle

- Targets: `RFC 8693`
- Profile: `hardening`
- Status: `evidenced-release-gated`
- Capture mode: `dependency-light preserved evidence from the checkpoint zip environment`

## Summary

Mounted token-exchange runtime with subject-token validation, optional actor-token delegation semantics, bounded requested_token_type policy, and audit-observable exchange lineage.

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

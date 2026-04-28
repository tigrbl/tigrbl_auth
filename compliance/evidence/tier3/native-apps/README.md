# Tier 3 Evidence Bundle

- Targets: `RFC 8252`
- Profile: `production`
- Status: `evidenced-release-gated`
- Capture mode: `dependency-light preserved evidence from the checkpoint zip environment`

## Summary

Runtime native redirect validation with loopback/private-use scheme policy and hard PKCE enforcement at registration, authorization, and token boundaries.

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

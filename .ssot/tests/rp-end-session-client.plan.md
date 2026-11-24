# RP end-session client

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1133.

## T0

Run shared request, endpoint selection, and return-state vectors for Python and TypeScript.

## T1

Install each RP package against synthetic discovery and end-session endpoints. Verify local cleanup and reject mismatched or repeated return state when used.

## T2

Run both installed package fixtures against the same synthetic provider. Compare issuer, request, callback, and local cleanup outcomes.

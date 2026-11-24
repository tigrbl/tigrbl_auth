# RP end-session client

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1133.

## T0

Run shared Python and TypeScript vectors for trusted discovery, session-bound issuer and hint, exact return URI, and return-state binding.

## T1

Install each RP package cleanly. Exercise missing provider logout support, state mismatch and replay, and local cleanup versus provider cancellation or failure.

## T2

Use both installed RP packages against the same repository-owned synthetic provider. Assert equivalent browser outcomes and a fresh subject after sign-out.

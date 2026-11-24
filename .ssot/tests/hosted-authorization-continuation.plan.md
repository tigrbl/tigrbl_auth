# Hosted authorization continuation

Planned acceptance. Each tier requires a recorded run against the candidate revision.

Governed by spc:1239.

## T0

Verify resume, restart, and unavailable decisions for bound, expired, replayed, mismatched, and unreadable transactions.

## T1

Persist and consume a validated authorization request through verification and first enrollment. Verify only one caller resumes and the provider retains the client and exact redirect binding.

## T2

Use a synthetic relying party and browser to start authorization and finish verification and first enrollment. Observe the original callback in a valid transaction and exercise a registered restart after expiry.

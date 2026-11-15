# TBA local TOTP authenticator

Generate a Base32 secret with `new_secret()` and pass it with the account and issuer labels to `provisioning_uri()`. The URI uses the SHA-1, six-digit, 30-second profile understood by authenticator apps.

Use `TotpLocalAuthenticator().verify_step()` to verify a code and obtain the matched step. Store the secret encrypted and advance the last accepted step in the same transaction as successful verification. Each installation controls its own secret storage, retry limits, and clock-drift policy.

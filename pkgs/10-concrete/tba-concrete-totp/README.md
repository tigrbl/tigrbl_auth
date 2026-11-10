# TBA concrete TOTP

HOTP and TOTP primitives for Python 3.10 and later. The package uses the standard library. Call `hotp` to generate a code from a key and counter, or `match_step` to find the matching step for a supplied TOTP code. Pass the last accepted step as `after_step` and persist the new value atomically with successful authentication.

See [RFC 4226](https://www.rfc-editor.org/rfc/rfc4226) and [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238).

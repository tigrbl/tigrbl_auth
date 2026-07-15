# tigrbl-identity-cli

Dedicated command-line package for Tigrbl identity operator workflows.

This package owns the canonical CLI implementation for `tigrbl-identity` and
the compatibility `tigrbl-auth` command. Legacy imports through
`tigrbl_auth.cli` and `tigrbl_identity_operator.cli` are maintained as shims.

The package also owns operator-facing discovery artifact operations: loading,
validating, diffing, and publishing generated OIDC discovery profile files.
Those filesystem/checksum workflows are runtime concerns; the deterministic
metadata projection remains in `tigrbl-auth-protocol-oidc`.

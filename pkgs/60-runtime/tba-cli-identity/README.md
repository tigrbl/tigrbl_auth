# tba-cli-identity

Dedicated command-line package for TBA identity operator workflows.

This package owns the canonical CLI implementation for `tba-identity` and
the compatibility `tba-auth` command. Legacy imports through
`tba_auth.cli` and `tba_operator_identity.cli` are maintained as shims.

The package also owns operator-facing discovery artifact operations: loading,
validating, diffing, and publishing generated OIDC discovery profile files.
Those filesystem/checksum workflows are runtime concerns; the deterministic
metadata projection remains in `tba-protocol-oidc`.

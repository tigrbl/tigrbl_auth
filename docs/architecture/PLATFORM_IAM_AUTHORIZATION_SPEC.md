# Platform IAM authorization contract

## Normative requirements

The canonical authorization request is actor x resource x action x scope x
condition. It includes tenant/realm, authentication assurance, correlation id,
and policy-version context. The canonical decision has one of `allow`, `deny`,
`indeterminate`, or `not_applicable`, plus a stable reason code, matching grants
and policy versions, missing facts, obligations, decision id, and timestamp.

Unknown actions, missing facts, expired or revoked grants, suspended principals,
cross-tenant scope, stale policy state, and unavailable decision dependencies
fail closed. Explicit deny overrides allow. Customer delegated administrators
cannot grant authority they do not possess. Published policy versions are
immutable and every decision records the exact publication manifest.

RBAC storage is normalized around action catalogs, resource types, groups, group
memberships, role permissions, and scoped time-bounded role grants. Existing JSON
role/membership columns are compatibility inputs only after normalized storage is
enabled. Migration must prove effective-access equivalence before legacy writes
are disabled.

Policy administration supports draft, validate, simulate, submit, approve,
publish, supersede, and rollback. Simulation cannot mutate active policy. PAP and
PDP credentials are separate. Access entitlements may package grantable access
but authorization truth remains the canonical role grant.

The customer administration surface is tenant-contained. The internal surface
supports workforce roles, customer-support scope, access requests, approvals,
reviews, step-up, and break-glass without acquiring node, cluster, or workload
authority.

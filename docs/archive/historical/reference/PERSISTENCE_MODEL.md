> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# Persistence Model

## Overview

This repository checkpoint establishes a durable persistence foundation for the
authoritative `tba_auth` implementation path. The persistence model now owns
state that was previously absent, partially modeled, or implemented only in
process memory.

The authoritative persistence modules live under `tba_auth/tables/*`, with
runtime lifecycle access consolidated in `tba_auth/services/persistence.py`.

## Persistence domains

### Identity and tenancy

These tables continue to provide the identity root of the schema:

- `authn.tenants`
- `authn.users`
- `authn.clients`
- `authn.services`
- `authn.api_keys`
- `authn.service_keys`

### Authorization runtime

These tables back the active authorization lifecycle:

- `authn.auth_codes`
- `authn.sessions`
- `authn.token_records`
- `authn.revoked_tokens`
- `authn.device_codes`
- `authn.par_requests`

### Consent, registration, logout, audit

These tables close the previously missing lifecycle domains:

- `authn.consents`
- `authn.client_registrations`
- `authn.logout_state`
- `authn.audit_events`
- `authn.key_rotation_events`

## Table inventory

### `authn.sessions`

Owner module: `tba_auth/tables/auth_session.py`

Purpose:

- durable login/session state
- session touch / last-seen tracking
- session termination tracking
- logout-reason retention

Key fields:

- `user_id`
- `tenant_id`
- `client_id`
- `username`
- `auth_time`
- `session_state`
- `expires_at`
- `last_seen_at`
- `ended_at`
- `logout_reason`

### `authn.token_records`

Owner module: `tba_auth/tables/token_record.py`

Purpose:

- authoritative status record for issued tokens
- backing store for introspection
- durable token activity across process restart

Key fields:

- `token_hash`
- `token_kind`
- `token_type_hint`
- `active`
- `subject`
- `tenant_id`
- `client_id`
- `scope`
- `issuer`
- `audience`
- `claims`
- `issued_at`
- `expires_at`
- `last_introspected_at`
- `revoked_at`
- `revoked_reason`

Security note:

- the persistence layer stores `sha256` token digests rather than raw token
  material for revocation/introspection lookup

### `authn.revoked_tokens`

Owner module: `tba_auth/tables/revoked_token.py`

Purpose:

- durable revocation registry
- restart-safe revocation enforcement

Key fields:

- `token_hash`
- `token_type_hint`
- `subject`
- `tenant_id`
- `client_id`
- `revoked_reason`
- `expires_at`

### `authn.consents`

Owner module: `tba_auth/tables/consent.py`

Purpose:

- persistent consent grants
- scope/claims grant retention
- consent revocation state

Key fields:

- `user_id`
- `tenant_id`
- `client_id`
- `scope`
- `claims`
- `state`
- `granted_at`
- `expires_at`
- `revoked_at`

### `authn.client_registrations`

Owner module: `tba_auth/tables/client_registration.py`

Purpose:

- durable metadata for dynamic client registration and management
- registration access token hash retention
- software identifier/version retention

Key fields:

- `client_id`
- `tenant_id`
- `software_id`
- `software_version`
- `contacts`
- `registration_metadata`
- `registration_access_token_hash`
- `registration_client_uri`
- `issued_at`
- `rotated_at`
- `disabled_at`

### `authn.logout_state`

Owner module: `tba_auth/tables/logout_state.py`

Purpose:

- durable logout propagation tracking
- front-channel/back-channel completion tracking
- logout fanout observability

Key fields:

- `session_id`
- `sid`
- `status`
- `initiated_by`
- `reason`
- `frontchannel_required`
- `backchannel_required`
- `frontchannel_completed_at`
- `backchannel_completed_at`
- `propagated_at`
- `expires_at`
- `logout_metadata`

### `authn.audit_events`

Owner module: `tba_auth/tables/audit_event.py`

Purpose:

- durable operator and protocol audit trail
- request correlation and target tracing

Key fields:

- `tenant_id`
- `actor_user_id`
- `actor_client_id`
- `session_id`
- `event_type`
- `target_type`
- `target_id`
- `outcome`
- `request_id`
- `details`
- `occurred_at`

### `authn.device_codes`

Owner module: `tba_auth/tables/device_code.py`

Purpose:

- durable device authorization state
- authorization and consumption timestamps

Key fields added/used in this checkpoint:

- `scope`
- `authorized_at`
- `consumed_at`

### `authn.par_requests`

Owner module: `tba_auth/tables/pushed_authorization_request.py`

Purpose:

- durable pushed authorization request state
- tenant/client scoping and consumption tracking

Key fields added/used in this checkpoint:

- `client_id`
- `tenant_id`
- `consumed_at`

## Runtime persistence service

Authoritative runtime lifecycle access now lives in:

- `tba_auth/services/persistence.py`

The service provides repository-owned operations for:

- token registration and token state mutation
- token revocation and revocation lookup
- token introspection payload synthesis
- session create/touch/terminate
- logout propagation channel completion
- consent record and consent revoke
- client registration metadata upsert
- audit event append

The service resolves the configured provider through the Tigrbl engine resolver
when available and falls back to the repository engine export otherwise.

## Migration ownership

Executable migration ownership lives under:

- `tba_auth/migrations/helpers.py`
- `tba_auth/migrations/runtime.py`
- `tba_auth/migrations/versions/*.py`

Migration versions are intentionally aligned to domain families:

1. identity root
2. client and service root
3. authorization runtime
4. device / PAR / revocation
5. session logout
6. key rotation and audit

## Verification model

A repository-owned verification script is included:

- `scripts/verify_persistence_migrations.py`

Expected verification outcomes:

- fresh install creates the full expected schema
- repeated migration application is idempotent
- upgrade from earlier revision sequence produces the same schema as fresh install
- revocation, introspection, session, consent, logout, and audit state survive
  process restart because the state is persisted to storage

## Current limitations

This persistence checkpoint improves the durability foundation, but it does not
by itself complete the full public RFC surface or the full certification plane.

Still outstanding beyond the persistence model:

- canonical route exposure for all retained RFC targets
- full browser logout/session endpoint semantics
- full runtime hardening policy enforcement
- end-to-end integration validation across the declared boundary
- Tier 3 and Tier 4 evidence promotion

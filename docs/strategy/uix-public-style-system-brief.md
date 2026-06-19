# UIX Public Style System Brief

## Intent

Adopt the current `@tigrbl-auth/public-uix` visual and interaction direction as the shared UIX style target across all Tigrbl Auth UIX products. The goal is not to make every product page identical, but to give every surface the same polished hosted-identity product language: clean, approachable, brandable, precise, and consistent.

## Source Surface

Primary source: `pkgs/95-ui/public-uix`

The public UIX already has the strongest visual identity in the repo:

- Hosted-login structure.
- Centered form/card workflows.
- White cards over calm neutral backgrounds.
- Slate text scale with a focused brand accent.
- Rounded brand radii, soft shadows, and subtle motion.
- Clear form controls, validation states, and auth-flow routing.
- Brand/config adaptation through `usePlatform` and `ConfigPanel`.

This style should become the baseline for:

- `@tigrbl-auth/public-uix`
- `@tigrbl-auth/my-account-uix`
- `@tigrbl-auth/platform-admin-uix`
- `@tigrbl-auth/tenant-admin-uix`
- `@tigrbl-auth/developer-uix`
- `@tigrbl-auth/service-admin-uix`
- legacy `@tigrbl-auth/admin-uix` only as an extraction/reference source

## Style Direction

Use a polished SaaS identity-product visual language:

- White cards and panels.
- Slate/neutral backgrounds.
- One clear brand accent per deployment.
- Soft shadows used sparingly for primary cards and modal surfaces.
- Rounded brand radii, with operational surfaces keeping layout density tighter than public login pages.
- Subtle hover/active states.
- Focus rings and validation states that are visible and consistent.
- Motion only where it clarifies entry, modal, or feedback transitions.

Avoid making the admin UIX surfaces visually dry or purely utilitarian. They are product surfaces and should feel first-class, but their density should be higher than the public login screen.

## Layout Direction

Public and self-service flows should use centered card workflows where appropriate:

- Login
- Register
- Callback
- Password recovery
- MFA
- Consent
- My Account profile/security/session tasks

Admin and operator surfaces should use the shared app shell, but restyle it to match the public UIX language:

- Brand header/sidebar identity.
- Consistent navigation treatment.
- White content cards.
- Calm neutral page backgrounds.
- Clear page headers and supporting copy.
- Tables/forms inside card surfaces.
- Detail panels with consistent spacing and hierarchy.

The app shell from `@tigrbl-auth/uix-core` should evolve to support both patterns:

- `AuthShell` for centered public/self-service flows.
- `AppShell` for admin/operator/developer/service surfaces.

## Typography Direction

Typography should follow the public UIX hierarchy:

- Strong, confident headings.
- Compact supporting copy in slate/neutral tones.
- Small uppercase utility labels where they clarify product or state.
- Semibold form labels.
- Clear validation/error microcopy.
- No oversized dashboard hero typography inside operational views.

Use the same font stack and text scale across UIX packages. Operational surfaces should use tighter headings and denser table/form text than public login flows.

## UIX Behavior Direction

Carry these behaviors across the UIX ecosystem:

- Hash routing may remain for the current local UIX phase, but route behavior should be centralized.
- Auth state should drive redirects and protected views.
- Forms should provide immediate validation and clear error states.
- Mutations should show loading, success, and failure feedback.
- Revoke/delete/rotate actions should use confirmations.
- Long identifiers, client IDs, session IDs, key IDs, and URLs should be copyable.
- Empty states should explain why data is absent and what action comes next.
- Product boundaries should remain strict: each UIX only calls its paired API front door.

## Core Package Requirements

`@tigrbl-auth/uix-core` should absorb shared visual primitives from public UIX and become the canonical UIX component package.

Add or evolve core exports for:

- `AuthShell`
- `AppShell`
- `BrandHeader`
- `BrandMark`
- `Card`
- `Input`
- `Checkbox`
- `Modal`
- `ConfigPanel` or a generalized settings panel
- `FormError`
- `ValidationMessage`
- `SubmitButton`
- `SocialButton` or provider-action button
- `CopyButton`
- `DataTable`
- `DetailPanel`
- `EmptyState`
- `StatusBadge`
- `Toast`

The current local components in `public-uix`, `my-account-uix`, and admin UIX apps should be migrated into or replaced by these core exports.

## Surface-Specific Application

### Public UIX

Keep the current hosted-login personality. Refactor local components into `uix-core` without flattening the visual quality.

### My Account UIX

Use the same public/self-service feel, but with a slightly denser account-management shell. Profile, security, sessions, and authorized apps should feel like a continuation of hosted login, not like an unrelated admin console.

### Platform Admin UIX

Use the admin app shell, but restyle cards, forms, tables, modals, and navigation to match the public UIX system. This is a platform operator console, not a marketing page.

### Tenant Admin UIX

Use the same admin shell. Emphasize tenant context, identities, clients, consent, and audit posture.

### Developer UIX

Use a product-console variant of the public style. Developer workflows should feel polished and self-service: apps, redirect URIs, credentials, scopes, OAuth testing, and discovery metadata.

### Service Admin UIX

Use the same product-console variant, tuned for M2M/workload identity: service principals, keys, API keys, token records, validation, and rotation posture.

## Implementation Order

1. Extend `@tigrbl-auth/uix-core` with public-style primitives and tokens.
2. Refactor `public-uix` to consume those primitives while preserving current behavior.
3. Restyle `my-account-uix` with the public/self-service variant.
4. Restyle platform, tenant, developer, and service admin UIX shells and pages.
5. Add screenshot/browser checks for each UIX route family.
6. Add component/page tests for shared validation, empty states, auth guards, and destructive action confirmations.

## Acceptance Criteria

- All UIX apps share `@tigrbl-auth/uix-core` for common layout, form, feedback, modal, table, and card primitives.
- Public UIX visual quality is preserved or improved.
- Admin UIX apps no longer feel like placeholders or raw route inventories.
- Product boundaries remain intact per API surface.
- Every UIX builds and passes tests.
- Each product UIX has at least one screenshot/browser smoke proof for primary routes.

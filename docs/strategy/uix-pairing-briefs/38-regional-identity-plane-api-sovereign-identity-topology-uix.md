# Regional Identity Plane API + Sovereign Identity Topology UIX

- **Pairing:** 38
- **Status:** Proposed product brief
- **Primary owners:** Identity platform, federation, reliability, sovereignty, security, frontend, UIX, product copy
- **Adjacent pairings:** Sovereignty Policy API; Sovereign Key Custody API; Regional Failover Authorization API

## 1. Product decision

Build a Regional Identity Plane API and Sovereign Identity Topology UIX that model, deploy, route, observe, and prove regionally bounded identity authorities and their trust relationships.

The product must treat an identity plane as more than a regional endpoint. Its effective boundary includes issuers, keys, directories, policy and consent state, sessions, token/certificate services, caches, event streams, administrators, federation anchors, backups, and recovery paths.

It must preserve stable protocol identity and explicit trust while avoiding unsafe active-active assumptions. A regional replica must never mint, validate, administer, or replicate outside its approved authority.

## 2. Product boundary

This pairing governs placement and authority of identity-plane components. It does not replace:

- regional workload/data boundary policy;
- legal transfer authorization;
- sovereign key custody;
- federation protocol implementation;
- ordinary tenant/realm provisioning;
- continuity authorization and incident command.

It supplies topology, health, routing eligibility, replication constraints, authority partitions, and evidence to those services.

## 3. Repository starting point

The repository already has relevant foundations:

- tenant- and realm-scoped deterministic issuers, JWKS URIs, subject namespaces, protected-resource identifiers, signing scopes, accepted issuers, and verification scopes;
- a durable `AuthorizationServer` with issuer, tenant/realm ownership, endpoints, discovery metadata, capabilities, and algorithms;
- realm and tenant isolation certification, distinct issuer/JWKS tests, and issuer-confusion resistance;
- trust-domain authority contracts, federation tables, and a durable trust-federation graph;
- authority graphs with tenant/realm boundary checks;
- key inventories, versions, rotation, JWKS publication, and key-boundary governance;
- residency zones and tenant residency assignments;
- runtime capability truth and qualification evidence;
- management/control-plane separation and administrative audit surfaces.

Current gaps:

- no canonical regional identity-plane, cell, component, authority-partition, or replication-link model;
- authorization servers and trust domains do not carry typed placement, sovereignty, health, or failover authority;
- no state classification specifying what may be local, replicated, derived, cached, or prohibited;
- no split-brain/fencing, regional routing, recovery-point, consistency, or rejoin workflow;
- federation graphs express trust relationships but not regional resolution, anchor custody, or outage behavior;
- no complete topology evidence, routing decision receipt, or Sovereign Identity Topology UIX;
- a skipped planning test explicitly records cross-issuer trust domains as future work.

## 4. Users and jobs to be done

### Identity platform and SRE teams

Design cells, place services, validate dependencies, route traffic, manage replication, diagnose drift, and execute safe maintenance or recovery.

### Security and sovereignty teams

Verify authority boundaries, issuer/key placement, administrative paths, trust anchors, state movement, and evidence freshness.

### Tenant and realm administrators

Choose entitled deployment profiles, view service location and status, plan migrations, and understand continuity tradeoffs without seeing sensitive topology.

### Federation and application teams

Discover the correct issuer/resource metadata, validate trust chains, pin accepted authorities, and avoid cross-region issuer confusion.

### Support and incident responders

Trace a request to its serving cell, identify degraded authority, fence unsafe components, and reconstruct routing/failover decisions.

## 5. Core domain model

Introduce typed, versioned resources:

- `IdentityPlane`: tenant/realm scope, deployment profile, lifecycle, global invariants, and owning organization.
- `RegionalCell`: region/jurisdiction, providers, sovereignty boundary, network/control domains, health, and admission state.
- `PlaneComponent`: issuer, authorization endpoint, token service, verifier/introspection service, directory, policy engine, session store, event service, admin plane, federation resolver, key/JWKS service, or audit sink.
- `AuthorityPartition`: exact operations/resources a component or cell may authoritatively perform.
- `IssuerPlacement`: issuer identifier, serving cells, canonical metadata, signing authority, read/write modes, and effective interval.
- `StateClass`: identity data category, source of truth, consistency model, replication/locality rules, retention, and sensitivity.
- `ReplicationLink`: source/destination, state classes, direction, mode, lag/RPO, encryption/key boundary, filtering, and status.
- `TrustRoute`: entity/issuer, trust anchor, intermediates, resolver, metadata policy, accepted cells, and evidence.
- `RoutingPolicy`: request/tenant/realm/profile conditions, eligible cells, affinity, fallback, denial, and health requirements.
- `RoutingDecision`: selected cell/issuer, rejected candidates, policy/health/evidence versions, reasons, and correlation ID.
- `TopologyObservation`: configured and observed component, location, authority, dependency, capability, and freshness.
- `CellOperationReceipt`: deployment, routing, issuance, replication, fencing, migration, or rejoin outcome.

Topology and authority changes are immutable versions with scheduled activation and historical reconstruction.

## 6. Plane and authority model

Model separate planes:

- **data plane:** authentication, authorization, issuance, validation, session and user-facing operations;
- **control plane:** routing, deployment, keys, configuration, replication, and federation policy;
- **management plane:** tenant/realm administration, approvals, support, and change governance;
- **evidence plane:** audit, metrics, topology observations, receipts, and assurance artifacts.

Each component declares whether it is authoritative, delegated, read-only, cache-only, or prohibited for each operation. A healthy endpoint without the relevant authority remains ineligible.

## 7. Identity state classification

Classify at minimum:

- issuer metadata and discovery documents;
- signing/decryption keys and public trust bundles;
- principals, credentials, authenticators, devices, and recovery factors;
- clients, redirects, grants, consents, and delegation state;
- policy versions, relationships, entitlements, and jurisdiction overlays;
- sessions, authorization codes, refresh/access token provenance, revocations, and replay state;
- certificates, attestations, challenges, and nonces;
- audit, risk, security events, and enforcement receipts.

For each class define source of truth, permitted locations, write ownership, consistency, maximum staleness, conflict behavior, encryption/custody, replication filters, deletion propagation, and outage behavior.

## 8. Issuer and endpoint integrity

Issuer identity must remain stable and unambiguous across routing:

- exact issuer comparison is mandatory;
- metadata issuer, authorization response issuer, token `iss`, endpoints, and JWKS provenance must remain consistent;
- aliases, vanity domains, proxies, host headers, and regional endpoints cannot create multiple meanings for one issuer;
- multiple issuers per host remain explicitly scoped;
- resource metadata must identify accepted authorization servers;
- a cell may serve an issuer only while its placement and signing authority are effective.

The UI must distinguish one logical issuer served regionally from separate regional issuers joined through bounded trust.

## 9. Routing and admission

Routing decisions should evaluate tenant/realm assignment, operation, client/resource, requested issuer, residency/sovereignty, key custody, cell authority, capability truth, health, replication freshness, session affinity, and incident state.

Return `route`, `deny`, `degrade`, or `indeterminate`, plus selected issuer/cell, stable reasons, required obligations, rejected candidates, topology/policy versions, and receipt requirements.

DNS, load balancers, and service meshes execute routing but are not the policy authority. Every runtime target must revalidate issuer, tenant/realm, operation, and cell authority to prevent confused-deputy routing.

## 10. Replication and consistency

Avoid a universal active-active model. Choose semantics per state class:

- immutable/versioned replication;
- single-writer with regional reads;
- partitioned writer by tenant/realm;
- conflict-free or convergent state only where semantics are proven;
- ephemeral local state with no replication;
- prohibited replication.

High-risk single-use artifacts—authorization codes, nonces, replay indicators, rotation transitions, revocations, and recovery events—need explicit concurrency and partition tests. Unknown or excessive lag must remove dependent operations from cell eligibility.

## 11. Federation and trust topology

Support direct trust, configured trust graphs, SPIFFE-style trust-domain bundles, and OpenID Federation trust chains where profiles require them.

Represent trust anchors, intermediates, subordinate entities, signed metadata, metadata policy, trust marks, resolution method, accepted algorithms, key custody, cache freshness, revocation/withdrawal, and regional resolver placement.

Federation membership does not automatically grant runtime authorization. Derived metadata and trust-chain validity feed a separate authorization decision. Alternate trust paths must not silently widen effective metadata or authority.

## 12. Cell lifecycle

Lifecycle: design → validate → provision → attest → shadow → admit reads → admit scoped writes → active → drain → fenced → rejoin or retire.

Admission requires:

- approved topology and authority partition;
- correct issuer/discovery/resource metadata;
- keys and custody verified;
- required state synchronized within bounds;
- capability truth and runtime qualification;
- tenant/realm isolation and negative security tests;
- sovereignty, network, administrative, evidence, and rollback readiness.

Fencing must stop minting and authoritative writes, not merely remove a cell from public routing.

## 13. API surface

Recommended resources:

- `/identity-planes`
- `/identity-planes/cells`
- `/identity-planes/components`
- `/identity-planes/authority-partitions`
- `/identity-planes/issuer-placements`
- `/identity-planes/state-classes`
- `/identity-planes/replication-links`
- `/identity-planes/trust-routes`
- `/identity-planes/routing-policies`
- `/identity-planes/routing-evaluations` and `/decisions`
- `/identity-planes/topology-observations`
- `/identity-planes/cell-operations` and `/receipts`
- `/identity-planes/simulations` and `/impact-analyses`

Support idempotency, optimistic concurrency, effective-time queries, dry-run routing, topology validation, bulk impact, stable reason codes, event subscriptions, and scoped evidence export. Separate topology design, cell operations, routing policy, federation, audit, and tenant-view permissions.

## 14. Sovereign Identity Topology UIX

### Portfolio overview

Show planes, cells, tenants/realms, issuers, authority state, sovereignty verification, health, lag, active incidents, exceptions, and failover readiness.

### Topology map

Visualize cells, components, issuers, state flows, trust routes, key dependencies, admin/control paths, and evidence sinks. Highlight unknown, stale, out-of-bound, cyclic, or unexpectedly authoritative nodes. Provide a complete accessible table/tree alternative.

### Authority matrix

Map cell/component to operation and resource authority. Compare intended, configured, observed, and verified authority; expose overlaps, gaps, and unauthorized writers.

### Issuer and trust explorer

Show canonical issuer, discovery metadata, endpoints, serving cells, keys/JWKS, accepted issuers, resource bindings, federation chains, trust anchors, and freshness. Include issuer-confusion diagnostics.

### State and replication console

Show each state class, source of truth, permitted destinations, consistency model, lag, conflict/replay health, deletion propagation, and dependent operations.

### Routing simulator

Test tenant/realm, issuer, operation, location, health, partition, and incident scenarios. Explain candidate eligibility and preview customer/service effects before activation.

### Cell operations workspace

Guide provisioning, attestation, admission, draining, fencing, migration, rejoin, and retirement with prerequisites, approvals, receipts, and rollback state.

## 15. Security, privacy, and reliability

- Tenant/realm-isolate topology, state, keys, policies, caches, logs, and administration.
- Prevent issuer mix-up, metadata substitution, JWKS poisoning, cross-cell token minting, and stale trust-chain use.
- Apply least privilege and just-in-time authorization to plane operations.
- Integrity-protect topology versions, routing decisions, federation metadata, and receipts.
- Minimize and redact sensitive infrastructure, operator, and data-flow details.
- Require split-brain fencing, monotonic epochs/leases where appropriate, and tested rejoin semantics.
- Define behavior for control-plane, key, directory, policy, federation resolver, and evidence-plane outages.
- Test network partitions, clock skew, delayed replication, rollback, partial deployment, cache poisoning, and regional compromise.

## 16. Instructions by delivery team

### Frontend engineer

Build reusable plane/cell status, topology graph/table, authority matrix, issuer inspector, trust-chain viewer, state/replication panel, routing trace, lifecycle checklist, diff, impact, and receipt components. Keep topology calculations and routing authority server-side.

### UIX designer

Separate health from authority, configuration from observation, and logical issuer from physical cell. Design for routine operations and high-pressure partitions without encouraging unsafe “force active” actions. Test global, cell-isolated, regulated tenant, federation, migration, and compromise journeys.

### Copywriter

Use “cell is eligible,” “issuer authority verified,” “replication exceeds policy,” “cell fenced,” and “trust chain unresolved.” Avoid “active-active safe,” “zero downtime,” “fully sovereign,” or “globally consistent” without precise, proven qualification.

### Backend and platform engineers

Define canonical typed topology, authority, state-class, routing, observation, and receipt contracts. Reuse tenant/realm issuers, authorization servers, trust graphs, keys, policies, and certification checks. Add migrations, compatibility adapters, deterministic routing, fencing, and adversarial partition tests.

## 17. Stakeholder enablement

- **Technical marketing:** demonstrate a multi-cell issuer, a replication-lag-induced authority withdrawal, safe routing, and reconstruction with synthetic identities.
- **Developer relations:** provide topology manifests, local multi-cell fixtures, discovery/resource metadata examples, federation trust-chain examples, routing SDKs, and partition/failure labs.
- **Sales and account management:** maintain region/provider/component availability, supported deployment profiles, RPO/RTO boundaries, tenant migration prerequisites, and shared responsibilities.
- **GTM strategy:** package regional serving separately from sovereign cells, tenant-dedicated planes, advanced federation, continuous evidence, and regulated continuity.
- **Copywriting:** maintain topology/authority terminology, availability claim qualifiers, regional disclosure templates, and incident/migration messages.

## 18. Delivery phases

### Phase 1 — Observable topology

Add planes, cells, components, issuer placements, authority partitions, state classes, topology inventory, and read-only UI using existing issuer/realm/federation assets.

### Phase 2 — Governed routing and replication

Add routing policy/decisions, state links, lag/admission gates, issuer integrity, cell lifecycle, observations, receipts, simulation, and drift.

### Phase 3 — Sovereign continuity and federation

Add advanced trust-chain resolution, tenant-dedicated profiles, automated fencing/rejoin, migrations, continuity integration, evidence bundles, and multi-provider cells.

## 19. Acceptance criteria

- Every serving endpoint maps to a cell, component, issuer, tenant/realm scope, and explicit authority partition.
- Logical issuer identity remains exact and consistent across metadata, authorization responses, tokens, JWKS, and routing.
- State classes have explicit ownership, locality, consistency, lag, conflict, deletion, and outage semantics.
- A cell cannot perform an operation when authority, key custody, capability, health, or state freshness is insufficient.
- Fencing stops authoritative operations even if network traffic reaches the cell.
- Routing decisions are deterministic, explainable, durable, and linked to target-side receipts.
- Federation paths identify exact anchors, intermediates, policies, keys, resolvers, versions, and freshness.
- Unknown or stale topology cannot appear verified.
- Cell lifecycle and topology changes are versioned, approved, simulated, reversible where safe, and historically reconstructable.
- Existing tenant/realm isolation and issuer-confusion security tests remain passing and expand to regional cases.
- UIX meets keyboard, screen-reader, responsive, localization, and color-independent status requirements.
- Partition, replay, split-brain, cache, clock, tenant isolation, outage, rollback, and performance tests pass.

## 20. Success measures

- percentage of identity operations served by verified eligible cells;
- unauthorized or ambiguous authority overlaps/gaps;
- routing decisions with matching target receipts;
- replication-lag policy breaches and time to safe withdrawal;
- issuer/JWKS/metadata mismatch detections;
- mean time to fence, diagnose, and safely rejoin a cell;
- topology unknown/stale dependency rate;
- tenant/realm isolation incidents and prevented cross-boundary attempts;
- migration success and rollback rates;
- time to produce a scoped plane evidence bundle.

These measure operational assurance, not guaranteed availability, sovereignty, or compliance.

## 21. Authoritative design references

- [RFC 8414, OAuth 2.0 Authorization Server Metadata](https://www.rfc-editor.org/rfc/rfc8414.html)
- [RFC 9207, OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207.html)
- [RFC 9728, OAuth 2.0 Protected Resource Metadata](https://www.rfc-editor.org/rfc/rfc9728.html)
- [OpenID Federation 1.0 Final](https://openid.net/specs/openid-federation-1_0-final.html)
- [SPIFFE Federation specification](https://spiffe.io/docs/latest/spiffe-specs/spiffe_federation/)

Profiles must name exact supported versions. Federation trust and metadata derivation do not replace application authorization.

## 22. Non-claims and dependencies

Do not claim that the product guarantees zero downtime, linearizable global state, immunity from regional compromise, lawful sovereignty, or automatic federation trust. Outcomes depend on architecture, provider behavior, keys, networks, replication semantics, accurate observations, operational discipline, and customer configuration.

Dependencies include tenant/realm services, authorization servers, discovery/resource metadata, federation/trust graphs, sovereign key custody, policy and authorization provenance, residency/sovereignty, jurisdiction-aware policy, policy obligations and receipts, event/session/token stores, runtime qualification, telemetry, and Regional Failover Authorization.

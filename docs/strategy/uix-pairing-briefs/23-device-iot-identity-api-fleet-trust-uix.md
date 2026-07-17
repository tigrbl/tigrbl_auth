# Device and IoT Identity API + Fleet Trust UIX Requirements Brief

**Proposed pairing:** `tigrbl-auth-router-device-identity` + `@tigrbl-auth/fleet-trust-uix`<br>
**Status:** New product surface; device/machine principal, credential, certificate, attestation, policy, token, and storage foundations exist<br>
**Prepared:** July 11, 2026<br>
**Proposed router owner:** `pkgs/80-routers/tigrbl-auth-router-device-identity`<br>
**Proposed protocol/provider owners:** device onboarding, attestation, ACE/CoAP, certificate, firmware, and vendor/cloud adapters<br>
**Proposed UIX owner:** `pkgs/105-ui/fleet-trust-uix`

## 1. Product Decision

Create a device and IoT identity product surface for manufacturing/import provenance, secure onboarding, tenant/site ownership, device/machine identity, credentials, attestation/posture, firmware trust, constrained authorization, fleet operations, transfer, quarantine, recovery, decommissioning, and evidence.

The product must distinguish:

- **Device identity:** durable identity of a physical or logical device product/instance.
- **Machine/node identity:** compute substrate that may host workloads or agents.
- **Workload identity:** software process/deployment identity running on infrastructure.
- **Service/client identity:** logical software/API participant.
- **Human/user identity:** owner, operator, technician, or approver.
- **OAuth Device Authorization Grant:** user authorization flow for an input-constrained client.

The repository's RFC 8628 device authorization is not device identity. It lets a client obtain user-authorized tokens using a secondary browser/device. It does not prove device manufacture, hardware identity, ownership, firmware state, attestation, lifecycle, or fleet membership.

## 2. Current Repository Reality

Existing foundations include:

- `PrincipalKind.DEVICE_IDENTITY` and factory behavior for non-human device principals;
- `MACHINE_IDENTITY` and durable `MachineIdentity` with principal, machine subject, tenant/realm, hardware ID, attestation type, trust anchor, status, and metadata;
- a planned `DevicePrincipal` model/test requiring representation, ownership, tenant isolation, lifecycle, and package boundaries;
- workload identity, service/client principals, tenant/realm trust domains, and trust graph;
- API/service keys, client secrets, DPoP keys, mTLS certificate credentials, key lifecycle/attestation, and audit;
- OAuth client credentials, token exchange, DPoP/mTLS, resource indicators, resource validation, and revocation;
- proposed Certificate Center, Attestation Center, Token Service, Workload Trust, Security Signals, and Policy Studio;
- RFC 8628 device authorization routes/tests/examples for user-login use cases.

Missing capabilities include:

- canonical durable device record distinct from generic machine metadata;
- manufacturing identity, make/model/hardware revision, secure element/IDevID, owner/custodian, site, fleet, lifecycle, and transfer records;
- zero-touch onboarding/voucher/registrar or vendor claim flows;
- device attestation/posture profiles and reference values;
- firmware/update manifest and deployment posture;
- ACE-OAuth/CWT/COSE/CoAP/DTLS/OSCORE profiles;
- device-specific grants/resources/commands, telemetry trust, fleet jobs, quarantine, recall, end-of-life, and UIX.

## 3. Users and Jobs

### Fleet/device administrator

1. import or discover devices and validate manufacturing/procurement evidence.
2. claim, onboard, assign tenant/site/group/owner, and issue operational credentials.
3. monitor identity, key/certificate, attestation, firmware, connectivity, and policy posture.
4. stage updates/credential rotations and contain compromised devices.
5. transfer ownership or decommission with complete credential/data/trust cleanup.

### Device manufacturer/integrator

1. provision unique manufacturing identity and trust anchors securely.
2. publish model/firmware/reference/endorsement metadata.
3. support authorized ownership claims, vouchers, recalls, and trust-anchor rollover.
4. avoid learning customer domain/activity beyond justified onboarding/support data.

### Embedded/IoT developer

1. authenticate device without shared fleet-wide secrets.
2. obtain audience/resource-scoped, proof-bound authorization suited to constrained hardware.
3. validate commands/updates before execution and handle clock/network/offline limits.
4. rotate credentials and recover from partial update or connectivity failure.
5. test with deterministic device/emulator fixtures.

### Security/SOC operator

1. detect cloned identities, shared/default credentials, attestation drift, firmware rollback, unusual token use, and ownership anomalies.
2. understand affected devices/sites/resources and take bounded response actions.
3. quarantine without bricking safety-critical devices or losing forensic evidence.
4. verify containment, re-provisioning, and return to service.

### Customer support/field technician

1. locate device by approved identifier/claim code/QR and see safe status.
2. perform authorized install, replacement, reset, transfer, or recovery workflows.
3. avoid access to fleet-wide credentials, sensitive telemetry, or other tenants.

## 4. Architectural Ownership

### Device identity domain owns

- device/product/model/fleet/site/ownership/custody/lifecycle semantics;
- manufacturing and operational identity linkage;
- onboarding/claim/transfer/decommission workflows;
- device credential/profile assignments and operational posture projection;
- device resource/action vocabulary and fleet operations.

### Protocol/provider packages own

- BRSKI/voucher/EST or other onboarding protocols;
- device attestation evidence generation/verification adapters;
- ACE-OAuth/CWT/COSE/CoAP/DTLS/OSCORE profiles;
- firmware/SUIT manifest validation and update-provider adapters;
- vendor/cloud/registry integrations.

### Device Identity API owns

- tenant-safe orchestration, management routes, lifecycle actions, jobs, policy integration, reports, audit, and UI schemas;
- no protocol semantics invented in UI/API handlers;
- no direct private-key/firmware secret handling beyond provider references.

### Existing products retain ownership

- Certificate Center owns certificate lifecycle;
- Attestation Center verifies device/platform evidence;
- Token Service owns OAuth/ACE token profiles and lineage;
- Policy Studio owns authorization decisions;
- Security Signals owns device/posture incidents and responses;
- Workload Trust owns software identities on devices;
- Provisioning/Directory owns human/operator identities;
- storage owns durable normalized state;
- UIX never determines device trust.

## 5. Device Identity and Lifecycle Model

### Device versus model

- **Device model:** manufacturer, product family, model, hardware revisions, capabilities, supported attestation/onboarding/credential/update profiles, lifecycle/support window, and reference sources.
- **Device instance:** unique immutable platform ID, model/revision, manufacturing identity, serial/public identifiers, current tenant/owner/site, state, operational identity, credentials, firmware/posture, and evidence.

Serial number is an inventory attribute, not sufficient authentication. MAC address, IP address, hostname, cloud resource name, user-entered code, or QR label alone must not become the durable proof-bearing device identity.

### Lifecycle states

- manufactured/unassigned;
- imported/inventory pending;
- claimable/claim pending;
- onboarding/attestation pending;
- active;
- degraded/noncompliant;
- quarantined;
- suspended/lost/stolen;
- maintenance/repair;
- transfer pending;
- factory reset/reprovision pending;
- decommissioned/retired/destroyed;
- recalled.

State changes use typed commands, authorization, evidence, reason, and expected side effects. A status string edit is insufficient.

### Ownership and custody

Track manufacturer, distributor/reseller, legal owner/customer, tenant, site, operational custodian, installer/technician, service contract, and current physical/administrative custody where required. Ownership does not imply possession; possession does not imply authorization; tenant assignment does not rewrite manufacturing provenance.

## 6. Manufacturing and Bootstrap Identity

### Manufacturing identity

- unique per-device credential, preferably hardware-protected and non-exportable;
- certificate/IDevID or profile-native key identity with manufacturer endorsement and chain;
- make/model/hardware revision and optional serial binding under privacy policy;
- initial trust anchors and update/onboarding authority;
- provisioning ceremony, production line, key provider, issuance time, and evidence;
- no fleet-wide default credential.

### Import/procurement

- signed manufacturer/distributor batch manifests or individually verified identity inventory;
- expected model/serial/public-key fingerprints and ownership entitlement;
- duplicate/clone/collision detection;
- quarantine unverifiable or previously claimed devices;
- do not activate a device solely because its serial appears in a CSV.

### Bootstrap trust options

- BRSKI with vouchers/IDevID/registrar/EST where applicable;
- vendor cloud claim APIs with signed challenge and customer entitlement;
- out-of-band QR/claim code plus device proof for lower-capability products;
- pre-enrolled enterprise certificate/profile;
- local technician-assisted onboarding with two-channel verification;
- attestation-driven enrollment.

Each profile must state who authenticates whom, root of trust, freshness, ownership authorization, network assumptions, credentials issued, failure/recovery, and privacy.

## 7. Onboarding and Claim Semantics

1. create short-lived claim/onboarding transaction bound to tenant/site/model/profile and authorized operator;
2. establish device connection and receive manufacturing/device identity proof;
3. validate chain/endorsement/voucher, nonce/freshness, model/serial/public key, status, and prior ownership;
4. verify customer entitlement/ownership and prevent cross-tenant claim race;
5. appraise device/firmware posture under current policy;
6. create/link canonical device principal and instance atomically;
7. assign operational identity, tenant/site/group, resource permissions, and update policy;
8. issue/activate device-specific operational credential with overlap only if needed;
9. deliver trusted domain/issuer/update/config metadata over authenticated protected channel;
10. device acknowledges installed identity/config; server verifies subsequent authenticated check-in;
11. consume claim/voucher/code, record evidence, and enter active or restricted commissioning state.

Manufacturing credentials should normally authenticate bootstrap, not remain the everyday operational credential. Operational re-provisioning must not erase manufacturing provenance.

## 8. BRSKI and Certificate Enrollment Opportunity

For enterprise/network devices, support may profile RFC 8995 BRSKI:

- pledge, join proxy, domain registrar, MASA, voucher request/voucher, IDevID, ownership assertion, nonce/freshness, audit log, and EST enrollment;
- verify manufacturer anchor and voucher, device identity, registrar/domain identity, and claim authorization;
- protect MASA/registrar/CA keys and long device-lifetime trust-anchor maintenance;
- keep manufacturer audit-log privacy and domain correlation visible in program design;
- support updated BRSKI-AE only as a pinned profile where needed.

BRSKI is not a universal consumer IoT onboarding method. Each target device class needs an applicability, transport, resource, privacy, and recovery analysis.

## 9. Device Credentials and Rotation

Supported credential profiles may include:

- operational mTLS certificate/LDevID;
- raw public key for constrained DTLS/CoAP profiles;
- device-specific pre-shared key only for constrained justified profiles;
- DPoP key for HTTP/OAuth device APIs;
- CWT/COSE proof key;
- secure-element/device attestation key used only for evidence, not routine authorization;
- emergency/recovery credential under stronger limits.

Requirements:

- per-device, tenant/site/resource bound, hardware-protected where possible;
- one-time display prohibited for device private material;
- issuance/activation acknowledgement and last-used posture;
- rotation with new key where supported, bounded overlap, fleet rollout, rollback, and old credential revocation;
- no global shared secret or credentials embedded identically across model/fleet;
- compromise of manufacturer/bootstrap key, operational CA, model firmware key, or device key has separate blast-radius handling;
- device clock and offline constraints explicitly accounted for.

## 10. Attestation and Posture

Device posture should consume Attestation Center results, not parse evidence in Fleet UIX.

Profiles may evaluate:

- manufacturing/model identity and hardware root of trust;
- secure/measured boot state;
- firmware/bootloader/OS/application version and measurements;
- security/TCB version, debug/unlock/root/jailbreak state;
- key protection and device configuration;
- update policy, support/EOL, tamper state, and runtime health;
- attached module/sensor identities for composite devices.

Posture states:

- not observed;
- evidence received but unverified;
- compliant under policy/version at time;
- noncompliant;
- indeterminate/unsupported/stale;
- attestation failed/replayed/subject mismatch;
- provider/reference unavailable.

Posture controls issuance/access through explicit policy. A valid manufacturing certificate does not prove current firmware or uncompromised runtime.

## 11. Firmware and Software Update Trust

### Fleet responsibilities

- device model/current/target firmware inventory;
- signed manifest/image provenance, compatibility, sequence/version, dependencies, size, rollout, and owner;
- staged rings, maintenance/safety constraints, offline/battery/network state, health gates, pause/rollback/recovery;
- desired versus observed update and attestation after reboot;
- vulnerability/advisory/recall/EOL linkage;
- emergency updates and quarantines.

### SUIT-aligned requirements

Use RFC 9019 architecture and RFC 9124 information model as design foundations where applicable:

- authenticate manifest and firmware digest/type;
- verify vendor/class/device compatibility before install;
- use monotonic sequence semantics to resist unauthorized rollback while permitting authorized version rollback via newer manifest;
- enforce dependency, precondition, component, storage, and installation policy;
- prevent time-of-check/time-of-use replacement;
- fail safely with recoverable partitions/boot paths where hardware permits;
- never treat "downloaded" as "installed" or "installed" as "healthy."

Fleet Trust orchestrates identity/posture/update policy but should use a dedicated update provider rather than become a binary distribution service by default.

## 12. ACE-OAuth, CWT, and Constrained Authorization

For constrained devices and resource servers, add a selected RFC 9200 ACE profile:

- OAuth-derived authorization server, client, resource server, token endpoint, `authz-info`, introspection/status as profiled;
- CWT/COSE token format and proof-of-possession keys;
- DTLS profile (RFC 9202) using raw public keys or PSKs, or OSCORE profile (RFC 9203), selected per deployment;
- mutual authentication, confidentiality, integrity, replay protection, and response/request binding;
- explicit `ace_profile` compatibility between client/resource server;
- compact audience/scope/resource/action vocabulary;
- key/token provisioning, rollover, sequence/replay state, offline expiry, and revocation strategy.

Do not send ordinary HTTP bearer JWTs to a constrained CoAP device and call it ACE. CWT/COSE/CBOR, transport/profile, key confirmation, and endpoint semantics are native requirements.

## 13. Device Resource and Authorization Model

Define resources/actions by device class, not unstructured scopes:

- telemetry read/stream;
- configuration read/write;
- command execute/cancel;
- firmware inspect/stage/install/rollback;
- credential rotate/revoke;
- attestation request/result read;
- diagnostics/log export;
- reset/reprovision/transfer/decommission;
- actuator-specific safety actions.

Authorization inputs include tenant/site/fleet/device/model, operator/service/workload identity, purpose, command parameters/digest, current state/posture, maintenance window, safety interlock, network/location, delegation, and credential/proof.

High-risk commands require transaction-bound authorization, step-up/dual control, short expiry, replay protection, device acknowledgement, and verified outcome. A fleet group membership change must not silently grant unsafe actuator authority.

## 14. Telemetry, Commands, and Trust

### Telemetry

- authenticated source device/credential and tenant/site binding;
- schema/version, sequence/time quality, replay/duplicate/out-of-order handling, integrity, and confidentiality;
- distinguish device-reported, gateway-reported, derived, and externally observed values;
- telemetry authenticity does not guarantee sensor truth/calibration;
- privacy/data residency/retention for location, audio/video, health, occupancy, and operational data;
- route bulk telemetry to specialized data systems, storing only identity/security posture in auth storage.

### Commands

- command ID, issuer/actor, device/resource/action, payload digest/schema, authorization decision, expiry, nonce/sequence, proof, and priority;
- signed/MACed/encrypted under profile;
- queued/sent/received/accepted/executing/succeeded/failed/rejected/expired/canceled outcome;
- idempotency and safe retry by command semantics;
- device verifies authorization and current safety/precondition state;
- outcome acknowledgement is not proof of physical-world effect without independent evidence.

## 15. Ownership Transfer and Decommissioning

### Transfer

1. authorize current owner and intended recipient/tenant through an explicit transaction;
2. verify device possession/identity and transfer eligibility/no recall/lien/policy block;
3. export only permitted non-sensitive service history;
4. revoke old operational credentials, tokens, grants, sessions, cloud bindings, technician access, and fleet membership;
5. erase tenant/customer secrets/data/config according to profile with device acknowledgement/attestation;
6. preserve immutable manufacturing/transfer evidence under privacy policy;
7. return to claimable or directly enroll into recipient with new keys/credentials;
8. verify no old owner access and new owner control.

### Decommission

- revoke all operational identity and authorization;
- remove trust/fleet/site/cloud integrations and queued commands;
- perform cryptographic erase/factory reset under device capability and verify evidence;
- record disposal/return/destruction and environmental/regulatory data where applicable;
- retain minimum audit/manufacturer provenance, delete tenant data, and prevent identity reuse;
- mark lost/stolen devices separately so later check-in triggers containment.

## 16. API Requirements

Use `/admin/device-identity` for management. Device protocol endpoints live in the selected provider/profile.

### Inventory and lifecycle

- CRUD/versioned models, fleets/groups, sites, devices, manufacturing imports, ownership/custody, profiles, and assignments;
- actions: validate-import, claim, onboard, attest, activate, suspend, quarantine, maintenance, recover, transfer, reset, decommission, recall;
- typed state-machine transition validation, idempotency, approval, and impact;
- safe lookup by device ID/public fingerprint/serial where authorized, with no cross-tenant existence disclosure.

### Credentials/posture/firmware

- credential profile/issuance/rotation/revocation status via owning services;
- attestation session/result/posture summaries;
- firmware model/release/manifest/rollout/desired-observed/compliance/health;
- key/certificate/update trust anchor inventory and impact;
- batch jobs with dry run, bounded target selection, approval, partial result manifest, pause/resume/rollback.

### Operations

- command policy/templates/transactions/outcomes;
- security events/incidents/quarantine/recovery;
- fleet posture reports and evidence export;
- no general remote shell or arbitrary command payload in the identity API;
- no bulk raw telemetry storage/query.

## 17. Canonical Data Requirements

### Device model/version

- manufacturer/product/model/hardware revisions and identifiers;
- supported onboarding, credential, attestation, firmware/update, transport, ACE, and recovery profiles;
- security capabilities, resource/action schema, support/EOL/recall, endorsements/reference sources, and owner;
- lifecycle/version/effective period and evidence.

### Device instance

- device/principal ID, tenant/realm, model/revision, immutable hardware/manufacturing references, public identifiers, state, and risk;
- manufacturer/distributor/owner/custodian/site/fleet/group;
- operational identity and credential/key/certificate references;
- attestation/posture, firmware desired/observed, last authenticated check-in, connectivity quality, and clock capability;
- claim/onboarding/transfer/decommission lineage, privacy/retention, and audit.

### Onboarding transaction

- profile, tenant/site, operator, device proof, voucher/claim-code digest, nonce, manufacturer/registrar/provider, state, expiry, attempts, entitlement, result, and evidence;
- manufacturing/operational key fingerprints and credential issuance links;
- no raw bootstrap secret after completion.

### Firmware rollout/device state

- release/manifest digest, model compatibility, sequence/version, authority, target set, rings, window, state, health gates, and rollback;
- per-device desired/downloaded/verified/installed/booted/attested/healthy states and reason;
- command and audit linkage.

### Ownership transfer

- source/destination owner/tenant references, device, state, approvals, possession proof, data/credential cleanup checklist, times, outcome, and evidence;
- sensitive commercial ownership data access-controlled and retained minimally.

## 18. Fleet Trust UIX

### Fleet overview

- devices by lifecycle/posture/firmware/credential/connectivity/site/model/owner;
- unmanaged/unclaimed, onboarding failure, stale attestation, expiring credential, vulnerable/outdated, quarantined, lost/stolen, recall/EOL, and failed update;
- priority actions sorted by safety/security/blast radius, not merely count;
- fleet health distinguishes unknown/offline from healthy.

### Inventory and device detail

- accessible large table/map optional, with site/fleet/model/owner/state/posture/version/credential/last check-in;
- detail timeline from manufacture/import/claim/onboarding through operations/transfer/decommission;
- identity, credential, attestation, firmware, policy/access, commands, signals, ownership/custody, and evidence tabs;
- sensitive hardware IDs, locations, and telemetry masked/permissioned;
- explicit logical device versus current connectivity endpoint.

### Onboarding wizard

1. choose/import model and expected inventory;
2. select tenant/site/fleet and onboarding profile;
3. scan/enter claim artifact or wait for device proof;
4. show manufacturer/device identity/trust and ownership entitlement;
5. appraise posture and firmware;
6. preview operational identity/credentials/policy/update;
7. approve and provision;
8. verify authenticated check-in;
9. finish commissioning or restrict/remediate.

### Policy, rollout, and commands

- device class resource/action builder linked to Policy Studio;
- target preview and exclusions;
- credential/firmware/config rollout rings with dry run, safety window, progress, partial failure, pause/rollback;
- command request shows typed parameters, authorization, affected physical behavior, expiry, proof, and acknowledgement;
- high-risk bulk action requires dual control/typed confirmation and emergency stop where applicable.

### Trust/posture explorer

- manufacturing identity, operational credential, attestation, firmware manifest, trust anchors, token/profile, and authorization chain;
- accessible table/tree plus optional graph;
- reason-coded posture and last evidence time/policy;
- blast radius for manufacturer/CA/key/reference/firmware/profile/fleet changes;
- no green "trusted" state without time, policy, evidence, and scope.

### Incident, transfer, and retirement

- quarantine that explains telemetry/command/update/connectivity consequences;
- clone/key/firmware/attestation/anomalous-use investigation timeline;
- recovery/rekey/reflash/re-attest/return-to-service checklist;
- guided ownership transfer with old-access cleanup proof;
- decommission/erase/dispose flow with irreversibility, offline-device handling, and evidence.

## 19. Security, Safety, Privacy, and Reliability

- Require unique device credentials; detect and block default/shared/fleet-wide secrets.
- Protect manufacturing/attestation/update/CA keys in HSM/KMS/secure production systems with separation of duties and rollover plans spanning device lifetime.
- Validate device identity proof, voucher/endorsement, nonce, tenant/ownership, attestation, and operational check-in before activation.
- Keep device private keys non-exportable and never return through API/UIX.
- Enforce tenant/site/device isolation in search, commands, telemetry routes, credentials, tokens, updates, exports, and analytics.
- Bound onboarding attempts, claim codes, payloads, CBOR/COSE, commands, batch targets, firmware size, and cryptographic work.
- Authenticate/integrity-protect/confidentiality-protect constrained communications and prevent replay/downgrade.
- Treat physical safety separately from cybersecurity authorization; safety interlocks remain local and cannot be bypassed by API policy.
- Use staged rollouts, watchdog/rollback/recovery partitions where supported, and never update an incompatible device.
- Design for intermittent/offline networks, weak/no trusted clocks, limited storage/battery, long lifetimes, and regional partitions.
- Minimize location/behavior/audio/video/health/occupancy data; auth services should retain only security posture.
- Secure supply chain, factory provisioning, logistics, repair, return, refurbish, and disposal paths.
- Exercise mass credential/key/firmware compromise, manufacturer outage, CA rollover, bricked rollout, recall, stolen fleet, and ownership-transfer failure.

## 20. Stakeholder Requirements

### Technical marketing

- demonstrate unique onboarding, hardware/manufacturer proof, credential issuance, attestation, constrained access, staged update, quarantine, and transfer using emulated devices;
- explain device flow versus device identity and authentication versus sensor truth;
- prepare stories for industrial IoT, medical devices, automotive/fleet, smart buildings, utilities, retail edge, logistics, telecom, agriculture, robotics, and consumer products;
- avoid "zero touch" or "hardware rooted" claims without the exact profile/evidence.

### Developer relations

- provide device emulator/reference firmware, onboarding, mTLS/DPoP, ACE/CWT/CoAP profiles, command validation, firmware manifest, rotation, and recovery quickstarts;
- deterministic positive/adversarial fixtures for clone, wrong tenant, replay, expired voucher/token, stale attestation, invalid firmware, rollback, offline, and partial update;
- document constraints, buffers, clocks, retry, idempotency, status, safe logging, and field-debugging;
- publish hardware/vendor support matrices separately from protocol support.

### Sales and account management

- use a fleet assessment for manufacturers/models/count, hardware roots, factory process, owners/sites, networks/transports, credentials, onboarding, firmware, attestation, resources/commands, safety, privacy, region, lifetime/EOL, and support;
- provide readiness report separating inventory, bootstrap, identity, credential, posture, authorization, update, operations, transfer, and retirement;
- define RACI across manufacturer, distributor, customer owner, operator, site technician, Tigrbl, CA/KMS, network/cloud, update provider, and incident team;
- quantify integration by device class/profile rather than assuming one connector covers all IoT.

### GTM strategist

- package Device Registry, Secure Onboarding, Credential/Attestation, Constrained Access, Firmware Trust, and Fleet Governance separately;
- prioritize gateway/edge and capable enterprise devices before ultra-constrained/battery devices requiring specialized ACE stacks;
- pair with Certificate, Attestation, Token, Policy, Workload, and Security Signals products;
- meter managed device, active site/fleet, onboarding, attestation, command/update operation, retention, or governance tier without charging for revocation/quarantine/security updates.

### Copywriter

- distinguish device, machine/node, workload, instance, model, owner, custodian, credential, attestation, posture, firmware, update, command, and telemetry;
- never call a device healthy because it checked in or trusted because its certificate parsed;
- say desired/downloaded/installed/booted/attested/healthy separately;
- explain offline/unknown, quarantine, safety impact, ownership, and irreversibility;
- avoid implying telemetry authenticity proves physical sensor accuracy.

## 21. Delivery Instructions

### Frontend engineer

- generate typed management clients and use server/provider results for trust/posture/authorization;
- never handle device private/bootstrap/update signing keys or raw fleet secrets;
- support large fleets with cursor pagination, virtualization, saved filters, background jobs, progress, partial failure, pause/resume, and safe retry;
- render unknown/offline separately from healthy and desired separately from observed;
- implement target snapshots/version checks so bulk actions cannot drift after approval;
- instrument lifecycle/posture/update/command stages with opaque IDs and no sensitive telemetry/hardware IDs.

### UIX designer

- separate identity, lifecycle, connectivity, credential, attestation, firmware, and safety state;
- design fleet-to-device progressive disclosure and accessible table/tree alternatives to maps/graphs;
- cover unclaimed, onboarding, proof failed, active, offline, stale, degraded, noncompliant, updating, partial, rollback, quarantined, lost/stolen, transfer, recall, EOL, and decommission states;
- make high-risk physical commands and bulk targets unmistakable with impact/approval/emergency stop;
- provide field/mobile workflows with poor connectivity and accessible QR/manual alternatives;
- meet WCAG 2.2 AA, non-color status, keyboard, focus, reduced motion, map alternatives, localization, and unit/timezone clarity.

### Copywriter

- create device lifecycle, onboarding/trust, credential, attestation, firmware, connectivity, command, transfer, incident, reason-code, confirmation, and recovery catalogs;
- write separate fleet admin, technician, developer, owner, and security language;
- disclose safety/physical effects, target count/snapshot, expiry, reversibility, and recovery;
- calibrate manufacturer/hardware/protocol/profile claims;
- provide lost/stolen, clone, bricked update, expired credential, ownership dispute, and EOL guidance.

## 22. Delivery Phases

### Phase 1: Canonical device fleet and manual governed onboarding

- DevicePrincipal/durable instance/model/site/fleet/ownership/lifecycle contracts/storage;
- one mTLS or DPoP capable device profile, claim transaction, operational credential, check-in, policy, audit, and Fleet Trust inventory;
- device emulator and negative fixtures.

### Phase 2: Attestation, rotation, and fleet operations

- device evidence profile, posture, reference/endorsement, credential rotation, command templates/outcomes, bulk jobs, quarantine/recovery, and security signals;
- firmware desired/observed inventory and staged provider adapter.

### Phase 3: Standards onboarding and constrained access

- selected BRSKI/EST or vendor zero-touch profile;
- selected ACE-OAuth CWT/COSE DTLS or OSCORE profile;
- SUIT-aligned manifest validation/update orchestration;
- interoperability/conformance evidence.

### Phase 4: Transfer, scale, and vertical packs

- ownership transfer/refurbish/decommission/recall;
- multi-region/offline gateways, manufacturer integrations, lifecycle analytics;
- medical/industrial/automotive/utilities/buildings/retail/telecom profiles with safety/regulatory evidence.

## 23. Acceptance Criteria

### API/runtime

- Every active device has canonical principal/instance/model/tenant/owner/site/lifecycle and a unique proof-bearing operational identity.
- Onboarding validates device/manufacturer proof, freshness, ownership entitlement, tenant, posture, and operational check-in.
- Shared/default credentials and cross-tenant claim races fail closed.
- Device authorization uses typed resources/actions, current posture, proof, expiry/replay, and safe command outcome.
- Credential/firmware rollouts are staged, target-snapshotted, observable, and rollback/recovery aware.
- Transfer/decommission removes old access/credentials/data and prevents identity reuse with evidence.
- RFC 8628 records/routes are not treated as device fleet identity.

### UIX

- Operators can trace manufacturing identity to onboarding, operational credential, posture, firmware, authorization, and current state.
- Unknown/offline/stale cannot appear healthy.
- Bulk target/physical effect/safety/rollback are visible before execution.
- Field onboarding works accessibly without relying only on QR/network.
- Incident/transfer/decommission workflows expose blast radius, irreversibility, and verified cleanup.

### Evidence/business

- DevRel can run deterministic emulated positive/adversarial device journeys.
- Technical marketing can demonstrate end-to-end lifecycle without production hardware secrets.
- Sales can provide device-class readiness/RACI and integration estimate.
- BRSKI/ACE/CWT/SUIT/hardware/vendor/vertical claims link to profile-specific certified evidence.

## 24. Success Measures

- inventoried/claimed/onboarded/active device coverage;
- duplicate/clone/shared-credential/cross-tenant claim detections;
- onboarding time/success by model/profile/reason;
- credential/attestation/posture freshness and rotation success;
- current/desired firmware, vulnerable/EOL/recall, rollout/rollback/brick rate;
- offline/stale/unknown duration and false-healthy incidents;
- command authorize/deliver/execute/verify latency and failure;
- quarantine/contain/recover time;
- transfer/decommission cleanup verification;
- device key/data/telemetry privacy/safety incidents.

Guardrails include default credentials, cloned identity, false attestation, unsafe command, cross-tenant control, firmware supply-chain compromise, fleet bricking, stale trust, ownership leakage, sensor-truth overclaim, privacy overcollection, and overstated standards support.

## 25. Source Evidence

### Repository

- `pkgs/02-contracts/tigrbl-identity-contracts/src/tigrbl_identity_contracts/principals/`;
- `pkgs/10-concrete/tigrbl-identity-principals/src/tigrbl_identity_principals/factories.py`;
- `pkgs/01-storage/tigrbl-identity-storage/src/tigrbl_identity_storage/tables/machine_identity/`;
- `tests/planned/identity_model/device-principal.md`;
- `tests/security/test_machine_identity_governance.py`;
- certificate, credential, key attestation, workload, trust-domain, OAuth token/proof, resource-validation, policy, audit, and security-signal foundations;
- RFC 8628 device authorization code/tests as a separate user authorization feature;
- Device/IoT opportunity-map entry.

### Standards and primary sources

- [RFC 9200: ACE-OAuth](https://www.rfc-editor.org/rfc/rfc9200)
- [RFC 8392: CBOR Web Token](https://www.rfc-editor.org/rfc/rfc8392)
- [RFC 8747: Proof-of-Possession Key Semantics for CWTs](https://www.rfc-editor.org/rfc/rfc8747)
- [RFC 9202: ACE DTLS Profile](https://www.rfc-editor.org/rfc/rfc9202)
- [RFC 9203: ACE OSCORE Profile](https://www.rfc-editor.org/rfc/rfc9203)
- [RFC 8995: BRSKI](https://www.rfc-editor.org/rfc/rfc8995)
- [RFC 8366: Voucher Profile for Bootstrapping Protocols](https://www.rfc-editor.org/rfc/rfc8366)
- [RFC 7030: Enrollment over Secure Transport](https://www.rfc-editor.org/rfc/rfc7030)
- [RFC 9019: Firmware Update Architecture for IoT](https://www.rfc-editor.org/rfc/rfc9019)
- [RFC 9124: Firmware Update Manifest Information Model](https://www.rfc-editor.org/rfc/rfc9124)
- [RFC 9711: Entity Attestation Token](https://www.rfc-editor.org/rfc/rfc9711)

## 26. Explicit Non-Claims

This brief does not claim that the current repository:

- implements a durable device fleet identity product;
- treats RFC 8628 Device Authorization as manufacturing/device identity;
- supports BRSKI, EST device onboarding, vouchers, MASA, or IDevID/LDevID lifecycle;
- implements ACE-OAuth, CWT/COSE, CoAP/DTLS/OSCORE profiles;
- verifies device secure boot, firmware, hardware roots, or sensor truth;
- manages SUIT firmware manifests or safe fleet updates;
- supports ownership transfer, device erase, recall, or decommission proof;
- interoperates with a named device manufacturer, cloud IoT platform, hardware secure element, or vertical certification.

Those claims require device-class-specific contracts, manufacturing/onboarding integrations, credential and attestation profiles, constrained protocol stacks, firmware safety/recovery, field operations, adversarial/interoperability testing, privacy/safety/regulatory analysis, and release certification.

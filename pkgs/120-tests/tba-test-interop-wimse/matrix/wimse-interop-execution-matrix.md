# WIMSE interop execution matrix

Use the [scenario matrix](wimse-interop-scenario-matrix.md) for inputs and expected results. This companion assigns implementation roles and directions. Each expanded run has one scenario variant, one authentication profile per hop, one set of pinned implementations, and one result. All pairings below are planned. Candidate capabilities come from the IETF draft or the thread and need a role-specific preflight.

## Authentication profiles

| Profile | TLS authentication | Application proof |
|---|---|---|
| WIC/mTLS | Mutual TLS with Workload Identity Certificates | None |
| WIT/WPT | Server-authenticated TLS | Workload Identity Token and Workload Proof Token |
| WIT/HTTP signatures | Server-authenticated TLS | Workload Identity Token and HTTP Message Signature |
| WIC/mTLS + WIT/WPT | Mutual TLS with WICs | WIT and WPT |
| WIC/mTLS + WIT/HTTP signatures | Mutual TLS with WICs | WIT and HTTP Message Signature |

## Peer and role assignments

An arrow points from the caller to the receiver of the protected request. Issuers are listed separately because credential issuance and peer verification are different roles. In the reverse run, swap caller and receiver while keeping the test topology equivalent. In a two-domain case, record both the role assignment and the actual source and destination domains. Add a separate run if a different issuer or trust configuration applies in the reverse direction.

| Pairing | Authentication profile | Forward caller → receiver | Reverse caller → receiver | Credential and version inputs |
|---|---|---|---|---|
| WIC with native identifiers | WIC/mTLS | TbA → wimsey | wimsey → TbA | Pin both commits, TLS library versions, issuer and trust bundles. Use native `wimse://` identifiers. Verify client and server WIC support in each direction. |
| WIC with SPIFFE identifiers | WIC/mTLS | TbA → wimsey | wimsey → TbA | Repeat with `spiffe://` identifiers. A SPIRE-issued X.509-SVID is a candidate input when the certificate and both peer configurations meet the WIC profile. Pin the SPIRE build and certificate profile if used. |
| Workload Proof Tokens | WIT/WPT | TbA → Cred | Cred → TbA | Cred candidate from the `hackathon/ietf127` branch. Pin the commit, WIT issuer and exact verifier configuration. Confirm WPT sending and receiving separately. |
| HTTP Message Signatures | WIT/HTTP signatures | TbA → Cofide PoC | Cofide PoC → TbA | Pin Cofide PoC and TbA commits, WIT issuer, signed components and response-signing settings. |
| WIT + HTTP Message Signatures | WIT/HTTP signatures | TbA → Cred | Cred → TbA | Pinned Cred draft-08 request signer and verifier. Direct HTTPS with lab-issued WITs for scenarios 01 and 07, including valid and substituted `Txn-Token` values. |
| WIC with Workload Proof Tokens | WIC/mTLS + WIT/WPT | TbA → independent endpoint with both capabilities | Independent endpoint → TbA | Preflight wimsey or a composed mTLS endpoint with a separate WPT implementation. Record which process terminates TLS and which verifies WPT. |
| WIC with HTTP Message Signatures | WIC/mTLS + WIT/HTTP signatures | TbA → independent endpoint with both capabilities | Independent endpoint → TbA | Preflight wimsey or Cofide behind an independent WIC endpoint. Record TLS termination and the HTTP signature verifier. |
| Issuer substitution | WIT/WPT or WIT/HTTP signatures | Reuse a validated forward application pair | Reuse its validated reverse pair | Replace the baseline WIT issuer with a pinned SPIRE experimental WIT-SVID build. Record go-spiffe v2.7.0 only where it actually consumes or handles the credential. Keep the endpoint pair fixed so the issuer change is isolated. |

Sources for candidate roles. [Hackathon proposal and implementation list](https://mailarchive.ietf.org/arch/msg/wimse/6ofJ6o3sK9H_XEPCQWn_7SVEza4), [Cred participant report](https://mailarchive.ietf.org/arch/msg/wimse/vC0V6-1i6HWHJMKp-KNHYTIaQr0), [workload credential draft implementation status](https://www.ietf.org/archive/id/draft-ietf-wimse-workload-creds-03.html#section-8).

## Execution groups

Expand every applicable scenario variant per pairing and direction. The scenario matrix determines the allowed profiles. Require the forward passing control before running failure cases for that direction. Preflight the reverse roles independently.

| Execution group | Scenario IDs | Pairings and roles | Evidence to capture |
|---|---|---|---|
| Peer authentication and composition | 01–06, 19 | Use the applicable peer rows above. For 04, assign the gateway inbound and outbound connections separately. | Peer URI and trust domain, trust-bundle ID, TLS termination point, application principal, verification stage, decision, and effect. |
| Token binding, domain exchange, direction | 07–08, 20 | Use the applicable peer rows. Name the A-side Transaction Token issuer and boundary client, B-side grant verifier and access-token issuer, and B resource server. | Token types and audiences, per-hop binding decision, trace through both domains, and final effect. Repeat with the issuer substituted where supported. |
| Authority and agent behavior | 09–10 | Use the applicable peer rows and assign the authority verifier, agent runtime for 10, resource, and protected output sinks. | Workload identity, authority source, grant and scope decision, and whether a protected resource was read, disclosed, or modified. |
| Status and before-effect enforcement | 11–12 | Assign the status authority and the enforcing service. Use the peer rows for workload authentication. MintID is a candidate independent before-effect component for 12. | Status publication, observation, first refusal, and measured effect. For MintID, record the attribution control and the component that enforced the decision. |
| Passport and delegation | 13–14, 16 | Assign receipt issuer and verifier. For 14, name both relying services and the accounting authority. For 16, name the issuer and verifier of the tool/build claims. | Parent/child grant decision, authoritative ledger and resource state, or digest comparison and call result. Independent passport peers require preflight. |
| Proxy, approval, bearer-only provider | 15, 17–18 | Assign proxy and downstream signature verifier for 15, OASNT R2 approval verifier for 17, and bearer broker plus provider fixture for 18. Cred is a candidate broker. | Signed components and downstream decision, approval decision and effect, or token-release time, provider decision, and actual provider effect. |

The MintID offer covers the enforcement hop, and the OASNT vector fixes the approval input. Record the precise boundary demonstrated by each run. [MintID reply](https://mailarchive.ietf.org/arch/msg/wimse/8wNHgFgnEncJymh7TqA_V0cQQ4g), [OASNT R2](https://www.ietf.org/archive/id/draft-thallapelly-oasnt-02.html#appendix-A.7.2), [P1–P8 follow-up](https://mailarchive.ietf.org/arch/msg/wimse/CuZS8gtTTiSPZI8AXSJF_Oy781s).

## Initial run rows

These rows start the peer qualification. Use the complete execution groups after capability preflight.

| Run | Scenario and variant | Profile | Caller → receiver | State |
|---|---|---|---|---|
| 01-WIC-01 | 01, native identifier | WIC/mTLS | TbA → wimsey | Planned |
| 01-WIC-02 | 01, native identifier | WIC/mTLS | wimsey → TbA | Planned |
| 01-WIC-03 | 01, SPIFFE URI | WIC/mTLS | TbA → wimsey | Planned |
| 01-WIC-04 | 01, SPIFFE URI | WIC/mTLS | wimsey → TbA | Planned |
| 01-WPT-01 | 01, valid peer | WIT/WPT | TbA → Cred | Planned |
| 01-WPT-02 | 01, valid peer | WIT/WPT | Cred → TbA | Planned |
| 01-HTTP-01 | 01, valid peer | WIT/HTTP signatures | TbA → Cofide PoC | Planned |
| 01-HTTP-02 | 01, valid peer | WIT/HTTP signatures | Cofide PoC → TbA | Planned |
| 01-WIC-WPT-01 | 01, both layers valid | WIC/mTLS + WIT/WPT | TbA → qualified independent peer | Awaiting peer qualification |
| 01-WIC-WPT-02 | 01, both layers valid | WIC/mTLS + WIT/WPT | Qualified independent peer → TbA | Awaiting peer qualification |
| 01-WIC-HTTP-01 | 01, both layers valid | WIC/mTLS + WIT/HTTP signatures | TbA → qualified independent peer | Awaiting peer qualification |
| 01-WIC-HTTP-02 | 01, both layers valid | WIC/mTLS + WIT/HTTP signatures | Qualified independent peer → TbA | Awaiting peer qualification |

## Run record

| Field | Record |
|---|---|
| Case | Run ID, scenario ID and exact variant, expected decision and reason, expected effect and evidence basis. |
| Hop configuration | Caller, receiver, issuer, verifier and any gateway, broker or provider for each hop. Include trust domains, direction, identifier scheme and authentication profile. |
| Version pins | Commit or artifact, relevant library versions, draft revisions, and deployment configuration or fixture IDs. |
| Outcome | Actual decision, reason and enforcement point, actual effect count or observed resource state, and relevant timing. |
| Evidence | Run timestamp, trace ID, sanitized logs, and resource or ledger evidence. |
| Status | Planned, awaiting peer qualification, blocked with reason, unsupported role, inapplicable, pass, or fail. A denial case passes when the denial and observed effect both match its oracle. |
| Claim | Independent wire interop for the named boundary and direction, issuer integration, component interop, or draft-vector conformance. |

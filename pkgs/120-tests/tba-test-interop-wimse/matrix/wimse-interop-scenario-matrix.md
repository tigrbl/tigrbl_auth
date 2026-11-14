# WIMSE agent call chain interop scenario matrix

This matrix turns the [IETF 127 thread](https://mailarchive.ietf.org/arch/msg/wimse/6ofJ6o3sK9H_XEPCQWn_7SVEza4) and its [P1–P8 follow-up](https://mailarchive.ietf.org/arch/msg/wimse/CuZS8gtTTiSPZI8AXSJF_Oy781s) into test cases. It adds WIC/mTLS as an independent profile and defines explicit compositions with each WIT proof. Expected outcomes are proposed test oracles. Record the basis as a pinned draft clause, a proposed draft change, or an explicit test policy.

## Invariants

| ID | Invariant | Evidence |
|---|---|---|
| I1 | The verifier accepts a workload identifier only after validating the credential, its proof of possession, the trust-domain-to-anchor mapping, and the expected peer where applicable. | Authenticated peer URI, trust domain, validation stage. For WIC, record the peer at each TLS termination. |
| I2 | When the selected request proof covers a token or request component, the verifier checks the value received. The harness declares the actual coverage, acceptable audience, and replay policy. | Proof type, coverage and decision. WPT binds the WIT and the Txn-Token when present. HTTP Message Signatures cover the applicable signed components. |
| I3 | A workload identity and authority to perform the operation are separately checked. Delegated authority can only narrow. Autonomous requests follow their own policy. Shared limits hold at their declared accounting point. | Workload principal, authorization mode, grant, scope decision, and accounting result. |
| I4 | A Txn-Token stays in its issuing domain. The destination independently validates the credential issued for it. Correlation IDs never grant authority. | Domain-local token handling, boundary grant and destination access-token decisions, and linked trace records. |
| I5 | When policy requires fresh authorization before an effect, the enforcing service checks before commit. Once it observes revocation, that operation has zero effects. | Initial decision, revocation publication and observation, last allowed operation, first refusal, and resource or ledger state. |
| I6 | Additional commitments are checked at their enforcement boundary. Tool/build pins match the claims presented, required human approval describes the executed action, and bearer release obeys the delegated grant. | Pin or approval decision, bearer-release state, provider decision, and actual effect. |

## Factors

| Factor | Levels |
|---|---|
| TLS peer authentication | Server-authenticated TLS / WIC mutual TLS |
| Application proof | None / WIT + WPT / WIT + HTTP Message Signature |
| Hop layout | Direct inside A / direct A → B / gateway terminates TLS and opens a new hop |
| WIC identifier and issuer | Native WIMSE URI / SPIFFE URI when the certificate and verifier meet the WIC profile; implementations in client and server roles |
| Authority | Autonomous / delegated within scope / delegated out of scope / child receipt expands grant |
| Transaction context | Absent / valid local Txn-Token / valid cross-domain exchange / foreign Txn-Token / binding mismatch |
| Freshness | Current / confirmed revoked / stale cache / unavailable source; revocation before authorization, between authorization and effect, or after bearer release |
| Effect | Protected read / local write / shared-budget operation / human-approved write / bearer-only provider call |
| Fault | None / one targeted invalid condition per row; use a named interaction row when the result depends on several factors |

The core profiles are **C** (WIC/mTLS), **P** (WIT/WPT over TLS), **S** (WIT/HTTP Message Signature over TLS), **CP** (C + P), and **CS** (C + S). Server-authenticated TLS with no application proof is a negative control where authenticated client identity is required. Profiles bind per hop. A gateway is a distinct TLS peer on its outbound connection, so the downstream service must use a separately validated request proof or an explicit trusted identity handoff if it needs the original caller. A valid WIC authenticates the connection peer. For C with transaction context, declare how the authenticated service consumes the token and whether a separate request binding is required. Mark a request-binding assertion inapplicable when that mechanism is absent.

## Scenario matrix

Braces expand to separate executions. For paired rows, keep all unnamed inputs equal to the passing control. **No effect** means no protected response or disclosure for reads and no committed mutation, accounting change, or provider operation for writes. Count successful effects separately in race and replay cases.

| Case | Profile | Layout and condition | Expected result |
|---|---|---|---|
| 01 · Peer identity | {C, P, S, CP, CS} | Direct inside A, valid credential and authorized autonomous operation | Expected identity is authenticated and exactly one intended effect occurs per execution. |
| 02 · Trust isolation | {C, P, S, CP, CS} | Valid credential from an untrusted domain, or wrong trust anchor for its claimed domain | Reject at the affected authentication layer. No effect. In CP/CS, vary each layer independently. |
| 03 · WIC identity selection | {C, CP, CS} | {Missing workload URI SAN, multiple workload URI SANs, wrong expected server identity} | Reject during peer validation, before granting protected access. |
| 04 · TLS termination | {C, CP, CS} | Gateway terminates and re-establishes TLS. Run with a valid configured origin proof or handoff, and with it absent. | B always identifies the gateway as the outbound TLS peer. An operation requiring original caller identity succeeds only with the independently validated proof or handoff. |
| 05 · Application proof required | {P, S, CP, CS} | {Missing proof, wrong proof key, wrong audience} | Reject the request. A valid TLS session alone does not satisfy this profile's application policy. |
| 06 · Application replay | {P, S, CP, CS} | Repeated proof within the validity window with replay rejection enabled | The first request succeeds. The duplicate produces zero additional effects. Record the replay policy and enforcement point. |
| 07 · Transaction binding | {P, S, CP, CS} | Valid local Txn-Token, then a second otherwise valid token substituted after proof generation | Control succeeds. Substitution fails WPT hash or HTTP signature verification. No effect from the substituted request. |
| 08 · Cross-domain chain | {C, P, S, CP, CS} | A → B with configured peer trust and destination access token. Pair with a foreign Txn-Token presented to B. | Valid exchange succeeds and trace evidence shows the Txn-Token stayed in A. Foreign token cannot authorize B's action. P/S/CP/CS verify the applicable token binding on each request. |
| 09 · Authority selection | {C, P, S, CP, CS} | {Autonomous call to delegated-only operation, delegated operation with insufficient scope, in-scope delegated control} | First two cases have no effect. Control produces the intended effect. |
| 10 · Prompt policy | {C, P, S} | Untrusted model input asks for a protected read or credential disclosure. Test harness uses inert input and synthetic protected values. | Authorization or disclosure policy denies the operation. Observe the protected resource and all output sinks in scope. |
| 11 · P1 Status evidence | {C, P, S} | Delegated action with {current, revoked, stale, unavailable} status under a declared fail-closed policy | Current control succeeds. Other cases have no effect. Preserve the reason where observable, or attach controls that establish the cause. Test bounded grace separately only when the selected policy permits it. |
| 12 · P2 Before effect | {C, P, S, CP, CS} | A delegates to B, initial authorization passes, then revoke A and make the update visible before B commits. Pair with no revocation. | Revoked case has zero effects after observation. Control commits once. Measure publication-to-observation and revocation-to-first-refusal separately. Include an already-established mTLS session for C. |
| 13 · P3 Child grant | {C, P, S} | {Narrower child control, wider host, extra method, longer expiry} | Accept the valid control. Reject each wider grant at receipt validation. No effect from the rejected requests. |
| 14 · P4 Shared budget | {C, P, S} | Two services, {independent counters, one authoritative accounting service}; include concurrent requests at the limit | Independent counters demonstrate that a per-service limit does not enforce a shared bound. In the authoritative case, the total committed debits and effects stay at or below N. Also exercise rejection of an ambiguous accounting audience if required by the selected receipt profile. |
| 15 · P5 Proxy rewrite | {S, CS} | {Unchanged request, changed signed authority, changed signed path} through proxy | Original signature verifies only for the unchanged control. A trusted proxy verification handoff, if configured, is a separate case with its own policy and trace. |
| 16 · P6 Tool/build drift | {C, P, S} | {Matching control, changed tool digest, changed build claim} under the pinning policy | Control succeeds. Call-time mismatch prevents the effect. Claim comparison establishes what the issuer asserted. Runtime attestation needs its own evidence. |
| 17 · P7 Approval display | {C, P, S} | {Matching control, OASNT R2 display mismatch} under the approval profile | Valid approval succeeds. R2 fails with display mismatch and no effect. |
| 18 · P8 Bearer release | {C, P, S} | {Valid delegated control, no delegation, read-only grant + write, revocation visible before token release, revocation after token release} | The control succeeds. Three invalid cases release no token and produce no action. After release, record provider behavior separately and measure exposure using provider expiry or revocation controls. |
| 19 · Credential composition | {CP, CS} | Both layers valid with different principals. Run under {required equality, explicitly allowed gateway-to-origin mapping}. | Equality policy rejects. Gateway mapping accepts only the configured pair and records both principals. Treat the composition rule as test policy. |
| 20 · Cross-domain direction | {C, P, S} | Repeat the passing boundary and representative trust and authority refusals with the peer implementations swapped where they implement both roles | Record each direction independently. Mark unsupported role combinations inapplicable with a reason. |

## Expansion and reporting

Coverage by invariant: **I1** → 01–05, 19–20. **I2** → 05–08, 15. **I3** → 09–10, 13–14, 18. **I4** → 08, 20. **I5** → 11–12, 18. **I6** → 16–18.

1. Run passing controls for each profile. Exercise draft-specific vectors separately from independent peer exchanges. For C, run native WIMSE URI and WIC-profile SPIFFE URI as distinct configurations when the peers support them.
2. Expand each explicit set in the matrix. For additional environment combinations, use constrained pairwise coverage over the factor table and retain cases 04, 07, 08, 12, 14, 18, and 19 as explicit interactions. Examples of constraints include WPT requires a WIT, the HTTP signature rewrite case requires the field to be signed, and post-release revocation requires an issued bearer credential.
3. Record scenario ID and factor levels, draft revisions and policy, peer versions and roles, expected decision and reason, actual decision and reason, effect evidence, and trace ID. Use explicit unsupported or inapplicable results with reasons. Use a separate control when a privacy-preserving verifier cannot name the underlying revocation reason.

Draft anchors: [WIMSE workload credentials -03](https://www.ietf.org/archive/id/draft-ietf-wimse-workload-creds-03.html), [mutual TLS -03](https://www.ietf.org/archive/id/draft-ietf-wimse-mutual-tls-03.html), [WPT -02](https://www.ietf.org/archive/id/draft-ietf-wimse-wpt-02.html), [HTTP signatures -08](https://www.ietf.org/archive/id/draft-ietf-wimse-http-signature-08.html), [OAuth identity chaining -17](https://www.ietf.org/archive/id/draft-ietf-oauth-identity-chaining-17.html), [Agent Passport -00](https://www.ietf.org/archive/id/draft-le-agent-passport-00.html#section-7), [OASNT R2](https://www.ietf.org/archive/id/draft-thallapelly-oasnt-02.html#appendix-A.7.2).

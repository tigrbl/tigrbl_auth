# Runtime closure for the 142,844-ID WIMSE matrix

The [published manifest](wimse-interop-all-tba-executions.json.gz) is the scope for this plan. It contains 2,043 one-hop, 11,544 two-hop, and 129,257 three-hop cases. The [native package plan](tba-native-baseline.md) lists the TbA components to reuse and the missing service roles.

## Starting evidence

| Runtime report | Distinct passing cases |
| --- | ---: |
| Original qualified peer matrix | 4,448 |
| Expanded standalone delegation and status runs | 6 |
| [Existing-peer three-call pilot](wimse-triple-call-pilot.xml) | 266 |
| [TbA-only three-call batch with baseline issuers](wimse-interop-all-tba-runtime.xml) | 3,584 |
| **Historical passes matched to the manifest** | **8,304** |
| **Cases without a recorded pass** | **134,540** |

The reports span several pinned TbA revisions. The 8,304 matches establish case-level historical coverage. The final audit requires runtime evidence for the single frozen set of pins selected for closure.

## Delivery tranches

Counts are disjoint ownership groups from the manifest after matching historical passes. A case can depend on more than one tranche. For example, some external endpoint cases also need a new support service.

| Tranche | Cases | Deliverable and acceptance check |
| --- | ---: | --- |
| **0. Freeze the inventory and expose blockers** | All 142,844 | Extend `coverage.py`, `evidence.py`, and `tests/support/blocker_report.py` to report the operation path, directional endpoint baseline, issuer and support bindings, and runtime adapter needed by every ID. Record explicit attempt status and reason. Preserve prior evidence and map the same logical case across pin changes while auditing results by exact pin. Reconcile every ID to one record. |
| **1. Run the existing adapter and qualify short native flows** | 24,136 | Run all **23,408** remaining original-peer three-call cases using `typed_workload_chain.py`. In parallel, wire the **728** native one- and two-hop workload cases with baseline issuers. Reuse `wic_fixture.py`, `wpt_fixture.py`, and the native endpoint factory. Update `qualification_overlay.py` and `tests/peer/conftest.py` to record exact caller and receiver baselines and select native adapters by binding. Exercise the selected profile and the scenario's actual decision and effect oracle. |
| **2. Qualify TbA X.509-SVID and WIT-SVID minting and use** | 46,849 | Bind TbA-issued credentials to the workload fixtures using the existing SPIFFE SVID protocol, X.509-SVID credential, SPIFFE WIT-SVID profile, bundle provider, and JOSE provider. Add a native issuer fixture under `tests/support/` and qualify exact trust domains, identity mappings, profiles, and directions in `qualification_overlay.py`. Run **16,710** WIT-SVID-only cases, **6,261** X.509-SVID-only cases, and **23,878** requiring both. Verify the qualified issuer was used on the wire and the expected wrong-authority cases refuse. |
| **3. Execute the existing typed service flows** | 21,140 | Extend `typed_hop_adapters.py` and reuse `wic_services.py`, `wic_support_cases.py`, and `signature_cases.py`. Start with status checks before, between, and after calls. Then wire delegation and grant redemption, source and destination exchange, and the broker-to-provider sequence. Register exact adapter paths in `tests/peer/conftest.py`. Reuse the same contracts for **14,899** native and **6,241** existing-peer cases. Run baseline-issuer subsets as each adapter lands and SVID subsets after tranche 2. Acquisition flows in this group also depend on the SPIRE Agent adapter in tranche 4. |
| **4. Implement credential acquisition on the wire** | 627 | All **627** native acquisition cases passed with the gRPC `FetchX509SVID` fixture in `tests/support/native_workload_api.py`. It uses the TbA protocol service and selector provider. Workload API delivery succeeded in 521 cases and correctly refused 106 unregistered callers. The next mTLS receiver observed the exact acquired certificate in all 520 cases that continued to a workload call. The [per-ID report](wimse-native-acquisition-results.csv) records both the manifest IDs and the IDs for the qualified runtime version. The 105 specialized cases are tracked in tranche 5. |
| **5. Wire specialized TbA support roles** | 11,276 | The [105 acquisition-dependent executions](wimse-native-specialized-acquisition-results.csv) passed with four local policy fixtures. All 85 issued X.509-SVIDs were observed on the next mTLS hop. The receiver recorded one write in each of 20 allowed flows and zero writes in each of 85 refused flows. The broader tranche covers transaction-token issuance and binding, non-revocation proofs, before-effect enforcement, delegation status and receipts, and approval verification. Reuse the existing TbA token-exchange, revocation and policy packages and the OASNT fixtures. Register the exact service bindings from `peers.toml` and `hops.toml` and verify protected effects. |
| **6. Qualify proposed external workload endpoints** | 27,732 | Qualify go-spiffe and Defakto for SPIFFE mTLS and investigate AgentMaurice's proposed WIT + WPT and HTTP Message Signatures roles. Pin a runnable implementation and configuration, then prove the caller and receiver directions separately. Add peer adapters alongside `wimsey_endpoint.py`, `cofide_endpoint.py`, and `cred_endpoint.py`. The groups include **5,514** go-spiffe-only, **5,514** Defakto-only, **14,312** AgentMaurice-only, and **2,392** mixed-candidate cases. **768** cases also need a support service from tranche 7. |
| **7. Qualify external support services** | 2,780 | Integrate Teleport tbot credential delivery, authgent transaction tokens, MintID status, OmniArx approval, EMILIA enforcement, and Redthread enforcement or receipt verification. Require each actual peer to supply a pinned runnable interface and exercise the role's positive and refusal outcomes. Run the **2,780** cases with existing workload peers and revisit the **768** already counted in tranche 6. |
| **8. Freeze runtime pins and certify the full result set** | All 142,844 | Generate and collect the same inventory with `--expand-hops --include-candidates --include-native` and the final snapshot. Run in batches by hop path and role. Audit the combined results with `--audit-peer-junit`. Publish per-ID outcomes, observations, runtime pins, and the rules used to join the reports. |

Start tranche 1 while tranche 0 lands. Build the WIT-SVID part of tranche 2 first because it enables the largest subset that has no other new issuer dependency. Start partner availability and capability verification for tranches 6 and 7 in parallel. If a proposed peer lacks the modeled capability, record the evidence and treat any replacement or change in matrix scope as an explicit case revision. A TbA substitute has its own result and does not provide that external peer's evidence.

The short native workload group is complete. All 220 one-hop cases and 508 two-hop cases passed after 16 controls qualified the eight baseline profile and identifier combinations. The [per-ID results](wimse-native-short-workload-results.csv) record the observed decision, enforcing hop, events, and resource effects.

All 2,396 specialized native flows with baseline issuers passed across 32 operation paths. Qualification covered 167 flow controls and 16 baseline profile controls. The [per-ID results](wimse-native-baseline-policy-results.csv) record reached hops, decision and effects, and the observed transaction-token and delegation-receipt evidence.

All 8,775 remaining specialized native SVID flows passed. The [per-ID results](wimse-native-svid-policy-results.csv) cover 4,132 WIT-SVID-only cases, 1,683 X.509-SVID-only cases, and 2,960 cases using both. The evidence records credential fingerprints and verification outcomes on reached hops after 389 flow controls and 49 profile controls passed.

The external workload tranche has 11,308 runtime passes and 16,424 blocked IDs. The pass count includes 11,136 go-spiffe and Defakto runs, 64 EMILIA Gate runs, 76 MintID runs, and 32 Teleport tbot runs. AgentMaurice is required on 16,296 of the blocked IDs, including 468 that also need an external support role. The other 128 are split evenly between Redthread and OmniArx and need runnable vendor verifiers. The 2,780 standalone external-support IDs are queued after this tranche. [External workload results](wimse-external-workload-results.csv) [Support-only blocker slice](wimse-external-support-per-id.csv)

## Definition of done

- Every execution produces a runtime observation for its planned path under the frozen pins. Each record includes reached hops, the decision hop, the observed decision or refusal, and the effect count or other applicable resource observation.
- A valid expected refusal passes when the harness observes the correct denial and downstream effects. Unexpected behavior is a case failure to diagnose and rerun. Report blocked, setup-failure, and missing results explicitly. Full execution requires zero in those categories. Full qualification also requires zero unexpected case failures.
- Use distinct native workload and service participants and keep the SPIFFE and WIMSE package boundaries independently usable. Record the reusable package and qualification evidence for each new role as its tranche closes.

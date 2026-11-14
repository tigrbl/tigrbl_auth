# TBA WIMSE interop tests

This Layer 120 test project contains the WIMSE scenario definitions, peer execution plans, and rules for counting combinations.

| File | Purpose |
| --- | --- |
| [Coverage workbook](matrix/wimse-interop-coverage.xlsx) | Factor levels, raw Cartesian matrix, and planned runs |
| [Scenario matrix](matrix/wimse-interop-scenario-matrix.md) | Scenario variants, expected decisions, and observable effects |
| [Execution matrix](matrix/wimse-interop-execution-matrix.md) | Candidate peers, versions, roles, and directions |
| [Factor catalog](src/tba_test_interop_wimse/factors.toml) | Factor levels and required pairings, bundled in the wheel |
| [Exclusions](src/tba_test_interop_wimse/exclusions.toml) | Incompatible combinations, bundled in the wheel |
| [Scenario catalog](src/tba_test_interop_wimse/scenarios.toml) | Named hops, variants, expected event order, decisions, and effects |
| [Peer catalog](src/tba_test_interop_wimse/peers.toml) | Endpoint capabilities by implementation, role, profile, and identifier scheme |

From this package directory, run `uv run tba-test-interop-wimse`. After installing the wheel, run `tba-test-interop-wimse` or `python -m tba_test_interop_wimse`. The command loads the TOML files from the installed package.

Give each factor a stable key under `[factors.<key>]`, a display name, and a list of levels. Each rule has an `id`, a `basis`, and a `when` predicate. When it matches, the `requires` predicate must hold or the `excludes` predicate must be false. Predicates can test a factor's level with `{ factor = "tls", in = ["WIC mutual TLS"] }` or combine predicates using `all`, `any`, and `not`. Keep expected denials in the scenario matrix when a request can occur and the verifier is expected to reject it.

The default command reports scenario families, endpoint capabilities, structural scenarios, and pending and qualified execution rows. Use `--json` to export the generated data and `--legacy-count` to reproduce the flat workbook count. The workbook's Generated Scenarios, Generated Executions, and Peer Capabilities sheets reflect the scoped model. Its Cartesian Matrix and Planned Runs sheets preserve the earlier flat model.

The generator expands authentication settings and issuer modes on each named hop. A terminating or chained call joins the receiving implementation on one hop to the calling implementation on the next. Its scenario variants define the fault target and ordered events. In the bearer fixture, a denied provider call stays in scope when the expected trace has no release. If a structurally valid scenario lacks a matching peer chain, it remains in Generated Scenarios without an execution row.

Qualify a peer capability by entering an exact version and evidence. A capability covers one profile, one role, and one identifier scheme. To qualify issuer or other support roles, add an entry under `qualified_support` in `peers.toml` keyed by the role reported in the execution output. Each entry must include its implementation, version, and evidence. Both endpoint capabilities and all support roles must qualify before an execution row qualifies.

Qualification also requires a configuration pin on each capability and support role, and a passing `[[baselines]]` record for each ordered caller/receiver pair. Each baseline has `outcome = "pass"`, an `evidence` reference, and `caller` and `receiver` tables with implementation, version, configuration, profile, and identifier scheme.

## Verification

Run the tier suites explicitly with `python -m pytest pkgs/120-tests/tba-test-interop-wimse/tests/t0 pkgs/120-tests/tba-test-interop-wimse/tests/t1` from the repository root.

- **T0:** Check every legacy factor level, each flat rule's allowed and excluded inputs, and the scoped catalog contract.
- **T1:** Compare the full scoped inventory against an independent reference enumeration. Check directional eligibility, result reconciliation, and the revocation and bearer-release contracts using synthetic authority and resource fixtures.
- **T2:** Build the wheel and set `TBA_WIMSE_INTEROP_WHEEL` to its absolute path. Run `tests/t2` to compare isolated wheel output with the verified source inventory.
- **T3 pilot:** Run `tests/t3` with the native WIC/mTLS and certificate-status package closure installed from the selected wheels, plus pytest and the Layer 120 workload credential fixtures. The pilot passes a native TLS control and checks the exact rejection reasons for the three identity variants. It covers four local WIC scenarios.

The 3,148 structural keys are exhaustive for the options declared by the current templates. The 20 flat axes are retained for comparison and are not all active independent axes in the templates. Runtime adapters and qualifying evidence for the remaining profiles and families are pending. No external peer pair is qualified. The spreadsheet is a snapshot of the current candidate inventory.

## Candidate peer runs

From the repository root, run:

```sh
python -m pytest pkgs/120-tests/tba-test-interop-wimse/tests/peer --collect-only -q
python -m pytest pkgs/120-tests/tba-test-interop-wimse/tests/peer -o junit_family=xunit1 --junitxml=peer-runs.xml
```

Pytest collects one item per generated execution ID. A single test function joins
each row to its scenario and calls the same runner used by the pilot. The report
retains the full execution ID, scenario ID, and runner result. Blocked items are
reported as skipped with their reason. A skipped item provides no runtime evidence.

Register real peer bindings in the `peer_adapters` fixture. An adapter can cover
multiple variants and families. The runner checks qualification, checks adapter
support, reuses setup controls within each worker, and opens an isolated context
for each row. Its setup key must include every setting that affects the control,
including ordered peer and issuer pins, configuration, and topology. Local
reference adapters belong in the internal tier tests.

The 31 flat rules remain available for comparison through `--legacy-count`. In the scoped model, hop layout handles the topology rules. Profile expansion handles WIC URI and issuer applicability. Variant definitions handle transaction, authority, accounting, and event ordering. The peer join handles role and profile matching. The broker trace exclusion stays explicit in `exclusions.toml`.

| Flat rule IDs | Scoped owner |
| --- | --- |
| `chain-hops`, `direct-hops`, `gateway-hops`, `missing-origin-identity` | Named hop lists and gateway variants |
| `wic-uri-required`, `wic-uri-inapplicable`, `issuer-wit`, `issuer-wic` | Per-hop profile and issuer expansion |
| `wic-faults`, `application-faults`, `identity-comparison`, `signature-rewrite`, `token-binding` | Target hop, verification layer, and family profile list |
| `token-domain`, `child-grant`, `human-display`, `human-effect`, `protected-read-attempt`, `read-only-write` | Typed scenario topology and named variants |
| `shared-accounting`, `shared-counter` | Shared budget variants and explicit accounting and schedule levels |
| `bearer-release`, `post-release`, `denied-broker-no-release`, `fail-closed-broker-visible-revocation` | Ordered provider events and the broker trace exclusion |
| `peer-profile-1` through `peer-profile-6` | Capability matching by profile, scheme, version, and role |

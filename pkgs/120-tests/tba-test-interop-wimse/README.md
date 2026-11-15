# TBA WIMSE interop tests

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-test-interop-wimse/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-test-interop-wimse/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-test-interop-wimse/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/120-tests"><img alt="Layer: 120 tests" src="https://img.shields.io/badge/Layer-120%20tests-0a7f5a"></a>
<a href="https://pypi.org/project/tba-test-interop-wimse/"><img alt="PyPI version for tba-test-interop-wimse" src="https://img.shields.io/pypi/v/tba-test-interop-wimse?label=tba-test-interop-wimse%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-test-interop-wimse"><img alt="Monthly PyPI downloads for tba-test-interop-wimse" src="https://static.pepy.tech/badge/tba-test-interop-wimse/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-test-interop-wimse/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

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

### Run either side of the WIC/mTLS fixture

Install the package with the `wic` extra using the selected TbA wheels. For
example, with a fixture wheelhouse use
`pip install --no-index --find-links ./wheelhouse "tba-test-interop-wimse[wic]==0.4.0.dev2"`.
The Python API exposes `WicCaller`, `WicReceiver`, and `WorkloadVerifier` from
`tba_test_interop_wimse.wic`. `WorkloadVerifier` accepts a certificate status
provider. `WicReceiver` accepts a resource implementing `commit(identity)`
and `snapshot()` and defaults to an in-memory ledger.

Give each role a JSON configuration with its own leaf and key, the TLS trust
anchor, its expected peer URI, and explicitly approved peer leaf certificates.
The fixture currently accepts direct issuance by the configured domain anchor.
Example caller configuration:

```json
{
  "tls": {
    "certificate": "caller.pem",
    "private_key": "caller.key",
    "trust_anchor": "test-ca.pem"
  },
  "expected_peer": "wimse://example.org/receiver",
  "domain_anchors": {"example.org": "test-ca.pem"},
  "good_certificates": ["receiver.pem"],
  "host": "127.0.0.1",
  "port": 8443,
  "dns_name": "receiver.example.org"
}
```

For the receiver configuration, supply its leaf and key, the expected caller
URI, and the caller certificate under `good_certificates`. Match the server
leaf's DNS SAN to the caller's `dns_name`. Run:

```sh
tba-wimse-wic-fixture receive receiver.json
tba-wimse-wic-fixture call caller.json
tba-wimse-wic-fixture readback caller.json
```

The receiver listens on loopback and prints its port as JSON. Use `"port": 0`
to allocate one automatically. A partner caller can use its own mTLS client to
send `POST /writes` and `GET /effects`. A partner receiver can implement those
same endpoints for the TbA caller. An allowed write returns HTTP 201 and the
authenticated workload URI. Readback returns HTTP 200 and the committed
identities. A workload identity refusal after a TLS handshake returns HTTP 403
from the receiver, or a `server-identity` denial from the TbA caller. If a
partner receiver provides a different contract, use its own resource readback.

### Run either side of the WIT/WPT fixture

Install `tba-test-interop-wimse[wpt]` from the selected wheelhouse. Import
`WptCaller` or `WptReceiver` from `tba_test_interop_wimse.wpt`, or use
`tba-wimse-wpt-fixture receive receiver.json`, `call caller.json`, and
`readback caller.json`. The receiver binds loopback. Both roles share the
WIC fixture's protected write and readback routes. HTTPS authenticates the
server by its DNS name. TbA authenticates the caller using WIT/WPT.

Receiver JSON takes `certificate`, `private_key`, `dns_name`, optional
`port` (zero selects a port), and `trust_by_domain` (a map from trust domain
to trusted issuer JWKs). Caller JSON takes `host` (defaults to loopback),
`port`, `dns_name`, `trust_anchor`, `wit_file`, and `private_key` (the PEM
proof key bound to the WIT). TLS file paths and key files are supplied by the
operator. The receiver checks the audience against its configured DNS name,
listening port, and the requested fixture route.

The local T3 suite uses TbA for both endpoints with separate TLS, issuer,
and proof keys. It exercises all five profiles and all eight profile/scheme
configurations in the baseline inventory. The 52 structural rows include
positive writes and readback, applicable identity and proof refusals, replay,
and the combined-profile identity equality policy. The replay case verifies
one committed write and no additional effect from the duplicate.

For WIT/HTTP signatures, use `SignatureCaller` and `SignatureReceiver` from
`tba_test_interop_wimse.httpsig`. This is the Ed25519, single-signature,
bodyless GET/POST subset of [the WIMSE HTTP signature draft -08](https://www.ietf.org/archive/id/draft-ietf-wimse-http-signature-08.html).
It does not implement signed responses, CONNECT, or the general signature
grammar. For a composition, use `CombinedCaller` with a WIC verifier and
the selected application caller. Supply both transport credentials and a
client verifier to the receiver. It requires the identities to be equal or
to match an exact configured pair. Use the `spiffe-wic` extra alongside
`wic` for `SpiffeWicVerifier`. The mixed SPIFFE setup keeps the WIT in the
native WIMSE namespace and configures the corresponding pair explicitly.
The SPIFFE client authenticates the expected workload URI after TLS chain
validation. The native WIMSE fixture also validates the TLS DNS name.

### Run the candidate inventory

Run `tba-test-interop-wimse --coverage` for a JSON inventory of every
structural scenario and peer execution ID. Add `--attempts attempts.json`
to reconcile peer results. The file is a JSON array with an `execution_id`,
positive integer `attempt`, and `status` per entry. Component tests are
evidence for the behavior they exercise and do not populate this file as
complete execution attempts.

The first component slices are opt-in:

- Set `TBA_WIMSEY_CHECKOUT` to a checkout of
  `56b070582f3e380c5006630698fb4ca808c08b04` built with
  `cargo build --locked -p wimsey-cli`. Run
  `tests/peer/test_wimsey_wic_component.py` with the
  WIC dependencies and Layer 120 certificate fixture available. This pairs
  the wimsey WIC verifier with TbA's verifier over the shared TLS fixture,
  recording which engine made the decision at the checked endpoint.
  `tests/peer/test_wimsey_http_signature.py` verifies request signatures
  in both directions against the same pinned CLI with synthetic inputs.
- Set `CRED_SDK_CHECKOUT` to the built revision described in the Cred
  testkit README and make that testkit and its WIT/WPT dependencies
  available. Run `tests/peer/test_baselines.py`. This exercises the pinned
  Cred verifier over loopback HTTP and checks the protected read response
  for the control, proof refusals, and duplicate presentation.

These checks belong to the external interop evidence track. The fixture
manifest identifies them as component bindings. Complete
candidate runs still require the pinned endpoint configuration and
directional baseline defined in the peer catalog.

From the repository root, run:

```sh
python -m pytest pkgs/120-tests/tba-test-interop-wimse/tests/peer --collect-only -q
python -m pytest pkgs/120-tests/tba-test-interop-wimse/tests/peer -o junit_family=xunit1 --junitxml=peer-runs.xml
```

For full-inventory validation, report only the candidate execution tests and
audit their results against the current catalog:

```sh
python -m pytest pkgs/120-tests/tba-test-interop-wimse/tests/peer/test_candidate_executions.py -o junit_family=xunit1 --junitxml=candidates.xml
tba-test-interop-wimse --audit-peer-junit candidates.xml
```

The audit exits 1 for an incomplete inventory. Use `--json` with the audit
to include each execution's status and observations.

For a local peer lab run, put the package's `src` and `tests` directories
on the Python path and configure `TBA_WIMSEY_CHECKOUT` and
`TBA_WIMSE_PEER_SNAPSHOT` (an output JSON path). Run
`python -m support.qualification_overlay` before pytest. This runs four
positive controls for the native WIMSE and SPIFFE WIC configurations,
in both directions, and captures the exact fixture source and wimsey
binary digests. It also records qualification of the ephemeral direct
test CA for that WIC configuration. The peer suite consumes the snapshot
through the same environment variable. Pass its path to the auditor
with `--peer-snapshot` so evidence is matched to the pinned execution IDs.
These are local lab results. Independent operator evidence and promotion
follow ADR-1011 and ADR-1023.

The direct WIC lab adapter also runs scenarios 09, 10, 11, 13, and 16
with baseline CA trust in both TbA/wimsey directions and both identifier
schemes. Peer verifiers run over mutual TLS. The shared test resource
owns the application policies, including synthetic delegation status,
protected operations, child grants, and tool and build claim checks.
The harness checks the rejection reason and reads back the resource
ledger over HTTPS after each policy request.

The same lab snapshot qualifies the shared support fixtures for gateway
origin handling, token exchange, revocation before effect, shared
accounting, approval display, and bearer release. Qualification executes
issuer controls in both directions and exercises every supported policy
variant before recording a role. The approval fixture verifies the
published V5 and R2 vectors from OASNT draft -02 Appendix A against its
enrolled test key and fixed clock.

Set `TBA_WIMSE_SPIRE=1` when building the snapshot to include the
SPIRE issuer. The lab uses the pinned local SPIRE 1.16.0 server image in a
disposable container with no external network. It exercises server-minted
X.509-SVIDs and their trust bundle. For malformed SAN and foreign domain
cases, it injects a separate fixture leaf into the peer input while keeping
the receiver's SPIRE workload trust pin. The issuer role covers the
server-mint path. Agent attestation and Workload API delivery are outside
that qualification. Cross-domain application issuers, budget and status
authorities, and the bearer provider are local test fixtures.

Set `TBA_WIMSE_COMBINED_SIGNATURE=1` to fill the combined-signature
candidate slot for the SPIFFE profile in the lab snapshot. In each direction
the control sends a signed write and independently reads the ledger over
mutual TLS. The wimsey side uses its pinned WIC verifier and HTTP signature
CLI. The shared fixture supplies the HTTPS resource, replay state, and
the mapping between the authenticated SPIFFE identity and the WIMSE WIT.
The controls cover the lab CA and, when enabled, SPIRE server-minted
X.509-SVIDs. Set `TBA_WIMSE_SPIRE_WIT=1` alongside
`TBA_WIMSE_SPIRE=1` to qualify the separate SPIRE WIT-SVID issuer. The
SPIRE server mints ES256 WIT-SVIDs with SPIFFE subjects, and the fixture
loads the matching WIT authority from the SPIFFE bundle. Separate
ephemeral SPIRE servers provide wrong-anchor and foreign-domain
credentials for denial cases. These controls exercise the SPIRE server
mint interface. Workload API delivery requires its own qualification.

Set `TBA_WIMSE_COMBINED_SIGNATURE_WIMSE=1` to qualify the WIMSE URI
variant in both directions. A lab CA issues the WIMSE transport
certificates. The application identity is either a lab-issued WIMSE
WIT or a server-minted SPIFFE WIT-SVID. The latter uses an explicit
mapping from the WIMSE transport identity to the SPIFFE subject.
When the other combined profiles are enabled, the support controls
exercise both orders of the eligible mixed-profile and mixed-identifier
chains.

The combined adapter also covers gateway origin handling, transaction
binding, delegated authority, proxy rewrites, cross-domain exchange,
revocation before effect, and gateway identity mapping. Its two-hop
controls exercise the supported arrangements of WIC-only and
combined-signature endpoints. The cross-domain token issuers, status
authority, effect store, and proxy handoff use local test fixtures.

Set `TBA_WIMSE_COMBINED_WPT=1` to also qualify the SPIFFE combined WPT
candidate slot with wimsey. This builds a small offline command-line
bridge against the pinned wimsey WIT and WPT crates. The bridge receives
the request's Txn-Token and destination access token and uses wimsey's
WPT binding APIs. The suite pins the bridge binary digest in the
qualification snapshot. Both directions exercise the four baseline
and SPIRE issuer combinations. The support controls also cover
chains with WPT, WIC-only, and HTTP-signature hops. The lab harness
provides HTTPS, replay state, the local support services, and ES256
proof signing on the TbA side for SPIRE-minted WIT-SVIDs.

Set `TBA_WIMSE_COMBINED_WPT_WIMSE=1` to qualify the WIMSE transport URI
variant in both directions using the same bridge. The lab CA issues
the transport certificates. The application proof uses a lab-issued WIMSE
WIT or a SPIRE server-minted WIT-SVID with a mapped SPIFFE subject.
With the other combined profiles enabled, qualification also exercises
WIMSE and SPIFFE hops together and both orders of the eligible mixed
WPT and HTTP-signature chains.

Set `TBA_WIMSE_COFIDE_BRIDGE` to the path of the compiled
`tests/support/cofide_bridge.go` executable to qualify Cofide in the
shared HTTPS lab. Build it in a temporary Go module using the pinned
Cofide checkout at `7984a60105002dc65b31e9cd08572cd5d10ed9d6` as the
replacement for `github.com/cofide/wimse-s2s-httpsig-poc`. Seed the
temporary module with the checkout's `go.mod` and `go.sum`, change its
module name, add a requirement on the replaced module, and build the
bridge with Go 1.25.3. The qualification snapshot pins the resulting
binary digest.

The bridge uses the prototype's Go signing function and its pinned
P-256 verification library. The lab profile signs the method,
request target, destination authority, WIT, and any applicable
authorization or transaction token headers. TbA checks the WIT issuer,
freshness, and replay state. The lab uses its own HTTPS endpoints and
support services. This qualification covers request signatures with
a lab-issued WIT or SPIRE server-minted WIT-SVID.

Set `TBA_WIMSE_CRED_CHECKOUT` to a clean Cred SDK checkout at
`586e1a76f487c2376e0ba0a4687bb2de8d3eb588` with its pinned dependencies
installed. Qualification builds Cred's identity modules and exposes its
demo client's signing function in a temporary adapter beside the snapshot.
The snapshot pins the generated modules and bridge. The adapter uses
Cred's WIT and WPT verification, with the lab supplying HTTPS, replay
state, token issuance and resource effects. Its caller signs the WPT for
the lab request URI and binds any transaction or destination access token.

The same checkout qualifies Cred independently as a second WIT + HTTP
Message Signatures peer alongside Cofide. For draft-08 requests, both
TbA → Cred and Cred → TbA exercise a baseline request, a request with a
valid signed transaction JWT, and a request with a second valid
transaction JWT substituted after signing. Each valid request records
one write. Each substitution fails signature verification and records
zero writes. These controls use direct HTTPS with a lab-issued WIT and
bodyless requests. To run them without building the other peers, run
`python -m pytest tests/peer/test_cred_http_signature.py` from the
package directory with `TBA_WIMSE_CRED_CHECKOUT` set.

After the candidate run, use
`python -m support.blocker_report snapshot.json candidates.xml` to count
remaining blockers. It reports the overlap between missing runtime
adapters, directional baselines, and issuer or support roles, so one row
can appear in several categories. Trust isolation is exercised by
holding the TLS CA fixed and varying the workload identity or its
configured workload anchor.

Run `tests/t3/test_structural_runtime.py` for one native result per
structural scenario. The native adapter registry is separate from the
peer lab registry. Rows without a runtime binding appear as skipped.

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

## Quick start

Run the suite from the repository root.

```bash
uv run --extra test python -m pytest pkgs/120-tests/tba-test-interop-wimse/tests
```

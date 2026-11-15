"""Default bindings for the peer suite. Local reference fixtures stay separate."""

import pytest
import json
import os
from pathlib import Path
from contextlib import nullcontext
from hashlib import sha256


@pytest.fixture(scope="session")
def peer_snapshot():
    location = os.getenv("TBA_WIMSE_PEER_SNAPSHOT")
    return json.loads(Path(location).read_text(encoding="utf-8")) if location else None


@pytest.fixture(scope="session")
def cred_http_signature_adapter(peer_snapshot, tmp_path_factory):
    from support.cred_endpoint import CredHttpSignatureAdapter, bridge_digest
    from support.qualification_overlay import wic_source_digest

    if not peer_snapshot.get("cred_http_signature_controls"):
        pytest.fail("Snapshot lacks Cred HTTP signature controls")
    location = Path(os.environ["TBA_WIMSE_PEER_SNAPSHOT"]).resolve()
    bridge = location.with_suffix(".cred") / "cred_bridge.mjs"
    if bridge_digest(bridge) != peer_snapshot["cred_bridge_sha256"]:
        pytest.fail("Cred bridge differs from the qualified snapshot")
    if not any(row["implementation"] == "tba" and row["profile"] == "wit-http-signature"
               and row.get("version") == "sha256:" + wic_source_digest()
               for row in peer_snapshot["peers"]["capabilities"]):
        pytest.fail("TbA fixture sources differ from the qualified snapshot")
    return CredHttpSignatureAdapter(tmp_path_factory.mktemp("cred-httpsig"), bridge)


@pytest.fixture(scope="session")
def peer_adapters(peer_snapshot, tmp_path_factory):
    """Map scenario family IDs to adapters backed by real peer deployments."""
    if not peer_snapshot:
        yield {}
        return
    from support.qualification_overlay import wic_source_digest
    from support.cred_endpoint import bridge_digest
    from support.wimsey_endpoint import WimseyWicAdapter
    from support.wimsey_signature_endpoint import PeerLabAdapter, WimseySignatureAdapter

    from support.spire_issuer import IMAGE, spire_issuer, spire_wit_issuers

    directory = tmp_path_factory.mktemp("peer-runtime")
    if peer_snapshot.get("spire_image") not in (None, IMAGE):
        pytest.fail("SPIRE image differs from the qualified snapshot")
    if peer_snapshot.get("spire_wit_svid"):
        issuer_context = spire_wit_issuers(directory)
    else:
        issuer_context = spire_issuer(directory) if peer_snapshot.get("spire_image") else nullcontext()
    with issuer_context as issuer:
        adapter = WimseyWicAdapter(directory, os.environ["TBA_WIMSEY_CHECKOUT"], issuer)
        if adapter.binary_sha256 != peer_snapshot["wimsey_binary_sha256"]:
            pytest.fail("wimsey binary differs from the qualified snapshot")
        if not any(row.get("version") == "sha256:" + wic_source_digest()
                   for row in peer_snapshot["peers"]["capabilities"]
                   if row["implementation"] == "tba"):
            pytest.fail("TbA fixture sources differ from the qualified snapshot")
        bridge = None
        has_wimse_wpt = bool(peer_snapshot.get("combined_wpt_wimse_controls"))
        if peer_snapshot.get("combined_wpt_controls") or has_wimse_wpt:
            bridge = adapter.binary.with_name("tba-wimsey-wpt-bridge" + adapter.binary.suffix)
            if sha256(bridge.read_bytes()).hexdigest() != peer_snapshot["wimsey_wpt_bridge_sha256"]:
                pytest.fail("wimsey WPT bridge differs from the qualified snapshot")
        has_wimse_signature = bool(peer_snapshot.get("combined_signature_wimse_controls"))
        has_signature = bool(peer_snapshot.get("combined_signature_controls")) or has_wimse_signature
        cofide = None
        if peer_snapshot.get("cofide_controls"):
            cofide = Path(os.environ["TBA_WIMSE_COFIDE_BRIDGE"]).resolve()
            if sha256(cofide.read_bytes()).hexdigest() != peer_snapshot["cofide_bridge_sha256"]:
                pytest.fail("Cofide bridge differs from the qualified snapshot")
        cred = None
        if peer_snapshot.get("cred_controls"):
            path = Path(os.environ["TBA_WIMSE_PEER_SNAPSHOT"]).resolve()
            cred = path.with_suffix(".cred") / "cred_bridge.mjs"
            if bridge_digest(cred) != peer_snapshot["cred_bridge_sha256"]:
                pytest.fail("Cred bridge differs from the qualified snapshot")
        signature = (WimseySignatureAdapter(directory, adapter.binary, issuer,
                                            wpt_bridge=bridge, signature=has_signature,
                                            wimse_signatures=has_wimse_signature, wimse_wpt=has_wimse_wpt,
                                            cofide_bridge=cofide, cred_bridge=cred)
                     if has_signature or bridge or cofide or cred else None)
        lab = PeerLabAdapter(adapter, signature)
        yield dict.fromkeys(lab.families, lab)


@pytest.fixture(scope="session")
def spiffe_peer_adapter(request, peer_snapshot, tmp_path_factory):
    from external_workload_selection import defakto_digest
    from support.go_spiffe_endpoint import SpiffePeerAdapter

    evidence = peer_snapshot["go_spiffe_qualification"]
    binary = Path(os.environ["TBA_WIMSE_GO_SPIFFE_BRIDGE"]).resolve()
    if sha256(binary.read_bytes()).hexdigest() != evidence["binary_sha256"]:
        pytest.fail("go-spiffe bridge differs from the qualified snapshot")
    commands = {"go-spiffe": [str(binary), "verify"]}
    if defakto := peer_snapshot.get("defakto_qualification"):
        bridge = Path(os.environ["TBA_WIMSE_DEFAKTO_BRIDGE"]).resolve()
        if defakto_digest(bridge) != defakto["bridge_sha256"]:
            pytest.fail("Defakto SDK bridge differs from the qualified snapshot")
        commands["defakto"] = ["node", str(bridge)]
    if os.getenv("TBA_WIMSE_GO_SPIFFE_ONLY") in {"teleport", "mintid"}:
        from support.spire_issuer import spire_issuer

        directory = tmp_path_factory.mktemp("spiffe-peer-runtime")
        with spire_issuer(directory) as issuer:
            yield SpiffePeerAdapter(None, commands, peer_snapshot["peers"], directory=directory, issuer=issuer)
    else:
        peer_adapters = request.getfixturevalue("peer_adapters")
        yield SpiffePeerAdapter(peer_adapters["01"].signature, commands, peer_snapshot["peers"])


@pytest.fixture(scope="session")
def peer_setup_cache():
    return {}


@pytest.fixture(scope="session")
def peer_workload_api(peer_adapters, tmp_path_factory):
    from support.spire_workload_api import spire_workload_api

    issuer = peer_adapters["01"].wic.issuer
    with spire_workload_api(issuer, tmp_path_factory.mktemp("workload-api")) as agent:
        yield agent


@pytest.fixture(scope="session")
def native_qualified_issuers(peer_snapshot):
    if not peer_snapshot:
        return set()
    from support.qualification_overlay import wic_source_digest
    from tba_test_interop_wimse.native_expansion import COMBINED_RECORD, COMBINED_SCOPE, NATIVE_ISSUERS

    version = "sha256:" + wic_source_digest()
    qualified = {
        issuer for issuer, (_, key) in NATIVE_ISSUERS.items()
        if (controls := peer_snapshot["peers"].get(key, {})).get("evidence")
        and controls.get("version") == version
    }
    combined = peer_snapshot["peers"].get(COMBINED_RECORD, {})
    if NATIVE_ISSUERS.keys() <= qualified and combined.get("version") == version and combined.get("evidence"):
        qualified.add(COMBINED_SCOPE)
    return qualified


@pytest.fixture(scope="session")
def native_workload_adapters(peer_snapshot, native_qualified_issuers, tmp_path_factory):
    from support.native_workload_endpoint import NativeSvidWorkloadAdapter
    from support.qualification_overlay import wic_source_digest
    from tba_test_interop_wimse.native_expansion import BASELINE_WORKLOAD_RECORD, COMBINED_SCOPE

    baseline = (peer_snapshot or {}).get("peers", {}).get(BASELINE_WORKLOAD_RECORD, {})
    baseline_qualified = bool(
        baseline.get("evidence") and baseline.get("version") == "sha256:" + wic_source_digest()
    )
    if not native_qualified_issuers and not baseline_qualified:
        return {}

    adapter = NativeSvidWorkloadAdapter(
        tmp_path_factory.mktemp("native-workload"),
        wit_qualified="tba-wit-svid" in native_qualified_issuers,
        x509_qualified="tba-x509-svid" in native_qualified_issuers,
        combined_qualified=COMBINED_SCOPE in native_qualified_issuers,
        baseline_qualified=baseline_qualified,
    )
    return dict.fromkeys(adapter.families, adapter)


@pytest.fixture(scope="session")
def typed_hop_adapters(request, peer_snapshot, tmp_path_factory):
    from support.typed_hop_adapters import LocalDelegationAdapter, LocalStatusAdapter
    from support.typed_service_bindings import TypedServiceBindings
    from support.typed_service_flow import TypedServiceFlow

    adapters = {("check",): LocalStatusAdapter(), ("delegate",): LocalDelegationAdapter()}
    acquisition_mode = os.getenv("TBA_WIMSE_NATIVE_ACQUISITION")
    policy_mode = os.getenv("TBA_WIMSE_NATIVE_BASELINE_POLICY")
    qualifying = os.getenv("TBA_WIMSE_SERVICE_CONTROLS") == "1"
    if (peer_snapshot and (os.getenv("TBA_WIMSEY_CHECKOUT") or peer_snapshot.get("teleport_qualification")
                          or peer_snapshot.get("mintid_qualification"))
            and acquisition_mode not in {"1", "specialized"}
            and policy_mode not in {"1", "svid"}):
        from types import SimpleNamespace
        from support.typed_workload_chain import TypedWorkloadChain

        def get_lab():
            if peer_snapshot.get("go_spiffe_qualification"):
                return SimpleNamespace(signature=request.getfixturevalue("spiffe_peer_adapter"))
            return request.getfixturevalue("peer_adapters")["01"]

        adapters[("call", "call", "call")] = TypedWorkloadChain(
            peer_snapshot["peers"], get_lab,
        )
        adapters[("service",)] = TypedServiceFlow(
            adapters[("call", "call", "call")], TypedServiceBindings,
            agent_factory=lambda: request.getfixturevalue("peer_workload_api"),
        )
        if emilia := peer_snapshot.get("emilia_qualification"):
            from external_workload_selection import endpoint_candidates
            from support.emilia_endpoint import OPERATION, EmiliaBindings, bridge_digest

            bridge = Path(os.environ["TBA_WIMSE_EMILIA_BRIDGE"]).resolve()
            if bridge_digest(bridge) != emilia["bridge_sha256"]:
                pytest.fail("EMILIA Gate bridge differs from the qualified snapshot")

            class EmiliaFlow(TypedServiceFlow):
                def supports(self, execution):
                    return (endpoint_candidates(execution) in ({"go-spiffe"}, {"defakto"})
                            and super().supports(execution))

            flow = EmiliaFlow(adapters[("call", "call", "call")], EmiliaBindings, agent_factory=lambda: bridge)
            adapters[("call", OPERATION)] = flow
            adapters[("call", "call", OPERATION)] = flow
        if teleport := peer_snapshot.get("teleport_qualification"):
            from support.teleport_endpoint import OPERATION, TeleportBindings, TeleportWorkloadAPI

            def teleport_agent():
                issuer = request.getfixturevalue("spiffe_peer_adapter").issuer
                agent = TeleportWorkloadAPI(os.environ["TBA_WIMSE_TELEPORT_CONTAINER"],
                                            tmp_path_factory.mktemp("teleport-svid"), issuer)
                if agent.image() != teleport["image"]:
                    pytest.fail("Teleport container image differs from the qualified snapshot")
                return agent

            flow = TypedServiceFlow(adapters[("call", "call", "call")], TeleportBindings,
                                    agent_factory=teleport_agent)
            adapters[(OPERATION, "call")] = flow
            adapters[(OPERATION, "call", "call")] = flow
        if peer_snapshot.get("mintid_qualification"):
            from mintid_endpoint import DECISION_TIMEOUT, OPERATION, MintIDBindings

            flow = TypedServiceFlow(adapters[("call", "call", "call")], MintIDBindings,
                                    agent_factory=lambda: os.environ["TBA_WIMSE_MINTID_CONTAINER"],
                                    workload_response_timeout=DECISION_TIMEOUT + 30)
            adapters[("call", OPERATION)] = flow
            adapters[("call", "call", OPERATION)] = flow
    if peer_snapshot and os.getenv("TBA_WIMSE_INCLUDE_NATIVE") == "1":
        from support.qualification_overlay import wic_source_digest
        from support.typed_workload_chain import TypedWorkloadChain
        from tba_test_interop_wimse.native_expansion import COMBINED_SCOPE

        version = "sha256:" + wic_source_digest()
        capabilities = [
            row for row in peer_snapshot["peers"]["capabilities"]
            if row["implementation"] == "tba" and row.get("version") == version
        ]
        if capabilities:
            issuers = request.getfixturevalue("native_qualified_issuers")
            chain = TypedWorkloadChain(
                {"capabilities": capabilities}, native_directory=tmp_path_factory.mktemp("native-typed"),
                native_wit_svid="tba-wit-svid" in issuers,
                native_x509_svid="tba-x509-svid" in issuers,
                native_combined_svid=COMBINED_SCOPE in issuers,
            )
            adapters[("native", "call", "call", "call")] = chain
            bindings, agent_factory = TypedServiceBindings, None
            if (peer_snapshot.get("native_acquisition_qualification")
                    or (acquisition_mode == "1" and qualifying)):
                from support.typed_service_bindings import NativeAcquisitionBindings

                bindings = NativeAcquisitionBindings
                agent_factory = lambda: request.getfixturevalue("tba_workload_api")
            adapters[("native", "service")] = TypedServiceFlow(
                chain, bindings, agent_factory=agent_factory,
            )
            if (peer_snapshot.get("native_specialized_acquisition_qualification")
                    or (acquisition_mode == "specialized" and qualifying)):
                from support.native_acquired_policy import NativeAcquiredPolicyBindings, SUPPORT

                specialized = TypedServiceFlow(
                    chain, NativeAcquiredPolicyBindings,
                    agent_factory=lambda: request.getfixturevalue("tba_workload_api"),
                )
                for operation in SUPPORT:
                    adapters[("native", "acquire", "call", operation)] = specialized
            baseline_policy = peer_snapshot.get("native_baseline_policy", {})
            svid_policy = peer_snapshot.get("native_svid_policy", {})
            policy_records = {
                mode: record for mode, record in (("1", baseline_policy), ("svid", svid_policy))
                if record.get("version") == version and (
                    record.get("evidence") or (qualifying and policy_mode == mode)
                )
            }
            if policy_records:
                from support.native_specialized_services import NativeSpecializedBindings
                from typed_service_selection import native_baseline_policy_case, native_svid_policy_case

                class NativePolicyFlow(TypedServiceFlow):
                    def supports(self, execution):
                        record = policy_records.get("svid" if native_svid_policy_case(execution) else "1")
                        path = [hop["operation"] for hop in execution["hops"]]
                        return bool(record and path in record["paths"] and (
                            native_svid_policy_case(execution) or native_baseline_policy_case(execution)
                        ) and super().supports(execution))

                policy_flow = NativePolicyFlow(chain, NativeSpecializedBindings, record_svids="svid" in policy_records)
                for record in policy_records.values():
                    for path in record["paths"]:
                        adapters[("native", *path)] = policy_flow
    return adapters


@pytest.fixture(scope="session")
def tba_workload_api():
    from support.native_workload_api import native_workload_api

    with native_workload_api() as api:
        yield api

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
def peer_setup_cache():
    return {}

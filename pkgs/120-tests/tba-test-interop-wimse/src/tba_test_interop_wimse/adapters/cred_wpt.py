"""Observe Cred's protected read through the existing pinned peer helper."""


def check_protected_read(peer, tokens, variant):
    wit = tokens.issue_wit()
    audience = peer.audience + "/wrong" if variant == "wrong-audience" else peer.audience
    headers = tokens.request_headers(wit, audience, wrong_key=variant == "wrong-proof-key")
    if variant == "missing-proof":
        headers.pop("Authorization")
    if variant in {"valid-peer", "first-presentation", "duplicate-presentation"}:
        status, payload = peer.connections(headers)
        assert status == 200, payload
        assert {entry["slug"] for entry in payload["connections"]} == {"google"}
    if variant not in {"valid-peer", "first-presentation"}:
        status, payload = peer.connections(headers)
        assert status == 401 and payload["error"] == "invalid_workload_identity", payload
        assert "connections" not in payload
    return {"http_status": status, "protected_read": status == 200,
            "initial_read": variant == "duplicate-presentation"}

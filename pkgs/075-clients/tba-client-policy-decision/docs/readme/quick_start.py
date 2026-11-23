from tba_client_policy_decision import PolicyDecisionClient

client = PolicyDecisionClient(
    request=lambda payload: {"allowed": payload["action"] == "read"}
)
assert client.decide({"action": "read"}) == {"allowed": True}
assert client.decide({"action": "write"}) == {"allowed": False}

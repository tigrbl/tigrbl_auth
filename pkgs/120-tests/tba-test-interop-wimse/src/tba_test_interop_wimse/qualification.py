"""Match independently evidenced baselines to exact ordered endpoints."""

def pair_has_baseline(peers, pair):
    pins = ("implementation", "version", "configuration", "profile", "identifier_scheme")
    return any(
        baseline.get("outcome") == "pass" and baseline.get("evidence")
        and all(
            all(pair[role].get(pin) and pair[role][pin] == baseline.get(role, {}).get(pin)
                for pin in pins)
            for role in ("caller", "receiver")
        )
        for baseline in peers.get("baselines", [])
    )

from tba_durability_replay_protection import RUNTIME_OPERATION_BY_ALIAS

aliases = sorted(RUNTIME_OPERATION_BY_ALIAS)
assert aliases
print(*aliases, sep="\n")

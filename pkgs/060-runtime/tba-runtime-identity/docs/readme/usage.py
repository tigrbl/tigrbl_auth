from tba_runtime_identity.profile_loader import load_runtime_profile
from tba_runtime_identity import registered_runner_names

profile = load_runtime_profile("default")
runners = registered_runner_names()

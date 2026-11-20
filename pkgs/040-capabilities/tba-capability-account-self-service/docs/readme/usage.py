import asyncio

from tba_capability_account_self_service import AccountSelfServiceCapability
from tba_contracts_identity.account_self_service import AccountPrincipal, AccountProfile


def read_profile(principal):
    return AccountProfile(
        principal.identity_id, "tenant", "alice", "alice@example.test"
    )


def unbound(*args):
    raise NotImplementedError("profile-only demo")


account = AccountSelfServiceCapability(
    profile_reader=read_profile,
    profile_updater=unbound,
    password_changer=unbound,
    session_lister=unbound,
    session_revoker=unbound,
    consent_lister=unbound,
    consent_revoker=unbound,
    authorized_app_revoker=unbound,
)
profile = asyncio.run(account.get_profile(AccountPrincipal("identity", "tenant")))
assert profile.username == "alice"

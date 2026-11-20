from tba_bases_authenticator import AuthenticatorBase

base = AuthenticatorBase(kind="password_local", factor_class="knowledge", amr=("pwd",))
assert base.supported_amr() == ("pwd",)
assert base.metadata().challenge_based is False

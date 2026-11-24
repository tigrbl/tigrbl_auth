from tba_runtime_mfa_lifecycle import FactorBinding

binding = FactorBinding('example-scope', 'account-1', 'totp', 'settings-enrollment')
assert binding.subject == 'account-1'

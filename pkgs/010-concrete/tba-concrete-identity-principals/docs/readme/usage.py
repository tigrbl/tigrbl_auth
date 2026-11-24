import tba_concrete_identity_principals as principals

directory = principals.PrincipalDirectory()
user = directory.add_principal(
    principals.create_user_principal("user@example.com", tenant_id="acme")
)
membership = principals.membership_for(user, "acme", roles=["viewer"])
directory.add_membership(membership)

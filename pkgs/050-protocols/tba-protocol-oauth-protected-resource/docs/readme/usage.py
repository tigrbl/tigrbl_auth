from tba_protocol_oauth_protected_resource import (
    AccessTokenClaims,
    ResourceRequirement,
    ResourceServerVerifier,
)

requirement = ResourceRequirement(audience="api://billing", scopes=("invoice.read",))
claims = AccessTokenClaims(
    iss="https://issuer.example.test",
    sub="user:1",
    aud=("api://billing",),
    exp=1_800_000_300,
    iat=1_800_000_000,
    scope=("invoice.read",),
)
result = ResourceServerVerifier().verify_token(claims, requirement)

# OIDC ACR and AMR Projection Test Plan

Planned tests will verify that OIDC claim emission projects canonical authentication context values.

The planned checks cover:

- `acr` emission uses agreed authentication context class values
- `amr` emission uses registered authentication method reference values
- protocol packages do not define independent AAL, AMR, or phishing-resistant registries
- invalid or unknown vocabulary values are rejected before token or claims projection

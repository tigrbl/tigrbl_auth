# Authentication Context Vocabulary Storage Test Plan

Planned tests will verify that authentication context vocabulary is table-owned durable data.

The planned checks cover:

- storage tables for ACR/AAL vocabulary, AMR vocabulary, and authenticator or session properties
- seeded `aal1`, `aal2`, `aal3`, and `phishing-resistant` entries with standards provenance
- `phishing-resistant` stored as a property or requirement, not as an ACR/AAL value
- no higher-layer local duplicate vocabulary registry

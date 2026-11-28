# Adaptive Access Authentication Context Test Plan

Planned tests will verify adaptive access evaluates required and achieved authentication context from canonical vocabulary.

The planned checks cover:

- required ACR/AAL, AMR, and property requirements are resolved from registry-backed vocabulary
- achieved session context records authenticator methods and properties
- step-up is required when achieved context does not satisfy policy requirements
- phishing-resistant requirements are checked as properties, not as AAL values

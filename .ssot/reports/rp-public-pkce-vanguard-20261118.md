# Public PKCE callback verification against Vanguard

November 18, 2026

The Python and TypeScript relying-party suites passed with 16 and 11 tests,
respectively. They exercise a public PKCE exchange and rejection of incorrect
state, duplicate callbacks, wrong issuer, wrong nonce, wrong or extra audiences,
expired tokens, and invalid signatures.

The locally built Python wheel and npm tarball were installed into separate
test targets. Each client completed sign-in against Cedar and Harbor test
tenants served by Vanguard revision `fd1807b91a42` over loopback HTTPS with
PostgreSQL. Each run validated the signed ID token, matched the UserInfo
subject, and rejected reuse of the callback. The two tenants returned distinct
subjects. The TypeScript consumer also passed a NodeNext declaration check
from the installed tarball.

| Artifact | SHA-256 |
| --- | --- |
| `tba_protocol_oidc_relying_party-0.4.0.dev2-py3-none-any.whl` | `ECB41A8A7742893589D7730C484E46E369F5FFA8701A8C70D525D403FF9C2EC9` |
| `tba-client-oidc-relying-party-0.4.0-dev.2.tgz` | `CDB9EE15296B9329FF7565EE92728E38322753C54D0B0C954584FC8EB481375E` |

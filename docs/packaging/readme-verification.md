# Package README quick start verification

The README rollout covers 486 active packages in the numbered layers under
`pkgs/`. The root README has its own discovery example.

| Packages | What was checked | Result |
| --- | --- | --- |
| 439 Python | Each quick start against the published version it names, in Python 3.12 | 439 passed |
| 39 Node | Workspace or standalone builds and TypeScript client examples under Node 24 | 39 passed |
| 8 restored Node prototypes | Install, type check, production build and launch, and browser interactions under Node 24 | 8 passed |

Python checks exercise the API shown on each page. Depending on the package,
that may be an import, claim construction, an inventory or capability query,
or a fixture demonstration. Node builds check bundling. Client examples
exercise local fixtures. These checks establish the documented quick starts,
with protocol conformance, live authentication, and deployed integrations
covered separately.

All 439 Python checkout versions were present on PyPI. The 47 Node package
names had no public npm listing when checked. Their quick starts use the
repository checkout.

## Restored UI prototypes

Each production build was launched on loopback. Browser checks at 390 px and
1280 px verified rendering, keyboard access, and the first interaction below.
The six prototypes with servers also passed direct HTTP checks of their local APIs.

| Prototype | Verified first interaction |
| --- | --- |
| [Authenticator Center](../../pkgs/106-ui/tba-ui-authenticator-center/README.md) | Filter the sample authenticator inventory |
| [Directory Provisioning SCIM](../../pkgs/106-ui/tba-ui-directory-provisioning-scim/README.md) | Filter the sample provisioning connections |
| [Directory SCIM Center](../../pkgs/106-ui/tba-ui-directory-scim-center/README.md) | Filter the sample SCIM connections |
| [Service Administration](../../pkgs/106-ui/tba-ui-service-administration-prototype/README.md) | Filter the sample service inventory |
| [Decision Lineage Explorer](../../pkgs/106-ui/tba-ui-authorization-provenance-decision-lineage-explorer/README.md) | Filter decision traces and replay the latest sample decision |
| [Authorization Studio](../../pkgs/106-ui/tba-ui-authorization-studio/README.md) | Evaluate a sample policy request |
| [Public Identity](../../pkgs/106-ui/tba-ui-public-identity/README.md) | Complete the sign-in walkthrough with local sample data |
| [Universal Authenticator](../../pkgs/106-ui/tba-ui-universal-authenticator/README.md) | Complete the passkey enrollment walkthrough with local sample data |

Additional HTTP checks verified same-tenant permits, cross-tenant and malformed
request denials, and a side-effect-free policy simulation in Authorization
Studio. Decision Lineage Explorer reproduced a seeded result and denied its
counterfactual replay after lowering the device trust score.

# CLI Conformance Snapshot

> Generated from `tigrbl_auth.cli.metadata` and argparse parser snapshots.

- Command count: `21`
- Verb count: `87`
- Global flag count: `16`
- Help snapshot count: `109`
- Required command families present: `True`
- Retired certified aliases absent: `True`
- Passed: `True`

## Help snapshots

### `tigrbl-auth`

```text
usage: tigrbl-auth [-h]
                   {serve,verify,gate,spec,claims,evidence,adr,doctor,bootstrap,migrate,release,tenant,client,identity,flow,session,token,keys,discovery,import,export}
                   ...

Tigrbl-native operator CLI for the tigrbl_auth package.

positional arguments:
  {serve,verify,gate,spec,claims,evidence,adr,doctor,bootstrap,migrate,release,tenant,client,identity,flow,session,token,keys,discovery,import,export}
    serve               Launch the selected runner-backed ASGI runtime.
    verify              Run verification scopes against the repository boundary.
    gate                Run release gate checks.
    spec                Generate, diff, and validate public contract artifacts.
    claims              Lint and materialize effective claims.
    evidence            Build evidence manifests and peer profile artifacts.
    adr                 List, inspect, create, and index ADRs.
    doctor              Run an aggregated repository health summary.
    bootstrap           Bootstrap deployment artifacts and checkpoint lifecycle state.
    migrate             Inspect migration readiness and plans.
    release             Build release bundles and recertification reports.
    tenant              Manage tenant records.
    client              Manage client records.
    identity            Manage identity records.
    flow                Manage flow records.
    session             Manage session records.
    token               Manage token records.
    keys                Manage key lifecycle and JWKS publication.
    discovery           Show, validate, publish, and diff discovery artifacts.
    import              Validate and run import portability workflows.
    export              Validate and run export portability workflows.

options:
  -h, --help            show this help message and exit
```

### `tigrbl-auth adr`

```text
usage: tigrbl-auth adr [-h] [--config CONFIG] [--env-file ENV_FILE]
                       [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                       [--tenant TENANT] [--issuer ISSUER]
                       [--surface-set {admin-rpc,diagnostics,public-rest}]
                       [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                       [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                       [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                       [--runtime-style {plugin,standalone}] [--strict]
                       [--no-strict] [--format {json,yaml,text}]
                       [--output OUTPUT] [--verbose] [--trace]
                       {list,show,new,index} ...

Architecture decision record operators.

positional arguments:
  {list,show,new,index}
    list                List ADRs.
    show                Show a single ADR.
    new                 Create a new ADR template.
    index               Generate the ADR index.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth adr index`

```text
usage: tigrbl-auth adr index [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                             [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                             [--runtime-style {plugin,standalone}] [--strict]
                             [--no-strict] [--format {json,yaml,text}]
                             [--output OUTPUT] [--verbose] [--trace]
                             [--repo-root REPO_ROOT] [--report-dir REPORT_DIR]

Generate the ADR index markdown and JSON summaries.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth adr list`

```text
usage: tigrbl-auth adr list [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                            [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                            [--runtime-style {plugin,standalone}] [--strict]
                            [--no-strict] [--format {json,yaml,text}]
                            [--output OUTPUT] [--verbose] [--trace]
                            [--repo-root REPO_ROOT]

List ADRs and their titles.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
```

### `tigrbl-auth adr new`

```text
usage: tigrbl-auth adr new [-h] [--config CONFIG] [--env-file ENV_FILE]
                           [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                           [--tenant TENANT] [--issuer ISSUER]
                           [--surface-set {admin-rpc,diagnostics,public-rest}]
                           [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                           [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                           [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                           [--runtime-style {plugin,standalone}] [--strict]
                           [--no-strict] [--format {json,yaml,text}]
                           [--output OUTPUT] [--verbose] [--trace]
                           [--repo-root REPO_ROOT] [--id ID] [--title TITLE]

Create a new ADR markdown document from a template.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --title TITLE         Human-readable title.
```

### `tigrbl-auth adr show`

```text
usage: tigrbl-auth adr show [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                            [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                            [--runtime-style {plugin,standalone}] [--strict]
                            [--no-strict] [--format {json,yaml,text}]
                            [--output OUTPUT] [--verbose] [--trace]
                            [--repo-root REPO_ROOT] [--id ID]

Render a selected ADR.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth bootstrap`

```text
usage: tigrbl-auth bootstrap [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                             [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                             [--runtime-style {plugin,standalone}] [--strict]
                             [--no-strict] [--format {json,yaml,text}]
                             [--output OUTPUT] [--verbose] [--trace]
                             {status,manifest,apply,verify} ...

Materialize and verify baseline bootstrap manifests for deployment or plugin installation.

positional arguments:
  {status,manifest,apply,verify}
    status              Summarize bootstrap readiness.
    manifest            Write bootstrap manifests.
    apply               Apply bootstrap materialization.
    verify              Verify bootstrap artifacts.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth bootstrap apply`

```text
usage: tigrbl-auth bootstrap apply [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT]
                                   [--bundle-dir BUNDLE_DIR] [--yes]
                                   [--dry-run] [--wait] [--timeout TIMEOUT]

Materialize bootstrap manifests and record an applied bootstrap checkpoint.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --bundle-dir BUNDLE_DIR
                        Explicit bundle output directory.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth bootstrap manifest`

```text
usage: tigrbl-auth bootstrap manifest [-h] [--config CONFIG]
                                      [--env-file ENV_FILE]
                                      [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                      [--tenant TENANT] [--issuer ISSUER]
                                      [--surface-set {admin-rpc,diagnostics,public-rest}]
                                      [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                      [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                      [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                      [--runtime-style {plugin,standalone}]
                                      [--strict] [--no-strict]
                                      [--format {json,yaml,text}]
                                      [--output OUTPUT] [--verbose] [--trace]
                                      [--repo-root REPO_ROOT]
                                      [--bundle-dir BUNDLE_DIR]

Write deployment, claims, evidence, and contract manifests for the selected profile.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --bundle-dir BUNDLE_DIR
                        Explicit bundle output directory.
```

### `tigrbl-auth bootstrap status`

```text
usage: tigrbl-auth bootstrap status [-h] [--config CONFIG]
                                    [--env-file ENV_FILE]
                                    [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                    [--tenant TENANT] [--issuer ISSUER]
                                    [--surface-set {admin-rpc,diagnostics,public-rest}]
                                    [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                    [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                    [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                    [--runtime-style {plugin,standalone}]
                                    [--strict] [--no-strict]
                                    [--format {json,yaml,text}]
                                    [--output OUTPUT] [--verbose] [--trace]
                                    [--repo-root REPO_ROOT]
                                    [--report-dir REPORT_DIR]

Summarize bootstrap readiness for the selected profile and surfaces.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth bootstrap verify`

```text
usage: tigrbl-auth bootstrap verify [-h] [--config CONFIG]
                                    [--env-file ENV_FILE]
                                    [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                    [--tenant TENANT] [--issuer ISSUER]
                                    [--surface-set {admin-rpc,diagnostics,public-rest}]
                                    [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                    [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                    [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                    [--runtime-style {plugin,standalone}]
                                    [--strict] [--no-strict]
                                    [--format {json,yaml,text}]
                                    [--output OUTPUT] [--verbose] [--trace]
                                    [--repo-root REPO_ROOT]
                                    [--report-dir REPORT_DIR]

Verify bootstrap manifests, effective artifacts, and applied checkpoint state.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth claims`

```text
usage: tigrbl-auth claims [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                          [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                          [--runtime-style {plugin,standalone}] [--strict]
                          [--no-strict] [--format {json,yaml,text}]
                          [--output OUTPUT] [--verbose] [--trace]
                          {lint,show,status} ...

Operate on the claims plane.

positional arguments:
  {lint,show,status}
    lint                Run claims lint.
    show                Write the effective claims manifest.
    status              Summarize the claims plane.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth claims lint`

```text
usage: tigrbl-auth claims lint [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--report-dir REPORT_DIR]

Validate declared claims against mappings and boundaries.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth claims show`

```text
usage: tigrbl-auth claims show [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]

Materialize the effective claims manifest for the active deployment.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
```

### `tigrbl-auth claims status`

```text
usage: tigrbl-auth claims status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--report-dir REPORT_DIR]

Summarize declared, effective, and promotable claims.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth client`

```text
usage: tigrbl-auth client [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                          [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                          [--runtime-style {plugin,standalone}] [--strict]
                          [--no-strict] [--format {json,yaml,text}]
                          [--output OUTPUT] [--verbose] [--trace]
                          {create,update,delete,get,list,rotate-secret,enable,disable}
                          ...

Stateful durable operator-plane client lifecycle operators.

positional arguments:
  {create,update,delete,get,list,rotate-secret,enable,disable}
    create              Create a client record.
    update              Update a client record.
    delete              Delete a client record.
    get                 Get a client record.
    list                List client records.
    rotate-secret       Rotate a client secret.
    enable              Enable a client.
    disable             Disable a client.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth client create`

```text
usage: tigrbl-auth client create [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--from-file FROM_FILE]
                                 [--set key=value]
                                 [--if-exists {fail,replace,merge,skip}]
                                 [--yes] [--dry-run] [--wait]
                                 [--timeout TIMEOUT]

Create a durable operator-plane client record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --if-exists {fail,replace,merge,skip}
                        Behavior when the target already exists.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth client delete`

```text
usage: tigrbl-auth client delete [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--yes] [--dry-run]

Delete a durable operator-plane client record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth client disable`

```text
usage: tigrbl-auth client disable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT] [--id ID] [--yes]
                                  [--dry-run]

Mark a client record disabled.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth client enable`

```text
usage: tigrbl-auth client enable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--yes] [--dry-run]

Mark a client record enabled.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth client get`

```text
usage: tigrbl-auth client get [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                              [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                              [--runtime-style {plugin,standalone}] [--strict]
                              [--no-strict] [--format {json,yaml,text}]
                              [--output OUTPUT] [--verbose] [--trace]
                              [--repo-root REPO_ROOT] [--id ID]

Return a single durable operator-plane client record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth client list`

```text
usage: tigrbl-auth client list [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--filter FILTER] [--limit LIMIT]
                               [--offset OFFSET]
                               [--sort {id,name,status,created_at,updated_at}]
                               [--status STATUS]

List durable operator-plane client records.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --filter FILTER       Simple substring filter applied to identifiers or names.
  --limit LIMIT         Maximum number of results to return.
  --offset OFFSET       Result offset for list operations.
  --sort {id,name,status,created_at,updated_at}
                        Sort key for list operations.
  --status STATUS       Status filter for list operations.
```

### `tigrbl-auth client rotate-secret`

```text
usage: tigrbl-auth client rotate-secret [-h] [--config CONFIG]
                                        [--env-file ENV_FILE]
                                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                        [--tenant TENANT] [--issuer ISSUER]
                                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                        [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                        [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                        [--runtime-style {plugin,standalone}]
                                        [--strict] [--no-strict]
                                        [--format {json,yaml,text}]
                                        [--output OUTPUT] [--verbose]
                                        [--trace] [--repo-root REPO_ROOT]
                                        [--id ID] [--yes] [--dry-run]

Rotate durable operator-plane client secret material.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth client update`

```text
usage: tigrbl-auth client update [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--from-file FROM_FILE]
                                 [--set key=value]
                                 [--if-missing {fail,create,skip}] [--yes]
                                 [--dry-run] [--wait] [--timeout TIMEOUT]

Update a durable operator-plane client record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --if-missing {fail,create,skip}
                        Behavior when the target does not already exist.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth discovery`

```text
usage: tigrbl-auth discovery [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                             [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                             [--runtime-style {plugin,standalone}] [--strict]
                             [--no-strict] [--format {json,yaml,text}]
                             [--output OUTPUT] [--verbose] [--trace]
                             {show,validate,publish,diff} ...

Discovery and metadata operators bound to repository snapshots.

positional arguments:
  {show,validate,publish,diff}
    show                Show discovery metadata.
    validate            Validate discovery metadata.
    publish             Publish discovery metadata.
    diff                Diff discovery metadata.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth discovery diff`

```text
usage: tigrbl-auth discovery diff [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT] [--input INPUT]
                                  [--report-dir REPORT_DIR]

Diff active discovery metadata against a provided or published baseline.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --input INPUT         Input path for import, validation, or diff operations.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth discovery publish`

```text
usage: tigrbl-auth discovery publish [-h] [--config CONFIG]
                                     [--env-file ENV_FILE]
                                     [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                     [--tenant TENANT] [--issuer ISSUER]
                                     [--surface-set {admin-rpc,diagnostics,public-rest}]
                                     [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                     [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                     [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                     [--runtime-style {plugin,standalone}]
                                     [--strict] [--no-strict]
                                     [--format {json,yaml,text}]
                                     [--output OUTPUT] [--verbose] [--trace]
                                     [--repo-root REPO_ROOT]
                                     [--checksum CHECKSUM] [--yes] [--dry-run]

Publish discovery metadata into a release-ready output directory.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --checksum CHECKSUM   Expected checksum or checksum algorithm for import/export validation.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth discovery show`

```text
usage: tigrbl-auth discovery show [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT]

Show the active discovery snapshot for the selected profile.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
```

### `tigrbl-auth discovery validate`

```text
usage: tigrbl-auth discovery validate [-h] [--config CONFIG]
                                      [--env-file ENV_FILE]
                                      [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                      [--tenant TENANT] [--issuer ISSUER]
                                      [--surface-set {admin-rpc,diagnostics,public-rest}]
                                      [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                      [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                      [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                      [--runtime-style {plugin,standalone}]
                                      [--strict] [--no-strict]
                                      [--format {json,yaml,text}]
                                      [--output OUTPUT] [--verbose] [--trace]
                                      [--repo-root REPO_ROOT]
                                      [--report-dir REPORT_DIR]

Validate discovery metadata and supporting contracts.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth doctor`

```text
usage: tigrbl-auth doctor [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                          [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                          [--runtime-style {plugin,standalone}] [--strict]
                          [--no-strict] [--format {json,yaml,text}]
                          [--output OUTPUT] [--verbose] [--trace]
                          [--repo-root REPO_ROOT] [--report-dir REPORT_DIR]

Aggregate core verification, runtime profile, contracts, evidence, and gate status.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth evidence`

```text
usage: tigrbl-auth evidence [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                            [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                            [--runtime-style {plugin,standalone}] [--strict]
                            [--no-strict] [--format {json,yaml,text}]
                            [--output OUTPUT] [--verbose] [--trace]
                            {bundle,status,verify,peer-status,peer-execute}
                            ...

Operate on Tier 3/Tier 4 evidence automation.

positional arguments:
  {bundle,status,verify,peer-status,peer-execute}
    bundle              Build an evidence bundle.
    status              Summarize evidence readiness.
    verify              Verify evidence and peer references.
    peer-status         Summarize peer profile execution readiness.
    peer-execute        Materialize peer execution manifests.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth evidence bundle`

```text
usage: tigrbl-auth evidence bundle [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT] [--tier {3,4,all}]
                                   [--bundle-dir BUNDLE_DIR]

Build a release/evidence bundle filtered by the effective deployment.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --tier {3,4,all}      Evidence tier selector.
  --bundle-dir BUNDLE_DIR
                        Explicit bundle output directory.
```

### `tigrbl-auth evidence peer-execute`

```text
usage: tigrbl-auth evidence peer-execute [-h] [--config CONFIG]
                                         [--env-file ENV_FILE]
                                         [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                         [--tenant TENANT] [--issuer ISSUER]
                                         [--surface-set {admin-rpc,diagnostics,public-rest}]
                                         [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                         [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                         [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                         [--runtime-style {plugin,standalone}]
                                         [--strict] [--no-strict]
                                         [--format {json,yaml,text}]
                                         [--output OUTPUT] [--verbose]
                                         [--trace] [--repo-root REPO_ROOT]
                                         [--peer-profile PEER_PROFILE]
                                         [--execution-mode {self-check,dry-run,record-only}]
                                         [--report-dir REPORT_DIR]

Materialize peer execution manifests for configured profiles.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --peer-profile PEER_PROFILE
                        Peer profile selector. May be supplied multiple times.
  --execution-mode {self-check,dry-run,record-only}
                        Peer execution mode.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth evidence peer-status`

```text
usage: tigrbl-auth evidence peer-status [-h] [--config CONFIG]
                                        [--env-file ENV_FILE]
                                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                        [--tenant TENANT] [--issuer ISSUER]
                                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                        [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                        [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                        [--runtime-style {plugin,standalone}]
                                        [--strict] [--no-strict]
                                        [--format {json,yaml,text}]
                                        [--output OUTPUT] [--verbose]
                                        [--trace] [--repo-root REPO_ROOT]
                                        [--report-dir REPORT_DIR]

Summarize configured peer execution profiles and bundle refs.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth evidence status`

```text
usage: tigrbl-auth evidence status [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT] [--tier {3,4,all}]
                                   [--report-dir REPORT_DIR]

Summarize Tier 3/Tier 4 evidence readiness.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --tier {3,4,all}      Evidence tier selector.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth evidence verify`

```text
usage: tigrbl-auth evidence verify [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT]
                                   [--report-dir REPORT_DIR]

Run evidence/peer readiness checks.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth export`

```text
usage: tigrbl-auth export [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                          [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                          [--runtime-style {plugin,standalone}] [--strict]
                          [--no-strict] [--format {json,yaml,text}]
                          [--output OUTPUT] [--verbose] [--trace]
                          {validate,run,status} ...

Export durable operator-plane state into portable artifacts.

positional arguments:
  {validate,run,status}
    validate            Validate export configuration.
    run                 Run an export.
    status              Show export status.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth export run`

```text
usage: tigrbl-auth export run [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                              [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                              [--runtime-style {plugin,standalone}] [--strict]
                              [--no-strict] [--format {json,yaml,text}]
                              [--output OUTPUT] [--verbose] [--trace]
                              [--repo-root REPO_ROOT] [--include-secrets]
                              [--redact] [--checksum CHECKSUM] [--yes]
                              [--dry-run] [--wait] [--timeout TIMEOUT]

Export durable operator-plane state to a portable artifact.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --include-secrets     Include secret material where the selected surface permits it.
  --redact              Redact secret material from exported output.
  --checksum CHECKSUM   Expected checksum or checksum algorithm for import/export validation.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth export status`

```text
usage: tigrbl-auth export status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]

Show the last durable operator-plane export status.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
```

### `tigrbl-auth export validate`

```text
usage: tigrbl-auth export validate [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT] [--include-secrets]
                                   [--redact] [--checksum CHECKSUM]
                                   [--report-dir REPORT_DIR]

Validate export configuration and current operator state.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --include-secrets     Include secret material where the selected surface permits it.
  --redact              Redact secret material from exported output.
  --checksum CHECKSUM   Expected checksum or checksum algorithm for import/export validation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth flow`

```text
usage: tigrbl-auth flow [-h] [--config CONFIG] [--env-file ENV_FILE]
                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                        [--tenant TENANT] [--issuer ISSUER]
                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                        [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                        [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                        [--runtime-style {plugin,standalone}] [--strict]
                        [--no-strict] [--format {json,yaml,text}]
                        [--output OUTPUT] [--verbose] [--trace]
                        {create,update,delete,get,list,enable,disable} ...

Stateful durable operator-plane flow lifecycle operators.

positional arguments:
  {create,update,delete,get,list,enable,disable}
    create              Create a flow record.
    update              Update a flow record.
    delete              Delete a flow record.
    get                 Get a flow record.
    list                List flow records.
    enable              Enable a flow.
    disable             Disable a flow.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth flow create`

```text
usage: tigrbl-auth flow create [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--from-file FROM_FILE]
                               [--set key=value]
                               [--if-exists {fail,replace,merge,skip}] [--yes]
                               [--dry-run] [--wait] [--timeout TIMEOUT]

Create a durable operator-plane flow record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --if-exists {fail,replace,merge,skip}
                        Behavior when the target already exists.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth flow delete`

```text
usage: tigrbl-auth flow delete [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--yes] [--dry-run]

Delete a durable operator-plane flow record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth flow disable`

```text
usage: tigrbl-auth flow disable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                [--runtime-style {plugin,standalone}]
                                [--strict] [--no-strict]
                                [--format {json,yaml,text}] [--output OUTPUT]
                                [--verbose] [--trace] [--repo-root REPO_ROOT]
                                [--id ID] [--yes] [--dry-run]

Mark a flow record disabled.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth flow enable`

```text
usage: tigrbl-auth flow enable [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--yes] [--dry-run]

Mark a flow record enabled.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth flow get`

```text
usage: tigrbl-auth flow get [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                            [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                            [--runtime-style {plugin,standalone}] [--strict]
                            [--no-strict] [--format {json,yaml,text}]
                            [--output OUTPUT] [--verbose] [--trace]
                            [--repo-root REPO_ROOT] [--id ID]

Return a single durable operator-plane flow record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth flow list`

```text
usage: tigrbl-auth flow list [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                             [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                             [--runtime-style {plugin,standalone}] [--strict]
                             [--no-strict] [--format {json,yaml,text}]
                             [--output OUTPUT] [--verbose] [--trace]
                             [--repo-root REPO_ROOT] [--filter FILTER]
                             [--limit LIMIT] [--offset OFFSET]
                             [--sort {id,name,status,created_at,updated_at}]
                             [--status STATUS]

List durable operator-plane flow records.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --filter FILTER       Simple substring filter applied to identifiers or names.
  --limit LIMIT         Maximum number of results to return.
  --offset OFFSET       Result offset for list operations.
  --sort {id,name,status,created_at,updated_at}
                        Sort key for list operations.
  --status STATUS       Status filter for list operations.
```

### `tigrbl-auth flow update`

```text
usage: tigrbl-auth flow update [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--from-file FROM_FILE]
                               [--set key=value]
                               [--if-missing {fail,create,skip}] [--yes]
                               [--dry-run] [--wait] [--timeout TIMEOUT]

Update a durable operator-plane flow record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --if-missing {fail,create,skip}
                        Behavior when the target does not already exist.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth gate`

```text
usage: tigrbl-auth gate [-h] [--config CONFIG] [--env-file ENV_FILE]
                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                        [--tenant TENANT] [--issuer ISSUER]
                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                        [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                        [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                        [--runtime-style {plugin,standalone}] [--strict]
                        [--no-strict] [--format {json,yaml,text}]
                        [--output OUTPUT] [--verbose] [--trace]
                        [--repo-root REPO_ROOT] [--report-dir REPORT_DIR]
                        [--name NAME]

Run one release gate or the full ordered release gate catalog.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
  --name NAME           Optional named release gate or artifact selector.
```

### `tigrbl-auth identity`

```text
usage: tigrbl-auth identity [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                            [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                            [--runtime-style {plugin,standalone}] [--strict]
                            [--no-strict] [--format {json,yaml,text}]
                            [--output OUTPUT] [--verbose] [--trace]
                            {create,update,delete,get,list,set-password,lock,unlock}
                            ...

Stateful durable operator-plane identity lifecycle operators.

positional arguments:
  {create,update,delete,get,list,set-password,lock,unlock}
    create              Create an identity record.
    update              Update an identity record.
    delete              Delete an identity record.
    get                 Get an identity record.
    list                List identity records.
    set-password        Set an identity password.
    lock                Lock an identity.
    unlock              Unlock an identity.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth identity create`

```text
usage: tigrbl-auth identity create [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT] [--id ID]
                                   [--from-file FROM_FILE] [--set key=value]
                                   [--if-exists {fail,replace,merge,skip}]
                                   [--yes] [--dry-run] [--wait]
                                   [--timeout TIMEOUT]

Create a durable operator-plane identity record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --if-exists {fail,replace,merge,skip}
                        Behavior when the target already exists.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth identity delete`

```text
usage: tigrbl-auth identity delete [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT] [--id ID] [--yes]
                                   [--dry-run]

Delete a durable operator-plane identity record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth identity get`

```text
usage: tigrbl-auth identity get [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                [--runtime-style {plugin,standalone}]
                                [--strict] [--no-strict]
                                [--format {json,yaml,text}] [--output OUTPUT]
                                [--verbose] [--trace] [--repo-root REPO_ROOT]
                                [--id ID]

Return a single durable operator-plane identity record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth identity list`

```text
usage: tigrbl-auth identity list [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--filter FILTER] [--limit LIMIT]
                                 [--offset OFFSET]
                                 [--sort {id,name,status,created_at,updated_at}]
                                 [--status STATUS]

List durable operator-plane identity records.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --filter FILTER       Simple substring filter applied to identifiers or names.
  --limit LIMIT         Maximum number of results to return.
  --offset OFFSET       Result offset for list operations.
  --sort {id,name,status,created_at,updated_at}
                        Sort key for list operations.
  --status STATUS       Status filter for list operations.
```

### `tigrbl-auth identity lock`

```text
usage: tigrbl-auth identity lock [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--yes] [--dry-run]

Mark an identity record locked.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth identity set-password`

```text
usage: tigrbl-auth identity set-password [-h] [--config CONFIG]
                                         [--env-file ENV_FILE]
                                         [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                         [--tenant TENANT] [--issuer ISSUER]
                                         [--surface-set {admin-rpc,diagnostics,public-rest}]
                                         [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                         [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                         [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                         [--runtime-style {plugin,standalone}]
                                         [--strict] [--no-strict]
                                         [--format {json,yaml,text}]
                                         [--output OUTPUT] [--verbose]
                                         [--trace] [--repo-root REPO_ROOT]
                                         [--id ID] [--from-file FROM_FILE]
                                         [--set key=value] [--yes] [--dry-run]

Set or rotate a durable operator-plane identity password hash.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth identity unlock`

```text
usage: tigrbl-auth identity unlock [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT] [--id ID] [--yes]
                                   [--dry-run]

Mark an identity record unlocked.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth identity update`

```text
usage: tigrbl-auth identity update [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT] [--id ID]
                                   [--from-file FROM_FILE] [--set key=value]
                                   [--if-missing {fail,create,skip}] [--yes]
                                   [--dry-run] [--wait] [--timeout TIMEOUT]

Update a durable operator-plane identity record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --if-missing {fail,create,skip}
                        Behavior when the target does not already exist.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth import`

```text
usage: tigrbl-auth import [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                          [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                          [--runtime-style {plugin,standalone}] [--strict]
                          [--no-strict] [--format {json,yaml,text}]
                          [--output OUTPUT] [--verbose] [--trace]
                          {validate,run,status} ...

Import durable operator-plane state from portable artifacts.

positional arguments:
  {validate,run,status}
    validate            Validate import input.
    run                 Run an import.
    status              Show import status.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth import run`

```text
usage: tigrbl-auth import run [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                              [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                              [--runtime-style {plugin,standalone}] [--strict]
                              [--no-strict] [--format {json,yaml,text}]
                              [--output OUTPUT] [--verbose] [--trace]
                              [--repo-root REPO_ROOT] [--input INPUT]
                              [--checksum CHECKSUM] [--yes] [--dry-run]
                              [--wait] [--timeout TIMEOUT]

Import durable operator-plane state from a portable artifact.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --input INPUT         Input path for import, validation, or diff operations.
  --checksum CHECKSUM   Expected checksum or checksum algorithm for import/export validation.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth import status`

```text
usage: tigrbl-auth import status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]

Show the last durable operator-plane import status.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
```

### `tigrbl-auth import validate`

```text
usage: tigrbl-auth import validate [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT] [--input INPUT]
                                   [--checksum CHECKSUM]
                                   [--report-dir REPORT_DIR]

Validate an import artifact without mutating state.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --input INPUT         Input path for import, validation, or diff operations.
  --checksum CHECKSUM   Expected checksum or checksum algorithm for import/export validation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth keys`

```text
usage: tigrbl-auth keys [-h] [--config CONFIG] [--env-file ENV_FILE]
                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                        [--tenant TENANT] [--issuer ISSUER]
                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                        [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                        [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                        [--runtime-style {plugin,standalone}] [--strict]
                        [--no-strict] [--format {json,yaml,text}]
                        [--output OUTPUT] [--verbose] [--trace]
                        {generate,import,export,rotate,retire,publish-jwks,get,list,delete}
                        ...

Stateful durable operator-plane key lifecycle and JWKS publication operators.

positional arguments:
  {generate,import,export,rotate,retire,publish-jwks,get,list,delete}
    generate            Generate a key record.
    import              Import key material.
    export              Export key material.
    rotate              Rotate active key material.
    retire              Retire a key.
    publish-jwks        Publish JWKS.
    get                 Get a key record.
    list                List key records.
    delete              Delete a key record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth keys delete`

```text
usage: tigrbl-auth keys delete [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--yes] [--dry-run]

Delete a durable operator-plane key record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth keys export`

```text
usage: tigrbl-auth keys export [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--include-secrets] [--redact]
                               [--checksum CHECKSUM]

Export durable operator-plane key metadata to a JSON or YAML file.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --include-secrets     Include secret material where the selected surface permits it.
  --redact              Redact secret material from exported output.
  --checksum CHECKSUM   Expected checksum or checksum algorithm for import/export validation.
```

### `tigrbl-auth keys generate`

```text
usage: tigrbl-auth keys generate [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--kid KID] [--alg ALG]
                                 [--use {sig,enc}] [--kty {RSA,EC,OKP,oct}]
                                 [--curve {Ed25519,P-256,P-384,X25519}]
                                 [--activate] [--retire-after RETIRE_AFTER]
                                 [--publish] [--yes] [--dry-run]

Generate durable operator-plane key metadata and optional JWKS publication.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --kid KID             Explicit key identifier.
  --alg ALG             JWA/JOSE algorithm identifier.
  --use {sig,enc}       JWK use classification.
  --kty {RSA,EC,OKP,oct}
                        JWK key type.
  --curve {Ed25519,P-256,P-384,X25519}
                        Curve for EC/OKP keys.
  --activate            Mark a generated or imported key active immediately.
  --retire-after RETIRE_AFTER
                        Retire-after hint or timestamp recorded with the key.
  --publish             Publish JWKS after a successful key mutation.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth keys get`

```text
usage: tigrbl-auth keys get [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                            [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                            [--runtime-style {plugin,standalone}] [--strict]
                            [--no-strict] [--format {json,yaml,text}]
                            [--output OUTPUT] [--verbose] [--trace]
                            [--repo-root REPO_ROOT] [--id ID]

Return a single durable operator-plane key record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth keys import`

```text
usage: tigrbl-auth keys import [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--from-file FROM_FILE]
                               [--input INPUT] [--activate] [--publish]
                               [--yes] [--dry-run]

Import durable operator-plane key metadata from a JSON or YAML file.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --input INPUT         Input path for import, validation, or diff operations.
  --activate            Mark a generated or imported key active immediately.
  --publish             Publish JWKS after a successful key mutation.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth keys list`

```text
usage: tigrbl-auth keys list [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                             [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                             [--runtime-style {plugin,standalone}] [--strict]
                             [--no-strict] [--format {json,yaml,text}]
                             [--output OUTPUT] [--verbose] [--trace]
                             [--repo-root REPO_ROOT] [--filter FILTER]
                             [--limit LIMIT] [--offset OFFSET]
                             [--sort {id,name,status,created_at,updated_at}]
                             [--status STATUS]

List durable operator-plane key records.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --filter FILTER       Simple substring filter applied to identifiers or names.
  --limit LIMIT         Maximum number of results to return.
  --offset OFFSET       Result offset for list operations.
  --sort {id,name,status,created_at,updated_at}
                        Sort key for list operations.
  --status STATUS       Status filter for list operations.
```

### `tigrbl-auth keys publish-jwks`

```text
usage: tigrbl-auth keys publish-jwks [-h] [--config CONFIG]
                                     [--env-file ENV_FILE]
                                     [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                     [--tenant TENANT] [--issuer ISSUER]
                                     [--surface-set {admin-rpc,diagnostics,public-rest}]
                                     [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                     [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                     [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                     [--runtime-style {plugin,standalone}]
                                     [--strict] [--no-strict]
                                     [--format {json,yaml,text}]
                                     [--output OUTPUT] [--verbose] [--trace]
                                     [--repo-root REPO_ROOT]
                                     [--include-secrets] [--redact]
                                     [--checksum CHECKSUM]

Publish the current durable operator-plane JWKS document.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --include-secrets     Include secret material where the selected surface permits it.
  --redact              Redact secret material from exported output.
  --checksum CHECKSUM   Expected checksum or checksum algorithm for import/export validation.
```

### `tigrbl-auth keys retire`

```text
usage: tigrbl-auth keys retire [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--yes] [--dry-run] [--publish]

Mark a durable operator-plane key retired.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --publish             Publish JWKS after a successful key mutation.
```

### `tigrbl-auth keys rotate`

```text
usage: tigrbl-auth keys rotate [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID] [--kid KID] [--alg ALG]
                               [--use {sig,enc}] [--kty {RSA,EC,OKP,oct}]
                               [--curve {Ed25519,P-256,P-384,X25519}]
                               [--activate] [--retire-after RETIRE_AFTER]
                               [--publish] [--yes] [--dry-run]

Generate successor key metadata and retire the previous active key.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --kid KID             Explicit key identifier.
  --alg ALG             JWA/JOSE algorithm identifier.
  --use {sig,enc}       JWK use classification.
  --kty {RSA,EC,OKP,oct}
                        JWK key type.
  --curve {Ed25519,P-256,P-384,X25519}
                        Curve for EC/OKP keys.
  --activate            Mark a generated or imported key active immediately.
  --retire-after RETIRE_AFTER
                        Retire-after hint or timestamp recorded with the key.
  --publish             Publish JWKS after a successful key mutation.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth migrate`

```text
usage: tigrbl-auth migrate [-h] [--config CONFIG] [--env-file ENV_FILE]
                           [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                           [--tenant TENANT] [--issuer ISSUER]
                           [--surface-set {admin-rpc,diagnostics,public-rest}]
                           [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                           [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                           [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                           [--runtime-style {plugin,standalone}] [--strict]
                           [--no-strict] [--format {json,yaml,text}]
                           [--output OUTPUT] [--verbose] [--trace]
                           {status,plan,apply,verify} ...

Migration-chain status, planning, application, and verification operators.

positional arguments:
  {status,plan,apply,verify}
    status              Show migration status.
    plan                Emit migration plan details.
    apply               Apply the migration checkpoint plan.
    verify              Verify migration artifacts.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth migrate apply`

```text
usage: tigrbl-auth migrate apply [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--yes] [--dry-run] [--wait]
                                 [--timeout TIMEOUT]

Record a migration application checkpoint for the structured plan.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth migrate plan`

```text
usage: tigrbl-auth migrate plan [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                [--runtime-style {plugin,standalone}]
                                [--strict] [--no-strict]
                                [--format {json,yaml,text}] [--output OUTPUT]
                                [--verbose] [--trace] [--repo-root REPO_ROOT]

Emit the structured migration plan and replacement order.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
```

### `tigrbl-auth migrate status`

```text
usage: tigrbl-auth migrate status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT]
                                  [--report-dir REPORT_DIR]

List migration revisions and current-to-target move status.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth migrate verify`

```text
usage: tigrbl-auth migrate verify [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT]
                                  [--report-dir REPORT_DIR]

Run migration-plan and project-tree verification.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth release`

```text
usage: tigrbl-auth release [-h] [--config CONFIG] [--env-file ENV_FILE]
                           [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                           [--tenant TENANT] [--issuer ISSUER]
                           [--surface-set {admin-rpc,diagnostics,public-rest}]
                           [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                           [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                           [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                           [--runtime-style {plugin,standalone}] [--strict]
                           [--no-strict] [--format {json,yaml,text}]
                           [--output OUTPUT] [--verbose] [--trace]
                           {bundle,sign,verify,status,recertify} ...

Release automation and recertification operators.

positional arguments:
  {bundle,sign,verify,status,recertify}
    bundle              Build a release bundle.
    sign                Sign a release bundle.
    verify              Verify a signed release bundle.
    status              Summarize release bundle status.
    recertify           Run recertification checks.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth release bundle`

```text
usage: tigrbl-auth release bundle [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT]
                                  [--bundle-dir BUNDLE_DIR]
                                  [--artifact {claims,evidence,contracts,all}]

Build a release bundle containing claims, evidence, contracts, ADR index, and peer refs.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --bundle-dir BUNDLE_DIR
                        Explicit bundle output directory.
  --artifact {claims,evidence,contracts,all}
                        Release artifact subset.
```

### `tigrbl-auth release recertify`

```text
usage: tigrbl-auth release recertify [-h] [--config CONFIG]
                                     [--env-file ENV_FILE]
                                     [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                     [--tenant TENANT] [--issuer ISSUER]
                                     [--surface-set {admin-rpc,diagnostics,public-rest}]
                                     [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                     [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                     [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                     [--runtime-style {plugin,standalone}]
                                     [--strict] [--no-strict]
                                     [--format {json,yaml,text}]
                                     [--output OUTPUT] [--verbose] [--trace]
                                     [--repo-root REPO_ROOT]
                                     [--report-dir REPORT_DIR]

Re-run recertification for Tigrbl and standards-boundary changes.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth release sign`

```text
usage: tigrbl-auth release sign [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                [--runtime-style {plugin,standalone}]
                                [--strict] [--no-strict]
                                [--format {json,yaml,text}] [--output OUTPUT]
                                [--verbose] [--trace] [--repo-root REPO_ROOT]
                                [--bundle-dir BUNDLE_DIR]
                                [--signing-key SIGNING_KEY]

Create externally verifiable Ed25519 attestations for an existing release bundle.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --bundle-dir BUNDLE_DIR
                        Explicit bundle output directory.
  --signing-key SIGNING_KEY
                        Optional Ed25519 private signing key path or seed.
```

### `tigrbl-auth release status`

```text
usage: tigrbl-auth release status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT]
                                  [--report-dir REPORT_DIR]

Summarize the current release bundle and release-gate posture.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth release verify`

```text
usage: tigrbl-auth release verify [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT]
                                  [--bundle-dir BUNDLE_DIR]

Verify release-bundle attestations and manifest integrity for an existing signed bundle.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --bundle-dir BUNDLE_DIR
                        Explicit bundle output directory.
```

### `tigrbl-auth serve`

```text
usage: tigrbl-auth serve [-h] [--config CONFIG] [--env-file ENV_FILE]
                         [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                         [--tenant TENANT] [--issuer ISSUER]
                         [--surface-set {admin-rpc,diagnostics,public-rest}]
                         [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                         [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                         [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                         [--runtime-style {plugin,standalone}] [--strict]
                         [--no-strict] [--format {json,yaml,text}]
                         [--output OUTPUT] [--verbose] [--trace]
                         [--repo-root REPO_ROOT] [--report-dir REPORT_DIR]
                         [--environment ENVIRONMENT]
                         [--server {hypercorn,tigrcorn,uvicorn}] [--host HOST]
                         [--port PORT] [--workers WORKERS] [--uds UDS]
                         [--log-level LOG_LEVEL]
                         [--access-log | --no-access-log] [--proxy-headers]
                         [--lifespan {auto,on,off}]
                         [--graceful-timeout GRACEFUL_TIMEOUT]
                         [--pid-file PID_FILE] [--health | --no-health]
                         [--metrics | --no-metrics] [--public | --no-public]
                         [--admin | --no-admin] [--rpc | --no-rpc]
                         [--diagnostics | --no-diagnostics]
                         [--require-tls | --no-require-tls]
                         [--enable-mtls | --no-enable-mtls]
                         [--cookies | --no-cookies]
                         [--jwks-refresh-seconds JWKS_REFRESH_SECONDS]
                         [--dry-run] [--check] [--db-safe-start]
                         [--uvicorn-loop {auto,asyncio,uvloop}]
                         [--uvicorn-http {auto,h11,httptools}]
                         [--uvicorn-ws {auto,websockets,wsproto,none}]
                         [--hypercorn-worker-class {asyncio,trio,uvloop}]
                         [--hypercorn-http2 | --no-hypercorn-http2]
                         [--tigrcorn-contract {auto,serve,run,server}]
                         [--tigrcorn-mode {asgi,auto}]

Resolve deployment, materialize a runner-qualified runtime plan, validate the selected profile, and optionally launch runtime.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
  --environment ENVIRONMENT
                        Deployment environment label.
  --server {hypercorn,tigrcorn,uvicorn}
                        Runner profile used to qualify and launch runtime.
  --host HOST           Bind host.
  --port PORT           Bind port.
  --workers WORKERS     Process count for the selected runtime profile.
  --uds UDS             Optional Unix domain socket path.
  --log-level LOG_LEVEL
                        Operator log level for serve plans.
  --access-log, --no-access-log
                        Enable access logging for the selected runtime profile.
  --proxy-headers       Honor proxy forwarding headers.
  --lifespan {auto,on,off}
                        ASGI lifespan policy.
  --graceful-timeout GRACEFUL_TIMEOUT
                        Graceful shutdown timeout in seconds.
  --pid-file PID_FILE   Optional PID file written for the launched runtime.
  --health, --no-health
                        Enable health endpoints in serve plans.
  --metrics, --no-metrics
                        Enable metrics in serve plans.
  --public, --no-public
                        Enable the public REST/auth plane.
  --admin, --no-admin   Enable the admin/control plane.
  --rpc, --no-rpc       Enable the JSON-RPC control plane.
  --diagnostics, --no-diagnostics
                        Enable diagnostics surfaces.
  --require-tls, --no-require-tls
                        Require TLS on the public plane.
  --enable-mtls, --no-enable-mtls
                        Enable mTLS slice for the serve plan.
  --cookies, --no-cookies
                        Enable cookie/session helpers in serve plans.
  --jwks-refresh-seconds JWKS_REFRESH_SECONDS
                        JWKS refresh cadence in seconds.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --check               Validate the selected runner profile and application factory without launching runtime.
  --db-safe-start       Require a safe database start posture.
  --uvicorn-loop {auto,asyncio,uvloop}
                        Uvicorn event-loop implementation.
  --uvicorn-http {auto,h11,httptools}
                        Uvicorn HTTP protocol implementation.
  --uvicorn-ws {auto,websockets,wsproto,none}
                        Uvicorn WebSocket implementation.
  --hypercorn-worker-class {asyncio,trio,uvloop}
                        Hypercorn worker class.
  --hypercorn-http2, --no-hypercorn-http2
                        Enable HTTP/2 ALPN for Hypercorn.
  --tigrcorn-contract {auto,serve,run,server}
                        Preferred Tigrcorn adapter contract.
  --tigrcorn-mode {asgi,auto}
                        Preferred Tigrcorn runtime mode hint.
```

### `tigrbl-auth session`

```text
usage: tigrbl-auth session [-h] [--config CONFIG] [--env-file ENV_FILE]
                           [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                           [--tenant TENANT] [--issuer ISSUER]
                           [--surface-set {admin-rpc,diagnostics,public-rest}]
                           [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                           [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                           [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                           [--runtime-style {plugin,standalone}] [--strict]
                           [--no-strict] [--format {json,yaml,text}]
                           [--output OUTPUT] [--verbose] [--trace]
                           {get,list,revoke,revoke-all} ...

Stateful durable operator-plane session control operators.

positional arguments:
  {get,list,revoke,revoke-all}
    get                 Get a session record.
    list                List session records.
    revoke              Revoke a session.
    revoke-all          Revoke all sessions.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth session get`

```text
usage: tigrbl-auth session get [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--id ID]

Return a single durable operator-plane session record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth session list`

```text
usage: tigrbl-auth session list [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                [--runtime-style {plugin,standalone}]
                                [--strict] [--no-strict]
                                [--format {json,yaml,text}] [--output OUTPUT]
                                [--verbose] [--trace] [--repo-root REPO_ROOT]
                                [--filter FILTER] [--limit LIMIT]
                                [--offset OFFSET]
                                [--sort {id,name,status,created_at,updated_at}]
                                [--status STATUS]

List durable operator-plane session records.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --filter FILTER       Simple substring filter applied to identifiers or names.
  --limit LIMIT         Maximum number of results to return.
  --offset OFFSET       Result offset for list operations.
  --sort {id,name,status,created_at,updated_at}
                        Sort key for list operations.
  --status STATUS       Status filter for list operations.
```

### `tigrbl-auth session revoke`

```text
usage: tigrbl-auth session revoke [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT] [--id ID] [--yes]
                                  [--dry-run]

Mark a durable operator-plane session revoked.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth session revoke-all`

```text
usage: tigrbl-auth session revoke-all [-h] [--config CONFIG]
                                      [--env-file ENV_FILE]
                                      [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                      [--tenant TENANT] [--issuer ISSUER]
                                      [--surface-set {admin-rpc,diagnostics,public-rest}]
                                      [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                      [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                      [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                      [--runtime-style {plugin,standalone}]
                                      [--strict] [--no-strict]
                                      [--format {json,yaml,text}]
                                      [--output OUTPUT] [--verbose] [--trace]
                                      [--repo-root REPO_ROOT]
                                      [--filter FILTER] [--status STATUS]
                                      [--yes] [--dry-run]

Mark all durable operator-plane sessions revoked.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --filter FILTER       Simple substring filter applied to identifiers or names.
  --status STATUS       Status filter for list operations.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth spec`

```text
usage: tigrbl-auth spec [-h] [--config CONFIG] [--env-file ENV_FILE]
                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                        [--tenant TENANT] [--issuer ISSUER]
                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                        [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                        [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                        [--runtime-style {plugin,standalone}] [--strict]
                        [--no-strict] [--format {json,yaml,text}]
                        [--output OUTPUT] [--verbose] [--trace]
                        {generate,validate,diff,report} ...

Operate on the OpenAPI and OpenRPC contract surfaces.

positional arguments:
  {generate,validate,diff,report}
    generate            Generate contract artifacts.
    validate            Validate generated contracts.
    diff                Diff generated contracts.
    report              Write contract summary reports.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth spec diff`

```text
usage: tigrbl-auth spec diff [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                             [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                             [--runtime-style {plugin,standalone}] [--strict]
                             [--no-strict] [--format {json,yaml,text}]
                             [--output OUTPUT] [--verbose] [--trace]
                             [--repo-root REPO_ROOT]
                             [--kind {openapi,openrpc,all}]
                             [--baseline-file BASELINE_FILE]
                             [--report-dir REPORT_DIR]

Regenerate contracts and compare them to committed artifacts.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --kind {openapi,openrpc,all}
                        Contract artifact kind.
  --baseline-file BASELINE_FILE
                        Optional explicit baseline artifact for diff operations.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth spec generate`

```text
usage: tigrbl-auth spec generate [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--kind {openapi,openrpc,all}]
                                 [--report-dir REPORT_DIR]

Generate OpenAPI/OpenRPC artifacts for the selected deployment.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --kind {openapi,openrpc,all}
                        Contract artifact kind.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth spec report`

```text
usage: tigrbl-auth spec report [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--kind {openapi,openrpc,all}]
                               [--report-dir REPORT_DIR]

Summarize active contract contents and profile coverage.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --kind {openapi,openrpc,all}
                        Contract artifact kind.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth spec validate`

```text
usage: tigrbl-auth spec validate [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--kind {openapi,openrpc,all}]
                                 [--report-dir REPORT_DIR]

Validate generated contracts against repository expectations.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --kind {openapi,openrpc,all}
                        Contract artifact kind.
  --report-dir REPORT_DIR
                        Directory for generated reports.
```

### `tigrbl-auth tenant`

```text
usage: tigrbl-auth tenant [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                          [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                          [--runtime-style {plugin,standalone}] [--strict]
                          [--no-strict] [--format {json,yaml,text}]
                          [--output OUTPUT] [--verbose] [--trace]
                          {create,update,delete,get,list,enable,disable} ...

Stateful durable operator-plane tenant lifecycle operators.

positional arguments:
  {create,update,delete,get,list,enable,disable}
    create              Create a tenant record.
    update              Update a tenant record.
    delete              Delete a tenant record.
    get                 Get a tenant record.
    list                List tenant records.
    enable              Enable a tenant.
    disable             Disable a tenant.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth tenant create`

```text
usage: tigrbl-auth tenant create [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--from-file FROM_FILE]
                                 [--set key=value]
                                 [--if-exists {fail,replace,merge,skip}]
                                 [--yes] [--dry-run] [--wait]
                                 [--timeout TIMEOUT]

Create a durable operator-plane tenant record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --if-exists {fail,replace,merge,skip}
                        Behavior when the target already exists.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth tenant delete`

```text
usage: tigrbl-auth tenant delete [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--yes] [--dry-run]

Delete a durable operator-plane tenant record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth tenant disable`

```text
usage: tigrbl-auth tenant disable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT] [--id ID] [--yes]
                                  [--dry-run]

Mark a tenant record disabled.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth tenant enable`

```text
usage: tigrbl-auth tenant enable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--yes] [--dry-run]

Mark a tenant record enabled.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth tenant get`

```text
usage: tigrbl-auth tenant get [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                              [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                              [--runtime-style {plugin,standalone}] [--strict]
                              [--no-strict] [--format {json,yaml,text}]
                              [--output OUTPUT] [--verbose] [--trace]
                              [--repo-root REPO_ROOT] [--id ID]

Return a single durable operator-plane tenant record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth tenant list`

```text
usage: tigrbl-auth tenant list [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                               [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                               [--runtime-style {plugin,standalone}]
                               [--strict] [--no-strict]
                               [--format {json,yaml,text}] [--output OUTPUT]
                               [--verbose] [--trace] [--repo-root REPO_ROOT]
                               [--filter FILTER] [--limit LIMIT]
                               [--offset OFFSET]
                               [--sort {id,name,status,created_at,updated_at}]
                               [--status STATUS]

List durable operator-plane tenant records.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --filter FILTER       Simple substring filter applied to identifiers or names.
  --limit LIMIT         Maximum number of results to return.
  --offset OFFSET       Result offset for list operations.
  --sort {id,name,status,created_at,updated_at}
                        Sort key for list operations.
  --status STATUS       Status filter for list operations.
```

### `tigrbl-auth tenant update`

```text
usage: tigrbl-auth tenant update [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--id ID] [--from-file FROM_FILE]
                                 [--set key=value]
                                 [--if-missing {fail,create,skip}] [--yes]
                                 [--dry-run] [--wait] [--timeout TIMEOUT]

Update a durable operator-plane tenant record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --if-missing {fail,create,skip}
                        Behavior when the target does not already exist.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
  --wait                Wait for completion when the operation supports asynchronous execution.
  --timeout TIMEOUT     Maximum wait time in seconds for supported long-running operations.
```

### `tigrbl-auth token`

```text
usage: tigrbl-auth token [-h] [--config CONFIG] [--env-file ENV_FILE]
                         [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                         [--tenant TENANT] [--issuer ISSUER]
                         [--surface-set {admin-rpc,diagnostics,public-rest}]
                         [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                         [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                         [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                         [--runtime-style {plugin,standalone}] [--strict]
                         [--no-strict] [--format {json,yaml,text}]
                         [--output OUTPUT] [--verbose] [--trace]
                         {get,list,introspect,revoke,exchange} ...

Stateful durable operator-plane token control operators.

positional arguments:
  {get,list,introspect,revoke,exchange}
    get                 Get a token record.
    list                List token records.
    introspect          Introspect a token.
    revoke              Revoke a token.
    exchange            Exchange a token.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
```

### `tigrbl-auth token exchange`

```text
usage: tigrbl-auth token exchange [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                  [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                  [--runtime-style {plugin,standalone}]
                                  [--strict] [--no-strict]
                                  [--format {json,yaml,text}]
                                  [--output OUTPUT] [--verbose] [--trace]
                                  [--repo-root REPO_ROOT] [--id ID]
                                  [--from-file FROM_FILE] [--set key=value]
                                  [--yes] [--dry-run]

Create a derived durable operator-plane token exchange record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --from-file FROM_FILE
                        Load mutation input from a JSON or YAML file.
  --set key=value       Inline mutation field assignment in key=value form. May be supplied multiple times.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth token get`

```text
usage: tigrbl-auth token get [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                             [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                             [--runtime-style {plugin,standalone}] [--strict]
                             [--no-strict] [--format {json,yaml,text}]
                             [--output OUTPUT] [--verbose] [--trace]
                             [--repo-root REPO_ROOT] [--id ID]

Return a single durable operator-plane token record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth token introspect`

```text
usage: tigrbl-auth token introspect [-h] [--config CONFIG]
                                    [--env-file ENV_FILE]
                                    [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                    [--tenant TENANT] [--issuer ISSUER]
                                    [--surface-set {admin-rpc,diagnostics,public-rest}]
                                    [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                    [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                    [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                    [--runtime-style {plugin,standalone}]
                                    [--strict] [--no-strict]
                                    [--format {json,yaml,text}]
                                    [--output OUTPUT] [--verbose] [--trace]
                                    [--repo-root REPO_ROOT] [--id ID]

Return active/revoked status and metadata for a token record.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
```

### `tigrbl-auth token list`

```text
usage: tigrbl-auth token list [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                              [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                              [--runtime-style {plugin,standalone}] [--strict]
                              [--no-strict] [--format {json,yaml,text}]
                              [--output OUTPUT] [--verbose] [--trace]
                              [--repo-root REPO_ROOT] [--filter FILTER]
                              [--limit LIMIT] [--offset OFFSET]
                              [--sort {id,name,status,created_at,updated_at}]
                              [--status STATUS]

List durable operator-plane token records.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --filter FILTER       Simple substring filter applied to identifiers or names.
  --limit LIMIT         Maximum number of results to return.
  --offset OFFSET       Result offset for list operations.
  --sort {id,name,status,created_at,updated_at}
                        Sort key for list operations.
  --status STATUS       Status filter for list operations.
```

### `tigrbl-auth token revoke`

```text
usage: tigrbl-auth token revoke [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                                [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                [--runtime-style {plugin,standalone}]
                                [--strict] [--no-strict]
                                [--format {json,yaml,text}] [--output OUTPUT]
                                [--verbose] [--trace] [--repo-root REPO_ROOT]
                                [--id ID] [--yes] [--dry-run]

Mark a durable operator-plane token revoked.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --id ID               Primary identifier for a single record.
  --yes                 Assume yes for state-changing confirmations.
  --dry-run             Resolve and emit the runtime plan without applying or launching state changes.
```

### `tigrbl-auth verify`

```text
usage: tigrbl-auth verify [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}]
                          [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                          [--runtime-style {plugin,standalone}] [--strict]
                          [--no-strict] [--format {json,yaml,text}]
                          [--output OUTPUT] [--verbose] [--trace]
                          [--repo-root REPO_ROOT] [--report-dir REPORT_DIR]
                          [--scope {governance,claims,runtime-foundation,feature-surface-modularity,boundary-enforcement,wrapper-hygiene,contract-sync,contracts,evidence-peer,project-tree-layout,migration-plan,state-reports,test-classification,release-gates,all}]

Execute one or more verification scopes and emit structured results.

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to the runtime/configuration file.
  --env-file ENV_FILE   Optional environment file loaded before resolution.
  --profile {baseline,production,hardening,fapi2-security,peer-claim}
                        Effective standards/compliance profile.
  --tenant TENANT       Tenant identifier for multi-tenant operators.
  --issuer ISSUER       Issuer override for discovery and contract generation.
  --surface-set {admin-rpc,diagnostics,public-rest}
                        Installable surface set. May be supplied multiple times.
  --slice {device,dpop,jar,mtls,par,rar,token-exchange}
                        Protocol slice. May be supplied multiple times.
  --extension {a2a-adapter,dns-privacy,mcp-adapter,set,webauthn-passkeys,webpush}
                        Extension boundary slice. May be supplied multiple times.
  --plugin-mode {admin-only,diagnostics-only,mixed,public-only}
                        Plugin composition mode.
  --runtime-style {plugin,standalone}
                        Runtime style for installation or standalone serving.
  --strict              Fail closed when governance or certification checks fail.
  --no-strict           Downgrade failures to warnings for exploratory use.
  --format {json,yaml,text}
                        Output format.
  --output OUTPUT       Optional output file path.
  --verbose, -v         Increase operator verbosity; may be repeated.
  --trace               Emit trace-oriented operator details.
  --repo-root REPO_ROOT
                        Repository root for governance automation.
  --report-dir REPORT_DIR
                        Directory for generated reports.
  --scope {governance,claims,runtime-foundation,feature-surface-modularity,boundary-enforcement,wrapper-hygiene,contract-sync,contracts,evidence-peer,project-tree-layout,migration-plan,state-reports,test-classification,release-gates,all}
                        Verification scope.
```

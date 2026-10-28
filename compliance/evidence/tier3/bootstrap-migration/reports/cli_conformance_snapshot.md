# CLI Conformance Snapshot

> Generated from `tba_auth.cli.metadata` and argparse parser snapshots.

- Command count: `20`
- Verb count: `83`
- Global flag count: `16`
- Help snapshot count: `104`
- Required command families present: `True`
- Retired certified aliases absent: `True`
- Passed: `True`

## Help snapshots

### `tba-auth`

```text
usage: tba-auth [-h]
                   {serve,verify,gate,spec,claims,evidence,doctor,bootstrap,migrate,release,tenant,client,identity,flow,session,token,keys,discovery,import,export}
                   ...

Tigrbl-native operator CLI for the tba_auth package.

positional arguments:
  {serve,verify,gate,spec,claims,evidence,doctor,bootstrap,migrate,release,tenant,client,identity,flow,session,token,keys,discovery,import,export}
    serve               Launch the selected runner-backed ASGI runtime.
    verify              Run verification scopes against the repository boundary.
    gate                Run release gate checks.
    spec                Generate, diff, and validate public contract artifacts.
    claims              Lint and materialize effective claims.
    evidence            Build evidence manifests and peer profile artifacts.
    doctor              Run an aggregated repository health summary.
    bootstrap           Bootstrap deployment artifacts and evidence bundle lifecycle state.
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

### `tba-auth bootstrap`

```text
usage: tba-auth bootstrap [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth bootstrap apply`

```text
usage: tba-auth bootstrap apply [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
                                   [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                   [--runtime-style {plugin,standalone}]
                                   [--strict] [--no-strict]
                                   [--format {json,yaml,text}]
                                   [--output OUTPUT] [--verbose] [--trace]
                                   [--repo-root REPO_ROOT]
                                   [--bundle-dir BUNDLE_DIR] [--yes]
                                   [--dry-run] [--wait] [--timeout TIMEOUT]

Materialize bootstrap manifests and record an applied bootstrap evidence bundle.

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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth bootstrap manifest`

```text
usage: tba-auth bootstrap manifest [-h] [--config CONFIG]
                                      [--env-file ENV_FILE]
                                      [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                      [--tenant TENANT] [--issuer ISSUER]
                                      [--surface-set {admin-rpc,diagnostics,public-rest}]
                                      [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                      [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth bootstrap status`

```text
usage: tba-auth bootstrap status [-h] [--config CONFIG]
                                    [--env-file ENV_FILE]
                                    [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                    [--tenant TENANT] [--issuer ISSUER]
                                    [--surface-set {admin-rpc,diagnostics,public-rest}]
                                    [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                    [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth bootstrap verify`

```text
usage: tba-auth bootstrap verify [-h] [--config CONFIG]
                                    [--env-file ENV_FILE]
                                    [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                    [--tenant TENANT] [--issuer ISSUER]
                                    [--surface-set {admin-rpc,diagnostics,public-rest}]
                                    [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                    [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
                                    [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                    [--runtime-style {plugin,standalone}]
                                    [--strict] [--no-strict]
                                    [--format {json,yaml,text}]
                                    [--output OUTPUT] [--verbose] [--trace]
                                    [--repo-root REPO_ROOT]
                                    [--report-dir REPORT_DIR]

Verify bootstrap manifests, effective artifacts, and applied evidence bundle state.

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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth claims`

```text
usage: tba-auth claims [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth claims lint`

```text
usage: tba-auth claims lint [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth claims show`

```text
usage: tba-auth claims show [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth claims status`

```text
usage: tba-auth claims status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client`

```text
usage: tba-auth client [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client create`

```text
usage: tba-auth client create [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client delete`

```text
usage: tba-auth client delete [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client disable`

```text
usage: tba-auth client disable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client enable`

```text
usage: tba-auth client enable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client get`

```text
usage: tba-auth client get [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client list`

```text
usage: tba-auth client list [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client rotate-secret`

```text
usage: tba-auth client rotate-secret [-h] [--config CONFIG]
                                        [--env-file ENV_FILE]
                                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                        [--tenant TENANT] [--issuer ISSUER]
                                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                        [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth client update`

```text
usage: tba-auth client update [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth discovery`

```text
usage: tba-auth discovery [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth discovery diff`

```text
usage: tba-auth discovery diff [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth discovery publish`

```text
usage: tba-auth discovery publish [-h] [--config CONFIG]
                                     [--env-file ENV_FILE]
                                     [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                     [--tenant TENANT] [--issuer ISSUER]
                                     [--surface-set {admin-rpc,diagnostics,public-rest}]
                                     [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                     [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth discovery show`

```text
usage: tba-auth discovery show [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth discovery validate`

```text
usage: tba-auth discovery validate [-h] [--config CONFIG]
                                      [--env-file ENV_FILE]
                                      [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                      [--tenant TENANT] [--issuer ISSUER]
                                      [--surface-set {admin-rpc,diagnostics,public-rest}]
                                      [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                      [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth doctor`

```text
usage: tba-auth doctor [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth evidence`

```text
usage: tba-auth evidence [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth evidence bundle`

```text
usage: tba-auth evidence bundle [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth evidence peer-execute`

```text
usage: tba-auth evidence peer-execute [-h] [--config CONFIG]
                                         [--env-file ENV_FILE]
                                         [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                         [--tenant TENANT] [--issuer ISSUER]
                                         [--surface-set {admin-rpc,diagnostics,public-rest}]
                                         [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                         [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth evidence peer-status`

```text
usage: tba-auth evidence peer-status [-h] [--config CONFIG]
                                        [--env-file ENV_FILE]
                                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                        [--tenant TENANT] [--issuer ISSUER]
                                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                        [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth evidence status`

```text
usage: tba-auth evidence status [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth evidence verify`

```text
usage: tba-auth evidence verify [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth export`

```text
usage: tba-auth export [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth export run`

```text
usage: tba-auth export run [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth export status`

```text
usage: tba-auth export status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth export validate`

```text
usage: tba-auth export validate [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth flow`

```text
usage: tba-auth flow [-h] [--config CONFIG] [--env-file ENV_FILE]
                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                        [--tenant TENANT] [--issuer ISSUER]
                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                        [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth flow create`

```text
usage: tba-auth flow create [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth flow delete`

```text
usage: tba-auth flow delete [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth flow disable`

```text
usage: tba-auth flow disable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth flow enable`

```text
usage: tba-auth flow enable [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth flow get`

```text
usage: tba-auth flow get [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth flow list`

```text
usage: tba-auth flow list [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth flow update`

```text
usage: tba-auth flow update [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth gate`

```text
usage: tba-auth gate [-h] [--config CONFIG] [--env-file ENV_FILE]
                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                        [--tenant TENANT] [--issuer ISSUER]
                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                        [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity`

```text
usage: tba-auth identity [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity create`

```text
usage: tba-auth identity create [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity delete`

```text
usage: tba-auth identity delete [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity get`

```text
usage: tba-auth identity get [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity list`

```text
usage: tba-auth identity list [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity lock`

```text
usage: tba-auth identity lock [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity set-password`

```text
usage: tba-auth identity set-password [-h] [--config CONFIG]
                                         [--env-file ENV_FILE]
                                         [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                         [--tenant TENANT] [--issuer ISSUER]
                                         [--surface-set {admin-rpc,diagnostics,public-rest}]
                                         [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                         [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity unlock`

```text
usage: tba-auth identity unlock [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth identity update`

```text
usage: tba-auth identity update [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth import`

```text
usage: tba-auth import [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth import run`

```text
usage: tba-auth import run [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth import status`

```text
usage: tba-auth import status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth import validate`

```text
usage: tba-auth import validate [-h] [--config CONFIG]
                                   [--env-file ENV_FILE]
                                   [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                   [--tenant TENANT] [--issuer ISSUER]
                                   [--surface-set {admin-rpc,diagnostics,public-rest}]
                                   [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                   [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys`

```text
usage: tba-auth keys [-h] [--config CONFIG] [--env-file ENV_FILE]
                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                        [--tenant TENANT] [--issuer ISSUER]
                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                        [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys delete`

```text
usage: tba-auth keys delete [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys export`

```text
usage: tba-auth keys export [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys generate`

```text
usage: tba-auth keys generate [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys get`

```text
usage: tba-auth keys get [-h] [--config CONFIG] [--env-file ENV_FILE]
                            [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                            [--tenant TENANT] [--issuer ISSUER]
                            [--surface-set {admin-rpc,diagnostics,public-rest}]
                            [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                            [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys import`

```text
usage: tba-auth keys import [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys list`

```text
usage: tba-auth keys list [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys publish-jwks`

```text
usage: tba-auth keys publish-jwks [-h] [--config CONFIG]
                                     [--env-file ENV_FILE]
                                     [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                     [--tenant TENANT] [--issuer ISSUER]
                                     [--surface-set {admin-rpc,diagnostics,public-rest}]
                                     [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                     [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys retire`

```text
usage: tba-auth keys retire [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth keys rotate`

```text
usage: tba-auth keys rotate [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth migrate`

```text
usage: tba-auth migrate [-h] [--config CONFIG] [--env-file ENV_FILE]
                           [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                           [--tenant TENANT] [--issuer ISSUER]
                           [--surface-set {admin-rpc,diagnostics,public-rest}]
                           [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                           [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
    apply               Apply the migration evidence bundle plan.
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth migrate apply`

```text
usage: tba-auth migrate apply [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
                                 [--plugin-mode {admin-only,diagnostics-only,mixed,public-only}]
                                 [--runtime-style {plugin,standalone}]
                                 [--strict] [--no-strict]
                                 [--format {json,yaml,text}] [--output OUTPUT]
                                 [--verbose] [--trace] [--repo-root REPO_ROOT]
                                 [--yes] [--dry-run] [--wait]
                                 [--timeout TIMEOUT]

Record a migration application evidence bundle for the structured plan.

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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth migrate plan`

```text
usage: tba-auth migrate plan [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth migrate status`

```text
usage: tba-auth migrate status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth migrate verify`

```text
usage: tba-auth migrate verify [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth release`

```text
usage: tba-auth release [-h] [--config CONFIG] [--env-file ENV_FILE]
                           [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                           [--tenant TENANT] [--issuer ISSUER]
                           [--surface-set {admin-rpc,diagnostics,public-rest}]
                           [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                           [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth release bundle`

```text
usage: tba-auth release bundle [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth release recertify`

```text
usage: tba-auth release recertify [-h] [--config CONFIG]
                                     [--env-file ENV_FILE]
                                     [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                     [--tenant TENANT] [--issuer ISSUER]
                                     [--surface-set {admin-rpc,diagnostics,public-rest}]
                                     [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                     [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth release sign`

```text
usage: tba-auth release sign [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth release status`

```text
usage: tba-auth release status [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth release verify`

```text
usage: tba-auth release verify [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth serve`

```text
usage: tba-auth serve [-h] [--config CONFIG] [--env-file ENV_FILE]
                         [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                         [--tenant TENANT] [--issuer ISSUER]
                         [--surface-set {admin-rpc,diagnostics,public-rest}]
                         [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                         [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth session`

```text
usage: tba-auth session [-h] [--config CONFIG] [--env-file ENV_FILE]
                           [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                           [--tenant TENANT] [--issuer ISSUER]
                           [--surface-set {admin-rpc,diagnostics,public-rest}]
                           [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                           [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth session get`

```text
usage: tba-auth session get [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth session list`

```text
usage: tba-auth session list [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth session revoke`

```text
usage: tba-auth session revoke [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth session revoke-all`

```text
usage: tba-auth session revoke-all [-h] [--config CONFIG]
                                      [--env-file ENV_FILE]
                                      [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                      [--tenant TENANT] [--issuer ISSUER]
                                      [--surface-set {admin-rpc,diagnostics,public-rest}]
                                      [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                      [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth spec`

```text
usage: tba-auth spec [-h] [--config CONFIG] [--env-file ENV_FILE]
                        [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                        [--tenant TENANT] [--issuer ISSUER]
                        [--surface-set {admin-rpc,diagnostics,public-rest}]
                        [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                        [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth spec diff`

```text
usage: tba-auth spec diff [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth spec generate`

```text
usage: tba-auth spec generate [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth spec report`

```text
usage: tba-auth spec report [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth spec validate`

```text
usage: tba-auth spec validate [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth tenant`

```text
usage: tba-auth tenant [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth tenant create`

```text
usage: tba-auth tenant create [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth tenant delete`

```text
usage: tba-auth tenant delete [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth tenant disable`

```text
usage: tba-auth tenant disable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth tenant enable`

```text
usage: tba-auth tenant enable [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth tenant get`

```text
usage: tba-auth tenant get [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth tenant list`

```text
usage: tba-auth tenant list [-h] [--config CONFIG] [--env-file ENV_FILE]
                               [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                               [--tenant TENANT] [--issuer ISSUER]
                               [--surface-set {admin-rpc,diagnostics,public-rest}]
                               [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                               [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth tenant update`

```text
usage: tba-auth tenant update [-h] [--config CONFIG] [--env-file ENV_FILE]
                                 [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                 [--tenant TENANT] [--issuer ISSUER]
                                 [--surface-set {admin-rpc,diagnostics,public-rest}]
                                 [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                 [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth token`

```text
usage: tba-auth token [-h] [--config CONFIG] [--env-file ENV_FILE]
                         [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                         [--tenant TENANT] [--issuer ISSUER]
                         [--surface-set {admin-rpc,diagnostics,public-rest}]
                         [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                         [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth token exchange`

```text
usage: tba-auth token exchange [-h] [--config CONFIG] [--env-file ENV_FILE]
                                  [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                  [--tenant TENANT] [--issuer ISSUER]
                                  [--surface-set {admin-rpc,diagnostics,public-rest}]
                                  [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                  [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth token get`

```text
usage: tba-auth token get [-h] [--config CONFIG] [--env-file ENV_FILE]
                             [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                             [--tenant TENANT] [--issuer ISSUER]
                             [--surface-set {admin-rpc,diagnostics,public-rest}]
                             [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                             [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth token introspect`

```text
usage: tba-auth token introspect [-h] [--config CONFIG]
                                    [--env-file ENV_FILE]
                                    [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                    [--tenant TENANT] [--issuer ISSUER]
                                    [--surface-set {admin-rpc,diagnostics,public-rest}]
                                    [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                    [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth token list`

```text
usage: tba-auth token list [-h] [--config CONFIG] [--env-file ENV_FILE]
                              [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                              [--tenant TENANT] [--issuer ISSUER]
                              [--surface-set {admin-rpc,diagnostics,public-rest}]
                              [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                              [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth token revoke`

```text
usage: tba-auth token revoke [-h] [--config CONFIG] [--env-file ENV_FILE]
                                [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                                [--tenant TENANT] [--issuer ISSUER]
                                [--surface-set {admin-rpc,diagnostics,public-rest}]
                                [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                                [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

### `tba-auth verify`

```text
usage: tba-auth verify [-h] [--config CONFIG] [--env-file ENV_FILE]
                          [--profile {baseline,production,hardening,fapi2-security,peer-claim}]
                          [--tenant TENANT] [--issuer ISSUER]
                          [--surface-set {admin-rpc,diagnostics,public-rest}]
                          [--slice {device,dpop,jar,mtls,par,rar,token-exchange}]
                          [--extension {dns-privacy,set,webauthn-passkeys,webpush}]
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
  --extension {dns-privacy,set,webauthn-passkeys,webpush}
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

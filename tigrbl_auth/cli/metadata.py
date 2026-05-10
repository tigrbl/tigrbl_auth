from __future__ import annotations

"""Canonical CLI metadata for parser generation, docs, and contract artifacts.

This module is the single source of truth for the operator CLI surface.
Argparse help output, markdown reference docs, machine-readable contract
artifacts, and conformance snapshots are all derived from these structures.
"""

import argparse
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from tigrbl_auth.config.deployment import (
    EXTENSION_REGISTRY,
    PLUGIN_MODE_TO_SURFACE_SETS,
    PROTOCOL_SLICE_REGISTRY,
    SURFACE_SET_REGISTRY,
)
from tigrbl_auth.runtime import iter_runner_adapters, registered_runner_names


@dataclass(slots=True)
class FlagSpec:
    key: str
    flags: tuple[str, ...]
    help: str
    kwargs: dict[str, Any] = field(default_factory=dict)
    group: str = "general"
    family: str = "general"

    def to_manifest(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "key": self.key,
            "flags": list(self.flags),
            "help": self.help,
            "group": self.group,
            "family": self.family,
        }
        for field_name in ("default", "choices", "required", "nargs", "metavar", "dest"):
            if field_name in self.kwargs:
                value = self.kwargs[field_name]
                payload[field_name] = list(value) if isinstance(value, tuple) else value
        action = self.kwargs.get("action")
        if action is not None:
            if isinstance(action, str):
                payload["action"] = action
            else:
                payload["action"] = getattr(action, "__name__", str(action))
        type_fn = self.kwargs.get("type")
        if type_fn is not None:
            payload["type"] = getattr(type_fn, "__name__", str(type_fn))
        return payload


# Backward-compatible alias for earlier checkpoints/tests.
ArgumentSpec = FlagSpec


@dataclass(slots=True, frozen=True)
class OutputSpec:
    name: str
    description: str
    fields: tuple[str, ...] = ()
    media_types: tuple[str, ...] = ("json", "yaml", "text")

    def to_manifest(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "fields": list(self.fields),
            "media_types": list(self.media_types),
        }


@dataclass(slots=True, frozen=True)
class ExitCodeSpec:
    code: int
    meaning: str

    def to_manifest(self) -> dict[str, Any]:
        return {"code": self.code, "meaning": self.meaning}


@dataclass(slots=True)
class VerbSpec:
    name: str
    help: str
    description: str
    handler: str
    flags: tuple[str, ...] = ()
    aliases: tuple[str, ...] = ()
    include_global: bool = True
    output: OutputSpec | None = None
    exit_codes: tuple[ExitCodeSpec, ...] = ()
    examples: tuple[str, ...] = ()
    family: str = "operator"

    @property
    def args(self) -> tuple[str, ...]:
        return self.flags

    def to_manifest(self, *, global_flags: Sequence[str]) -> dict[str, Any]:
        return {
            "name": self.name,
            "help": self.help,
            "description": self.description,
            "handler": self.handler,
            "aliases": list(self.aliases),
            "include_global": self.include_global,
            "global_flags": list(global_flags) if self.include_global else [],
            "flags": list(self.flags),
            "output": self.output.to_manifest() if self.output is not None else None,
            "exit_codes": [spec.to_manifest() for spec in self.exit_codes],
            "examples": list(self.examples),
            "family": self.family,
        }


@dataclass(slots=True)
class CommandSpec:
    name: str
    help: str
    description: str
    handler: str | None = None
    flags: tuple[str, ...] = ()
    verbs: tuple[VerbSpec, ...] = ()
    aliases: tuple[str, ...] = ()
    include_global: bool = True
    family: str = "operator"
    examples: tuple[str, ...] = ()
    output: OutputSpec | None = None
    exit_codes: tuple[ExitCodeSpec, ...] = ()

    @property
    def args(self) -> tuple[str, ...]:
        return self.flags

    @property
    def subcommands(self) -> tuple[VerbSpec, ...]:
        return self.verbs

    def to_manifest(self, *, global_flags: Sequence[str]) -> dict[str, Any]:
        return {
            "name": self.name,
            "help": self.help,
            "description": self.description,
            "handler": self.handler,
            "aliases": list(self.aliases),
            "include_global": self.include_global,
            "global_flags": list(global_flags) if self.include_global else [],
            "flags": list(self.flags),
            "verbs": [verb.to_manifest(global_flags=global_flags) for verb in self.verbs],
            "family": self.family,
            "examples": list(self.examples),
            "output": self.output.to_manifest() if self.output is not None else None,
            "exit_codes": [spec.to_manifest() for spec in self.exit_codes],
        }


def _runner_flag_kwargs(value_type: str, default: Any, choices: Sequence[str]) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}
    if value_type == "int":
        kwargs["type"] = int
    elif value_type == "float":
        kwargs["type"] = float
    elif value_type == "bool":
        kwargs["action"] = argparse.BooleanOptionalAction
    if choices:
        kwargs["choices"] = list(choices)
    if default is not None:
        kwargs["default"] = default
    return kwargs


def _runtime_runner_argument_specs() -> dict[str, FlagSpec]:
    specs: dict[str, FlagSpec] = {}
    for adapter in iter_runner_adapters():
        for meta in adapter.flag_metadata:
            if meta.name in specs or meta.name in ARGUMENT_SPECS:
                continue
            specs[meta.name] = FlagSpec(
                meta.name,
                meta.flags,
                meta.description,
                _runner_flag_kwargs(meta.value_type, meta.default, meta.choices),
                group="serve",
                family="runtime-backend",
            )
    return specs


ARGUMENT_SPECS: dict[str, FlagSpec] = {
    # Global/shared flags.
    "env_file": FlagSpec("env_file", ("--env-file",), "Optional environment file loaded before resolution.", {"default": None}, group="global", family="global"),
    "profile": FlagSpec("profile", ("--profile",), "Runtime profile reference: packaged profile id or external YAML profile path.", {"default": "baseline"}, group="global", family="global"),
    "tenant": FlagSpec("tenant", ("--tenant",), "Tenant identifier for multi-tenant operators.", {"default": None}, group="global", family="global"),
    "issuer": FlagSpec("issuer", ("--issuer",), "Issuer override for discovery and contract generation.", {"default": None}, group="global", family="global"),
    "surface_set": FlagSpec("surface_set", ("--surface-set",), "Installable surface set. May be supplied multiple times.", {"action": "append", "choices": sorted(SURFACE_SET_REGISTRY), "default": []}, group="global", family="global"),
    "slice": FlagSpec("slice", ("--slice",), "Protocol slice. May be supplied multiple times.", {"action": "append", "choices": sorted(PROTOCOL_SLICE_REGISTRY), "default": []}, group="global", family="global"),
    "extension": FlagSpec("extension", ("--extension",), "Extension boundary slice. May be supplied multiple times.", {"action": "append", "choices": sorted(EXTENSION_REGISTRY), "default": []}, group="global", family="global"),
    "plugin_mode": FlagSpec("plugin_mode", ("--plugin-mode",), "Plugin composition mode.", {"choices": sorted(PLUGIN_MODE_TO_SURFACE_SETS), "default": "mixed"}, group="global", family="global"),
    "runtime_style": FlagSpec("runtime_style", ("--runtime-style",), "Runtime style for installation or standalone serving.", {"choices": ["plugin", "standalone"], "default": "standalone"}, group="global", family="global"),
    "strict": FlagSpec("strict", ("--strict",), "Fail closed when governance or certification checks fail.", {"action": "store_true", "default": True}, group="global", family="global"),
    "no_strict": FlagSpec("no_strict", ("--no-strict",), "Downgrade failures to warnings for exploratory use.", {"action": "store_true"}, group="global", family="global"),
    "offline": FlagSpec("offline", ("--offline",), "Avoid network or external peer execution assumptions.", {"action": "store_true"}, group="global", family="global"),
    "format": FlagSpec("format", ("--format",), "Output format.", {"choices": ["json", "yaml", "text"], "default": "json"}, group="global", family="global"),
    "output": FlagSpec("output", ("--output",), "Optional output file path.", {"default": None}, group="global", family="global"),
    "verbose": FlagSpec("verbose", ("--verbose", "-v"), "Increase operator verbosity; may be repeated.", {"action": "count", "default": 0}, group="global", family="global"),
    "trace": FlagSpec("trace", ("--trace",), "Emit trace-oriented operator details.", {"action": "store_true"}, group="global", family="global"),
    "color": FlagSpec("color", ("--color",), "Color policy for terminal output.", {"choices": ["auto", "always", "never"], "default": "auto"}, group="global", family="global"),
    # Common operator plumbing.
    "repo_root": FlagSpec("repo_root", ("--repo-root",), "Repository root for governance automation.", {"default": None}, group="plumbing", family="plumbing"),
    "report_dir": FlagSpec("report_dir", ("--report-dir",), "Directory for generated reports.", {"default": None}, group="plumbing", family="plumbing"),
    "name": FlagSpec("name", ("--name",), "Optional named release gate or artifact selector.", {"default": None}, group="plumbing", family="plumbing"),
    "environment": FlagSpec("environment", ("--environment",), "Deployment environment label.", {"default": "development"}, group="plumbing", family="plumbing"),
    # Serve/runtime flags.
    "server": FlagSpec("server", ("--server",), "Runner profile used to qualify and launch runtime.", {"choices": list(registered_runner_names()), "default": "uvicorn"}, group="serve", family="serve-portable"),
    "host": FlagSpec("host", ("--host",), "Bind host.", {"default": "127.0.0.1"}, group="serve", family="serve-portable"),
    "port": FlagSpec("port", ("--port",), "Bind port.", {"type": int, "default": 8000}, group="serve", family="serve-portable"),
    "uds": FlagSpec("uds", ("--uds",), "Optional Unix domain socket path.", {"default": None}, group="serve", family="serve-portable"),
    "workers": FlagSpec("workers", ("--workers",), "Process count for the selected runtime profile.", {"type": int, "default": 1}, group="serve", family="serve-portable"),
    "public": FlagSpec("public", ("--public",), "Enable the public REST/auth plane.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "admin": FlagSpec("admin", ("--admin",), "Enable the admin/control plane.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "rpc": FlagSpec("rpc", ("--rpc",), "Enable the JSON-RPC control plane.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "diagnostics": FlagSpec("diagnostics", ("--diagnostics",), "Enable diagnostics surfaces.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "proxy_headers": FlagSpec("proxy_headers", ("--proxy-headers",), "Honor proxy forwarding headers.", {"action": "store_true"}, group="serve", family="serve-portable"),
    "require_tls": FlagSpec("require_tls", ("--require-tls",), "Require TLS on the public plane.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "enable_mtls": FlagSpec("enable_mtls", ("--enable-mtls",), "Enable mTLS slice for the serve plan.", {"action": argparse.BooleanOptionalAction, "default": False}, group="serve", family="serve-portable"),
    "db_safe_start": FlagSpec("db_safe_start", ("--db-safe-start",), "Require a safe database start posture.", {"action": "store_true"}, group="serve", family="serve-portable"),
    "jwks_refresh_seconds": FlagSpec("jwks_refresh_seconds", ("--jwks-refresh-seconds",), "JWKS refresh cadence in seconds.", {"type": int, "default": 300}, group="serve", family="serve-portable"),
    "cookies": FlagSpec("cookies", ("--cookies",), "Enable cookie/session helpers in serve plans.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "health": FlagSpec("health", ("--health",), "Enable health endpoints in serve plans.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "metrics": FlagSpec("metrics", ("--metrics",), "Enable metrics in serve plans.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "log_level": FlagSpec("log_level", ("--log-level",), "Operator log level for serve plans.", {"default": "INFO"}, group="serve", family="serve-portable"),
    "access_log": FlagSpec("access_log", ("--access-log",), "Enable access logging for the selected runtime profile.", {"action": argparse.BooleanOptionalAction, "default": True}, group="serve", family="serve-portable"),
    "lifespan": FlagSpec("lifespan", ("--lifespan",), "ASGI lifespan policy.", {"choices": ["auto", "on", "off"], "default": "auto"}, group="serve", family="serve-portable"),
    "graceful_timeout": FlagSpec("graceful_timeout", ("--graceful-timeout",), "Graceful shutdown timeout in seconds.", {"type": int, "default": 30}, group="serve", family="serve-portable"),
    "pid_file": FlagSpec("pid_file", ("--pid-file",), "Optional PID file written for the launched runtime.", {"default": None}, group="serve", family="serve-portable"),
    "dry_run": FlagSpec("dry_run", ("--dry-run",), "Resolve and emit the runtime plan without applying or launching state changes.", {"action": "store_true"}, group="serve", family="serve-portable"),
    "check": FlagSpec("check", ("--check",), "Validate the selected runner profile and application factory without launching runtime.", {"action": "store_true"}, group="serve", family="serve-portable"),
    # Verification and release flags.
    "scope": FlagSpec("scope", ("--scope",), "Verification scope.", {"choices": [
        "governance",
        "claims",
        "runtime-foundation",
        "feature-surface-modularity",
        "boundary-enforcement",
        "wrapper-hygiene",
        "contract-sync",
        "contracts",
        "evidence-peer",
        "project-tree-layout",
        "migration-plan",
        "state-reports",
        "test-classification",
        "release-gates",
        "all",
    ], "default": "all"}, group="verify", family="verify"),
    "kind": FlagSpec("kind", ("--kind",), "Contract artifact kind.", {"choices": ["openapi", "openrpc", "all"], "default": "all"}, group="contracts", family="contracts"),
    "baseline_file": FlagSpec("baseline_file", ("--baseline-file",), "Optional explicit baseline artifact for diff operations.", {"default": None}, group="contracts", family="contracts"),
    "tier": FlagSpec("tier", ("--tier",), "Evidence tier selector.", {"choices": ["3", "4", "all"], "default": "all"}, group="evidence", family="evidence"),
    "bundle_dir": FlagSpec("bundle_dir", ("--bundle-dir",), "Explicit bundle output directory.", {"default": None}, group="release", family="release"),
    "artifact": FlagSpec("artifact", ("--artifact",), "Release artifact subset.", {"choices": ["claims", "evidence", "contracts", "all"], "default": "all"}, group="release", family="release"),
    "signing_key": FlagSpec("signing_key", ("--signing-key",), "Optional Ed25519 private signing key path or seed.", {"default": None}, group="release", family="release"),
    "peer_profile": FlagSpec("peer_profile", ("--peer-profile",), "Peer profile selector. May be supplied multiple times.", {"action": "append", "default": []}, group="evidence", family="evidence"),
    "execution_mode": FlagSpec("execution_mode", ("--execution-mode",), "Peer execution mode.", {"choices": ["self-check", "dry-run", "record-only"], "default": "self-check"}, group="evidence", family="evidence"),
    "title": FlagSpec("title", ("--title",), "Human-readable title.", {"default": None}, group="governance", family="governance"),
    # Query and mutation flag families.
    "id": FlagSpec("id", ("--id",), "Primary identifier for a single record.", {"default": None}, group="selection", family="query-selection"),
    "filter": FlagSpec("filter", ("--filter",), "Simple substring filter applied to identifiers or names.", {"default": None}, group="selection", family="query-selection"),
    "limit": FlagSpec("limit", ("--limit",), "Maximum number of results to return.", {"type": int, "default": 50}, group="selection", family="query-selection"),
    "offset": FlagSpec("offset", ("--offset",), "Result offset for list operations.", {"type": int, "default": 0}, group="selection", family="query-selection"),
    "sort": FlagSpec("sort", ("--sort",), "Sort key for list operations.", {"choices": ["id", "name", "status", "created_at", "updated_at"], "default": "id"}, group="selection", family="query-selection"),
    "status_filter": FlagSpec("status_filter", ("--status",), "Status filter for list operations.", {"default": None}, group="selection", family="query-selection"),
    "from_file": FlagSpec("from_file", ("--from-file",), "Load mutation input from a JSON or YAML file.", {"default": None}, group="mutation", family="mutation-input"),
    "set_item": FlagSpec("set_item", ("--set",), "Inline mutation field assignment in key=value form. May be supplied multiple times.", {"action": "append", "default": [], "metavar": "key=value"}, group="mutation", family="mutation-input"),
    "if_exists": FlagSpec("if_exists", ("--if-exists",), "Behavior when the target already exists.", {"choices": ["fail", "replace", "merge", "skip"], "default": "fail"}, group="mutation", family="mutation-input"),
    "if_missing": FlagSpec("if_missing", ("--if-missing",), "Behavior when the target does not already exist.", {"choices": ["fail", "create", "skip"], "default": "fail"}, group="mutation", family="mutation-input"),
    "yes": FlagSpec("yes", ("--yes",), "Assume yes for state-changing confirmations.", {"action": "store_true"}, group="mutation", family="mutation-input"),
    "wait": FlagSpec("wait", ("--wait",), "Wait for completion when the operation supports asynchronous execution.", {"action": "store_true"}, group="mutation", family="mutation-input"),
    "timeout": FlagSpec("timeout", ("--timeout",), "Maximum wait time in seconds for supported long-running operations.", {"type": int, "default": 30}, group="mutation", family="mutation-input"),
    # Import/export.
    "input_path": FlagSpec("input_path", ("--input",), "Input path for import, validation, or diff operations.", {"default": None}, group="portability", family="import-export"),
    "include_secrets": FlagSpec("include_secrets", ("--include-secrets",), "Include secret material where the selected surface permits it.", {"action": "store_true"}, group="portability", family="import-export"),
    "redact": FlagSpec("redact", ("--redact",), "Redact secret material from exported output.", {"action": "store_true"}, group="portability", family="import-export"),
    "checksum": FlagSpec("checksum", ("--checksum",), "Expected checksum or checksum algorithm for import/export validation.", {"default": None}, group="portability", family="import-export"),
    # Key lifecycle.
    "alg": FlagSpec("alg", ("--alg",), "JWA/JOSE algorithm identifier.", {"default": None}, group="keys", family="key-lifecycle"),
    "kid": FlagSpec("kid", ("--kid",), "Explicit key identifier.", {"default": None}, group="keys", family="key-lifecycle"),
    "use": FlagSpec("use", ("--use",), "JWK use classification.", {"choices": ["sig", "enc"], "default": "sig"}, group="keys", family="key-lifecycle"),
    "kty": FlagSpec("kty", ("--kty",), "JWK key type.", {"choices": ["RSA", "EC", "OKP", "oct"], "default": "OKP"}, group="keys", family="key-lifecycle"),
    "curve": FlagSpec("curve", ("--curve",), "Curve for EC/OKP keys.", {"choices": ["Ed25519", "P-256", "P-384", "X25519"], "default": "Ed25519"}, group="keys", family="key-lifecycle"),
    "activate": FlagSpec("activate", ("--activate",), "Mark a generated or imported key active immediately.", {"action": "store_true"}, group="keys", family="key-lifecycle"),
    "retire_after": FlagSpec("retire_after", ("--retire-after",), "Retire-after hint or timestamp recorded with the key.", {"default": None}, group="keys", family="key-lifecycle"),
    "publish": FlagSpec("publish", ("--publish",), "Publish JWKS after a successful key mutation.", {"action": "store_true"}, group="keys", family="key-lifecycle"),
}
ARGUMENT_SPECS.update(_runtime_runner_argument_specs())


GLOBAL_ARGUMENT_KEYS: tuple[str, ...] = (
    "env_file",
    "profile",
    "tenant",
    "issuer",
    "surface_set",
    "slice",
    "extension",
    "plugin_mode",
    "runtime_style",
    "strict",
    "no_strict",
    "format",
    "output",
    "verbose",
    "trace",
)

RESOURCE_COMMANDS: tuple[str, ...] = (
    "tenant",
    "client",
    "identity",
    "flow",
    "session",
    "token",
    "keys",
    "discovery",
    "import",
    "export",
)


PORTABLE_EXIT_CODES: tuple[ExitCodeSpec, ...] = (
    ExitCodeSpec(0, "Operation completed successfully."),
    ExitCodeSpec(1, "Operation failed or verification did not pass."),
    ExitCodeSpec(2, "CLI argument or contract validation failed before execution."),
)
MUTATION_EXIT_CODES: tuple[ExitCodeSpec, ...] = PORTABLE_EXIT_CODES + (
    ExitCodeSpec(3, "Requested record or dependent resource was not found."),
)


OUTPUT_RUNTIME = OutputSpec(
    "runtime-launch",
    "Runtime plan, runner diagnostics, and launch/evidence metadata.",
    fields=("command", "server", "launch_mode", "runtime_plan", "selected_runner_profile", "runner_profile_report_paths"),
)
OUTPUT_RECORD = OutputSpec(
    "resource-record",
    "Single operator resource record with state and metadata.",
    fields=("command", "resource", "record", "state_path"),
)
OUTPUT_COLLECTION = OutputSpec(
    "resource-collection",
    "Collection output for list/status operations.",
    fields=("command", "resource", "items", "total", "offset", "limit"),
)
OUTPUT_VERIFICATION = OutputSpec(
    "verification-report",
    "Verification result payload with summary, failures, and warnings.",
    fields=("command", "passed", "summary", "failures"),
)
OUTPUT_RELEASE = OutputSpec(
    "release-artifact",
    "Release bundle, signing, or recertification payload.",
    fields=("command", "bundle_dir", "summary"),
)
OUTPUT_CLAIMS = OutputSpec(
    "claims-artifact",
    "Claims/evidence payload describing effective certification state.",
    fields=("command", "claims_manifest", "evidence_manifest", "active_targets"),
)
OUTPUT_CONTRACT = OutputSpec(
    "contract-artifact",
    "OpenAPI/OpenRPC contract generation or validation payload.",
    fields=("command", "generated", "reports"),
)


def _verb(
    name: str,
    help_text: str,
    description: str,
    handler: str,
    flags: Sequence[str],
    *,
    family: str,
    output: OutputSpec = OUTPUT_RECORD,
    exit_codes: tuple[ExitCodeSpec, ...] = MUTATION_EXIT_CODES,
    examples: Sequence[str] = (),
) -> VerbSpec:
    return VerbSpec(
        name=name,
        help=help_text,
        description=description,
        handler=handler,
        flags=tuple(flags),
        family=family,
        output=output,
        exit_codes=exit_codes,
        examples=tuple(examples),
    )


COMMAND_SPECS: tuple[CommandSpec, ...] = (
    CommandSpec(
        name="serve",
        help="Launch the selected runner-backed ASGI runtime.",
        description="Resolve deployment, materialize a runner-qualified runtime plan, validate the selected profile, and optionally launch runtime.",
        handler="serve",
        flags=(
            "repo_root",
            "report_dir",
            "environment",
            "server",
            "host",
            "port",
            "workers",
            "uds",
            "log_level",
            "access_log",
            "proxy_headers",
            "lifespan",
            "graceful_timeout",
            "pid_file",
            "health",
            "metrics",
            "public",
            "admin",
            "rpc",
            "diagnostics",
            "require_tls",
            "enable_mtls",
            "cookies",
            "jwks_refresh_seconds",
            "dry_run",
            "check",
            "db_safe_start",
            "uvicorn_loop",
            "uvicorn_http",
            "uvicorn_ws",
            "hypercorn_worker_class",
            "hypercorn_http2",
            "tigrcorn_contract",
            "tigrcorn_mode",
        ),
        family="runtime",
        examples=(
            "tigrbl-auth serve --server uvicorn --check",
            "tigrbl-auth serve --server hypercorn --host 0.0.0.0 --port 8443",
            "tigrbl-auth serve --server tigrcorn --dry-run --format yaml",
        ),
        output=OUTPUT_RUNTIME,
        exit_codes=PORTABLE_EXIT_CODES,
    ),
    CommandSpec(
        name="verify",
        help="Run verification scopes against the repository boundary.",
        description="Execute one or more verification scopes and emit structured results.",
        handler="verify",
        flags=("repo_root", "report_dir", "scope"),
        family="governance",
        output=OUTPUT_VERIFICATION,
        exit_codes=PORTABLE_EXIT_CODES,
    ),
    CommandSpec(
        name="gate",
        help="Run release gate checks.",
        description="Run one release gate or the full ordered release gate catalog.",
        handler="gate",
        flags=("repo_root", "report_dir", "name"),
        family="governance",
        output=OUTPUT_VERIFICATION,
        exit_codes=PORTABLE_EXIT_CODES,
    ),
    CommandSpec(
        name="spec",
        help="Generate, diff, and validate public contract artifacts.",
        description="Operate on the OpenAPI and OpenRPC contract surfaces.",
        verbs=(
            _verb("generate", "Generate contract artifacts.", "Generate OpenAPI/OpenRPC artifacts for the selected deployment.", "spec.generate", ("repo_root", "kind", "report_dir"), family="contracts", output=OUTPUT_CONTRACT, exit_codes=PORTABLE_EXIT_CODES),
            _verb("validate", "Validate generated contracts.", "Validate generated contracts against repository expectations.", "spec.validate", ("repo_root", "kind", "report_dir"), family="contracts", output=OUTPUT_CONTRACT, exit_codes=PORTABLE_EXIT_CODES),
            _verb("diff", "Diff generated contracts.", "Regenerate contracts and compare them to committed artifacts.", "spec.diff", ("repo_root", "kind", "baseline_file", "report_dir"), family="contracts", output=OUTPUT_CONTRACT, exit_codes=PORTABLE_EXIT_CODES),
            _verb("report", "Write contract summary reports.", "Summarize active contract contents and profile coverage.", "spec.report", ("repo_root", "kind", "report_dir"), family="contracts", output=OUTPUT_CONTRACT, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="contracts",
    ),
    CommandSpec(
        name="claims",
        help="Lint and materialize effective claims.",
        description="Operate on the claims plane.",
        verbs=(
            _verb("lint", "Run claims lint.", "Validate declared claims against mappings and boundaries.", "claims.lint", ("repo_root", "report_dir"), family="governance", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("show", "Write the effective claims manifest.", "Materialize the effective claims manifest for the active deployment.", "claims.show", ("repo_root",), family="governance", output=OUTPUT_CLAIMS, exit_codes=PORTABLE_EXIT_CODES),
            _verb("status", "Summarize the claims plane.", "Summarize declared, effective, and promotable claims.", "claims.status", ("repo_root", "report_dir"), family="governance", output=OUTPUT_CLAIMS, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="governance",
    ),
    CommandSpec(
        name="evidence",
        help="Build evidence manifests and peer profile artifacts.",
        description="Operate on Tier 3/Tier 4 evidence automation.",
        verbs=(
            _verb("bundle", "Build an evidence bundle.", "Build a release/evidence bundle filtered by the effective deployment.", "evidence.bundle", ("repo_root", "tier", "bundle_dir"), family="evidence", output=OUTPUT_RELEASE, exit_codes=PORTABLE_EXIT_CODES),
            _verb("status", "Summarize evidence readiness.", "Summarize Tier 3/Tier 4 evidence readiness.", "evidence.status", ("repo_root", "tier", "report_dir"), family="evidence", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("verify", "Verify evidence and peer references.", "Run evidence/peer readiness checks.", "evidence.verify", ("repo_root", "report_dir"), family="evidence", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("peer-status", "Summarize peer profile execution readiness.", "Summarize configured peer execution profiles and bundle refs.", "evidence.peer_status", ("repo_root", "report_dir"), family="evidence", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("peer-execute", "Materialize peer execution manifests.", "Materialize peer execution manifests for configured profiles.", "evidence.peer_execute", ("repo_root", "peer_profile", "execution_mode", "report_dir"), family="evidence", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="evidence",
    ),
    CommandSpec(
        name="doctor",
        help="Run an aggregated repository health summary.",
        description="Aggregate core verification, runtime profile, contracts, evidence, and gate status.",
        handler="doctor",
        flags=("repo_root", "report_dir"),
        family="governance",
        output=OUTPUT_VERIFICATION,
        exit_codes=PORTABLE_EXIT_CODES,
    ),
    CommandSpec(
        name="bootstrap",
        help="Bootstrap deployment artifacts and checkpoint lifecycle state.",
        description="Materialize and verify baseline bootstrap manifests for deployment or plugin installation.",
        verbs=(
            _verb("status", "Summarize bootstrap readiness.", "Summarize bootstrap readiness for the selected profile and surfaces.", "bootstrap.status", ("repo_root", "report_dir"), family="operator", output=OUTPUT_COLLECTION),
            _verb("manifest", "Write bootstrap manifests.", "Write deployment, claims, evidence, and contract manifests for the selected profile.", "bootstrap.manifest", ("repo_root", "bundle_dir"), family="operator", output=OUTPUT_RECORD),
            _verb("apply", "Apply bootstrap materialization.", "Materialize bootstrap manifests and record an applied bootstrap checkpoint.", "bootstrap.apply", ("repo_root", "bundle_dir", "yes", "dry_run", "wait", "timeout"), family="operator", output=OUTPUT_RECORD),
            _verb("verify", "Verify bootstrap artifacts.", "Verify bootstrap manifests, effective artifacts, and applied checkpoint state.", "bootstrap.verify", ("repo_root", "report_dir"), family="operator", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="operator",
    ),
    CommandSpec(
        name="migrate",
        help="Inspect migration readiness and plans.",
        description="Migration-chain status, planning, application, and verification operators.",
        verbs=(
            _verb("status", "Show migration status.", "List migration revisions and current-to-target move status.", "migrate.status", ("repo_root", "report_dir"), family="operator", output=OUTPUT_COLLECTION),
            _verb("plan", "Emit migration plan details.", "Emit the structured migration plan and replacement order.", "migrate.plan", ("repo_root",), family="operator", output=OUTPUT_RECORD),
            _verb("apply", "Apply the migration checkpoint plan.", "Record a migration application checkpoint for the structured plan.", "migrate.apply", ("repo_root", "yes", "dry_run", "wait", "timeout"), family="operator", output=OUTPUT_RECORD),
            _verb("verify", "Verify migration artifacts.", "Run migration-plan and project-tree verification.", "migrate.verify", ("repo_root", "report_dir"), family="operator", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="operator",
    ),
    CommandSpec(
        name="release",
        help="Build release bundles and recertification reports.",
        description="Release automation and recertification operators.",
        verbs=(
            _verb("bundle", "Build a release bundle.", "Build a release bundle containing claims, evidence, contracts, ADR index, and peer refs.", "release.bundle", ("repo_root", "bundle_dir", "artifact"), family="release", output=OUTPUT_RELEASE, exit_codes=PORTABLE_EXIT_CODES),
            _verb("sign", "Sign a release bundle.", "Create externally verifiable Ed25519 attestations for an existing release bundle.", "release.sign", ("repo_root", "bundle_dir", "signing_key"), family="release", output=OUTPUT_RELEASE, exit_codes=PORTABLE_EXIT_CODES),
            _verb("verify", "Verify a signed release bundle.", "Verify release-bundle attestations and manifest integrity for an existing signed bundle.", "release.verify", ("repo_root", "bundle_dir"), family="release", output=OUTPUT_RELEASE, exit_codes=PORTABLE_EXIT_CODES),
            _verb("status", "Summarize release bundle status.", "Summarize the current release bundle and release-gate posture.", "release.status", ("repo_root", "report_dir"), family="release", output=OUTPUT_RELEASE, exit_codes=PORTABLE_EXIT_CODES),
            _verb("recertify", "Run recertification checks.", "Re-run recertification for Tigrbl and standards-boundary changes.", "release.recertify", ("repo_root", "report_dir"), family="release", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="release",
    ),
    CommandSpec(
        name="tenant",
        help="Manage tenant records.",
        description="Stateful durable operator-plane tenant lifecycle operators.",
        verbs=(
            _verb("create", "Create a tenant record.", "Create a durable operator-plane tenant record.", "tenant.create", ("repo_root", "id", "from_file", "set_item", "if_exists", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("update", "Update a tenant record.", "Update a durable operator-plane tenant record.", "tenant.update", ("repo_root", "id", "from_file", "set_item", "if_missing", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("delete", "Delete a tenant record.", "Delete a durable operator-plane tenant record.", "tenant.delete", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("get", "Get a tenant record.", "Return a single durable operator-plane tenant record.", "tenant.get", ("repo_root", "id"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("list", "List tenant records.", "List durable operator-plane tenant records.", "tenant.list", ("repo_root", "filter", "limit", "offset", "sort", "status_filter"), family="admin", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("enable", "Enable a tenant.", "Mark a tenant record enabled.", "tenant.enable", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("disable", "Disable a tenant.", "Mark a tenant record disabled.", "tenant.disable", ("repo_root", "id", "yes", "dry_run"), family="admin"),
        ),
        family="admin",
    ),
    CommandSpec(
        name="client",
        help="Manage client records.",
        description="Stateful durable operator-plane client lifecycle operators.",
        verbs=(
            _verb("create", "Create a client record.", "Create a durable operator-plane client record.", "client.create", ("repo_root", "id", "from_file", "set_item", "if_exists", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("update", "Update a client record.", "Update a durable operator-plane client record.", "client.update", ("repo_root", "id", "from_file", "set_item", "if_missing", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("delete", "Delete a client record.", "Delete a durable operator-plane client record.", "client.delete", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("get", "Get a client record.", "Return a single durable operator-plane client record.", "client.get", ("repo_root", "id"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("list", "List client records.", "List durable operator-plane client records.", "client.list", ("repo_root", "filter", "limit", "offset", "sort", "status_filter"), family="admin", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("rotate-secret", "Rotate a client secret.", "Rotate durable operator-plane client secret material.", "client.rotate_secret", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("enable", "Enable a client.", "Mark a client record enabled.", "client.enable", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("disable", "Disable a client.", "Mark a client record disabled.", "client.disable", ("repo_root", "id", "yes", "dry_run"), family="admin"),
        ),
        family="admin",
    ),
    CommandSpec(
        name="identity",
        help="Manage identity records.",
        description="Stateful durable operator-plane identity lifecycle operators.",
        verbs=(
            _verb("create", "Create an identity record.", "Create a durable operator-plane identity record.", "identity.create", ("repo_root", "id", "from_file", "set_item", "if_exists", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("update", "Update an identity record.", "Update a durable operator-plane identity record.", "identity.update", ("repo_root", "id", "from_file", "set_item", "if_missing", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("delete", "Delete an identity record.", "Delete a durable operator-plane identity record.", "identity.delete", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("get", "Get an identity record.", "Return a single durable operator-plane identity record.", "identity.get", ("repo_root", "id"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("list", "List identity records.", "List durable operator-plane identity records.", "identity.list", ("repo_root", "filter", "limit", "offset", "sort", "status_filter"), family="admin", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("set-password", "Set an identity password.", "Set or rotate a durable operator-plane identity password hash.", "identity.set_password", ("repo_root", "id", "from_file", "set_item", "yes", "dry_run"), family="admin"),
            _verb("lock", "Lock an identity.", "Mark an identity record locked.", "identity.lock", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("unlock", "Unlock an identity.", "Mark an identity record unlocked.", "identity.unlock", ("repo_root", "id", "yes", "dry_run"), family="admin"),
        ),
        family="admin",
    ),
    CommandSpec(
        name="flow",
        help="Manage flow records.",
        description="Stateful durable operator-plane flow lifecycle operators.",
        verbs=(
            _verb("create", "Create a flow record.", "Create a durable operator-plane flow record.", "flow.create", ("repo_root", "id", "from_file", "set_item", "if_exists", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("update", "Update a flow record.", "Update a durable operator-plane flow record.", "flow.update", ("repo_root", "id", "from_file", "set_item", "if_missing", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("delete", "Delete a flow record.", "Delete a durable operator-plane flow record.", "flow.delete", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("get", "Get a flow record.", "Return a single durable operator-plane flow record.", "flow.get", ("repo_root", "id"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("list", "List flow records.", "List durable operator-plane flow records.", "flow.list", ("repo_root", "filter", "limit", "offset", "sort", "status_filter"), family="admin", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("enable", "Enable a flow.", "Mark a flow record enabled.", "flow.enable", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("disable", "Disable a flow.", "Mark a flow record disabled.", "flow.disable", ("repo_root", "id", "yes", "dry_run"), family="admin"),
        ),
        family="admin",
    ),
    CommandSpec(
        name="session",
        help="Manage session records.",
        description="Stateful durable operator-plane session control operators.",
        verbs=(
            _verb("get", "Get a session record.", "Return a single durable operator-plane session record.", "session.get", ("repo_root", "id"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("list", "List session records.", "List durable operator-plane session records.", "session.list", ("repo_root", "filter", "limit", "offset", "sort", "status_filter"), family="admin", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("revoke", "Revoke a session.", "Mark a durable operator-plane session revoked.", "session.revoke", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("revoke-all", "Revoke all sessions.", "Mark all durable operator-plane sessions revoked.", "session.revoke_all", ("repo_root", "filter", "status_filter", "yes", "dry_run"), family="admin"),
        ),
        family="admin",
    ),
    CommandSpec(
        name="token",
        help="Manage token records.",
        description="Stateful durable operator-plane token control operators.",
        verbs=(
            _verb("get", "Get a token record.", "Return a single durable operator-plane token record.", "token.get", ("repo_root", "id"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("list", "List token records.", "List durable operator-plane token records.", "token.list", ("repo_root", "filter", "limit", "offset", "sort", "status_filter"), family="admin", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("introspect", "Introspect a token.", "Return active/revoked status and metadata for a token record.", "token.introspect", ("repo_root", "id"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("revoke", "Revoke a token.", "Mark a durable operator-plane token revoked.", "token.revoke", ("repo_root", "id", "yes", "dry_run"), family="admin"),
            _verb("exchange", "Exchange a token.", "Create a derived durable operator-plane token exchange record.", "token.exchange", ("repo_root", "id", "from_file", "set_item", "yes", "dry_run"), family="admin"),
        ),
        family="admin",
    ),
    CommandSpec(
        name="keys",
        help="Manage key lifecycle and JWKS publication.",
        description="Stateful durable operator-plane key lifecycle and JWKS publication operators.",
        verbs=(
            _verb("generate", "Generate a key record.", "Generate durable operator-plane key metadata and optional JWKS publication.", "keys.generate", ("repo_root", "id", "kid", "alg", "use", "kty", "curve", "activate", "retire_after", "publish", "yes", "dry_run"), family="admin"),
            _verb("import", "Import key material.", "Import durable operator-plane key metadata from a JSON or YAML file.", "keys.import", ("repo_root", "id", "from_file", "input_path", "activate", "publish", "yes", "dry_run"), family="admin"),
            _verb("export", "Export key material.", "Export durable operator-plane key metadata to a JSON or YAML file.", "keys.export", ("repo_root", "id", "output", "format", "include_secrets", "redact", "checksum"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("rotate", "Rotate active key material.", "Generate successor key metadata and retire the previous active key.", "keys.rotate", ("repo_root", "id", "kid", "alg", "use", "kty", "curve", "activate", "retire_after", "publish", "yes", "dry_run"), family="admin"),
            _verb("retire", "Retire a key.", "Mark a durable operator-plane key retired.", "keys.retire", ("repo_root", "id", "yes", "dry_run", "publish"), family="admin"),
            _verb("publish-jwks", "Publish JWKS.", "Publish the current durable operator-plane JWKS document.", "keys.publish_jwks", ("repo_root", "output", "format", "include_secrets", "redact", "checksum"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("get", "Get a key record.", "Return a single durable operator-plane key record.", "keys.get", ("repo_root", "id"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("list", "List key records.", "List durable operator-plane key records.", "keys.list", ("repo_root", "filter", "limit", "offset", "sort", "status_filter"), family="admin", output=OUTPUT_COLLECTION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("delete", "Delete a key record.", "Delete a durable operator-plane key record.", "keys.delete", ("repo_root", "id", "yes", "dry_run"), family="admin"),
        ),
        family="admin",
    ),
    CommandSpec(
        name="discovery",
        help="Show, validate, publish, and diff discovery artifacts.",
        description="Discovery and metadata operators bound to repository snapshots.",
        verbs=(
            _verb("show", "Show discovery metadata.", "Show the active discovery snapshot for the selected profile.", "discovery.show", ("repo_root",), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
            _verb("validate", "Validate discovery metadata.", "Validate discovery metadata and supporting contracts.", "discovery.validate", ("repo_root", "report_dir"), family="admin", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("publish", "Publish discovery metadata.", "Publish discovery metadata into a release-ready output directory.", "discovery.publish", ("repo_root", "output", "format", "checksum", "yes", "dry_run"), family="admin", output=OUTPUT_RECORD),
            _verb("diff", "Diff discovery metadata.", "Diff active discovery metadata against a provided or published baseline.", "discovery.diff", ("repo_root", "input_path", "report_dir"), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="admin",
    ),
    CommandSpec(
        name="import",
        help="Validate and run import portability workflows.",
        description="Import durable operator-plane state from portable artifacts.",
        verbs=(
            _verb("validate", "Validate import input.", "Validate an import artifact without mutating state.", "import.validate", ("repo_root", "input_path", "format", "checksum", "report_dir"), family="admin", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("run", "Run an import.", "Import durable operator-plane state from a portable artifact.", "import.run", ("repo_root", "input_path", "format", "checksum", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("status", "Show import status.", "Show the last durable operator-plane import status.", "import.status", ("repo_root",), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="admin",
    ),
    CommandSpec(
        name="export",
        help="Validate and run export portability workflows.",
        description="Export durable operator-plane state into portable artifacts.",
        verbs=(
            _verb("validate", "Validate export configuration.", "Validate export configuration and current operator state.", "export.validate", ("repo_root", "output", "format", "include_secrets", "redact", "checksum", "report_dir"), family="admin", output=OUTPUT_VERIFICATION, exit_codes=PORTABLE_EXIT_CODES),
            _verb("run", "Run an export.", "Export durable operator-plane state to a portable artifact.", "export.run", ("repo_root", "output", "format", "include_secrets", "redact", "checksum", "yes", "dry_run", "wait", "timeout"), family="admin"),
            _verb("status", "Show export status.", "Show the last durable operator-plane export status.", "export.status", ("repo_root",), family="admin", output=OUTPUT_RECORD, exit_codes=PORTABLE_EXIT_CODES),
        ),
        family="admin",
    ),
)


COMMAND_FAMILY_ORDER: tuple[str, ...] = (
    "runtime",
    "governance",
    "contracts",
    "evidence",
    "operator",
    "release",
    "admin",
)

FAMILY_TITLES: dict[str, str] = {
    "runtime": "Runtime",
    "governance": "Governance and certification",
    "contracts": "Contracts and automation",
    "evidence": "Evidence and peer validation",
    "operator": "Bootstrap, migration, and operator lifecycle",
    "release": "Release certification and recertification",
    "admin": "Admin/control and resource planes",
}


def _add_argument(parser: argparse.ArgumentParser, spec: FlagSpec) -> None:
    parser.add_argument(*spec.flags, help=spec.help, **dict(spec.kwargs))


def _global_parent() -> argparse.ArgumentParser:
    parent = argparse.ArgumentParser(add_help=False)
    for key in GLOBAL_ARGUMENT_KEYS:
        _add_argument(parent, ARGUMENT_SPECS[key])
    return parent


def _attach_command_spec(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    spec: CommandSpec,
    *,
    global_parent: argparse.ArgumentParser,
) -> None:
    parents = [global_parent] if spec.include_global else []
    parser = subparsers.add_parser(
        spec.name,
        aliases=list(spec.aliases),
        help=spec.help,
        description=spec.description,
        parents=parents,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.set_defaults(top_command=spec.name)
    for key in spec.flags:
        if spec.include_global and key in GLOBAL_ARGUMENT_KEYS:
            continue
        _add_argument(parser, ARGUMENT_SPECS[key])
    if spec.verbs:
        nested = parser.add_subparsers(dest=f"{spec.name}_command", required=True)
        for verb in spec.verbs:
            sub_parents = [global_parent] if verb.include_global else []
            sub_parser = nested.add_parser(
                verb.name,
                aliases=list(verb.aliases),
                help=verb.help,
                description=verb.description,
                parents=sub_parents,
                formatter_class=argparse.RawTextHelpFormatter,
            )
            sub_parser.set_defaults(top_command=spec.name, command=spec.name, handler_name=verb.handler)
            for key in verb.flags:
                if verb.include_global and key in GLOBAL_ARGUMENT_KEYS:
                    continue
                _add_argument(sub_parser, ARGUMENT_SPECS[key])
    else:
        parser.set_defaults(command=spec.name, handler_name=spec.handler)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tigrbl-auth",
        description="Tigrbl-native operator CLI for the tigrbl_auth package.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    global_parent = _global_parent()
    for spec in COMMAND_SPECS:
        _attach_command_spec(subparsers, spec, global_parent=global_parent)
    return parser


def iter_command_specs(specs: Sequence[CommandSpec] | None = None) -> Iterable[CommandSpec]:
    for spec in specs or COMMAND_SPECS:
        yield spec


def build_cli_contract_manifest() -> dict[str, Any]:
    family_counts: dict[str, int] = {}
    verb_count = 0
    for spec in COMMAND_SPECS:
        family_counts[spec.family] = family_counts.get(spec.family, 0) + 1
        verb_count += len(spec.verbs)
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "generated_from": "tigrbl_auth.cli.metadata",
        "summary": {
            "command_count": len(COMMAND_SPECS),
            "verb_count": verb_count,
            "direct_command_count": len([spec for spec in COMMAND_SPECS if not spec.verbs]),
            "nested_command_count": len([spec for spec in COMMAND_SPECS if spec.verbs]),
            "family_count": len(family_counts),
            "family_command_counts": family_counts,
            "global_flag_count": len(GLOBAL_ARGUMENT_KEYS),
            "flag_count": len(ARGUMENT_SPECS),
            "resource_command_count": len(RESOURCE_COMMANDS),
        },
        "global_flags": [ARGUMENT_SPECS[key].to_manifest() for key in GLOBAL_ARGUMENT_KEYS],
        "flag_catalog": {key: spec.to_manifest() for key, spec in sorted(ARGUMENT_SPECS.items())},
        "commands": [spec.to_manifest(global_flags=GLOBAL_ARGUMENT_KEYS) for spec in COMMAND_SPECS],
    }


def _normalize_help_snapshot(text: str) -> str:
    """Normalize argparse help text across Python minor versions."""
    return re.sub(r" \(default: (?:True|False)\)", "", text)


def build_help_snapshots() -> dict[str, str]:
    parser = build_parser()
    snapshots: dict[str, str] = {"tigrbl-auth": _normalize_help_snapshot(parser.format_help())}
    root_subparsers = next(action for action in parser._actions if isinstance(action, argparse._SubParsersAction))
    for spec in COMMAND_SPECS:
        command_parser = root_subparsers.choices[spec.name]
        snapshots[f"tigrbl-auth {spec.name}"] = _normalize_help_snapshot(command_parser.format_help())
        if spec.verbs:
            nested = next(action for action in command_parser._actions if isinstance(action, argparse._SubParsersAction))
            for verb in spec.verbs:
                snapshots[f"tigrbl-auth {spec.name} {verb.name}"] = _normalize_help_snapshot(nested.choices[verb.name].format_help())
    return snapshots


def build_cli_conformance_snapshot() -> dict[str, Any]:
    contract = build_cli_contract_manifest()
    help_snapshots = build_help_snapshots()
    required_verbs = {
        "bootstrap": {"status", "manifest", "apply", "verify"},
        "migrate": {"status", "plan", "apply", "verify"},
        "tenant": {"create", "update", "delete", "get", "list", "enable", "disable"},
        "client": {"create", "update", "delete", "get", "list", "rotate-secret", "enable", "disable"},
        "identity": {"create", "update", "delete", "get", "list", "set-password", "lock", "unlock"},
        "flow": {"create", "update", "delete", "get", "list", "enable", "disable"},
        "session": {"get", "list", "revoke", "revoke-all"},
        "token": {"get", "list", "introspect", "revoke", "exchange"},
        "keys": {"generate", "import", "export", "rotate", "retire", "publish-jwks", "get", "list", "delete"},
        "spec": {"generate", "validate", "diff", "report"},
        "discovery": {"show", "validate", "publish", "diff"},
        "import": {"validate", "run", "status"},
        "export": {"validate", "run", "status"},
        "release": {"bundle", "sign", "verify", "status"},
    }
    missing: dict[str, list[str]] = {}
    catalog_only: list[str] = []
    for spec in COMMAND_SPECS:
        actual = {verb.name for verb in spec.verbs}
        expected = required_verbs.get(spec.name)
        if expected is not None:
            absent = sorted(expected - actual)
            if absent:
                missing[spec.name] = absent
        if spec.name in RESOURCE_COMMANDS:
            meaningful = actual - {"get", "list", "show", "status"}
            if not meaningful:
                catalog_only.append(spec.name)
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "summary": {
            **contract["summary"],
            "help_snapshot_count": len(help_snapshots),
            "required_command_families_present": all(name in {spec.name for spec in COMMAND_SPECS} for name in [
                "serve", "bootstrap", "migrate", "verify", "gate", "spec", "claims", "evidence", "doctor", "release",
                "tenant", "client", "identity", "flow", "session", "token", "keys", "discovery", "import", "export",
            ]),
            "missing_required_verbs": missing,
            "catalog_only_resource_commands": catalog_only,
            "retired_certified_aliases_absent": "key" not in {spec.name for spec in COMMAND_SPECS},
            "passed": not missing and not catalog_only,
        },
        "help_snapshots": help_snapshots,
    }


def render_cli_markdown() -> str:
    lines: list[str] = [
        "# CLI Surface",
        "",
        "> Generated from `tigrbl_auth.cli.metadata`; argparse help, CLI docs, contract artifacts, and conformance snapshots derive from the same metadata source.",
        "",
        "## Global flags",
        "",
    ]
    for key in GLOBAL_ARGUMENT_KEYS:
        arg = ARGUMENT_SPECS[key]
        lines.append(f"- `{', '.join(arg.flags)}` — {arg.help}")
    lines.append("")

    for family in COMMAND_FAMILY_ORDER:
        lines.extend([f"## {FAMILY_TITLES[family]}", ""])
        for spec in COMMAND_SPECS:
            if spec.family != family:
                continue
            lines.append(f"### `{spec.name}`")
            lines.append("")
            lines.append(spec.description)
            lines.append("")
            if spec.aliases:
                lines.append(f"- Aliases: `{', '.join(spec.aliases)}`")
            if spec.flags:
                lines.append("- Flags:")
                for key in spec.flags:
                    arg = ARGUMENT_SPECS[key]
                    lines.append(f"  - `{', '.join(arg.flags)}` — {arg.help}")
            if spec.verbs:
                lines.append("- Verbs:")
                for verb in spec.verbs:
                    lines.append(f"  - `{verb.name}` — {verb.help}")
                    if verb.flags:
                        for key in verb.flags:
                            arg = ARGUMENT_SPECS[key]
                            lines.append(f"    - `{', '.join(arg.flags)}` — {arg.help}")
                    if verb.output is not None:
                        lines.append(f"    - Output: `{verb.output.name}` — {verb.output.description}")
                    if verb.exit_codes:
                        lines.append("    - Exit codes:")
                        for exit_code in verb.exit_codes:
                            lines.append(f"      - `{exit_code.code}` — {exit_code.meaning}")
            elif spec.output is not None:
                lines.append(f"- Output: `{spec.output.name}` — {spec.output.description}")
                if spec.exit_codes:
                    lines.append("- Exit codes:")
                    for exit_code in spec.exit_codes:
                        lines.append(f"  - `{exit_code.code}` — {exit_code.meaning}")
            if spec.examples:
                lines.append("- Examples:")
                for example in spec.examples:
                    lines.append(f"  - `{example}`")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_cli_conformance_markdown(snapshot: dict[str, Any] | None = None) -> str:
    snapshot = snapshot or build_cli_conformance_snapshot()
    summary = snapshot["summary"]
    lines = [
        "# CLI Conformance Snapshot",
        "",
        "> Generated from `tigrbl_auth.cli.metadata` and argparse parser snapshots.",
        "",
        f"- Command count: `{summary['command_count']}`",
        f"- Verb count: `{summary['verb_count']}`",
        f"- Global flag count: `{summary['global_flag_count']}`",
        f"- Help snapshot count: `{summary['help_snapshot_count']}`",
        f"- Required command families present: `{summary['required_command_families_present']}`",
        f"- Retired certified aliases absent: `{summary['retired_certified_aliases_absent']}`",
        f"- Passed: `{summary['passed']}`",
        "",
    ]
    missing = summary.get("missing_required_verbs", {}) or {}
    if missing:
        lines.extend(["## Missing required verbs", ""])
        for command, verbs in sorted(missing.items()):
            lines.append(f"- `{command}`: `{', '.join(verbs)}`")
        lines.append("")
    catalog_only = summary.get("catalog_only_resource_commands", []) or []
    if catalog_only:
        lines.extend(["## Catalog-only resource commands", ""])
        for command in catalog_only:
            lines.append(f"- `{command}`")
        lines.append("")
    lines.extend(["## Help snapshots", ""])
    for name in sorted(snapshot.get("help_snapshots", {})):
        lines.append(f"### `{name}`")
        lines.append("")
        lines.append("```text")
        lines.append(snapshot["help_snapshots"][name].rstrip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


__all__ = [
    "ARGUMENT_SPECS",
    "ARGUMENT_SPECS",
    "ArgumentSpec",
    "CommandSpec",
    "COMMAND_FAMILY_ORDER",
    "COMMAND_SPECS",
    "ExitCodeSpec",
    "FAMILY_TITLES",
    "FlagSpec",
    "GLOBAL_ARGUMENT_KEYS",
    "OutputSpec",
    "RESOURCE_COMMANDS",
    "VerbSpec",
    "build_cli_conformance_snapshot",
    "build_cli_contract_manifest",
    "build_help_snapshots",
    "build_parser",
    "iter_command_specs",
    "render_cli_conformance_markdown",
    "render_cli_markdown",
]

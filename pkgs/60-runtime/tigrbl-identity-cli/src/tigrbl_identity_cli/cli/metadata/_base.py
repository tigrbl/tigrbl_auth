from __future__ import annotations

"""Canonical CLI metadata for parser generation, docs, and contract artifacts.

This module is the single source of truth for the identity CLI surface.
Argparse help output, markdown reference docs, machine-readable contract
artifacts, and conformance snapshots are all derived from these structures.
"""

import argparse
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from tigrbl_identity_runtime.deployment import (
    EXTENSION_REGISTRY,
    PLUGIN_MODE_TO_SURFACE_SETS,
    PROTOCOL_SLICE_REGISTRY,
    SURFACE_SET_REGISTRY,
)
from tigrbl_identity_runtime import iter_runner_adapters, registered_runner_names


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
    "tenant": FlagSpec("tenant", ("--tenant",), "Tenant identifier for multi-tenant commands.", {"default": None}, group="global", family="global"),
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
    "verbose": FlagSpec("verbose", ("--verbose", "-v"), "Increase CLI verbosity; may be repeated.", {"action": "count", "default": 0}, group="global", family="global"),
    "trace": FlagSpec("trace", ("--trace",), "Emit trace-oriented execution details.", {"action": "store_true"}, group="global", family="global"),
    "color": FlagSpec("color", ("--color",), "Color policy for terminal output.", {"choices": ["auto", "always", "never"], "default": "auto"}, group="global", family="global"),
    # Common CLI plumbing.
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
    "log_level": FlagSpec("log_level", ("--log-level",), "Log level for serve plans.", {"default": "INFO"}, group="serve", family="serve-portable"),
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
    "Single storage-backed resource record with metadata.",
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
